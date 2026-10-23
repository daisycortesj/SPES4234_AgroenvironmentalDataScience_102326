# Git & GitHub: the 5-minute version

**You do NOT need Git for this class.** Downloading the ZIP works fine. This page is for when you're curious.

## What are they?
* **Git** = "track changes" for a folder of code, on your computer. It remembers every saved version (*commit*), so you can go back in time.
* **GitHub** = a website that stores Git folders (*repositories*, or "repos") online so you can share and collaborate.

Analogy: Git is like the version history in Google Docs, but for a whole project folder and under your control.

## Vocabulary
| Word | Meaning |
|---|---|
| **repository (repo)** | A project folder tracked by Git |
| **clone** | Download a full copy of a repo (with its history) |
| **commit** | A saved snapshot, with a message saying what changed |
| **push / pull** | Send your commits to GitHub / get new commits from GitHub |
| **fork** | Your own copy of someone else's repo on GitHub |

## The only commands you need to start
```bash
git clone https://github.com/daisycortesj/SPES4234_AgroenvironmentalDataScience_102326.git   # get a copy (once)
cd SPES4234_AgroenvironmentalDataScience_102326                                                # go into it
git pull                                                              # get the latest updates
```

## Want your own copy online? (needs a free GitHub account)
1. On the repo page click **Fork** → creates `github.com/<you>/SPES4234_AgroenvironmentalDataScience_102326`.
2. Clone *your* fork, make changes, then:
```bash
git add .                         # stage everything you changed
git commit -m "Add my heatmap"    # save a snapshot with a message
git push                          # upload to GitHub
```

## Friendlier than the command line
* **GitHub Desktop**: [desktop.github.com](https://desktop.github.com) (point-and-click)
* **RStudio**: *File → New Project → Version Control → Git* (built in)
* **VS Code**: Source Control panel (built in)

## Learn more
* [Happy Git and GitHub for the useR](https://happygitwithr.com/) (excellent for R users)
* [Software Carpentry: Version Control with Git](https://swcarpentry.github.io/git-novice/)
