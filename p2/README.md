# DRAFT! Don't start yet

# P2 (3% of grade): Distributed Property Lookup Service

## Overview

In this project, you'll work with a multi-container application for
looking up property addresses in Madison.  You'll have multiple
containers serving the dataset, so that if one fails, the system will
remain available.  You'll also have multiple caching containers that
will serve REST requests and minimize load on the dataset.

In this project, there is already a legacy dataset backend, written in
Java.  You are not expected to know Java.  With the help of AI, you
will port this code to Python.

Learning objectives:
* tolerate failures with retries
* implement an LRU cache
* implement new gRPC calls
* generate and review code with AI assistance
* port code between languages (Java → Python)

Before starting, please review the [general project directions](../projects.md).

## Corrections/Clarifications

* none yet

## AI Usage

You may use AI to ask questions about code and understand it on all
parts of this project, but there are restrictions on code generation.
Specifically, you may only use AI to generate code in parts 3 and 4,
and you may only use a specific tool: Aider, configured to use Gemini 2.5 pro.

Do NOT:
- Use models other than gemini-2.5-pro for code generation
- Copy/paste some or all of the text of the project spec (we may run similarity detection between your prompts and our spec)
- Submit code you don't understand (either prompt Aider to use other approaches you are familiar with, or read on your own to understand Aider-generated code)
- Don't do one big commit (or just a few): there should be incremental progress across many commits

Do:
- Break your work into many prompts, written using your own phrasing
- Write code manually on occasion when Aider is struggling and you can do things yourself faster
- Submit (commit+push) Aider prompt history

## Setup

There is quite a bit of starter code for this project.  You will need
to copy it from our main semester repo to your cloned project repo.

Go to the `p2` directory in the main repo, then run the following (replacing `<PROJECT REPO>` with the path to where you cloned your repo:

```
cp -r property.proto property-original.proto src build.gradle settings.gradle cache.py parcel_lookup.py Dockerfile.java-dataset Dockerfile.cache Dockerfile.dataset docker-compose.yml addresses.csv.gz ai.md port.sh <PROJECT REPO>
cd <PROJECT REPO>
git add property.proto property-original.proto src build.gradle settings.gradle cache.py parcel_lookup.py Dockerfile.java-dataset Dockerfile.cache Dockerfile.dataset docker-compose.yml addresses.csv.gz ai.md port.sh
git commit -m 'starter code'
```

Now, look at the docker-compose.yaml file, and run this:

```
export PROJECT=p2
docker compose up --build -d -t 0
```

Things to note:
* this compose file specifies how to build the three Docker images needed for the project (look at the `context` and `dockerfile` fields), and the `--build` option tells compose to do the builds if anything has changed
* the `-t 0` option says to immediately replace existing containers if you want to update your code, without waiting
* all the port forwarding options specify 5000 as the port inside a container, but we do not specify what VM port should forward to this.  Compose will pick for you

Run `docker compose ps -a`.  You should see 3 cache containers with starter code and 2 dataset containers, based on Java.  The Python-based dataset servers will have exited because the code for them is not written yet (that will be your job!).

Determine the port number (VM side) for one of the cache containers, and send it a request for parcel `070922106137`:

```
curl localhost:<PORT>/parcelnum/070922106137
```

For your convenience, we provide a small script (port.sh) for looking up the external port number for one of your containers, because it make change each time.  You can use backticks to run the script to get the port number, then immediately use it in a curl command.  For example, you could do the following (change your container name as necessary):

```
curl localhost:`./port.sh p2-cache-1`/parcelnum/070922106137

```
You should get `{"addrs":["1308 W Dayton St"],"error":null,"source":"1"}`.  This indicates parcel number 070922106137 corresponds to "1308 W Dayton St" (Union South!).

For testing purposes, you make wish to bypass the cache, and fetch data from the dataset directly.  Note that these communicate via gRPC (not REST), so you will need a special program, which we provide (`parcel_lookup.py`), for making the gRPC call:

```
python3 parcel_lookup.py localhost `./port.sh p2-java-dataset-1` 070922106137
```

To run the above outside of a container, you need to create a Python venv and install gRPC/protobuf packages (check Dockerfile.cache and match versions).

## Architecture

The system has 7 containers managed by Docker Compose, which interact as follows:

<img src="arch.png" width=600>

| Service | Replicas | Language | Role |
|---|---|---|---|
| `cache` | 3 | Python/Flask | HTTP layer — receives web requests, forwards to dataset via gRPC |
| `java-dataset` | 2 | Java | gRPC server — serves address data (provided, reference implementation) |
| `dataset` | 2 | Python | gRPC server — you build this by porting the Java code |

The cache layer initially talks to `java-dataset`.  After you port the
backend to Python in Part 3, you'll switch it to talk to `dataset`
instead.

## Part 1: Load Balance and Retry

Write code for this part by hand, without AI code gen, in cache.py.

In cache.py, we have one stub corresponding to the server in java-dataset-1.  Create a second stub corresponding to the other Java dataset server, and keep track of what stub received the previous request.  Alternate between them to balance the load between the dataset servers (this is called *load balancing*).  The "source" field should indicate whether our result is from `java-dataset-1` ("2") or `java-dataset-1` ("2").

You should always think carefully about the different ways code can fail.  Ask: should we propogate an error (so it is more clear what went wrong)?  Can we handle the failure somehow?

Look at cache.py, and observe there are three broad cases to consider:
1. we get a gRPC response from the server, but the failed flag is True
2. the gRPC call produces a gRPC specific exception (browse this repo to learn what the exception is, and how to catch it: https://github.com/avinassh/grpc-errors/tree/master/python)
3. the gRPC call produces a different kind of exception

For (3), convert the exception to a str and return it in the "error" field of the JSON response.

For (2), try the gRPC request one more time, to the other dataset server.  If that one fails too, return "grpc error" in the "error" field of the JSON response.

Verify your work manually before proceeding:
1. repeatedly make requests with curl to one of the cache servers.  Make sure the "source" field alternates between the stubs.
2. use `docker kill` to kill one of the dataset containers.  Make sure the "source" always indicates we're getting a response from the healthy server
3. kill the other dataset and makes sure we get the expected "grpc error"

## Part 2: LRU Caching

Write code for this part by hand, without AI code gen.

Review the LRU cache implementation we did in class: https://git.doit.wisc.edu/cdis/cs/courses/cs544/s26/main/-/tree/main/demos/cache-practice.

Implement an LRU cache of size 6 in `cache.py` for `parcel_lookup`.  If there is a parcel number in the cache, we should use the cache ("source" will be "cache") instead of making a request to a dataset server.

## Part 3: Port Java Backend to Python

To install Aider, use pip to install the Aider installer program
(perhaps in a virtual env): `pip3 install aider-install`.  Then, run
the installer itself: `aider-install`.

Aider can be used in combination with different AI models.  For this
project, you are required to use `gemini-2.5-pro`.  To get access:

* go to https://aistudio.google.com/
* create an API key, and copy it
* store the key in an environment variable, like this: `export GEMINI_API_KEY="your-api-key-here"`.  You may want to put this in `~/.bashrc` so it runs with every new bash session (or whatever file is equivalent if you are using a different shell)
* follow the directions on [Canvas](https://canvas.wisc.edu/courses/501599/discussion_topics/2367597) to link it to your Google Cloud credits.

After `cd`ing to your the directory where you cloned the repo for your project, start Aider like this:

```
aider --model gemini/gemini-2.5-pro
```

Read through `src/main/java/DatasetServer.java` carefully.  Your goal
is to create a `dataset.py` that implements the same gRPC service in
Python — given a parcel string, it returns the same sorted list of
addresses.

Steps:
1. Create `dataset.py` implementing the `AddressByParcel` RPC
   - Read `addresses.csv.gz` at startup, build an in-memory index by parcel
   - Return addresses sorted alphanumerically (matching the Java behavior)
   - Serve on port 5000 with a single-threaded gRPC server
2. Complete `Dockerfile.dataset` so it copies in your `dataset.py` and runs it
3. Build and test:
   ```
   docker build . -f Dockerfile.dataset -t p2-dataset
   ```
4. Use `parcel_lookup.py` to verify your Python server returns the same
   results as the Java server (check mapped ports with `docker compose ps`):
   ```bash
   python parcel_lookup.py localhost <java-dataset-port> 081023301063
   python parcel_lookup.py localhost <dataset-port> 081023301063
   ```
   The output should be identical.
5. Once verified, update `cache.py` to point at the Python `dataset`
   containers instead of `java-dataset`:
   - Change `{project}-java-dataset-1:5000` → `{project}-dataset-1:5000`
   - Change `{project}-java-dataset-2:5000` → `{project}-dataset-2:5000`
6. Rebuild the cache image and redeploy to confirm everything still works end-to-end

**AI Requirement**: use Aider to help port the Java code.  Use `/ask`
to ask Aider about different approaches to reading the gzipped CSV in
Python.  Comment in `ai.md` about what you chose, and why.

## Part 4 (With Aider): New Endpoints End-to-End

Add two new lookup endpoints that go all the way through the stack:
new RPCs in the proto, new handler code in `dataset.py`, and new HTTP
routes in `cache.py`.

Before you start, look at the columns in `addresses.csv.gz` — you'll
need to figure out which columns to use.  Note that `StreetName` and
`Address` are different columns (e.g., `StreetName` might be
`"Congress"` while `Address` is `"5462 Congress Ave Unit 3"`).

| HTTP Route | Lookup Logic | Returns |
|---|---|---|
| `GET /addresses/zip/<zipcode>` | Match rows where `ZipCode` equals the given zipcode | `Address` values (sorted) |
| `GET /addresses/street/<street>` | Match rows where `StreetName` equals the given street name | `Address` values (sorted) |

Steps:
1. Extend `property.proto` with new RPC methods (you have flexibility
   in how you design the request/response messages)
2. Implement the new RPCs in `dataset.py`
3. Add new HTTP routes in `cache.py` that call the new RPCs
4. Rebuild all images (`Dockerfile.dataset` and `Dockerfile.cache`
   both compile the proto, so both need rebuilding)

Specifications:
* All endpoints return the same JSON shape: `{"addrs": [...], "source": "...", "error": null}`
* Addresses should be sorted alphanumerically
* Retry logic from Part 1 should apply to the new endpoints too
* No caching is required for the new endpoints

Example test:
```bash
curl http://localhost:<port>/addresses/zip/53718
curl http://localhost:<port>/addresses/street/Congress
```

**AI Requirement**: use Aider to help add these endpoints.  Ask Aider
for suggestions to make your code more efficient, and comment about
this in `ai.md`.

## Submission

Read the directions [here](../projects.md) about how to create the
repo.

Please add `.aider.input.history` and `.aider.chat.history.md` to
your repo, and fill in the `ai.md` file.  You must be able to build
and run like this:

```
docker build . -f Dockerfile.cache -t p2-cache
docker build . -f Dockerfile.dataset -t p2-dataset
docker compose up -d
```

We will copy in the `docker-compose.yml` and `addresses.csv.gz` files,
overwriting anything you might have changed.

## Tester

Use the **autobadger** tool on your machine to run tests against your code:

```bash
autobadger --project=p2 --verbose
```

The `--verbose` flag will print more information to the console as your tests are running.

Pushing to `main` will submit your project and we will grade your code
on `main` from a remote VM.  A GitLab issue should be pushed to your
repository shortly after you submit.
