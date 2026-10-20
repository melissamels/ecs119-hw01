"""
Part 2: Performance Comparisons

In this part, we will explore comparing the performance
of different pipelines.
First, we will set up some helper classes.
Then we will do a few comparisons
between two or more versions of a pipeline
to report which one is faster.
"""

import part1
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import math
import time
import io
import contextlib
from itertools import repeat
from pathlib import Path


"""
=== Questions 1-5: Throughput and Latency Helpers ===

We will design and fill out two helper classes.

The first is a helper class for throughput (Q1).
The class is created by adding a series of pipelines
(via .add_pipeline(name, size, func))
where name is a title describing the pipeline,
size is the number of elements in the input dataset for the pipeline,
and func is a function that can be run on zero arguments
which runs the pipeline (like def f()).

The second is a similar helper class for latency (Q3).

1. Throughput helper class

Fill in the add_pipeline, eval_throughput, and generate_plot functions below.
"""

# Number of times to run each pipeline in the following results.
# You may modify this as you go through the file if you like, but make sure
# you set it back to 10 at the end before you submit.
NUM_RUNS = 10

class ThroughputHelper:
    def __init__(self):
        # Initialize the object.
        # Pipelines: a list of functions, where each function
        # can be run on no arguments.
        # (like: def f(): ... )
        self.pipelines = []

        # Pipeline names
        # A list of names for each pipeline
        self.names = []

        # Pipeline input sizes
        self.sizes = []

        # Pipeline throughputs
        # This is set to None, but will be set to a list after throughputs
        # are calculated.
        self.throughputs = None

    def add_pipeline(self, name, size, func):
        self.names.append(name)
        self.sizes.append(size)
        self.pipelines.append(func)

    def compare_throughput(self):
        # Measure the throughput of all pipelines
        # and store it in a list in self.throughputs.
        # Make sure to use the NUM_RUNS variable.
        # Also, return the resulting list of throughputs,
        # in **number of items per second.**
        self.throughputs = []
        for size, func in zip(self.sizes, self.pipelines):
            start = time.perf_counter()
            for _ in range(NUM_RUNS):
                func()
            elapsed = time.perf_counter() - start
            self.throughputs.append(size * NUM_RUNS / elapsed)
        return self.throughputs

    def generate_plot(self, filename):
        # Generate a plot for throughput using matplotlib.
        # You can use any plot you like, but a bar chart probably makes
        # the most sense.
        # Make sure you include a legend.
        # Save the result in the filename provided.
        if self.throughputs is None:
            self.compare_throughput()
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.bar(self.names, self.throughputs, label="Throughput")
        ax.set_ylabel("Items per second")
        ax.set_title("Pipeline Throughput")
        ax.tick_params(axis="x", rotation=30)
        ax.legend()
        fig.tight_layout()
        Path(filename).parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(filename)
        plt.close(fig)

"""
As your answer to this part,
return the name of the method you decided to use in
matplotlib.

(Example: "boxplot" or "scatter")
"""

def q1():
    # Return plot method (as a string) from matplotlib
    return "bar"

"""
2. A simple test case

To make sure your monitor is working, test it on a very simple
pipeline that adds up the total of all elements in a list.

We will compare three versions of the pipeline depending on the
input size.
"""

LIST_SMALL = [10] * 100
LIST_MEDIUM = [10] * 100_000
LIST_LARGE = repeat(10, 100_000_000)  # Same 100 million tens, without an 800 MB list

def add_list(l):
    # TODO
    # Please use a for loop (not a built-in)
    total = 0
    for value in l:
        total += value
    return total

def q2a():
    # Create a ThroughputHelper object
    h = ThroughputHelper()
    for name, values in [("small", LIST_SMALL), ("medium", LIST_MEDIUM), ("large", LIST_LARGE)]:
        h.add_pipeline(name, 100_000_000 if name == "large" else len(values),
                       lambda values=values: add_list(values))
    result = h.compare_throughput()
    h.generate_plot("output/part2-q2a.png")
    return result

"""
2b.
Which pipeline has the highest throughput?
Is this what you expected?

=== ANSWER Q2b BELOW ===
The large pipeline had the highest throughput in my run. I expected the larger inputs to do more work, but throughput measures items per second, not total time. The large input spreads out the timing overhead.

=== END OF Q2b ANSWER ===
"""

"""
3. Latency helper class.

Now we will create a similar helper class for latency.

The helper should assume a pipeline that only has *one* element
in the input dataset.

It should use the NUM_RUNS variable as with throughput.
"""

LIST_ONE_ITEM = [10]

class LatencyHelper:
    def __init__(self):
        # Initialize the object.
        # Pipelines: a list of functions, where each function
        # can be run on no arguments.
        # (like: def f(): ... )
        self.pipelines = []

        # Pipeline names
        # A list of names for each pipeline
        self.names = []

        # Pipeline latencies
        # This is set to None, but will be set to a list after latencies
        # are calculated.
        self.latencies = None

    def add_pipeline(self, name, func):
        self.names.append(name)
        self.pipelines.append(func)

    def compare_latency(self):
        # Measure the latency of all pipelines
        # and store it in a list in self.latencies.
        # Also, return the resulting list of latencies,
        # in **milliseconds.**
        self.latencies = []
        for func in self.pipelines:
            start = time.perf_counter()
            for _ in range(NUM_RUNS):
                func()
            elapsed = time.perf_counter() - start
            self.latencies.append(elapsed * 1000 / NUM_RUNS)
        return self.latencies

    def generate_plot(self, filename):
        # Generate a plot for latency using matplotlib.
        # You can use any plot you like, but a bar chart probably makes
        # the most sense.
        # Make sure you include a legend.
        # Save the result in the filename provided.
        if self.latencies is None:
            self.compare_latency()
        fig, ax = plt.subplots(figsize=(8, 5))
        ax.bar(self.names, self.latencies, label="Latency")
        ax.set_ylabel("Milliseconds per item")
        ax.set_title("Pipeline Latency")
        ax.tick_params(axis="x", rotation=30)
        ax.legend()
        fig.tight_layout()
        Path(filename).parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(filename)
        plt.close(fig)

"""
As your answer to this part,
return the number of input items that each pipeline should
process if the class is used correctly.
"""

def q3():
    # Return the number of input items in each dataset,
    # for the latency helper to run correctly.
    return 1

"""
4. To make sure your monitor is working, test it on
the simple pipeline from Q2.

For latency, all three pipelines would only process
one item. Therefore instead of using
LIST_SMALL, LIST_MEDIUM, and LIST_LARGE,
for this question run the same pipeline three times
on a single list item.
"""

LIST_SINGLE_ITEM = [10] # Note: a list with only 1 item

def q4a():
    # Create a LatencyHelper object
    h = LatencyHelper()
    for name in ("first", "second", "third"):
        h.add_pipeline(name, lambda: add_list(LIST_SINGLE_ITEM))
    result = h.compare_latency()
    h.generate_plot("output/part2-q4a.png")
    return result

"""
4b.
How much did the latency vary between the three copies of the pipeline?
Is this more or less than what you expected?

=== ANSWER Q4b BELOW ===
The three latency measurements were close to each other. Small differences are normal because other things on the computer can affect timing.

=== END OF Q4b ANSWER ===
"""

"""
Now that we have our helpers, let's do a simple comparison.

NOTE: you may add other helper functions that you may find useful
as you go through this file.

5. Comparison on Part 1

Finally, use the helpers above to calculate the throughput and latency
of the pipeline in part 1.

Remember that for latency you should use a version of the pipeline with only one input row!
You may need to write a new version of the pipeline for this to work.
"""

# You will need these:
# part1.load_input
# part1.PART_1_PIPELINE

def q5a():
    # Return the throughput of the pipeline in part 1.
    # Three 100-row input files are processed by the original Part 1 pipeline.
    h = ThroughputHelper()
    with contextlib.redirect_stdout(io.StringIO()):
        size = sum(len(df) for df in part1.load_input())
        h.add_pipeline("part1", size, part1.PART_1_PIPELINE)
        return h.compare_throughput()[0]

def q5b():
    # Run the same data-processing stages as Part 1 on one ranking row.
    # Some Part 1 tasks require multiple rows (such as sampling five),
    # so use the stages that are meaningful for a one-row input.
    original_dfs = part1.load_input()
    one_row_dfs = [df.iloc[:1].copy() for df in original_dfs]

    def single_row_part1():
        dfs = [df.copy() for df in one_row_dfs]
        part1.q1(dfs)
        part1.q2(dfs)
        part1.q3(dfs)
        part1.q5b(dfs)
        part1.q7(dfs)
        part1.q8a(dfs)
        part1.q9(dfs)
        averages = part1.q10_helper(dfs)
        part1.q10(averages)
        part1.q11(averages)

    h = LatencyHelper()
    h.add_pipeline("part1 one row", lambda: _quiet_run(single_row_part1))
    return h.compare_latency()[0]


def _quiet_run(func):
    # Part 1 prints tables while processing. Do not benchmark console output.
    with contextlib.redirect_stdout(io.StringIO()):
        return func()

"""
===== Questions 6-10: Performance Comparison 1 =====

For our first performance comparison,
let's look at the cost of getting input from a file, vs. in an existing DataFrame.

6. We will use the same population dataset
that we used in lecture 3.

Load the data using load_input() given the file name.

- Make sure that you clean the data by removing
  continents and world data!
  (World data is listed under OWID_WRL)

Then, set up a simple pipeline that computes summary statistics
for the following:

- *Year over year increase* in population, per country

    (min, median, max, mean, and standard deviation)

How you should compute this:

- For each country, we need the maximum year and the minimum year
in the data. We should divide the population difference
over this time by the length of the time period.

- Make sure you throw out the cases where there is only one year
(if any).

- We should at this point have one data point per country.

- Finally, as your answer, return a list of the:
    min, median, max, mean, and standard deviation
  of the data.

Hints:
You can use the describe() function in Pandas to get these statistics.
You should be able to do something like
df.describe().loc["min"]["colum_name"]

to get a specific value from the describe() function.

You shouldn't use any for loops.
See if you can compute this using Pandas functions only.
"""

def load_input(filename):
    # Return a dataframe containing the population data
    # **Clean the data here**
    df = pd.read_csv(filename)
    # The aggregated regions have no ISO country code, and OWID codes
    # represent aggregates or historical regions, not current countries.
    df = df[df["Code"].notna() & ~df["Code"].str.startswith("OWID_", na=False)].copy()
    return df

def population_pipeline(df):
    # Input: the dataframe from load_input()
    # Return a list of min, median, max, mean, and standard deviation
    # Compute each country's change divided by its year span.
    by_country = df.groupby("Entity").agg(
        first_year=("Year", "min"), last_year=("Year", "max")
    )
    first = df.sort_values("Year").drop_duplicates("Entity", keep="first").set_index("Entity")
    last = df.sort_values("Year").drop_duplicates("Entity", keep="last").set_index("Entity")
    span = by_country["last_year"] - by_country["first_year"]
    yearly = ((last["Population (historical)"] - first["Population (historical)"]) / span).loc[span > 0]
    return [float(yearly.min()), float(yearly.median()), float(yearly.max()),
            float(yearly.mean()), float(yearly.std())]

def q6():
    # As your answer to this part,
    # call load_input() and then population_pipeline()
    # Return a list of min, median, max, mean, and standard deviation
    return population_pipeline(load_input("data/population.csv"))

"""
7. Varying the input size

Next we want to set up three different datasets of different sizes.

Create three new files,
    - data/population-small.csv
      with the first 600 rows
    - data/population-medium.csv
      with the first 6000 rows
    - data/population-single-row.csv
      with only the first row
      (for calculating latency)

You can edit the csv file directly to extract the first rows
(remember to also include the header row)
and save a new file.

Make four versions of load input that load your datasets.
(The _large one should use the full population dataset.)
Each should return a dataframe.

The input CSV file will have 600 rows, but the DataFrame (after your cleaning) may have less than that.
"""

def load_input_small():
    return load_input("data/population-small.csv")

def load_input_medium():
    return load_input("data/population-medium.csv")

def load_input_large():
    return load_input("data/population.csv")

def load_input_single_row():
    # This is the pipeline we will use for latency.
    return load_input("data/population-single-row.csv")

def q7():
    # Don't modify this part
    s = load_input_small()
    m = load_input_medium()
    l = load_input_large()
    x = load_input_single_row()
    return [len(s), len(m), len(l), len(x)]

"""
8.
Create baseline pipelines

First let's create our baseline pipelines.
Create four pipelines,
    baseline_small
    baseline_medium
    baseline_large
    baseline_latency

based on the three datasets above.
Each should call your population_pipeline from Q6.

Your baseline_latency function will not be very interesting
as the pipeline does not produce any meaningful output on a single row!
You may choose to instead run an example with two rows,
or you may fill in this function in any other way that you choose
that you think is meaningful.
"""

def baseline_small():
    return population_pipeline(load_input_small())

def baseline_medium():
    return population_pipeline(load_input_medium())

def baseline_large():
    return population_pipeline(load_input_large())

def baseline_latency():
    return population_pipeline(load_input_single_row())

def q8():
    # Don't modify this part
    _ = baseline_medium()
    return ["baseline_small", "baseline_medium", "baseline_large", "baseline_latency"]

"""
9.
Finally, let's compare whether loading an input from file is faster or slower
than getting it from an existing Pandas dataframe variable.

Create four new dataframes (constant global variables)
directly in the script.
Then use these to write 3 new pipelines:
    fromvar_small
    fromvar_medium
    fromvar_large
    fromvar_latency

These pipelines should produce the same answers as in Q8.

As your answer to this part;
a. Generate a plot in output/part2-q9a.png of the throughputs
    Return the list of 6 throughputs in this order:
    baseline_small, baseline_medium, baseline_large, fromvar_small, fromvar_medium, fromvar_large
b. Generate a plot in output/part2-q9b.png of the latencies
    Return the list of 2 latencies in this order:
    baseline_latency, fromvar_latency
"""

POPULATION_SMALL = load_input_small()
POPULATION_MEDIUM = load_input_medium()
POPULATION_LARGE = load_input_large()
POPULATION_SINGLE_ROW = load_input_single_row()

def fromvar_small():
    return population_pipeline(POPULATION_SMALL)

def fromvar_medium():
    return population_pipeline(POPULATION_MEDIUM)

def fromvar_large():
    return population_pipeline(POPULATION_LARGE)

def fromvar_latency():
    return population_pipeline(POPULATION_SINGLE_ROW)

def q9a():
    # Add all 6 pipelines for a throughput comparison
    # Generate plot in output/part2-q9a.png
    # Return list of 6 throughputs
    h = ThroughputHelper()
    for name, size, fn in [
        ("baseline_small", len(POPULATION_SMALL), baseline_small),
        ("baseline_medium", len(POPULATION_MEDIUM), baseline_medium),
        ("baseline_large", len(POPULATION_LARGE), baseline_large),
        ("fromvar_small", len(POPULATION_SMALL), fromvar_small),
        ("fromvar_medium", len(POPULATION_MEDIUM), fromvar_medium),
        ("fromvar_large", len(POPULATION_LARGE), fromvar_large)]:
        h.add_pipeline(name, size, fn)
    result = h.compare_throughput()
    h.generate_plot("output/part2-q9a.png")
    return result

def q9b():
    # Add 2 pipelines for a latency comparison
    # Generate plot in output/part2-q9b.png
    # Return list of 2 latencies
    h = LatencyHelper()
    h.add_pipeline("baseline_latency", baseline_latency)
    h.add_pipeline("fromvar_latency", fromvar_latency)
    result = h.compare_latency()
    h.generate_plot("output/part2-q9b.png")
    return result

"""
10.
Comment on the plots above!
How dramatic is the difference between the two pipelines?
Which differs more, throughput or latency?
What does this experiment show?

===== ANSWER Q10 BELOW =====
The variable pipelines avoid repeatedly reading CSV files. They are generally faster, especially for small inputs where loading the file takes a large part of the total time. Latency changes too, but these timings are noisy.

===== END OF Q10 ANSWER =====
"""

"""
===== Questions 11-14: Performance Comparison 2 =====

Our second performance comparison will explore vectorization.

Operations in Pandas use Numpy arrays and vectorization to enable
fast operations.
In particular, they are often much faster than using for loops.

Let's explore whether this is true!

11.
First, we need to set up our pipelines for comparison as before.

We already have the baseline pipelines from Q8,
so let's just set up a comparison pipeline
which uses a for loop to calculate the same statistics.

Your pipeline should produce the same answers as in Q6 and Q8.

Create a new pipeline:
- Iterate through the dataframe entries. You can assume they are sorted.
- Manually compute the minimum and maximum year for each country.
- Compute the same answers as in Q6.
- Manually compute the summary statistics for the resulting list (min, median, max, mean, and standard deviation).
"""

def for_loop_pipeline(df):
    # Input: the dataframe from load_input()
    # Return a list of min, median, max, mean, and standard deviation
    # Walk rows to collect the first and last observation for each country.
    first_and_last = {}
    for row in df.itertuples(index=False):
        country, year, population = row.Entity, row.Year, row[3]
        if country not in first_and_last:
            first_and_last[country] = [year, population, year, population]
        else:
            v = first_and_last[country]
            if year < v[0]:
                v[0], v[1] = year, population
            if year > v[2]:
                v[2], v[3] = year, population
    increases = []
    for start_year, start_pop, end_year, end_pop in first_and_last.values():
        if end_year > start_year:
            increases.append((end_pop - start_pop) / (end_year - start_year))
    if not increases:
        return [float("nan")] * 5
    increases.sort()
    n = len(increases)
    mid = (increases[(n - 1) // 2] + increases[n // 2]) / 2
    avg = sum(increases) / n
    variance = sum((v - avg) ** 2 for v in increases) / (n - 1) if n > 1 else float("nan")
    return [float(increases[0]), float(mid), float(increases[-1]),
            float(avg), float(math.sqrt(variance))]

def q11():
    # As your answer to this part, call load_input() and then
    # for_loop_pipeline() to return the 5 numbers.
    # (these should match the numbers you got in Q6.)
    # ** Please return these as Python floats, not Numpy **
    return for_loop_pipeline(load_input("data/population.csv"))

"""
12.
Now, let's create our pipelines for comparison.

As before, write 4 pipelines based on the datasets from Q7.
"""

def for_loop_small():
    return for_loop_pipeline(load_input_small())

def for_loop_medium():
    return for_loop_pipeline(load_input_medium())

def for_loop_large():
    return for_loop_pipeline(load_input_large())

def for_loop_latency():
    return for_loop_pipeline(load_input_single_row())

def q12():
    # Don't modify this part
    _ = for_loop_medium()
    return ["for_loop_small", "for_loop_medium", "for_loop_large", "for_loop_latency"]

"""
13.
Finally, let's compare our two pipelines,
as we did in Q9.

a. Generate a plot in output/part2-q13a.png of the throughputs
    Return the list of 6 throughputs in this order:
    baseline_small, baseline_medium, baseline_large, for_loop_small, for_loop_medium, for_loop_large

b. Generate a plot in output/part2-q13b.png of the latencies
    Return the list of 2 latencies in this order:
    baseline_latency, for_loop_latency
"""

def q13a():
    # Add all 6 pipelines for a throughput comparison
    # Generate plot in output/part2-q13a.png
    # Return list of 6 throughputs
    h = ThroughputHelper()
    for name, size, fn in [
        ("baseline_small", len(POPULATION_SMALL), baseline_small),
        ("baseline_medium", len(POPULATION_MEDIUM), baseline_medium),
        ("baseline_large", len(POPULATION_LARGE), baseline_large),
        ("for_loop_small", len(POPULATION_SMALL), for_loop_small),
        ("for_loop_medium", len(POPULATION_MEDIUM), for_loop_medium),
        ("for_loop_large", len(POPULATION_LARGE), for_loop_large)]:
        h.add_pipeline(name, size, fn)
    result = h.compare_throughput()
    h.generate_plot("output/part2-q13a.png")
    return result

def q13b():
    # Add 2 pipelines for a latency comparison
    # Generate plot in output/part2-q13b.png
    # Return list of 2 latencies
    h = LatencyHelper()
    h.add_pipeline("baseline_latency", baseline_latency)
    h.add_pipeline("for_loop_latency", for_loop_latency)
    result = h.compare_latency()
    h.generate_plot("output/part2-q13b.png")
    return result

"""
14.
Comment on the results you got!

14a. Which pipelines is faster in terms of throughput?

===== ANSWER Q14a BELOW =====
In my run, the for-loop pipelines had higher throughput for the small and medium inputs. The Pandas version was slightly ahead for the large input. The winner depends on the input size.

===== END OF Q14a ANSWER =====

14b. Which pipeline is faster in terms of latency?

===== ANSWER Q14b BELOW =====
The loop pipeline had lower latency in my run. Since this test only has one row, setting up a Pandas groupby adds more overhead than the actual work.

===== END OF Q14b ANSWER =====

14c. Do you notice any other interesting observations?
What does this experiment show?

===== ANSWER Q14c BELOW =====
The timing depends on both the amount of data and the work being done. Vectorization is useful, but groupby setup also has a cost.

===== END OF Q14c ANSWER =====
"""

"""
===== Questions 15-17: Reflection Questions =====
15.

Take a look at all your pipelines above.
Which factor that we tested (file vs. variable, vectorized vs. for loop)
had the biggest impact on performance?

===== ANSWER Q15 BELOW =====
In my timing results, reusing an existing DataFrame made a big difference, especially for the large dataset. Using a loop instead of Pandas also changed performance, but the winner depended on input size.

===== END OF Q15 ANSWER =====

16.
Based on all of your plots, form a hypothesis as to how throughput
varies with the size of the input dataset.

(Any hypothesis is OK as long as it is supported by your data!
This is an open ended question.)

===== ANSWER Q16 BELOW =====
My hypothesis is that throughput changes as the input gets bigger because the startup cost is spread over more rows, but it may level off for large inputs.

===== END OF Q16 ANSWER =====

17.
Based on all of your plots, form a hypothesis as to how
throughput is related to latency.

(Any hypothesis is OK as long as it is supported by your data!
This is an open ended question.)

===== ANSWER Q17 BELOW =====
For the same amount of work, higher latency usually means lower throughput. They are related, but the input sizes have to match for the comparison to be fair.

===== END OF Q17 ANSWER =====
"""

"""
===== Extra Credit =====

This part is optional.

Use your pipeline to compare something else!

Here are some ideas for what to try:
- the cost of random sampling vs. the cost of getting rows from the
  DataFrame manually
- the cost of cloning a DataFrame
- the cost of sorting a DataFrame prior to doing a computation
- the cost of using different encodings (like one-hot encoding)
  and encodings for null values
- the cost of querying via Pandas methods vs querying via SQL
  For this part: you would want to use something like
  pandasql that can run SQL queries on Pandas data frames. See:
  https://stackoverflow.com/a/45866311/2038713

As your answer to this part,
as before, return
a. the list of 6 throughputs
and
b. the list of 2 latencies.

and generate plots for each of these in the following files:
    output/part2-ec-a.png
    output/part2-ec-b.png
"""

# Extra credit (optional)

def extra_credit_a():
    # Compare sorted versus unsorted DataFrame computations.
    h = ThroughputHelper()
    for name, data in [("unsorted-small", POPULATION_SMALL), ("unsorted-medium", POPULATION_MEDIUM),
                       ("unsorted-large", POPULATION_LARGE)]:
        h.add_pipeline(name, len(data), lambda data=data: population_pipeline(data))
    for name, data in [("sorted-small", POPULATION_SMALL), ("sorted-medium", POPULATION_MEDIUM),
                       ("sorted-large", POPULATION_LARGE)]:
        h.add_pipeline(name, len(data), lambda data=data: population_pipeline(data.sort_values("Year")))
    result = h.compare_throughput()
    h.generate_plot("output/part2-ec-a.png")
    return result

def extra_credit_b():
    h = LatencyHelper()
    h.add_pipeline("unsorted", lambda: population_pipeline(POPULATION_SINGLE_ROW))
    h.add_pipeline("sorted", lambda: population_pipeline(POPULATION_SINGLE_ROW.sort_values("Year")))
    result = h.compare_latency()
    h.generate_plot("output/part2-ec-b.png")
    return result

"""
===== Wrapping things up =====

**Don't modify this part.**

To wrap things up, we have collected
your answers and saved them to a file below.
This will be run when you run the code.
"""

ANSWER_FILE = "output/part2-answers.txt"
UNFINISHED = 0

def log_answer(name, func, *args):
    try:
        answer = func(*args)
        print(f"{name} answer: {answer}")
        with open(ANSWER_FILE, 'a') as f:
            f.write(f'{name},{answer}\n')
            print(f"Answer saved to {ANSWER_FILE}")
    except NotImplementedError:
        print(f"Warning: {name} not implemented.")
        with open(ANSWER_FILE, 'a') as f:
            f.write(f'{name},Not Implemented\n')
        global UNFINISHED
        UNFINISHED += 1

def PART_2_PIPELINE():
    open(ANSWER_FILE, 'w').close()

    # Q1-5
    log_answer("q1", q1)
    log_answer("q2a", q2a)
    # 2b: commentary
    log_answer("q3", q3)
    log_answer("q4a", q4a)
    # 4b: commentary
    log_answer("q5a", q5a)
    log_answer("q5b", q5b)

    # Q6-10
    log_answer("q6", q6)
    log_answer("q7", q7)
    log_answer("q8", q8)
    log_answer("q9a", q9a)
    log_answer("q9b", q9b)
    # 10: commentary

    # Q11-14
    log_answer("q11", q11)
    log_answer("q12", q12)
    log_answer("q13a", q13a)
    log_answer("q13b", q13b)
    # 14: commentary

    # 15-17: reflection
    # 15: commentary
    # 16: commentary
    # 17: commentary

    # Extra credit
    log_answer("extra credit (a)", extra_credit_a)
    log_answer("extra credit (b)", extra_credit_b)

    # Answer: return the number of questions that are not implemented
    if UNFINISHED > 0:
        print("Warning: there are unfinished questions.")

    return UNFINISHED

"""
=== END OF PART 2 ===

Main function
"""

if __name__ == '__main__':
    log_answer("PART 2", PART_2_PIPELINE)
