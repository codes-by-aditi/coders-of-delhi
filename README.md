# 📘 Coders of Delhi — Social Network Analysis
### Coders of Delhi | Pure Python | Data Science Portfolio Project

<p align="left">
  <img src="https://img.shields.io/badge/Python-3.8+-blue?style=flat-square&logo=python&logoColor=white"/>
  <img src="https://img.shields.io/badge/Libraries-Pure%20Python%20%2B%20JSON-brightgreen?style=flat-square"/>
  <img src="https://img.shields.io/badge/Jupyter-Notebook-F37626?style=flat-square&logo=jupyter&logoColor=white"/>
  <img src="https://img.shields.io/badge/Domain-Social%20Network%20Analysis-9B59B6?style=flat-square"/>
  <img src="https://img.shields.io/badge/Algorithms-Mutual%20Friends%20%7C%20Collab%20Filtering-orange?style=flat-square"/>
</p>

> A social network analysis and recommendation engine for **CodeBook** — a fictional  
> programmer community in Delhi — built using **only pure Python and JSON**.  
> No pandas. No NumPy. No external libraries.

---

## 🎯 Problem Statement

> **"How does a social network decide who to suggest as a friend,  
> and which pages a user might want to follow?"**

This project answers that question by implementing **two real-world recommendation algorithms**  
from scratch using pure Python — the same logic used by LinkedIn, Facebook, and Instagram.

---

## ✨ Features

| Feature | Algorithm | Description |
|---|---|---|
| **People You May Know** | Mutual Friends (Set Intersection) | Suggest users who share the most common friends with the target user |
| **Pages You Might Like** | Collaborative Filtering (Friend Votes) | Recommend pages that a user's friends like, ranked by how many friends liked them |

**Plus a full Data Cleaning Pipeline:**

| Step | What It Fixes |
|---|---|
| Remove empty names | Incomplete registrations with no name field |
| Remove duplicate friends | Same friend ID appearing multiple times in a list |
| Remove inactive users | Accounts with no activity for 180+ days |
| Remove duplicate pages | Same page listed more than once in the database |

---

## 📂 Project Structure

```
CodeBook_Project/
│
├── data/
│   ├── raw_data.json          ← Original messy dataset (11 users, 8 pages with issues)
│   └── cleaned_data.json      ← Auto-generated after running Notebook 02
│
├── notebooks/
│   ├── 01_data_loading.ipynb          ← Load + explore raw data
│   ├── 02_data_cleaning.ipynb         ← 4-step cleaning pipeline with before/after
│   ├── 03_people_you_may_know.ipynb   ← Mutual friends algorithm + analysis
│   └── 04_pages_you_might_like.ipynb  ← Collaborative filtering + network insights
│
├── src/
│   ├── data_loader.py     ← load_data(), display_users(), display_pages(), get_summary()
│   ├── data_cleaning.py   ← 4 cleaning functions + master clean_data() pipeline
│   └── recommendation.py  ← people_you_may_know() + pages_you_might_like()
│
├── README.md
└── requirements.txt
```

---

## 🛠️ Tech Stack

| Tool | Purpose |
|---|---|
| **Python 3.8+** | Core language |
| **`json`** (stdlib) | Loading and saving all data |
| **`os`** (stdlib) | Cross-platform file path handling |
| **`sys`** (stdlib) | Python path configuration in notebooks |
| **`copy`** (stdlib) | Deep copying data before mutation |
| **Jupyter Notebook** | Interactive, documented analysis environment |

**Zero external dependencies** — runs on any machine with Python installed.

---

## 🧠 Algorithm Explanations

### Algorithm 1 — People You May Know (Mutual Friends)

```
Score(A, B) = |friends(A) ∩ friends(B)|

For each candidate user B:
  1. Compute set intersection of A's friends and B's friends
  2. Score = number of mutual friends
  3. Skip if B is already A's friend
  4. Rank all candidates by score (highest first)
  5. Return top N
```

**Time Complexity:** O(U × F) where U = users, F = avg friend list size  
**Python tool:** `set` intersection — `set_a & set_b`

---

### Algorithm 2 — Pages You Might Like (Collaborative Filtering)

```
For each page P not yet liked by user A:
  score(P) = count of A's friends who liked P

Rank pages by score (highest friend votes = top recommendation)
```

**Why "Collaborative Filtering"?**  
We use the collective behaviour of similar users (friends) to predict  
what the target user will like — the same core idea as Netflix's recommendation engine.

---

## 🚀 How to Run

### 1. Clone the repository
```bash
git clone https://github.com/codes-by-aditi/CodeBook-Social-Network-Analysis.git
cd CodeBook-Social-Network-Analysis
```

### 2. Install Jupyter (only external dependency)
```bash
pip install jupyter
```

### 3. Launch Jupyter
```bash
jupyter notebook
```

### 4. Run notebooks in order
```
notebooks/01_data_loading.ipynb        → Explore raw data
notebooks/02_data_cleaning.ipynb       → Clean data + save cleaned_data.json
notebooks/03_people_you_may_know.ipynb → Friend recommendations
notebooks/04_pages_you_might_like.ipynb → Page recommendations
```

> ⚠️ Run **Notebook 02 first** — it generates `cleaned_data.json` which is required by Notebooks 03 and 04.

---

## 📤 Sample Output

### People You May Know — for Aarav Sharma
```
═══════════════════════════════════════════════════════
  👥  People You May Know — for Aarav Sharma
═══════════════════════════════════════════════════════

  #1  Ananya Joshi  (ID: u007)
       Mutual Friends (2): Rohan Gupta, Sneha Kapoor

  #2  Vikram Rao  (ID: u008)
       Mutual Friends (1): Sneha Kapoor

  #3  Meera Nair  (ID: u010)
       Mutual Friends (1): Sneha Kapoor

═══════════════════════════════════════════════════════
```

### Pages You Might Like — for Aarav Sharma
```
═══════════════════════════════════════════════════════
  📄  Pages You Might Like — for Aarav Sharma
═══════════════════════════════════════════════════════

  #1  AI & Machine Learning India
       Category  : Education
       Followers : 31,000
       Friend Votes: 2 friend(s) liked this
       Liked by  : Rohan Gupta, Sneha Kapoor

  #2  Competitive Programming Arena
       Category  : Education
       Followers : 19,800
       Friend Votes: 1 friend(s) liked this
       Liked by  : Sneha Kapoor

═══════════════════════════════════════════════════════
```

---

## 💡 Data Quality Issues Fixed

| Issue Found in Raw Data | How It Was Fixed |
|---|---|
| 2 users with blank `name` field | Removed — identified using `str.strip()` check |
| Duplicate friend IDs (e.g., `u003` appearing twice) | Deduplicated preserving original order |
| 2 users inactive for 400–500 days | Removed using 180-day activity threshold |
| Page `p005` listed twice in pages array | Removed duplicate using ID-based set tracking |

---

## 🏆 Skills Demonstrated

| Skill | Evidence |
|---|---|
| **Data Cleaning** | 4-step pipeline with explicit reasoning per step |
| **Algorithm Design** | Mutual friends (set intersection) + collaborative filtering |
| **Modular Code** | Logic split across 3 clean Python modules in `src/` |
| **JSON Handling** | Load, parse, transform, and save structured JSON data |
| **Social Network Concepts** | Friend graphs, recommendation engines, network analysis |
| **Python Data Structures** | Lists, dicts, sets — used correctly and efficiently |
| **Jupyter Notebooks** | Documented, beginner-friendly, recruiter-readable format |
| **Code Quality** | Docstrings, type hints, comments, consistent naming |

---

## 📝 Resume Bullet Points

Copy these directly onto your resume or LinkedIn:

```
• Built a Social Network Recommendation System in pure Python (no external libraries),
  implementing mutual-friend-based "People You May Know" and collaborative-filtering-based
  "Pages You Might Like" features — the same algorithms used by LinkedIn and Facebook.

• Designed and applied a 4-step data cleaning pipeline on a JSON social graph dataset
  (removing empty records, deduplicating friend lists, filtering inactive users, and
  eliminating duplicate pages) with documented reasoning for each decision.

• Architected the project as a modular, production-style codebase (src/ + notebooks/)
  with separate modules for data loading, cleaning, and recommendation logic —
  demonstrating clean code structure and separation of concerns.
```

---

## 🔮 Future Improvements

- [ ] Add **interest-based matching** to the friend recommendation score (not just mutual friends)
- [ ] Build a **command-line interface (CLI)** to run recommendations without Jupyter
- [ ] Extend to a **graph visualisation** using Python's `turtle` or export to Gephi format
- [ ] Add **unit tests** using Python's built-in `unittest` module
- [ ] Load data from a **REST API** instead of a static JSON file

---

## 👩‍💻 Author

**Aditi Chaudhary**  
Aspiring Data Scientist | Python · SQL · Machine Learning | VTU '26

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-0A66C2?style=flat-square&logo=linkedin)](https://www.linkedin.com/in/aditi-chaudhary-bb3324250)
[![GitHub](https://img.shields.io/badge/GitHub-codes--by--aditi-181717?style=flat-square&logo=github)](https://github.com/codes-by-aditi)

---

> ⭐ If this project was useful, consider starring the repo — it helps others find it!
