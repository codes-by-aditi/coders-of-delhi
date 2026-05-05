"""
recommendation.py
=================
Two recommendation engines for CodeBook Social Network — built with pure Python.

Engine 1 — People You May Know
    Uses mutual friend count as the relevance score.
    Logic: if user A and user B share many common friends,
           they are likely to know each other too.

Engine 2 — Pages You Might Like
    Uses collaborative filtering logic (item-based).
    Logic: find friends of the user → look at pages they liked
           → recommend pages the user hasn't liked yet,
              ranked by how many friends liked each page.

Author : Aditi Chaudhary
Project: CodeBook – Social Network Analysis (Pure Python)
"""


# ──────────────────────────────────────────────────────────────────────────────
# HELPER — Build lookup dictionaries
# ──────────────────────────────────────────────────────────────────────────────

def build_user_map(users: list) -> dict:
    """
    Build a dictionary mapping user_id → user dict for O(1) lookup.

    Parameters
    ----------
    users : list  — List of user dicts from the cleaned dataset.

    Returns
    -------
    dict  {user_id: user_dict}
    """
    return {u["id"]: u for u in users}


def build_page_map(pages: list) -> dict:
    """
    Build a dictionary mapping page_id → page dict for O(1) lookup.

    Parameters
    ----------
    pages : list  — List of page dicts from the cleaned dataset.

    Returns
    -------
    dict  {page_id: page_dict}
    """
    return {p["id"]: p for p in pages}


# ──────────────────────────────────────────────────────────────────────────────
# ENGINE 1 — People You May Know (Mutual Friends)
# ──────────────────────────────────────────────────────────────────────────────

def get_mutual_friends(user_a: dict, user_b: dict) -> list:
    """
    Return the list of user IDs that are friends with BOTH user_a and user_b.

    Parameters
    ----------
    user_a : dict — First user dictionary.
    user_b : dict — Second user dictionary.

    Returns
    -------
    list  — List of mutual friend IDs.
    """
    friends_a = set(user_a.get("friends", []))
    friends_b = set(user_b.get("friends", []))
    return list(friends_a & friends_b)         # set intersection


def people_you_may_know(target_user_id: str,
                         user_map: dict,
                         top_n: int = 3) -> list:
    """
    Recommend users the target user might know, based on mutual friend count.

    Algorithm
    ---------
    1. Get the target user's current friend list.
    2. For every OTHER user in the network (not already a friend, not self):
       a. Count mutual friends between target and that user.
       b. Score = number of mutual friends.
    3. Sort candidates by score descending.
    4. Return top_n recommendations.

    Parameters
    ----------
    target_user_id : str  — The user ID to generate recommendations for.
    user_map       : dict — {user_id: user_dict} lookup map.
    top_n          : int  — Number of recommendations to return (default 3).

    Returns
    -------
    list of dicts — Each dict contains:
        {
          "user_id"        : str,
          "name"           : str,
          "mutual_friends" : list,
          "mutual_count"   : int
        }
    """
    if target_user_id not in user_map:
        print(f"⚠️  User ID '{target_user_id}' not found in the dataset.")
        return []

    target = user_map[target_user_id]
    target_friends = set(target.get("friends", []))

    candidates = []

    for uid, user in user_map.items():
        # Skip self
        if uid == target_user_id:
            continue

        # Skip people already friends with target
        if uid in target_friends:
            continue

        # Also skip if target is in their friend list (bidirectional check)
        if target_user_id in set(user.get("friends", [])):
            continue

        mutual = get_mutual_friends(target, user)

        # Only recommend if there is at least 1 mutual friend
        if mutual:
            candidates.append({
                "user_id"       : uid,
                "name"          : user.get("name"),
                "mutual_friends": mutual,
                "mutual_count"  : len(mutual)
            })

    # Sort by mutual friend count, highest first
    candidates.sort(key=lambda x: x["mutual_count"], reverse=True)

    return candidates[:top_n]


def display_people_recommendations(target_user_id: str,
                                    user_map: dict,
                                    top_n: int = 3) -> None:
    """
    Pretty-print the "People You May Know" recommendations for a user.

    Parameters
    ----------
    target_user_id : str  — User to generate recommendations for.
    user_map       : dict — Lookup map of all users.
    top_n          : int  — Number of results to display.
    """
    target_name = user_map.get(target_user_id, {}).get("name", target_user_id)
    recs = people_you_may_know(target_user_id, user_map, top_n)

    print(f"\n{'═' * 55}")
    print(f"  👥  People You May Know — for {target_name}")
    print(f"{'═' * 55}")

    if not recs:
        print("  No recommendations found (no mutual friends).")
    else:
        for rank, rec in enumerate(recs, start=1):
            mutual_names = [
                user_map[fid]["name"]
                for fid in rec["mutual_friends"]
                if fid in user_map
            ]
            print(f"\n  #{rank}  {rec['name']}  (ID: {rec['user_id']})")
            print(f"       Mutual Friends ({rec['mutual_count']}): "
                  f"{', '.join(mutual_names)}")

    print(f"\n{'═' * 55}\n")


# ──────────────────────────────────────────────────────────────────────────────
# ENGINE 2 — Pages You Might Like (Collaborative Filtering)
# ──────────────────────────────────────────────────────────────────────────────

def pages_you_might_like(target_user_id: str,
                          user_map: dict,
                          page_map: dict,
                          top_n: int = 3) -> list:
    """
    Recommend pages using friend-based collaborative filtering.

    Algorithm
    ---------
    1. Get the target user's already-liked pages (to exclude later).
    2. Get the target user's friends list.
    3. For each friend, look at pages they have liked.
    4. For each page a friend likes that the target doesn't already like:
       - Increment that page's score by 1 (one friend = one vote).
    5. Sort pages by score descending.
    6. Return top_n pages with highest friend-vote counts.

    Why this is Collaborative Filtering
    ------------------------------------
    We are using the behaviour of similar users (friends) to recommend
    items (pages) — this is the core idea behind user-based collaborative
    filtering, the same algorithm used by Netflix and Spotify.

    Parameters
    ----------
    target_user_id : str  — User to generate recommendations for.
    user_map       : dict — {user_id: user_dict} lookup map.
    page_map       : dict — {page_id: page_dict} lookup map.
    top_n          : int  — Number of pages to recommend (default 3).

    Returns
    -------
    list of dicts — Each dict contains:
        {
          "page_id"        : str,
          "page_name"      : str,
          "category"       : str,
          "followers"      : int,
          "friend_votes"   : int,
          "liked_by_friends": list of friend names
        }
    """
    if target_user_id not in user_map:
        print(f"⚠️  User ID '{target_user_id}' not found in the dataset.")
        return []

    target        = user_map[target_user_id]
    already_liked = set(target.get("liked_pages", []))
    friends       = target.get("friends", [])

    # page_id → {"votes": int, "liked_by": [friend_names]}
    page_votes = {}

    for friend_id in friends:
        if friend_id not in user_map:
            continue                          # friend might have been cleaned out

        friend = user_map[friend_id]
        friend_liked_pages = friend.get("liked_pages", [])

        for pid in friend_liked_pages:
            if pid in already_liked:
                continue                      # target already likes this page

            if pid not in page_votes:
                page_votes[pid] = {"votes": 0, "liked_by": []}

            page_votes[pid]["votes"]    += 1
            page_votes[pid]["liked_by"].append(friend.get("name", friend_id))

    # Build recommendation list
    recommendations = []
    for pid, vote_data in page_votes.items():
        page_info = page_map.get(pid, {})
        recommendations.append({
            "page_id"          : pid,
            "page_name"        : page_info.get("name", "Unknown Page"),
            "category"         : page_info.get("category", "Unknown"),
            "followers"        : page_info.get("followers", 0),
            "friend_votes"     : vote_data["votes"],
            "liked_by_friends" : vote_data["liked_by"]
        })

    # Sort by friend votes (most popular among friends first)
    recommendations.sort(key=lambda x: x["friend_votes"], reverse=True)

    return recommendations[:top_n]


def display_page_recommendations(target_user_id: str,
                                  user_map: dict,
                                  page_map: dict,
                                  top_n: int = 3) -> None:
    """
    Pretty-print the "Pages You Might Like" recommendations for a user.

    Parameters
    ----------
    target_user_id : str  — User to generate recommendations for.
    user_map       : dict — Lookup map of all users.
    page_map       : dict — Lookup map of all pages.
    top_n          : int  — Number of results to display.
    """
    target_name = user_map.get(target_user_id, {}).get("name", target_user_id)
    recs = pages_you_might_like(target_user_id, user_map, page_map, top_n)

    print(f"\n{'═' * 55}")
    print(f"  📄  Pages You Might Like — for {target_name}")
    print(f"{'═' * 55}")

    if not recs:
        print("  No page recommendations found.")
    else:
        for rank, rec in enumerate(recs, start=1):
            print(f"\n  #{rank}  {rec['page_name']}")
            print(f"       Category  : {rec['category']}")
            print(f"       Followers : {rec['followers']:,}")
            print(f"       Friend Votes: {rec['friend_votes']} friend(s) liked this")
            print(f"       Liked by  : {', '.join(rec['liked_by_friends'])}")

    print(f"\n{'═' * 55}\n")
