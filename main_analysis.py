import pandas as pd
from IPython.display import display
import seaborn as sns
from matplotlib import pyplot as plt
import result_data
import AB_test

def analysis(df):
    df.info()
    display(df)
    
    # Convert data types
    df['SawStep'] = df['SawStep'].astype('int64')
    df['cry_per_user'] = df['cry_per_user'].astype('float')
    df['LRC'] = df['LRC'].astype('float')
    df['churn'] = df['churn'].astype('float')
    df.info()
    print(df.describe())
    
    # Check for duplicate records
    print(df.duplicated().sum())
    # No duplicates found

    # Detect outliers to identify potential imbalances between hard currency spending and player churn
    sns.boxplot(x=df['SawStep'])
    plt.show()
    # No outliers found
    sns.boxplot(x=df['cry_per_user'])
    plt.show()
    # No outliers found
    sns.boxplot(x=df['LRC'])
    plt.show()
    # Outliers indicate unusually low level complexity
    Q1 = df['LRC'].quantile(0.25)
    Q3 = df['LRC'].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    outliers = df[(df['LRC'] < lower_bound)]
    display(outliers)
    # Low level complexity, low hard currency spending, and low churn are consistent with each other and do not pose a risk to the game economy
    sns.boxplot(x=df['churn'])
    plt.show()
    # High churn outliers detected. Inspect these steps, including exporting them to a separate file,
    # and identify potential ways to reduce churn
    Q1 = df['churn'].quantile(0.25)
    Q3 = df['churn'].quantile(0.75)
    IQR = Q3 - Q1
    upper_bound = Q3 + 1.5 * IQR
    outliers_churn = df[(df['churn'] > upper_bound)]
    display(outliers_churn)
    # Compare average churn and level complexity on these steps with the overall dataset averages (0.006 and 0.6162, respectively)
    print(outliers_churn.describe())
    # Average churn on these steps is 0.018, with an average level complexity of 0.7529
    # 1. Proposed A/B test: evaluate whether reducing level complexity by approximately 0.03
    # or introducing an optional booster can reduce churn on these steps

    # 2. Identify steps with high spending but low level complexity.
    # Consider increasing difficulty to improve the balance between spending and difficulty
    df['cry_per_user_LRC_relation'] = df['cry_per_user']/df['LRC']
    sns.boxplot(x=df['cry_per_user_LRC_relation'])
    plt.show()
    Q1 = df['cry_per_user_LRC_relation'].quantile(0.25)
    Q3 = df['cry_per_user_LRC_relation'].quantile(0.75)
    IQR = Q3 - Q1
    upper_bound = Q3 + 1.5 * IQR
    outliers_cry_per_user_LRC_relation = df[(df['cry_per_user_LRC_relation'] > upper_bound)]
    display(outliers_cry_per_user_LRC_relation)
    # Some upper outliers are present, but churn remains within an acceptable range.
    # Higher costs are associated with higher level complexity, which appears acceptable to players.
    # No further investigation is required

    # 3. Identify steps where players churn despite spending relatively little.
    # These steps may be too difficult; consider reducing difficulty or lowering the cost per attempt
    df['churn_cry_per_user_relation'] = df['churn'] / df['cry_per_user']
    sns.boxplot(x=df['churn_cry_per_user_relation'])
    plt.show()
    Q1 = df['churn_cry_per_user_relation'].quantile(0.25)
    Q3 = df['churn_cry_per_user_relation'].quantile(0.75)
    IQR = Q3 - Q1
    upper_bound = Q3 + 1.5 * IQR
    outliers_churn_cry_per_user_relation = df[(df['churn_cry_per_user_relation'] > upper_bound)]
    display(outliers_churn_cry_per_user_relation.sort_values(by='LRC', ascending=False))
    # Identified 76 steps. Exclude those with churn of 0.015 or higher,
    # as they have already been selected for the first analysis.
    # Also exclude steps with churn of 0.006 or lower,
    # as this is the average churn rate across the entire dataset
    outliers_churn_cry_per_user_relation_filtered = outliers_churn_cry_per_user_relation[
        (outliers_churn_cry_per_user_relation['churn'] < 0.015) & (outliers_churn_cry_per_user_relation['churn'] >= 0.006)]
    display(outliers_churn_cry_per_user_relation_filtered.sort_values(by='LRC', ascending=False))
    outliers_churn_cry_per_user_relation_filtered.sort_values(by='LRC', ascending=False).to_csv('output.csv', index=False)
    # Identified 55 steps. Consider increasing the cost per attempt or adjusting level difficulty.
    # Another A/B test could be conducted to evaluate these changes

    # 4. Analyze the ratio of hard currency spending to churn.
    # A high ratio indicates higher spending relative to churn,
    # while a low ratio indicates lower spending relative to churn
    df['cry_per_churn'] = df['cry_per_user'] / df['churn']
    sns.boxplot(x=df['cry_per_churn'])
    plt.show()
   # Only upper outliers are observed, suggesting no apparent issue requiring further analysis
    Q1 = df['cry_per_churn'].quantile(0.25)
    Q3 = df['cry_per_churn'].quantile(0.75)
    IQR = Q3 - Q1
    upper_bound = Q3 + 1.5 * IQR
    outliers_cry_per_churn = df[(df['cry_per_churn'] > upper_bound)]
    outliers_cry_per_churn.sort_values('churn', ascending=False).to_csv('output.csv', index=False)
    # Check churn rates for these steps and confirm that they are not relevant
    # (churn is below the overall average of 0.006)

def main():
    df = pd.read_csv('input_data.csv', sep=';')

    # Run the analysis to identify potential A/B tests
    analysis(df)

    # Define test parameters and generate the results of the first experiment
    n_per_group = 87000  # Sample size was determined using an online calculator with a significance level of 0.05,
    # statistical power of 0.8, a minimum detectable effect of 0.1,
    # and a baseline churn rate of 0.018 (the average for the selected problem subset)
    base_churn = 0.018  # Baseline churn rate (1.8%)
    expected_reduction = 0.0018  # Expected absolute reduction in churn (0.18 percentage points)
    result_data.create_result(n_per_group, base_churn, expected_reduction)

    # Load the generated test results for further analysis and interpretation
    df_result = pd.read_csv('ab_test_churn_data.csv')
    
    # Run the statistical test and evaluate the results
    AB_test.AB_test(df_result)


if __name__ == '__main__':
    main()
