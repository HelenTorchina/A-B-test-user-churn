import pandas as pd
from statsmodels.stats.power import NormalIndPower
from statsmodels.stats.proportion import proportions_ztest, proportion_confint, proportion_effectsize


def AB_test(df_result):

    # Смотрим первые строки и статистику
    print(df_result.head())
    print(df_result['group'].value_counts())
    print(df_result['churned'].value_counts())

    # Таблица сопряжённости: сколько ушло / осталось в каждой группе
    contingency_table = pd.crosstab(df_result['group'], df_result['churned'])
    print("\nТаблица сопряжённости:")
    print(contingency_table)

    # Количество ушедших по группам
    churn_counts = contingency_table[1].values
    # Всего пользователей по группам
    nobs = contingency_table.sum(axis=1).values

    print(f"Ушло: {churn_counts}")
    print(f"Всего: {nobs}")

    # Z-тест
    z_stat, p_val = proportions_ztest(count=churn_counts, nobs=nobs, alternative='larger')
    # 'larger' — потому что мы проверяем, что конверсия в control больше, чем в test (ожидаем уменьшение)

    print(f"\nZ-статистика: {z_stat:.3f}")
    print(f"P-value: {p_val:.5f}")

    # Доверительные интервалы для долей
    confint_control = proportion_confint(count=churn_counts[0], nobs=nobs[0], alpha=0.05)
    confint_test = proportion_confint(count=churn_counts[1], nobs=nobs[1], alpha=0.05)

    rate_control = churn_counts[0] / nobs[0]
    rate_test = churn_counts[1] / nobs[1]

    print(f'\n Отток (control): {rate_control:.4%}, 95% CI: [{confint_control[0]:.4%}, {confint_control[1]:.4%}]')
    print(f' Отток (test):    {rate_test:.4%}, 95% CI: [{confint_test[0]:.4%}, {confint_test[1]:.4%}]')

    # Абсолютный эффект (разница)
    diff = rate_control - rate_test
    print(f'\n Абсолютное снижение оттока: {diff:.4%}')

    # Финальный краткий вывод
    alpha = 0.05
    if p_val < alpha:
        print('\n РЕЗУЛЬТАТ: есть статистически значимое снижение оттока! Нулевая гипотеза отклоняется.')
    else:
        print('\n РЕЗУЛЬТАТ: статистически значимого снижения оттока не найдено. Нулевая гипотеза не отклоняется.')

