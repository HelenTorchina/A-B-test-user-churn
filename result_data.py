import pandas as pd
import numpy as np


# Generate A/B test results and save them to a CSV file
def create_result(n_per_group, base_churn, expected_reduction):
    # Generate data for Group A (control)
    group_A_churn = np.random.binomial(1, base_churn, n_per_group)

    # Generate data for Group B (test)
    group_B_churn = np.random.binomial(1, base_churn - expected_reduction, n_per_group)

    # Use a binomial distribution because there are two possible outcomes:
    # a player either churns or remains in the game

    # Combine both groups into a single DataFrame
    df = pd.DataFrame({
        'group': ['A'] * n_per_group + ['B'] * n_per_group,
        'churned': np.concatenate([group_A_churn, group_B_churn])
    })

    # Display a summary of churn rates by group
    summary = df.groupby('group')['churned'].mean()
    print("Churn rate by group:")
    print(summary)

    # Save the generated data to a CSV file in the current working directory
    output_path = "ab_test_churn_data.csv"
    df.to_csv(output_path, index=False)

    print(f"\nA/B test results saved to: {output_path}")
