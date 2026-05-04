"""
data_loader.py
==============
Handles loading and displaying raw data from JSON files.
Part of CodeBook Social Network Analysis project.

Author : Aditi Chaudhary
Project: CodeBook – Social Network Analysis (Pure Python)
"""

import json
import os


# ──────────────────────────────────────────────────────────────────────────────
# LOAD
# ──────────────────────────────────────────────────────────────────────────────

def load_data(filepath: str) -> dict:
    """
    Load JSON data from the given file path.

    Parameters
    ----------
    filepath : str
        Path to the JSON file.

    Returns
    -------
    dict
        Parsed JSON content as a Python dictionary.

    Raises
    ------
    FileNotFoundError
        If the file does not exist at the given path.
    """
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Data file not found: {filepath}")

    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)

    print(f"✅ Data loaded successfully from: {filepath}")
    return data


# ──────────────────────────────────────────────────────────────────────────────
# DISPLAY
# ──────────────────────────────────────────────────────────────────────────────

def display_users(data: dict) -> None:
    """
    Print a summary of all users in the dataset.

    Parameters
    ----------
    data : dict
        Full dataset loaded from JSON.
    """
    users = data.get("users", [])
    print(f"\n{'═' * 55}")
    print(f"  👥  CODEBOOK USERS  ({len(users)} total)")
    print(f"{'═' * 55}")

    for user in users:
        name     = user.get("name", "").strip() or "[No Name]"
        uid      = user.get("id", "N/A")
        city     = user.get("city", "N/A")
        friends  = len(user.get("friends", []))
        active   = user.get("last_active_days_ago", "?")
        interests = ", ".join(user.get("interests", [])[:2])  # show first 2

        print(f"  [{uid}] {name:<20} | City: {city:<8} | "
              f"Friends: {friends} | Active: {active}d ago | "
              f"Interests: {interests}")

    print(f"{'═' * 55}\n")


def display_pages(data: dict) -> None:
    """
    Print a summary of all pages in the dataset.

    Parameters
    ----------
    data : dict
        Full dataset loaded from JSON.
    """
    pages = data.get("pages", [])
    print(f"\n{'═' * 55}")
    print(f"  📄  CODEBOOK PAGES  ({len(pages)} total)")
    print(f"{'═' * 55}")

    for page in pages:
        pid       = page.get("id", "N/A")
        name      = page.get("name", "N/A")
        category  = page.get("category", "N/A")
        followers = page.get("followers", 0)

        print(f"  [{pid}] {name:<35} | "
              f"Category: {category:<12} | Followers: {followers:,}")

    print(f"{'═' * 55}\n")


def get_summary(data: dict) -> dict:
    """
    Return a quick summary dictionary of the dataset.

    Parameters
    ----------
    data : dict
        Full dataset loaded from JSON.

    Returns
    -------
    dict
        Summary stats including counts of users and pages.
    """
    users = data.get("users", [])
    pages = data.get("pages", [])

    total_friendships = sum(len(u.get("friends", [])) for u in users)
    total_page_likes  = sum(len(u.get("liked_pages", [])) for u in users)

    summary = {
        "total_users"      : len(users),
        "total_pages"      : len(pages),
        "total_friendships": total_friendships,
        "total_page_likes" : total_page_likes,
    }

    print("\n📊 Dataset Summary:")
    for key, val in summary.items():
        print(f"   {key.replace('_', ' ').title():<22}: {val}")

    return summary
