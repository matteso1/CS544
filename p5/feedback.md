# P5 Project Specification Feedback

## Critical Issues to Fix Before Release

### 1. **Typo in Q6 (Line 237)**
There's a clear copy-paste error:
```
Measure the number of seconds it takes each of the three times we do the average calculations.s_generated` filtering only.
```
Should be something like:
```
Measure the number of seconds it takes each of the three times we do the average calculations.
```

### 2. **Inconsistent Terminology: cf_score vs cf_rating**
Throughout the spec, you use both `cf_score` and `cf_rating` interchangeably:
- Problems table has `cf_rating` (Q1, Q9 setup)
- Q9 instructions say "Train it... using `cf_score` for the label" but should be `cf_rating`
- The answer tuple also mentions `cf_rating` but the training instruction says `cf_score`

**Recommendation:** Use `cf_rating` consistently throughout.

### 3. **Tester Section**
Line 347 says "Coming soon..." - this should be updated before release or removed entirely.

### 4. **Missing GEMINI_API_KEY Setup Instructions**
Students are told to set `GEMINI_API_KEY` but not where to obtain it. Add:
- Link to get Gemini API key
- Whether students need to create their own account
- Any free tier limitations they should be aware of
- Whether the course provides keys

### 5. **Ambiguous boss/worker Dockerfile Instructions**
Line 108 says "look at the lecture code for spark" but doesn't specify which lecture directory or file. Be more specific, e.g., "See `lec/spark/` for example Dockerfiles."

## Moderate Issues

### 6. **Vague Learning Objective (Line 16)**
"grouping and optimizing queries" should be:
- Capitalized properly: "Grouping and optimizing queries"
- More specific: "Group data and optimize queries using bucketing and caching"

### 7. **Q1 Pattern Clarification**
The pattern "\_A." needs clarification. Is this:
- A literal string (underscore, A, period)?
- A regex pattern?
- Case sensitive as stated?

**Recommendation:** Add an example, e.g., "For example, 'problem_A.txt' matches but 'problem_a.txt' does not."

### 8. **Q3 Answer Format Confusion**
You show:
```python
{'Easy': 409, 'Medium': 5768, 'Hard': 2396}
```
But say "Your answer should return this dictionary" - this makes it sound like students should hardcode these values. Clarify: "Your answer should return a dictionary in this format (the exact counts will vary):" OR if these are the actual expected values, say "Your answer should compute and return this dictionary:"

### 9. **get_data.py Execution Details Missing**
Students aren't told:
- From which directory to run `get_data.py`
- Where the output files will be created
- How long the download will take (dataset size?)
- What to do if the download fails

### 10. **Docker Command Inconsistency**
Line 105 uses `docker compose` (no hyphen) but conventionally it could be `docker-compose` depending on the Docker version. Verify which version students will use.

## Minor Issues & Suggestions

### 11. **Port Number Verification**
Line 123 mentions port 5000 for Jupyter. Verify this is correct - Jupyter typically runs on 8888. If you've customized it to 5000, this is fine, but make sure it matches the docker-compose.yml configuration.

### 12. **Q2 Instruction Clarity**
"DO NOT HARDCODE THE CODEFORCES ID" - while good advice, explain why or give a hint about the proper approach. E.g., "Instead, filter the sources view where the name is 'CODEFORCES'."

### 13. **Q6 Instructions Flow**
The Q6 instructions could be clearer about what's being averaged:
```
Current: "Implement a query that first filters rows... Write some code to compute the average input_chars and output_chars over this DataFrame."

Suggested: "Implement a query that first filters rows of problem_tests to get rows where is_generated is False. You will compute the average of input_chars and output_chars columns on this filtered data."
```

### 14. **Q10 Output Format**
"The output for your Q10 cell should be both the plot image and the JSON string" - clarify whether these should both be in a single cell or if the plot displays automatically and the JSON prints below it.

### 15. **Missing Information**
Consider adding:
- Estimated time to complete (e.g., "This project should take 8-12 hours")
- Point distribution across questions
- Whether partial credit is available
- Deadlines/due date
- Whether the notebook should be run with "Restart & Run All" before submission

### 16. **Q9 Data Split Clarity**
The even/odd split based on `problem_id` is clever, but clarify:
- Is `problem_id` a numeric field or string?
- If string, how do students determine even/odd? (e.g., parse the numeric part, hash it, etc.)

### 17. **build.sh Script**
You mention "A build.sh script is included for your convenience" but don't explain what it does or when to use it. Either explain or remove the mention if it's obvious.

## Positive Aspects

✓ Clear structure with numbered questions
✓ Good use of example outputs to show expected format
✓ Progressive difficulty from basic queries to ML
✓ Integration of multiple Spark APIs (RDD, DataFrame, SQL)
✓ Modern and interesting dataset (DeepMind CodeContests)
✓ AI integration component is timely and relevant
✓ Explicit reminder to include question numbers as comments
✓ Helpful hint for SQL CASE statement in Q3
✓ Good coverage of important Spark concepts (bucketing, caching, query plans)

## Suggested Additions

1. **Debugging Tips Section:** Common issues students might face (HDFS connection errors, Spark context conflicts, etc.)
2. **Expected Runtime:** Note if certain queries are expected to take a long time
3. **Resource Requirements:** Confirm memory requirements for Docker containers
4. **Validation Checks:** Suggest students verify their setup by checking specific outputs before proceeding

## Overall Assessment

The project is well-structured and covers important Spark concepts. The main issues are typos, terminology inconsistencies, and missing setup details that could cause student confusion. Once the critical and moderate issues are addressed, this will be a solid project specification.
