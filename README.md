# A/B Test: User Churn Analysis

## Project Overview

The `input_data.csv` file contains data on player progression in a match-3 mobile game featuring a "SawStep" mechanic.

Each SawStep represents a level that a player must complete to progress further in the game. The step number indicates the order in which the level appears in the player's progression.

The dataset contains the following metrics:

- `SawStep` — step number in the player's progression.
- `cry_per_user` — average amount of hard currency spent by a player at a given step.
- `churn` — percentage of players who leave the game at a given step.
- `LRC` — Level Relative Complexity, measured as the percentage of failed attempts out of all attempts started at that step.

## Project Goals

1. Analyze the balance between hard currency spending and player churn across different steps.
2. Propose A/B tests based on independent hypotheses to improve the balance of the game economy and reduce churn.

## Project Workflow

### 1. Initial Data Analysis (`main_analysis.py`)

Analyze the initial dataset to evaluate the relationship between hard currency spending, level complexity, and player churn.

The analysis includes:
- Data type validation and duplicate checks.
- Outlier detection using boxplots and the IQR method.
- Identification of steps with unusually high churn.
- Analysis of the relationship between currency spending, level complexity, and churn.
- Recommendations for potential A/B tests.

### 2. A/B Test Simulation (`result_data.py`)

Generate simulated A/B test data to evaluate a proposed game change.

The first test considers reducing level difficulty or introducing a booster on problematic steps.

**Hypotheses:**

- **Null hypothesis (H₀):** The proposed change does not affect player churn.
- **Alternative hypothesis (H₁):** The proposed change leads to a statistically significant reduction in player churn on problematic steps.

The simulation uses a binomial distribution to generate player outcomes for the control and test groups.

### 3. A/B Test Evaluation (`AB_test.py`)

Analyze the generated test data and evaluate whether the proposed change has a statistically significant effect on player churn.

The analysis includes:
- A contingency table showing churned and retained players in each group.
- A two-proportion Z-test.
- 95% confidence intervals for churn rates in both groups.
- Calculation of the absolute difference in churn rates.
- A conclusion based on the selected significance level.

## Further Research Opportunities

Additional A/B tests could focus on steps where player churn is relatively high while hard currency spending remains low.

Potential experiments include:
- Increasing level difficulty.
- Increasing the cost of attempts.
- Adjusting the balance between level difficulty and attempt cost.

The goal would be to evaluate how these changes affect player churn and hard currency revenue.

## Important Note

The A/B test results in this project are simulated using generated data. They illustrate the testing methodology and statistical evaluation process and do not represent the results of a real experiment.
