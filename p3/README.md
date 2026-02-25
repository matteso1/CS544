# DRAFT!  Don't start yet.

# P3 (3% of grade): Loans and Performance Study

## Overview

In this project, you will explore concurrent programming, data processing, and controlled AI-assisted development through a housing affordability pipeline.

You will work with:

- HMDA loan-level data (client side)
- ACS tract-level median household income data (server side)

The client performs multi-threaded processing and uses a thread-safe FIFO cache to reduce repeated server lookups.

## Learning Objectives

- Implement thread-safe shared data structures (`FIFO`) with correct lock usage
- Build a multi-threaded client that interacts with a remote data service
- Understand GIL vs No-GIL performance behavior under different thread counts
- Design tests that validate correctness and edge-case handling
- Benchmark and analyze format performance (`CSV` and `Parquet`)

Before starting, review general project directions from class.

## Corrections/Clarifications

- Follow course announcements for any updates.

## AI Usage

You must write `cache.py` by hand, without AI.  For the rest, you may use Aider with gemini-2.5-pro for anything you like.  You must use it for at least one thing of your choice.  You may not use other AI for code generation (only for asking generation questions; for example, to learn about Python data structures you might use).

## Runtime Modes (Experiments)

TODO: move this into part 4

Use only these two modes in experiments:

1. `python3.13-nogil -X gil=1`
2. `python3.13-nogil -X gil=0`

`python` baseline is removed from the main benchmark workflow.

## Setup

Copy starter files from the `p3` directory in the main repo to your project repo:

```
cp -r app_server Dockerfile.server Dockerfile.client \
  docker-compose.yml port.sh <PROJECT REPO>
cd <PROJECT REPO>
git add app_server Dockerfile.server Dockerfile.client docker-compose.yml port.sh
git commit -m 'starter code'
```

Download the HMDA Wisconsin 2021 data into a `data` directory (this will be mounted into the client container):

```bash
mkdir -p data
wget https://pages.cs.wisc.edu/~harter/cs544/data/2021_public_lar_csv.zip -O data/2021_public_lar_csv.zip
wget https://pages.cs.wisc.edu/~harter/cs544/data/2021_public_lar.parquet -O data/2021_public_lar.parquet
```

Do NOT add or commit these large files in your repo.

Build and start:

```bash
export PROJECT=p3
docker compose up --build -d -t 0
```

Verify the server is working from your VM.  We provide a small script (`port.sh`) for looking up the external port number for one of your containers, because it may change each time.  You can use backticks to run the script to get the port number, then immediately use it in a curl command:

```bash
curl localhost:`./port.sh p3-server-1`/55079010900
```

You should get back a number (the median household income in thousands for that census tract).

## Part 1: Income Analysis

The HDMA data contains US-wide loan applications for 2021.  Loan
applications are associated with census tracts.  The American
Community Survey (ACS) provides data about average income per census
tract.

You will write a program to study housing affordability, and answer this question:

**For each state, what percent of loan applicants have below-median income for the corresponding census tract area?**

You will write a client program that loops over the HDMA data
directly.  But instead of accessing ACS data directly, the client will
send requests to a server to lookup average income.  

The server exposes tract-income lookup as REST:

- Method: `GET`
- Path: `/<tract_geoid>`
- Success response (`200`): plain-text numeric tract median income (in thousands)
- Missing tract (`404`): no body

The client will need to lookup certain values repeatedly, so we will
cache these.  Given the server implements a REST API, you will
implement a generic HTTP cache, keyed by URL (values will be the HTTP
responses).

### HTTP Cache (cache.py)

Look at `http_get` in cache.py.  The call implements retry, but no
caching (yet).  The cache.py code can work as a program (for `python3
cache.py args...`, the `__main__` code will run, or a module (for
`import cache`, the main won't run, but the importer can use
`http_get`).

Add thread-safe caching functionality to `http_get`, and return True for cache
hits.

Requirements:
* one global lock, and use it whenever shared data structures are accessed
* do not hold the lock when doing I/O
* implement a FIFO policy
* choose data structures so that eviction is an O(1) operation.  You'll need to do some reading and investigation to find good built-in data types.  Note that popping index 0 from a list (as in lecture) is an O(N) operation

The `__main__` block in `cache.py` lets you test caching directly.  It initializes a cache of size 3 and fetches each URL given as an argument, printing the total hit count at the end.  Try it with `docker compose exec` (make sure compose is up first):

```bash
docker exec p3-client-1 python3.13-nogil app_cli/cache.py \
  http://server:8001/55079010900 \
  http://server:8001/55079002402 \
  http://server:8001/55079010900 \
  http://server:8001/55079002402 \
  http://server:8001/55079010900
```

You should see `hits: 3` (the first two are misses, the last three are cache hits).

Try testing your eviction policy too.  With a cache of size 3, try passing 4 different URLs, then repeating the first -- since the cache is FIFO, the first URL should have been evicted.

### Analyzer (client.py)

Write a client.py program that works like this:

```bash
docker exec p3-client-1 python3.13-nogil app_cli/client.py /data/2021_public_lar_csv.zip --rows 50000 --cache 2000 --threads 8
```

It should open the data file, supporting zipped CSV and Parquet (infer which to do based on file extension).  Read all values from these columns to Python lists:

- `state_code`
- `census_tract`
- `income`

After making the complete list, slice these to the first `rows` entries, based on the cmd line argument.  If `--rows=-1`, do not slice.

Import the cache you wrote and initialize to the given size.

Start the specified number of threads to perform the analysis.  Each should be passed a start and stop index.  Each thread will loop over the indicated range of the Python lists you loaded.  The ranges should be roughly even in size.  For example, say there are a million rows, but you load like this: `--rows 9 --cache 2000 --threads 3`.  The ranges might be like this (inclusive start, exclusive end):

* thread 0: indexes 0-3
* thread 1: indexes 3-6
* thread 2: indexes 6-9

When a thread loops over the index for a state/tract/income, it should lookup the median income for the tract (with the help of a the cache), and count the loan application as under (income < tract median income) or over (income >= tract median income).  The thread should also count hits.

The client should skip bad rows safely (with `continue`) instead of crashing.  Bad rows include:

- invalid or missing `census_tract`
- invalid, missing, or non-positive `income`
- rows where server lookup returns `404` (tract not found in server dataset)

After the threads exit, you will need to output the hit rate and a percentage per state (what percent of incomes for loan applicants are < the median for the corresponding state).

For example, imagine 6 rows across 2 states and 3 tracts.  Suppose the server returns median incomes of 50 for tract A, 60 for tract B, and 40 for tract C.

| row | state     | tract       | income | tractmedian |
|-----|-----------|-------------|--------|-------------|
| 0   | WI        | A           | 50     | 60          |
| 1   | WI        | A           | 100    | 60          |
| 2   | IL        | B           | 50     | 70          |
| 3   | IL        | B           | 100    | 70          |
| 4   | IL        | C           | 50     | 40          |
| 5   | IL        | C           | 100    | 40          |

WI has 2 rows, 1 is under: 50%.  IL has 4 rows, 1 is under the associated tract median: 25%.  There are 3 unique tracts but 6 lookups, so with a large enough cache we'd expect 3 hits out of 6 lookups, a 50% hit rate.

The output format will be like this (round down percents with `int(...)`):

```
...other output you may want...
IL: 25
WI: 50
hit rate: 50%
```

Make sure you calculate statistics in a thread-safe way.  There are a couple approaches you could consider:
1. adding another lock in client.py, and hold it when a thread updates stats that other threads might update too
2. compute partial stats/counts for each thread, and wait until after all threads return (using `join`) before adding to get totals

## Part 2: Storage Performance

Is Parquet or zipped CSV faster?  Write a benchmark program that tries
running your client both ways.  You can read about how to write a
program that runs other programs here:
https://docs.python.org/3/library/subprocess.html.

Your benchmark should write the measurements to a CSV file.  Another
program should take this CSV file in, and produce a bar plot in a file
named `storage.svg`.  You can name the other files (the two programs
and CSV file) as you like.

To measure storage performance specifically, run with `--rows=0` so
that no rows are processed after the load.

Your measurements may vary, but the plot should look something like this:

TODO: plot example.

## Part 3: Memory Performance

How does cache size impact your hit rate?  Write a benchmark program
that runs your client with cache sizes of 1, 10, 100, 1000, and
10000.  Use 4 threads and Parquet input for all runs.

Your benchmark should write the measurements to a CSV file.  Another
program should take this CSV file in, and produce a line plot in a
file named `memory.svg`.  The x-axis should be cache size and the
y-axis should be hit rate.

Your measurements may vary, but the plot should look something like this:

TODO: plot example.

## Part 4: Compute Performance

How is performance impacted by the GIL and the number of threads?
Write a benchmark program that runs your client with thread counts of
1, 2, 4, and 8.  For each thread count, run twice: once with
`python3.13-nogil -X gil=1` and once with `python3.13-nogil -X gil=0`.
Use Parquet input and a cache size of 1000 for all runs.

Your benchmark should write the measurements to a CSV file.  Another
program should take this CSV file in, and produce a line plot in a
file named `compute.svg`.  The x-axis should be thread count and the
y-axis should be seconds.  Plot one line for each GIL mode.

Your measurements may vary, but the plot should look something like this:

TODO: plot example.

## Submission

Read the directions [here](../projects.md) about how to create the
repo.

Fill in the template here: TODO.  Do not change the page count or
layout.  Save as a pdf (`perf.pdf`), and include it in this repo.

Please add `.aider.input.history` and `.aider.chat.history.md` to your
repo.  You must be able to clone your repo to a fresh directory, and
bring it up like this:

```
export PROJECT=p3
docker compose up --build -d -t 0
```

TODO: describe how we will interact with their code

TODO: describe what files we expect, both with specific names, and in general.

**Optional:** consider providing feedback on the project to earn extra credit: https://tyler.caraza-harter.com/cs544/s26/forms.html.

## Tester

Details coming soon.  Section 1 will be autograded.  Sections 2-4 will be human reviewed.