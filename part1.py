"""
Part 1: Data Processing in Pandas

=== Instructions ===

There are 22 questions in this part.
For each part you will implement a function (q1, q2, etc.)
Each function will take as input a data frame
or a list of data frames and return the answer
to the given question.

To run your code, you can run `python3 part1.py`.
This will run all the questions that you have implemented so far.
It will also save the answers to part1-answers.txt.

=== Dataset ===

In this part, we will use a dataset of world university rankings
called the "QS University Rankings".

The ranking data was taken 2019--2021 from the following website:
https://www.topuniversities.com/university-rankings/world-university-rankings/2021

=== Grading notes ===

- Once you have completed this part, make sure that
  your code runs, that part1-answers.txt is being re-generated
  every time the code is run, and that the answers look
  correct to you.

- Be careful about output types. For example if the question asks
  for a list of DataFrames, don't return a numpy array or a single
  DataFrame. When in doubt, ask on Piazza!

- Make sure that you remove any NotImplementedError exceptions;
  you won't get credit for any part that raises this exception
  (but you will still get credit for future parts that do not raise it
  if they don't depend on the previous parts).

- Make sure that you fill in answers for the parts
  marked "ANSWER ___ BELOW" and that you don't modify
  the lines above and below the answer space.

- Q6 has a few unit tests to help you check your work.
  Make sure that you removed the `@pytest.mark.skip` decorators
  and that all tests pass (show up in green, no red text!)
  when you run `pytest part3.py`.

- For plots: There are no specific requirements on which
  plotting methods you use; if not specified, use whichever
  plot you think might be most appropriate for the data
  at hand.
  Please ensure your plots are labeled and human-readable.
  For example, call .legend() on the plot before saving it!

===== Questions 1-6: Getting Started =====

To begin, let's load the Pandas library.
"""

import pandas as pd

"""
1. Load the dataset into Pandas

Our first step is to load the data into a Pandas DataFrame.
We will also change the column names
to lowercase and reorder to get only the columns we are interested in.

Implement the rest of the function load_input()
by filling in the parts marked TODO below.

Return as your answer to q1 the number of dataframes loaded.
(This part is implemented for you.)
"""

NEW_COLUMNS = ['rank', 'university', 'region', 'academic reputation', 'employer reputation', 'faculty student', 'citations per faculty', 'overall score']

def load_input():
    # Read each year's rankings.
    df_2019 = pd.read_csv('data/2019.csv', encoding='latin-1')
    df_2020 = pd.read_csv('data/2020.csv', encoding='latin-1')
    df_2021 = pd.read_csv('data/2021.csv', encoding='latin-1')
    for df in [df_2019, df_2020, df_2021]:
        df.columns = df.columns.str.lower()
    # Keep only the columns we need, in the requested order.
    df_2019 = df_2019[NEW_COLUMNS]
    df_2020 = df_2020[NEW_COLUMNS]
    df_2021 = df_2021[NEW_COLUMNS]
    return [df_2019, df_2020, df_2021]

def q1(dfs):
    # As the "answer" to this part, let's just return the number of dataframes.
    # Check that your answer shows up in part1-answers.txt.
    return len(dfs)

"""
2. Input validation

Let's do some basic sanity checks on the data for Q1.

Check that all three data frames have the same shape,
and the correct number of rows and columns in the correct order.

As your answer to q2, return True if all validation checks pass,
and False otherwise.
"""

def q2(dfs):
    # All three tables should have matching dimensions and columns.
    return all(df.shape == dfs[0].shape and
               list(df.columns) == NEW_COLUMNS for df in dfs)

"""
===== Interlude: Checking your output so far =====

Run your code with `python3 part1.py` and open up the file
output/part1-answers.txt to see if the output looks correct so far!

You should check your answers in this file after each part.

You are welcome to also print out stuff to the console
in each question if you find it helpful.
"""

ANSWER_FILE = "output/part1-answers.txt"

def interlude():
    print("Answers so far:")
    with open(f"{ANSWER_FILE}") as fh:
        print(fh.read())

"""
===== End of interlude =====

3a. Input validation, continued

Now write a validate another property: that the set of university names
in each year is the same.
As in part 2, return a Boolean value.
(True if they are the same, and False otherwise)

Once you implement and run your code,
remember to check the output in part1-answers.txt.
(True if the checks pass, and False otherwise)
"""

def q3(dfs):
    names = [set(df['university']) for df in dfs]
    return names[0] == names[1] == names[2]

"""
3b (commentary).
Did the checks pass or fail?
Comment below and explain why.

=== ANSWER Q3b BELOW ===
The check failed. The top 100 universities are not exactly the same in all three years. Some universities moved in or out of the list.
=== END OF Q3b ANSWER ===
"""

"""
4. Random sampling

Now that we have the input data validated, let's get a feel for
the dataset we are working with by taking a random sample of 5 rows
at a time.

Implement q4() below to sample 5 points from each year's data.

As your answer to this part, return the *university name*
of the 5 samples *for 2021 only* as a list.
(That is: ["University 1", "University 2", "University 3", "University 4", "University 5"])

Code design: You can use a for for loop to iterate over the dataframes.
If df is a DataFrame, df.sample(5) returns a random sample of 5 rows.

Hint:
    to get the university name:
    try .iloc on the sample, then ["university"].
"""

def q4(dfs):
    samples = []
    for year, df in zip([2019, 2020, 2021], dfs):
        sample = df.sample(5)
        print(f"Sample for {year}:")
        print(sample)
        samples.append(sample)
    return samples[2]['university'].tolist()

"""
Once you have implemented this part,
you can run a few times to see different samples.

4b (commentary).
Based on the data, write down at least 2 strengths
and 3 weaknesses of this dataset.
This is subjective - you may interpret this however you like!
If you were to use this dataset for a project, what would *you* consider to be
some advantages and drawbacks?

=== ANSWER Q4b BELOW ===
Strengths:
1. It includes several measures besides the overall ranking.
2. It covers three years, so we can compare changes.

Weaknesses:
1. Some scores could be missing.
2. The data only includes ranked universities, not every university.
3. Reputation scores can be subjective.
=== END OF Q4b ANSWER ===
"""

"""
5. Data cleaning

Let's see where we stand in terms of null values.
We can do this in two different ways.

a. Use .info() to see the number of non-null values in each column
displayed in the console.

b. Write a version using .count() to calculate the number of
non-null values in each column.

In both 5a and 5b: return as your answer
*for the 2021 data only*
as a list of the number of non-null values in each column.

Example: if there are 5 non-null values in the first column, 3 in the second, 4 in the third, and so on, you would return
    [5, 3, 4, ...]
"""

def q5a(dfs):
    # info() prints the non-null counts. We also collect those counts
    # as a list for the answer file.
    for df in dfs:
        df.info()
    return dfs[2].notna().sum().tolist()
    # Remember to return the list here
    # (Since .info() does not return any values,
    # for this part, you will need to copy and paste
    # the output as a hardcoded list.)

def q5b(dfs):
    for df in dfs:
        print(df.count())
    return dfs[2].count().tolist()
    # Remember to return the list here

"""
5c.
One other thing:
Also fill this in with how many non-null values are expected (for the 2021 data).
This should be a list for each column as before.
We will use this in the unit tests below.
"""

def q5c():
    # The provided 2021 file has 100 non-null values in every selected column.
    return [100, 100, 100, 100, 100, 100, 100, 100]
    # TODO: fill this in with the expected number
    # num_non_null = [0, 0, ...]
    # return num_non_null

"""
===== Interlude again: Unit tests =====

Unit tests

Now that we have completed a few parts,
let's talk about unit tests.
We won't be using them for the entire assignment
(in fact we won't be using them after this),
but they can be a good way to ensure your work is correct
without having to manually inspect the output.

We need to import pytest first.
"""

import pytest

"""
The following are a few unit tests for Q1-5.

To run the unit tests,
first, remove (or comment out) the `@pytest.mark.skip` decorator
from each unit test (function beginning with `test_`).
Then, run `pytest part1.py` in the terminal.
"""

def test_q1():
    dfs = load_input()
    assert len(dfs) == 3
    assert all([isinstance(df, pd.DataFrame) for df in dfs])

def test_q2():
    dfs = load_input()
    assert q2(dfs)

@pytest.mark.xfail(reason="University sets may differ across years", strict=False)
def test_q3():
    dfs = load_input()
    assert q3(dfs)

def test_q4():
    dfs = load_input()
    samples = q4(dfs)
    assert len(samples) == 5

def test_q5():
    dfs = load_input()
    num_non_null = q5c()
    assert len(num_non_null) > 0
    assert q5a(dfs) == num_non_null
    assert q5b(dfs) == num_non_null

"""
6a. Are there any tests which fail?

=== ANSWER Q6a BELOW ===
Yes. The test for q3 fails because the university lists are not exactly the same each year.
=== END OF Q6a ANSWER ===

6b. For each test that fails, is it because your code
is wrong or because the test is wrong?

=== ANSWER Q6b BELOW ===
The q3 code is correct. The test expects True, but there are changes in the university lists across the years, so the test assumption is wrong.
=== END OF Q6b ANSWER ===

IMPORTANT: for any failing tests, if you think you have
not made any mistakes, mark it with
@pytest.mark.xfail
above the test to indicate that the test is expected to fail.
Run pytest part1.py again to see the new output.

6c. Return the number of tests that failed, even after your
code was fixed as the answer to this part.
(As an integer)
Please include expected failures (@pytest.mark.xfail).
(If you have no failing or xfail tests, return 0.)
"""

def q6c():
    # One provided test assumes the university lists are identical.
    # This is an expected failure only when the lists differ.
    return int(not q3(load_input()))

"""
===== End of interlude =====

===== Questions 7-10: Data Processing =====

7. Adding columns

Notice that there is no 'year' column in any of the dataframe. As your first task, append an appropriate 'year' column in each dataframe.

Append a column 'year' in each dataframe. It must correspond to the year for which the data is represented.

As your answer to this part, return the number of columns in each dataframe after the addition.
"""

def q7(dfs):
    for year, df in zip([2019, 2020, 2021], dfs):
        df['year'] = year
    return [len(df.columns) for df in dfs]
    # Remember to return the list here

"""
8a.
Next, find the count of universities in each region that made it to the Top 100 each year. Print all of them.

As your answer, return the count for "USA" in 2021.
"""

def q8a(dfs):
    for year, df in zip([2019, 2020, 2021], dfs):
        counts = df[pd.to_numeric(df['rank'], errors='coerce') <= 100]['region'].value_counts()
        print(f"Top 100 by region in {year}:")
        print(counts)
        if year == 2021:
            usa_count = int(counts.get('USA', 0))
    return usa_count
    # Remember to return the count here

"""
8b.
Do you notice some trend? Comment on what you observe and why might that be consistent throughout the years.

=== ANSWER Q8b BELOW ===
The USA has the most universities in the top 100 in all three years: 30 in 2019 and 29 in both 2020 and 2021. The UK stays close to 18 or 19. This seems reasonable since both have a lot of established research universities.
=== END OF Q8b ANSWER ===
"""

"""
9.
From the data of 2021, find the average score of all attributes for all universities.

As your answer, return the list of averages (for all attributes)
in the order they appear in the dataframe:
academic reputation, employer reputation, faculty student, citations per faculty, overall score.

The list should contain 5 elements.
"""

def q9(dfs):
    columns = NEW_COLUMNS[3:]
    scores = dfs[2][columns].apply(pd.to_numeric, errors='coerce')
    return scores.mean().tolist()
    # Return the list here

"""
10.
From the same data of 2021, now find the average of *each* region for **all** attributes **excluding** 'rank' and 'year'.

In the function q10_helper, store the results in a variable named **avg_2021**
and return it.

Then in q10, print the first 5 rows of the avg_2021 dataframe.
"""

def q10_helper(dfs):
    columns = NEW_COLUMNS[3:]
    scores = dfs[2][['region'] + columns].copy()
    scores[columns] = scores[columns].apply(pd.to_numeric, errors='coerce')
    avg_2021 = scores.groupby('region')[columns].mean()
    return avg_2021

def q10(avg_2021):
    print(avg_2021.head(5))
    return 5
    # Return 5

"""
===== Questions 11-14: Exploring the avg_2021 dataframe =====

11.
Sort the avg_2021 dataframe from the previous question based on overall score in a descending fashion (top to bottom).

As your answer to this part, return the first row of the sorted dataframe.
"""

def q11(avg_2021):
    sorted_df = avg_2021.sort_values('overall score', ascending=False)
    print(sorted_df.head())
    return sorted_df.iloc[0]

"""
12a.
What do you observe from the table above? Which country tops the ranking?

What is one country that went down in the rankings
between 2019 and 2021?

You will need to load the data from 2019 to get the answer to this part.
You may choose to do this
by writing another function like q10_helper and running q11,
or you may just do it separately
(e.g., in a Python shell) and return the name of the country/region
that you found went down in the rankings.

Errata: please note that the 2021 dataset we provided is flawed
(it is almost identical to the 2020 data).
This is why the question now asks for the difference between 2019 and 2021.

For the answer to this part return the name of the country/region that tops the ranking
and the name of one country/region that went down in the rankings.
"""

def q12a(avg_2021):
    top_2021 = avg_2021['overall score'].idxmax()
    # Compare average overall score rankings between 2019 and 2021.
    df_2019 = pd.read_csv('data/2019.csv', encoding='latin-1')
    df_2019.columns = df_2019.columns.str.lower()
    scores_2019 = df_2019[['region', 'overall score']].copy()
    scores_2019['overall score'] = pd.to_numeric(scores_2019['overall score'], errors='coerce')
    avg_2019 = scores_2019.groupby('region')['overall score'].mean()
    rank_2019 = avg_2019.rank(ascending=False, method='min')
    rank_2021 = avg_2021['overall score'].rank(ascending=False, method='min')
    dropped = [name for name in rank_2019.index.intersection(rank_2021.index)
               if rank_2021[name] > rank_2019[name]]
    dropped_region = dropped[0] if dropped else 'None found'
    return (top_2021, dropped_region)

"""
12b.
Comment on why the country above is at the top of the list.
(Note: This is an open-ended question.)

=== ANSWER Q12b BELOW ===
Singapore comes first by average overall score. Its two universities in this dataset have high scores, especially on faculty-student ratio and citations. Since there are only two, the average can also be higher than in countries with more universities.
=== END OF Q12b ANSWER ===
"""

"""
13a.
Represent all the attributes in the avg_2021 dataframe using a box and whisker plot.

Store your plot in output/part1-13a.png.

As the answer to this part, return the name of the plot you saved.

**Hint:** You can do this using subplots (and also otherwise)
"""

import matplotlib.pyplot as plt

def q13a(avg_2021):
    avg_2021.boxplot(rot=30, figsize=(10, 6))
    plt.title('Average ranking attributes by region (2021)')
    plt.ylabel('Score')
    plt.tight_layout()
    plt.savefig('output/part1-13a.png')
    plt.close()
    return 'output/part1-13a.png'
    # return "output/part1-13a.png"

"""
b. Do you observe any anomalies in the box and whisker
plot?

=== ANSWER Q13b BELOW ===
The overall-score plot has Singapore as a high outlier. The spreads also look different depending on the attribute, so the regions do not all perform similarly.
=== END OF Q13b ANSWER ===
"""

"""
14a.
Pick two attributes in the avg_2021 dataframe
and represent them using a scatter plot.

Store your plot in output/part1-14a.png.

As the answer to this part, return the name of the plot you saved.
"""

def q14a(avg_2021):
    plt.figure(figsize=(7, 5))
    plt.scatter(avg_2021['academic reputation'], avg_2021['overall score'])
    plt.xlabel('Academic reputation')
    plt.ylabel('Overall score')
    plt.title('Academic reputation vs overall score (2021)')
    plt.tight_layout()
    plt.savefig('output/part1-14a.png')
    plt.close()
    return 'output/part1-14a.png'
    # return "output/part1-14a.png"

"""
Do you observe any general trend?

=== ANSWER Q14b BELOW ===
There is a general upward trend: regions with better academic reputation often have better overall scores too. But the points are spread out, so reputation is not the only thing affecting the score.
=== END OF Q14b ANSWER ===

===== Questions 15-20: Exploring the data further =====

We're more than halfway through!

Let's come to the Top 10 Universities and observe how they performed over the years.

15. Create a smaller dataframe which has the top ten universities from each year, and only their overall scores across the three years.

Hint:

*   There will be four columns in the dataframe you make
*   The top ten universities are same across the three years. Only their rankings differ.
*   Use the merge function. You can read more about how to use it in the documentation: https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.merge.html
*   Shape of the resultant dataframe should be (10, 4)

As your answer, return the shape of the new dataframe.
"""

def q15_helper(dfs):
    tables = []
    for year, df in zip([2019, 2020, 2021], dfs):
        top = df.copy()
        top['rank_num'] = pd.to_numeric(top['rank'], errors='coerce')
        top = top.nsmallest(10, 'rank_num')[['university', 'overall score']]
        top = top.rename(columns={'overall score': f'score_{year}'})
        tables.append(top)
    top_10 = tables[0].merge(tables[1], on='university').merge(tables[2], on='university')
    return top_10

def q15(top_10):
    print(top_10)
    return top_10.shape

"""
16.
You should have noticed that when you merged,
Pandas auto-assigned the column names. Let's change them.

For the columns representing scores, rename them such that they describe the data that the column holds.

You should be able to modify the column names directly in the dataframe.
As your answer, return the new column names as a list.
"""

def q16(top_10):
    top_10.columns = ['university', 'score_2019', 'score_2020', 'score_2021']
    return list(top_10.columns)
    # return list(df.columns)

"""
17a.
Draw a suitable plot to show how the overall scores of the Top 10 universities varied over the three years. Clearly label your graph and attach a legend. Explain why you chose the particular plot.

Save your plot in output/part1-17a.png.

As the answer to this part, return the name of the plot you saved.

Note:
*   All universities must be in the same plot.
*   Your graph should be clear and legend should be placed suitably
"""

def q17a(top_10):
    score_columns = [c for c in top_10.columns if c != 'university']
    plt.figure(figsize=(11, 6))
    for _, row in top_10.iterrows():
        plt.plot([2019, 2020, 2021],
                 [pd.to_numeric(row[c], errors='coerce') for c in score_columns],
                 marker='o', label=row['university'])
    plt.xticks([2019, 2020, 2021])
    plt.xlabel('Year')
    plt.ylabel('Overall score')
    plt.title('Top universities: overall scores across three years')
    plt.legend(bbox_to_anchor=(1.02, 1), loc='upper left', fontsize=8)
    plt.tight_layout()
    plt.savefig('output/part1-17a.png', bbox_inches='tight')
    plt.close()
    return 'output/part1-17a.png'
    # return "output/part1-17a.png"

"""
17b.
What do you observe from the plot above? Which university has remained consistent in their scores? Which have increased/decreased over the years?

=== ANSWER Q17b BELOW ===
I used a line graph because it makes the changes across three years easy to compare. MIT stayed at 100 every year. UCL and Imperial College London increased, while Harvard and the University of Chicago decreased. The 2020 and 2021 scores are the same here for these universities.
=== END OF Q17b ANSWER ===
"""

"""
===== Questions 18-19: Correlation matrices =====

We're almost done!

Let's look at another useful tool to get an idea about how different variables are corelated to each other. We call it a **correlation matrix**

A correlation matrix provides a correlation coefficient (a number between -1 and 1) that tells how strongly two variables are correlated. Values closer to -1 mean strong negative correlation whereas values closer to 1 mean strong positve correlation. Values closer to 0 show variables having no or little correlation.

You can learn more about correlation matrices from here: https://www.statology.org/how-to-read-a-correlation-matrix/

18.
Plot a correlation matrix to see how each variable is correlated to another. You can use the data from 2021.

Print your correlation matrix and save it in output/part1-18.png.

As the answer to this part, return the name of the plot you saved.

**Helpful link:** https://datatofish.com/correlation-matrix-pandas/
"""

def q18(dfs):
    numeric = dfs[2][['rank'] + NEW_COLUMNS[3:]].apply(pd.to_numeric, errors='coerce')
    corr = numeric.corr()
    print(corr)
    fig, ax = plt.subplots(figsize=(9, 7))
    im = ax.imshow(corr, vmin=-1, vmax=1, cmap='coolwarm')
    ax.set_xticks(range(len(corr.columns)), corr.columns, rotation=45, ha='right')
    ax.set_yticks(range(len(corr.index)), corr.index)
    fig.colorbar(im, ax=ax, label='Correlation')
    plt.title('2021 ranking correlations')
    plt.tight_layout()
    plt.savefig('output/part1-18.png')
    plt.close()
    return 'output/part1-18.png'
    # return "output/part1-18.png"

"""
19. Comment on at least one entry in the matrix you obtained in the previous
part that you found surprising or interesting.

=== ANSWER Q19 BELOW ===
The relationship between rank and overall score is interesting because smaller rank numbers mean better universities. So a negative correlation makes sense even when better scores mean better performance.
=== END OF Q19 ANSWER ===
"""

"""
===== Questions 20-23: Data manipulation and falsification =====

This is the last section.

20. Exploring data manipulation and falsification

For fun, this part will ask you to come up with a way to alter the
rankings such that your university of choice comes out in 1st place.

The data does not contain UC Davis, so let's pick a different university.
UC Berkeley is a public university nearby and in the same university system,
so let's pick that one.

We will write two functions.
a.
First, write a function that calculates a new column
(that is you should define and insert a new column to the dataframe whose value
depends on the other columns)
and calculates
it in such a way that Berkeley will come out on top in the 2021 rankings.

Note: you can "cheat"; it's OK if your scoring function is picked in some way
that obviously makes Berkeley come on top.
As an extra challenge to make it more interesting, you can try to come up with
a scoring function that is subtle!

b.
Use your new column to sort the data by the new values and return the top 10 university names as a list.

"""

def q20a(dfs):
    df = dfs[2]
    # A deliberately biased score to show how easy manipulation can be.
    original = pd.to_numeric(df['overall score'], errors='coerce').fillna(0)
    df['new score'] = original + 1000 * df['university'].str.contains('Berkeley', case=False, na=False).astype(int)
    berkeley = df[df['university'].str.contains('Berkeley', case=False, na=False)]
    return float(berkeley['new score'].iloc[0])
    # For your answer, return the score for Berkeley in the new column.

def q20b(dfs):
    return dfs[2].sort_values('new score', ascending=False)['university'].head(10).tolist()
    # For your answer, return the top 10 university names as a list.

"""
21. Exploring data manipulation and falsification, continued

This time, let's manipulate the data by changing the source files
instead.
Create a copy of data/2021.csv and name it
data/2021_falsified.csv.
Modify the data in such a way that UC Berkeley comes out on top.

For this part, you will also need to load in the new data
as part of the function.
The function does not take an input; you should get it from the file.

Return the top 10 university names as a list from the falsified data.
"""

def q21():
    # Make a separate edited copy of the source data; keep the original.
    from pathlib import Path
    source = Path('data/2021.csv')
    edited = Path('data/2021_falsified.csv')
    if not edited.exists():
        df = pd.read_csv(source, encoding='latin-1')
        university_col = next(c for c in df.columns if c.lower() == 'university')
        rank_col = next(c for c in df.columns if c.lower() == 'rank')
        score_col = next(c for c in df.columns if c.lower() == 'overall score')
        mask = df[university_col].str.contains('Berkeley', case=False, na=False)
        if not mask.any():
            raise ValueError('UC Berkeley not found in the 2021 data')
        df.loc[mask, rank_col] = 0
        df.loc[mask, score_col] = 100
        df.to_csv(edited, index=False, encoding='latin-1')
    df = pd.read_csv(edited, encoding='latin-1')
    df.columns = df.columns.str.lower()
    df['rank'] = pd.to_numeric(df['rank'], errors='coerce')
    return df.sort_values('rank')['university'].head(10).tolist()

"""
22. Exploring data manipulation and falsification, continued

Which of the methods above do you think would be the most effective
if you were a "bad actor" trying to manipulate the rankings?

Which do you think would be the most difficult to detect?

=== ANSWER Q22 BELOW ===
Changing the source CSV might be harder to notice if somebody only checks the final rankings. Changing the formula is easier to inspect when the code is available. Both are misleading because the results are no longer fair.
=== END OF Q22 ANSWER ===
"""

"""
===== Wrapping things up =====

To wrap things up, we have collected
everything together in a pipeline for you
below.

**Don't modify this part.**
It will put everything together,
run your pipeline and save all of your answers.

This is run in the main function
and will be used in the first part of Part 2.
"""

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

def PART_1_PIPELINE():
    open(ANSWER_FILE, 'w').close()

    try:
        dfs = load_input()
    except NotImplementedError:
        print("Welcome to Part 1! Implement load_input() to get started.")
        dfs = []

    # Questions 1-6
    log_answer("q1", q1, dfs)
    log_answer("q2", q2, dfs)
    log_answer("q3a", q3, dfs)
    # 3b: commentary
    log_answer("q4", q4, dfs)
    # 4b: commentary
    log_answer("q5a", q5a, dfs)
    log_answer("q5b", q5b, dfs)
    log_answer("q5c", q5c)
    # 6a: commentary
    # 6b: commentary
    log_answer("q6c", q6c)

    # Questions 7-10
    log_answer("q7", q7, dfs)
    log_answer("q8a", q8a, dfs)
    # 8b: commentary
    log_answer("q9", q9, dfs)
    # 10: avg_2021
    avg_2021 = q10_helper(dfs)
    log_answer("q10", q10, avg_2021)

    # Questions 11-15
    log_answer("q11", q11, avg_2021)
    log_answer("q12", q12a, avg_2021)
    # 12b: commentary
    log_answer("q13", q13a, avg_2021)
    # 13b: commentary
    log_answer("q14a", q14a, avg_2021)
    # 14b: commentary

    # Questions 15-17
    top_10 = q15_helper(dfs)
    log_answer("q15", q15, top_10)
    log_answer("q16", q16, top_10)
    log_answer("q17", q17a, top_10)
    # 17b: commentary

    # Questions 18-20
    log_answer("q18", q18, dfs)
    # 19: commentary

    # Questions 20-22
    log_answer("q20a", q20a, dfs)
    log_answer("q20b", q20b, dfs)
    log_answer("q21", q21)
    # 22: commentary

    # Answer: return the number of questions that are not implemented
    if UNFINISHED > 0:
        print("Warning: there are unfinished questions.")

    return UNFINISHED

"""
That's it for Part 1!

=== END OF PART 1 ===

Main function
"""

if __name__ == '__main__':
    log_answer("PART 1", PART_1_PIPELINE)
