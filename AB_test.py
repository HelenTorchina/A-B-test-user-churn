import pandas as pd
from statsmodels.stats.proportion import proportions_ztest, proportion_confint


def AB_test(df_result):

    # Display the first rows and basic statistics
    print(df_result.head())
    print(df_result['group'].value_counts())
    print(df_result['churned'].value_counts())

    # Create a contingency table showing churned and retained players in each group
    contingency_table = pd.crosstab(df_result['group'], df_result['churned'])
    print("\nContingency table:")
    print(contingency_table)

    # Number of churned players in each group
    churn_counts = contingency_table[1].values
    # Total number of players in each group
    nobs = contingency_table.sum(axis=1).values

    print(f"Churned players: {churn_counts}")
    print(f"Total players: {nobs}")

    # Perform a two-proportion Z-test
    z_stat, p_val = proportions_ztest(count=churn_counts, nobs=nobs, alternative='larger')
    # 'larger' is used because we test whether the churn rate in the control group
    # is higher than in the test group (i.e. whether the test reduces churn)
    
    print(f"\nZ-statistic: {z_stat:.3f}")
    print(f"P-value: {p_val:.5f}")

    # Calculate confidence intervals for churn rates
    confint_control = proportion_confint(count=churn_counts[0], nobs=nobs[0], alpha=0.05)
    confint_test = proportion_confint(count=churn_counts[1], nobs=nobs[1], alpha=0.05)

    rate_control = churn_counts[0] / nobs[0]
    rate_test = churn_counts[1] / nobs[1]

    print(f'\n Churn rate (control): {rate_control:.4%}, 95% CI: [{confint_control[0]:.4%}, {confint_control[1]:.4%}]')
    print(f' Churn rate (test):    {rate_test:.4%}, 95% CI: [{confint_test[0]:.4%}, {confint_test[1]:.4%}]')

    # Calculate the absolute effect (difference in churn rates)
    diff = rate_control - rate_test
    print(f'\n Absolute churn reduction: {diff:.4%}')

    # Print the final conclusion
    alpha = 0.05
    if p_val < alpha:
        print('\n RESULT: A statistically significant reduction in churn was found. The null hypothesis is rejected.')
    else:
        print('\n RESULT: No statistically significant reduction in churn was found. The null hypothesis cannot be rejected.')

