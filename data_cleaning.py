"""
data_cleaning.py
================
All data cleaning logic for the CodeBook Social Network dataset.
Operates purely on Python dicts/lists — no external libraries required.

Cleaning Steps
--------------
1. Remove users with empty or whitespace-only names
2. Remove duplicate friend IDs within each user's friend list
3. Remove inactive users (last active > 180 days ago)
4. Remove duplicate pages (same page ID appearing more than once)

Author : Aditi Chaudhary
Project: CodeBook – Social Network Analysis (Pure Python)
"""

import json
import copy


# ──────────────────────────────────────────────────────────────────────────────
# STEP 1 — Remove users with empty names
# ──────────────────────────────────────────────────────────────────────────────

def remove_empty_names(users: list) -> tuple:
    """
    Filter out users whose name field is empty or whitespace-only.

    Parameters
    ----------
    users : list
        List of user dictionaries.

    Returns
    -------
    tuple
        (cleaned_list, removed_list) — both are lists of user dicts.
    """
    cleaned = []
    removed = []

    for user in users:
        name = user.get("name", "").strip()
        if name:                      # non-empty name → keep
            cleaned.append(user)
        else:                         # empty name → remove
            removed.append(user)

    print(f"  🗑️  Empty names removed : {len(removed)} user(s)")
    if removed:
        for u in removed:
            print(f"       └─ Removed user ID: {u.get('id')}")

    return cleaned, removed


# ──────────────────────────────────────────────────────────────────────────────
# STEP 2 — Remove duplicate friends inside each user's friend list
# ──────────────────────────────────────────────────────────────────────────────

def remove_duplicate_friends(users: list) -> tuple:
    """
    For every user, deduplicate the friends list while preserving order.

    Parameters
    ----------
    users : list
        List of user dictionaries.

    Returns
    -------
    tuple
        (cleaned_list, total_duplicates_removed: int)
    """
    total_dupes = 0

    for user in users:
        original  = user.get("friends", [])
        seen      = set()
        unique    = []

        for fid in original:
            if fid not in seen:
                seen.add(fid)
                unique.append(fid)

        dupes_here = len(original) - len(unique)
        if dupes_here > 0:
            print(f"  🔁 Duplicate friends removed for {user['name']}: "
                  f"{dupes_here} duplicate(s) → {original} → {unique}")
            total_dupes += dupes_here

        user["friends"] = unique

    print(f"  ✅ Total duplicate friend entries removed: {total_dupes}")
    return users, total_dupes


# ──────────────────────────────────────────────────────────────────────────────
# STEP 3 — Remove inactive users
# ──────────────────────────────────────────────────────────────────────────────

def remove_inactive_users(users: list, threshold_days: int = 180) -> tuple:
    """
    Remove users who have not been active within the threshold window.

    Parameters
    ----------
    users          : list  — List of user dictionaries.
    threshold_days : int   — Users inactive beyond this many days are removed.
                             Default is 180 days (≈ 6 months).

    Returns
    -------
    tuple
        (active_users, inactive_users) — both are lists of user dicts.
    """
    active   = []
    inactive = []

    for user in users:
        days_ago = user.get("last_active_days_ago", 0)
        if days_ago <= threshold_days:
            active.append(user)
        else:
            inactive.append(user)
            print(f"  💤 Inactive user removed: {user.get('name', 'Unknown')} "
                  f"(last active {days_ago} days ago)")

    print(f"  ✅ Active users retained : {len(active)}")
    print(f"  🗑️  Inactive users removed: {len(inactive)}")
    return active, inactive


# ──────────────────────────────────────────────────────────────────────────────
# STEP 4 — Remove duplicate pages
# ──────────────────────────────────────────────────────────────────────────────

def remove_duplicate_pages(pages: list) -> tuple:
    """
    Remove duplicate pages based on page ID, keeping only the first occurrence.

    Parameters
    ----------
    pages : list
        List of page dictionaries.

    Returns
    -------
    tuple
        (unique_pages, duplicates_removed: int)
    """
    seen_ids   = set()
    unique     = []
    duplicates = 0

    for page in pages:
        pid = page.get("id")
        if pid not in seen_ids:
            seen_ids.add(pid)
            unique.append(page)
        else:
            duplicates += 1
            print(f"  🔁 Duplicate page removed: [{pid}] {page.get('name')}")

    print(f"  ✅ Unique pages retained : {len(unique)}")
    print(f"  🗑️  Duplicate pages removed: {duplicates}")
    return unique, duplicates


# ──────────────────────────────────────────────────────────────────────────────
# MASTER CLEANING PIPELINE
# ──────────────────────────────────────────────────────────────────────────────

def clean_data(raw_data: dict, inactive_threshold: int = 180) -> dict:
    """
    Run all four cleaning steps in sequence and return the cleaned dataset.

    Parameters
    ----------
    raw_data           : dict — Full raw dataset loaded from JSON.
    inactive_threshold : int  — Days threshold for inactive users (default 180).

    Returns
    -------
    dict
        Cleaned dataset with the same structure as raw_data.
    """
    # Deep copy so we never mutate the original
    data = copy.deepcopy(raw_data)

    users = data.get("users", [])
    pages = data.get("pages", [])

    print("\n" + "═" * 55)
    print("  🧹  DATA CLEANING PIPELINE")
    print("═" * 55)

    # Step 1
    print("\n📌 Step 1 — Removing users with empty names")
    users, _ = remove_empty_names(users)

    # Step 2
    print("\n📌 Step 2 — Removing duplicate friends")
    users, _ = remove_duplicate_friends(users)

    # Step 3
    print(f"\n📌 Step 3 — Removing inactive users (>{inactive_threshold} days)")
    users, _ = remove_inactive_users(users, threshold_days=inactive_threshold)

    # Step 4
    print("\n📌 Step 4 — Removing duplicate pages")
    pages, _ = remove_duplicate_pages(pages)

    data["users"] = users
    data["pages"] = pages

    print("\n" + "═" * 55)
    print(f"  ✅  Cleaning complete!")
    print(f"      Users : {len(raw_data['users'])} → {len(users)}")
    print(f"      Pages : {len(raw_data['pages'])} → {len(pages)}")
    print("═" * 55 + "\n")

    return data


# ──────────────────────────────────────────────────────────────────────────────
# SAVE CLEANED DATA
# ──────────────────────────────────────────────────────────────────────────────

def save_cleaned_data(cleaned_data: dict, filepath: str) -> None:
    """
    Save the cleaned dataset to a JSON file.

    Parameters
    ----------
    cleaned_data : dict — The cleaned dataset dictionary.
    filepath     : str  — Destination file path.
    """
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(cleaned_data, f, indent=2, ensure_ascii=False)

    print(f"💾 Cleaned data saved to: {filepath}")
