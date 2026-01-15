# General Project Directions

## Collaboration/Conduct Guidance

Students may work alone or optionally work in groups of two.

**Code copying between students is not allowed in this course, except
between project partners.  Copying includes emailing, taking photos,
looking while typing line by line, etc.  Copying code then changing it
is still copying and thus not allowed.  Lock your compute when it's
not attended.**

**Partners**
* there should only be one submission repo for the team
* it's NOT OK to submit code from your partner that you didn't help write or understand

**Other Collaboration**
* you can talk about logic and help each other debug
* **no code copying**; for example, no emailing code (or similar), no photos of code, no looking at code and typing it line by line
* copying code then changing it is still copying and thus not allowed

**ChatGPT, Large Language Models, Interactive Tools**
* policy will vary by project (please check carefully each time!)

**Other Online Resources**
* you **may not** use any online resource intended to provide solutions specific to CS 544
* you **may** use other online resources, with proper citation
* add a comment in your code before anything you copied from such sources
* never post your project solutions anywhere publicly online (for example, on a public GitHub repo) because current or future students may find and use your code

## Compute Setup

For most projects, we'll use VMs provided by CSL.  See the directions
[here](csl-vm.md) about how to access it.  The first project will
involve some setup (like installing docker) on the VM.

For later projects, we'll share details about how to do use cloud
resources.

## Project Repository

### Creation

At the start of each project, you must submit the [Project
Form](https://tyler.caraza-harter.com/cs544/s26/forms.html).  This
will indicate whether or not you have a partner (and if so, who).
Upon a valid a submission, we'll create a repo for you and your
partner (if any) on GitLab and email you a link.

### Clone

You will want to clone your new repo to your VM.  There are multiple
ways to authenticate.  One is via SSH key:

1. on your VM, run `ssh-keygen` to generate a new key, following the steps indicated
2. print the key with `cat ~/.ssh/id_ed25519.pub`, then copy it
3. go to https://git.doit.wisc.edu/-/user_settings/ssh_keys
4. click "Add new key"
5. paste the key you copied, give it any title you wish, and optionally specify an expiration
6. find your new repo (you can navigate from https://git.doit.wisc.edu/cdis/cs/courses/cs544)
7. click the "Code" dropdown
8. copy the "Clone with SSH" URL
9. on your VM, run `git clone URL` (replacing "URL" with the one you copied)

### Initialization

Your initial repository should have a `requirements-dev.txt` file listing
some packages we'll use for projects.  You can create a Python virtual
environment (for using these packages for a specific project, instead
of across the whole system), then install them as follows:

```
sudo apt install python3-venv
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements-dev.txt
```

> **NOTE**: Do NOT touch or edit `submit.sh`, `.gitlab-ci.yml` in your repository. These files are used to automate grading. Editing them could hinder your ability to submit properly.

<!--
To clone your GitLab repository on a VM, you can run the following command:
```bash
git clone https://oauth2:$GITLAB_ACCESS_TOKEN@repo_url
```

where `repo_url` is the `https` url (minus `https://` at the beginning and `.git` at the end) found at your remote project on GitLab

Ex:
```
git.doit.wisc.edu/cdis/cs/courses/cs544/s26/PROJECT/NET_ID
```

And where `$GITLAB_ACCESS_TOKEN` is a user-level defined access token. To create a user-level access token (only need to do this once), follow these steps:

1. Go to GitLab's Access Token Settings:
  - Log in to your GitLab account.
  - Click on your profile picture in the top-left corner and go to Preferences.
  - On the left-hand sidebar, click Access Tokens.
2. Create a New Access Token:
  - Name: Give your token a descriptive name (e.g., "CS 544 Access Token").
  - Expires at: Optionally, set an expiration date for the token (i.e. some time after the semester ends).
  - Scopes: Choose the appropriate scopes based on your use case. Here are some common ones:
    - `api`: Full access to the API, including project and repository management.
    - `read_repository`: Allows read access to repositories (e.g., cloning).
    - `write_repository`: Allows pushing to repositories.
3. After selecting the desired scopes, click Create personal access token.
4. Copy the Token:
5. After creating the token, GitLab will display it once. Copy it and store it on your machine as an `env` variable:

```bash
nano ~/.bashrc
```

Write contents to file:
```bash
GITLAB_ACCESS_TOKEN="YOUR_TOKEN_GOES_HERE"
```

Reload shell (if applicable):
```bash
source ~/.bashrc
```

You can double check that the `env` variable was saved with:
```bash
echo $GITLAB_ACCESS_TOKEN
```

### Environment
If one does not already exist for your project, create a `venv`:
```bash
python3.10 -m venv venv
source venv/bin/activate
```

Note that if the above command fails, you may need run the following:

```bash
sudo apt install python3-venv
```

and use `python3` instead of `python3.10` when creating your `venv`.

-->

## Testing

We have developed a command-line tool to run the autograder for your projects. We highly encourage you run this on your code locally to check your progress.

> **NOTE**: Running `autobadger` on your machine does NOT submit your assignment (more on that below).

To use it, make your your `venv` is still active in the terminal.

You can run `autobadger` as a command in the terminal:

```bash
autobadger --info
```
This will output something like:
```text
Welcome to Autobadger!
Current Version: [version]
Usage: autobadger [--project PROJECT (p1-p8)] [--stdout STDOUT (print|json)]
```

Note that we will be updating the `autobadger` CLI throughout the semester to handle new projects and bug fixes. Be sure to install the latest version with each new project. If we ever need to release changes during a project, we will make an announcement in Canvas and share the latest version.

To update the version, you can the following (again, inside your `venv`):
```bash
pip install -r requirements.txt
```

## Submission

Whenever you push to `main`, we run `autobadger` on your `main` branch. We then push our results to your repository under `Issues`.

This issue will contain the contents of `autobadger` as well as some other metadata and notes. This will almost always be your project's final grade, though we do manual reviews of your code as well to check against cheating and hardcoding. We take the grade from your _most recent_ submission. Make sure your latest Gitlab issue has a score that you expect _before_ the deadline!

### IMPORTANT!

**It is important to note that it is *your responsibility* to verify**:

1. You receive a GitLab issue (within a reasonable amount of time, i.e. an hour, but normally much shorter than that)
2. The results you see align with what you expect.

If there is an issue with (1) or (2), double check your code, give it some time before you push again or [rerun your GitLab pipeline](https://piazza.com/class/merk8zm4in1ib/post/38) manually. If the issue is not resolved after a few attempts, then reach out to your [TA](https://tyler.caraza-harter.com/cs544/s26/messages.html?topic=ta) or visit us in office hours.

> **NOTE**: in cases around/after the deadline, it is better manually rerun the pipeline (if you suspect that your code is fine) than to push to `main` again. We keep track of your latest push to check against the project's deadline.

As such, it is _highly recommended_ to start early, push often, and not wait till the minutes before the deadline to submit! Give yourself a buffer against unexpected issues.

> **NOTE**: Be careful not to push after the deadline unless your intention is to submit late (see policy below).

### Miscellaneous

* projects have four parts; for notebooks, use big headers to divide your work into the four parts ("# Part 1: ...")
* for question based project work, (Q1, Q2, etc), include comments like ("# Q1: ...") before the answers
* each project will specify some specific files you need to commit (like a p1.ipynb or server.py); in addition to those, include whatever is needed (except data) for somebody to run your code

## Policies

### Late/Sick Policy

The general rule is that no submissions are accepted more than 3 days
after the deadline.  Furthermore, each day late suffers a 10% penalty
(so a 90% submission that is 2 days late gets 70%).

We understand that illness and other circumstances may make it
difficult to always submit on time.  However, we also think it is
reasonable to ask students to start early.  Thus, you can qualify for
a **waiver** of the late penalty if you have passed at least **2
tests** in the `autobadger`, at least **3 days prior** to the
deadline. That means we should be able to see those 2 tests passing in
a GitLab project `Issue` that was created at least 3 days before the
deadline.  Passing tests locally without pushing does not qualify you.

In cases of extreme documented illness (for example, long
hospitalizations), you may ask your instructor to consider waiving the
late penalty even if you didn't start early.  In the vast majority of
cases when a student becomes sick, we think it still reasonable expect
an early start on the project given you usually have 1-2 weeks to work
on each one.

If you are eligible for the 3-day waiver, it will be applied
automatically.  Only email your instructor if you do not believe the
standard late policy applies to your situation (TAs are not involved
in handling these special cases).

> **NOTE**: A waiver does NOT extend the 3-day hard deadline; it just waives the 10%/day penalty.

> **NOTE**: McBurney accomodations: please **email your instructor** a proposed policy for the semester if the general flexibility does not fit your needs (we can discuss again if your situation changes during the semester)

### Resubmission Policy

Resubmissions generally won't be allowed once projects have been graded, except in unusual situations, or when we made a mistake on our end (like a misleading specification).

### "Pre-grading" Policy

We won't pre-grade work, so don't ask questions like "does this all
look good?" during office hours.  When grading many assignments, it's
natural we'll notice issues someone might miss during office hours.
We also don't have the staff time to effectively grade submissions
twice.

You can always ask more specific questions if you're looking for some reassurance, such as:

* "does X in the spec mean Y, or does it mean Z"
* "what would be a good way to test this function?"
* "would this plot be clearer with ????, or without it"
* "is this result supposed to be deterministic, or are there reasons it might be different for other deployments?"
