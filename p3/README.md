# DRAFT!  Don't start yet.

# P3 (3% of grade): Threads and Benchmarking

## Overview

In this project, you will explore concurrent programming, data processing, and controlled AI-assisted development through a housing affordability pipeline.

You will work with:

- HMDA loan-level data (client side)
- ACS tract-level median household income data (server side)

The client performs multi-threaded processing and uses a thread-safe LRU cache to reduce repeated server lookups.

## Learning Objectives

- Implement thread-safe shared data structures (`LRU`) with correct lock usage
- Build a multi-threaded client that interacts with a remote data service
- Understand GIL vs No-GIL performance behavior under different thread counts
- Design tests that validate correctness and edge-case handling
- Benchmark and analyze format performance (`CSV`, `Parquet`, `Arrow`)

Before starting, review general project directions from class.

## Corrections/Clarifications

- Follow course announcements for any updates.

## AI Usage

This project intentionally separates sections where AI is and is not allowed.

- **Part 1**: do **not** use AI (manual implementation required)
- **Part 2-4**: AI assistance is allowed per course policy

If your section requires specific tools/models (for example Aider + approved models), follow that policy exactly.

## Runtime Modes (Experiments)

Use only these two modes in experiments:

1. `python3.13-nogil -X gil=1`
2. `python3.13-nogil -X gil=0`

`python` baseline is removed from the main benchmark workflow.

## Setup

Copy starter files from the `p3` directory in the main repo to your project repo:

```
cp -r app_server Dockerfile.server Dockerfile.client \
  docker-compose.yml <PROJECT REPO>
cd <PROJECT REPO>
git add app_server Dockerfile.server Dockerfile.client docker-compose.yml
git commit -m 'starter code'
```

Download the HMDA Wisconsin 2021 data into a `data` directory (this will be mounted into the client container):

```bash
mkdir -p data
wget https://pages.cs.wisc.edu/~harter/cs544/data/hdma-wi-2021.zip -O data/hdma-wi-2021.zip
cd data && unzip hdma-wi-2021.zip && cd ..
```

Build and start:

```bash
export PROJECT=p3
docker compose up --build -d -t 0
```

The compose file defines two services:

- **server**: a Flask app serving ACS tract income lookups on port 8001.  The dataset is downloaded at image build time.  You should not modify the server.
- **client**: has `python3.13-nogil` installed.  Your `data/` directory is mounted read-only at `/data`.

Verify the server is working from your VM:

```bash
curl http://localhost:8001/55079010900
```

You should get back a number (the median household income in thousands for that census tract).

As in P2, rebuild and restart after code changes with `docker compose up --build -d -t 0`.

## Part 1: Thread-Safe LRU Cache

In this part, you need to implement a class called `ThreadSafeLRUCache` in `app_cli/LRU.py`, which provides a thread-safe implementation of an LRU (Least Recently Used) cache.

Requirements:

- Correct LRU behavior
- Implement thread-safe `get` and `put` methods using locks
- Maintain `hits` and `misses` counters, and implemment `get_hits()` and `get_misses()` methods to retrieve these counts.

## Part 2: Client Implementation

Implement:

- `app_cli/client.py`

Provided server:

- `app_server/server.py` (students should not change server logic)

### Client Workflow

The client should follow two stages:

1. **Read input**
2. **Send requests to the server + compute ratios**

### Server Query API

The provided server exposes tract-income lookup as REST:

- Host: `127.0.0.1`
- Port: `8001`
- Base URL: `http://127.0.0.1:8001`
- Method: `GET`
- Path: `/<tract_geoid>`
- Success response (`200`): plain-text numeric tract median income (in thousands)
- Missing tract (`404`): no body required
  Example request: `curl http://127.0.0.1:8001/55079010900`

The client should treat `404` as lookup failure and skip that row.
`404` is expected for some rows because some tract IDs from client input (`inputs/raw/hmda_wi_2021.csv`) do not exist in the server table (`inputs/raw/acs5_2021_tract_income_us.csv`).

### Reading Input

For this stage, you need to implement the following function in `app_cli/client.py`:

```python
def load_input(path: str) -> "pd.DataFrame":
    ...
```

It should take file path as input, and return a DataFrame with the following columns:

- `census_tract`
- `income`

It should support file formats of `.csv`, `.parquet`, and `.arrow`.
It should keep row order as in the original file.

- For `.csv`: use normal pandas reading
- For `.parquet`: use normal parquet reading
- For `.arrow`: use memory mapping (`mmap`)
- Raise `ValueError` for unsupported extensions

### Client CLI

Use this invocation format:

```bash
python app_cli/client.py [input_file] --threads <T> --capacity <C>
```

Notes:

- `input_file` is optional; default is `inputs/raw/hmda_wi_2021.csv`

### Request/Compute Stage (Stage 2)

In this stage you need to implement `app_cli/client.py` that reads HMDA input rows and uses multiple threads to send tract-income lookup requests to the server. Before each request, the client must check `ThreadSafeLRUCache` implemented in Part 1; on a cache miss, it should query the server, store the result in cache, and compute the affordability ratio as `income / tract_median_income_k`.

`--threads` is a required tuning variable for concurrency. If user provides `--threads T`, the client must launch exactly `T` worker threads.

The client should skip bad rows safely with `continue` instead of crashing. In this project, bad rows include:

- invalid or missing `census_tract`
- invalid, missing, or non-positive `income`
- rows where server lookup returns `404` (tract key not found in server dataset)

Quick integration run (with compose already up):

```bash
docker compose exec client python3.13-nogil -X gil=1 app_cli/client.py /data/hdma-wi-2021.csv --threads 4 --capacity 64
```

## Part 3: Thread Benchmarking

Run a benchmark comparing thread count impact under both runtime modes.

Benchmark script:

- `benchmarks/thread_bench.py`

Invocation:

```bash
docker run --rm -v "$(pwd)/outputs:/outputs" p3-nogil-bench python3.13-nogil benchmarks/thread_bench.py /outputs
```

Expected outputs:

- `outputs/threads.csv`
- `outputs/threads.svg`

Required columns in `threads.csv`:

- `threads`
- `gil1_seconds`
- `gil0_seconds`

Required setup:

- fixed input format (`csv`)
- fixed cache size (e.g., `capacity=800`)
- benchmark thread counts: `1, 2, 4, 8`

## Part 4: Format Benchmarking

Run a benchmark comparing **load_input I/O time only** across formats.
This part should measure Stage 1 (reading) only, not request/compute.

Benchmark script:

- `benchmarks/format_bench.py`

Invocation:

```bash
docker run --rm -v "$(pwd)/outputs:/outputs" p3-nogil-bench python3.13-nogil benchmarks/format_bench.py /outputs
```

Expected outputs:

- `outputs/formats.csv`
- `outputs/formats.svg`

Required columns in `formats.csv`:

- `mode` (`gil1` / `gil0`)
- `format` (`csv`, `parquet`, `arrow`)
- `io_seconds`

benchmark should call `load_input(...)` directly and won't send requests to the server, thus cache size and thread count are not part of this benchmark.

## Part 5: Hit Rate Benchmarking

Run a benchmark focused on cache hit rate.

Benchmark script:

- `benchmarks/hitrate_bench.py`

Invocation:

```bash
docker run --rm -v "$(pwd)/outputs:/outputs" p3-nogil-bench python3.13-nogil benchmarks/hitrate_bench.py /outputs
```

Expected outputs:

- `outputs/hitrate.csv`
- `outputs/hitrate.svg`

Required columns in `hitrate.csv`:

- `capacity`
- `hit_rate`
- `hits`
- `misses`

Required setup:

- single thread only (`threads = 1`)
- pick exactly one input format for this benchmark and keep it fixed for all runs (`csv`, `parquet`, or `arrow`, your choice)
- sweep cache size exactly over: `1, 4, 8, 16, 32`
- report hit rate as `hits / (hits + misses)`

## Submission

At minimum, repository should include:

- `app_cli/LRU.py`
- `app_cli/client.py`
- `app_server/server.py` (provided)
- `Dockerfile`
- benchmark scripts:
  - `benchmarks/thread_bench.py`
  - `benchmarks/format_bench.py`
  - `benchmarks/hitrate_bench.py`
- benchmark outputs:
  - `outputs/threads.csv`
  - `outputs/threads.svg`
  - `outputs/formats.csv`
  - `outputs/formats.svg`
  - `outputs/hitrate.csv`
  - `outputs/hitrate.svg`
