# DRAFT! Don't start yet

# P1 (3% of grade): Dockerized Git Analyzer

## Overview

In this project, you'll practice using Docker and shell scripts.  You'll build a dockerized tool that clones a git repo, extracts the difference between two branches, then summarizes the difference with the help of a small LLM (large language model).

Learning objectives:
* follow directions to install Docker
* write Dockerfiles to define how to build Docker images
* use redirection and piping techniques to send data between files/processes
* write a simple bash script

Before starting, please review the [general project directions](../projects.md).

## Corrections/Clarifications

* [2025.09.22] Updated `autobadger` to `1.0.4` to allow multiple versions of `docker`.
* [2025.09.15] Updated `autobadger` to `1.0.3` to allow multi-line `apt-get`.
* [2025.09.11] Updated `autobadger` to cover more cases for `apt-get` and `git diff` checks. This doesn't affect already submitted solutions.
* [2025.09.11] Added some clarifications in `p1.md`. This doesn't affect already submitted solutions.

## AI Usage

For this project, you must use Google Gemini (as provided by the University: https://it.wisc.edu/generative-ai-services-uw-madison/).  You may not use any other AI assistance.

Fill in question answers about your interactions with Gemini as you go in [`ai.md`](ai.md).

## Part 1: Docker Install

Carefully follow the directions here to install Docker on your virtual machine: https://docs.docker.com/engine/install/ubuntu/

Notes:
* There are several different approaches described under "Installation methods".  Use the directions under "Install using the apt repository".  Make sure you don't keep going after you reach "Install from a package".
* The first step under "Install Docker Engine" has two options: "Latest" or "Specific version".  Choose **"Specific version"** (`VERSION_STRING=5:28.4.0-1~ubuntu.24.04~noble`).

To avoid needing to run every Docker command with root, there are a few more steps you should do here:
https://docs.docker.com/engine/install/linux-postinstall/#manage-docker-as-a-non-root-user
(don't go beyond the "Manage Docker as a non-root user" section).

Create some files to verify your Docker installation:

```
docker version > docker.txt
docker compose version > compose.txt
```

## Part 2: Docker Image: ollama base

Write a Dockerfile named "Dockerfile.ollama" that can be built like this:

```
docker build -f Dockerfile.ollama -t p1-ollama .
```

It should start from the latest LTS version of Ubuntu.  Inside the
image, you should have ollama installed, with the "gemma3:1b" model
already pulled.

> Ollama is a lightweight library for running and interacting with local language models.  

Ask Gemini to explain how to install, run, and prompt ollama.  Also
prompt it to generate the Dockerfile for you.  
> Like all LLMs, it's not a given that Gemini be correct--you might have to re-prompt it, do some back-and-forth and/or manual verification.

Answer some questions
about this in `ai.md`.  Brainstorm with Gemini about how to manually
verify the Dockerfile does what you want before proceeding to part 3.

## Part 3: Analyzer Script

Look at this repo:
https://git.doit.wisc.edu/cdis/cs/courses/cs544/misc/calculator.
There are a few branches.  Browse through them.

Write an `analyze.sh` bash script that clones the repo, compares the
`fix` branch to the `main` branch with a git diff, and generates a
"prompt.txt" file (using both `>` and `>>` redirections).  The file
should be formatted to look like this:

```
Summarize the following code diff:
<git diff output here...>
```

Use `cat` and a pipe (`|`) to send the prompt to `ollama` to get a
summary of the code change.  Note that even though gemma3:1b is quite
small, it will run slowly on your VM because we only have access to
CPUs (it would be much faster on a GPU).

Gemini might be useful with some of the following:
* explain the concept of git remotes
* how to compare remote branches via diff
* how to wait a while to give a server (ollama) a chance to startup before you try to communicate with it
* other...

**Requirements:** `analyze.sh` must use each of the following in a sensible way:
 * use both `>` and `>>` (for making prompt.txt)
 * use `&` and `&>` to run `ollama serve` in the background and record its output
 * use `cat` and `|` to send the prompt to `ollama run ...`

## Part 4: Docker Image: analyzer

Create a `Dockerfile.analyzer` Dockerfile with `analyze.sh` and the
necessary software installed so we can simply run the following to get
an English description of the difference between the `fix` and `main`
branches.

```
docker build -f Dockerfile.analyzer -t p1-analyzer .
docker run p1-analyzer
```

Your `Dockerfile.analyzer` should start from the image you created in
Part 2 (`p1-ollama:latest`) so you don’t have to reinstall Ollama or
re-pull the model.

Note: during testing, we may want to build your second Docker image on
bases other than your first image, so your `FROM` line should make use
of a `${PROJECT}` env variable.  You can define the environment
variable with a default like this, at the top of your Dockerfile:

```
ARG PROJECT=p1
```

## Submission

Read the directions [here](../projects.md) about how to create the repo.

Your submission repo should contain the following files:
* `docker.txt` - Docker version output
* `compose.txt` - Docker Compose version output  
* `Dockerfile.ollama` - Base image with ollama and gemma3:1b
* `Dockerfile.analyzer` - Analyzer image that builds on ollama image
* `analyze.sh` - Startup script for the analyzer container
* `ai.md` - Answers about your AI usage

## Tester

You can run the grader *locally* with the command (in your project directory):
```bash
autobadger --project p1 --verbose
```
> Note: this runs the tester locally and is not a submission. You must push your code to your `main` branch. Our grading VM will run the same script against your most current code. Upon completion, it will push a new issue to your GitLab repository. See the `Issues` tab of your repository. It normally takes a few minutes (sometimes longer, depending on the project). See [project](https://git.doit.wisc.edu/cdis/cs/courses/cs544/f25/main/-/blob/main/projects.md?ref_type=heads) for more detail.
