# 📋 Demo Instructions

This repo is a contrived demo for showcasing **GitHub Pull Request Merge Queues**.

## Overview

A tiny Python Flask café menu app where 18 "developers" are all pushing changes
at once. The key insight: **every PR passes CI on its own, but merging several
together breaks the build.** Merge queues catch this before it hits `main`.

## Prerequisites

- Python 3.12+
- [GitHub CLI](https://cli.github.com/) (`gh`) authenticated with push access
- Merge queue ruleset already configured (see below)

## Demo Flow

### Part 1: The Problem (without merge queue)

Show what happens when PRs are merged directly:

1. Disable the merge queue ruleset temporarily:
   - Go to **Settings → Rules → Rulesets → "Merge Queue"** and set enforcement to **Disabled**
2. Merge drink PRs one at a time (#1 through #5)
   - Each passes CI individually ✅
   - After the 5th drink PR merges, `main` has **7 menu items** — exceeding the `MAX_MENU_SIZE = 6` limit
   - The 6th drink PR's CI will now **fail** when rebased on main ❌
3. **Talking point:** _"Each developer did their job correctly. Each PR passed CI.
   But the combination broke the build. This is the 'semantic conflict' problem."_

### Part 2: The Solution (with merge queue)

1. Reset the demo: `python3 scripts/reset_demo.py`
2. Re-enable the merge queue ruleset:
   - Go to **Settings → Rules → Rulesets → "Merge Queue"** and set enforcement to **Active**
3. Go to the [PR list](https://github.com/wilsonwong1990-org/merge-queue-cafe/pulls)
4. Click **"Merge when ready"** on all 18 PRs (or a subset of the drink PRs)
5. Watch the **merge queue tab** — GitHub will:
   - Batch compatible PRs together
   - Run CI on the **combined result** (not just each PR alone)
   - Catch the size/price failures **before** they reach `main`
   - Dequeue the failing PRs and notify the authors

### What Breaks and When

| Drink PRs merged | Total items | Size test (max 6) | Avg price test (max $4.50) |
|-----------------|-------------|-------------------|---------------------------|
| 1               | 3           | ✅ Pass           | ✅ Pass                   |
| 2               | 4           | ✅ Pass           | ✅ Pass                   |
| 3               | 5           | ✅ Pass           | ✅ Pass                   |
| 4               | 6           | ✅ Pass           | ✅ Pass                   |
| 5               | 7           | ❌ **Fail**       | ✅ Pass                   |
| 6               | 8           | ❌ Fail           | ✅ Pass                   |
| 7               | 9           | ❌ Fail           | ✅ Pass                   |
| 8 (all)         | 10          | ❌ Fail           | ❌ **Fail**               |

## Scripts

### `scripts/create_prs.py`

Creates all 18 branches and PRs. Run from the repo root:

```bash
python3 scripts/create_prs.py
```

### `scripts/reset_demo.py`

Resets the repo for a fresh demo run:

```bash
python3 scripts/reset_demo.py
```

This will:
1. Close all open PRs and delete their branches
2. Force-reset `main` to the `demo-base` tag
3. Clean up local and remote branches
4. Re-run `create_prs.py` to create 18 fresh PRs

## The 18 PRs

| #  | Branch               | Changes            | Conflict type          |
|----|---------------------|--------------------|------------------------|
| 1  | `add-espresso`      | `menu.py`          | CI breakage (size)     |
| 2  | `add-latte`         | `menu.py`          | CI breakage (size)     |
| 3  | `add-cappuccino`    | `menu.py`          | CI breakage (size)     |
| 4  | `add-americano`     | `menu.py`          | CI breakage (size)     |
| 5  | `add-cold-brew`     | `menu.py`          | CI breakage (size)     |
| 6  | `add-matcha-latte`  | `menu.py`          | CI breakage (size+avg) |
| 7  | `add-chai-latte`    | `menu.py`          | CI breakage (size+avg) |
| 8  | `add-hot-chocolate`  | `menu.py`          | CI breakage (size+avg) |
| 9  | `dark-mode`         | `styles.css`       | Clean                  |
| 10 | `responsive-layout` | `styles.css`       | Clean                  |
| 11 | `fancy-fonts`       | `styles.css`, `index.html` | Clean           |
| 12 | `menu-card-redesign`| `styles.css`       | Clean                  |
| 13 | `search-bar`        | `index.html`       | Clean                  |
| 14 | `category-tabs`     | `index.html`       | Clean                  |
| 15 | `price-sort`        | `index.html`       | Clean                  |
| 16 | `favorites-feature` | `index.html`, `styles.css` | Clean           |
| 17 | `add-ruff-config`   | `ruff.toml` (new)  | Clean                  |
| 18 | `add-pyproject`     | `pyproject.toml` (new) | Clean              |

## Merge Queue Settings

The repo has a ruleset called **"Merge Queue"** with:
- **Grouping strategy:** ALLGREEN — batches are tested together
- **Max entries to build:** 5
- **Min entries to merge:** 1
- **Merge method:** MERGE
- **Admin bypass:** Enabled (for reset script force-pushes)
