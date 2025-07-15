import pandas as pd
import numpy as np


# Генерация результатов А/В теста с сохранением в файл .csv
def create_result():
    # Сгенерируем данные для группы A (контроль)
    group_A_churn = np.random.binomial(1, base_churn, n_per_group)

    # Сгенерируем данные для группы B (тест)
    group_B_churn = np.random.binomial(1, base_churn - expected_reduction, n_per_group)

    # Используем биномиальное распределение, т.к. у нас два исхода: игрок остался либо ушёл

    #   Соберем в один DataFrame
    df = pd.DataFrame({
        'group': ['A'] * n_per_group + ['B'] * n_per_group,
        'churned': np.concatenate([group_A_churn, group_B_churn])
    })

    # Посмотрим на сводку
    summary = df.groupby('group')['churned'].mean()
    print(summary)

    # Сохраним файл
    output_path = "D:/AB test/ab_test_churn_data.csv"
    df.to_csv(output_path, index=False)
