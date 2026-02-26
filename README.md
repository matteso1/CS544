# CS544 Repository Workflow

This repository tracks my coursework and Anki decks for CS544, as well as the official class repository cloned from the UW-Madison GitLab.

## Initial Setup Summary
This project has two remotes configured:
1. `class_repo`: The official course GitLab repository where new assignments are posted.
2. `origin`: My personal GitHub repository where my work and notes are saved.

## How to Get New Assignments (Pulling)
When the professor updates the class repository with new files or assignments, run this command to pull them into your local folder:

`git pull class_repo main`

*Note: If Git complains about "unrelated histories" during the first pull, use: `git pull class_repo main --allow-unrelated-histories`*

## How to Save My Work (Pushing)
After completing an assignment, updating notes, or adding Anki decks, save the changes to your personal GitHub repository (which syncs with Claude):

1. Stage all new changes:
   `git add .`

2. Commit the changes with a message:
   `git commit -m "completed homework 1 and added new anki cards"`

3. Push the changes to personal GitHub:
   `git push origin main`

## Troubleshooting
- **Check Remotes:** If you forget the remote names, run `git remote -v`.
- **Branch Check:** Ensure you are always working on the `main` branch. Run `git branch` to verify.
