import pandas as pd
from IPython.display import display
import seaborn as sns
from matplotlib import pyplot as plt
from statsmodels.stats.proportion import proportions_ztest, proportion_confint


def main():
    df = pd.read_csv('input_data.csv', sep=';')
    # df = df['SawStep;cry_per_user;LRC;churn'].str.split(';', expand=True)
    # df.rename(columns={0: "SawStep", 1: "cry_per_user", 2: "LRC", 3: "churn"}, inplace=True)
    df.info()
    display(df)
    df['SawStep'] = df['SawStep'].astype('int64')
    df['cry_per_user'] = df['cry_per_user'].astype('float')
    df['LRC'] = df['LRC'].astype('float')
    df['churn'] = df['churn'].astype('float')
    df.info()
    print(df.describe())
    # print(df.duplicated().sum())
    # sns.boxplot(x=df['SawStep'])
    # plt.show()
    # sns.boxplot(x=df['cry_per_user'])
    # plt.show()
    # sns.boxplot(x=df['LRC'])
    # plt.show()
    # Q1 = df['LRC'].quantile(0.25)
    # Q3 = df['LRC'].quantile(0.75)
    # IQR = Q3 - Q1
    # lower_bound = Q1 - 1.5 * IQR
    # outliers = df[(df['LRC'] < lower_bound)]
    # display(outliers)
    # #низкий уровень сложности, небольшое количество полученной игровой валюты и небольшой отток - всё логично
    # sns.boxplot(x=df['churn'])
    # plt.show()
    Q1 = df['churn'].quantile(0.25)
    Q3 = df['churn'].quantile(0.75)
    IQR = Q3 - Q1
    upper_bound = Q3 + 1.5 * IQR
    outliers_churn = df[(df['churn'] > upper_bound)]
    display(outliers_churn)
    print(outliers_churn.describe())
    # подозрительными выглядят пара выбросов: 1209 и 1071, думаю, можно забить


    # Посмотрим графики, как изменяется каждый показатель в зависимости от шага
    plt.figure(figsize=(12, 6))
    sns.lineplot(x='SawStep', y='cry_per_user', data=df, label='Cry per user')
    sns.lineplot(x='SawStep', y='LRC', data=df, label='LRC')
    sns.lineplot(x='SawStep', y='churn', data=df, label='Churn')
    plt.title('Динамика валюты, поражений и оттока по шагам')
    plt.show()

    # 1. Где резко растёт отток? Где выбросы в churn, т.е. outliers - вопрос, почему? Строки 1071 (шаг 2324) и 1209 (шаг 2604) вообще интересные, можно сделать А/В тест




    # 2. Где большие траты, но маленькая сложность? Может быть, стоит поднять сложность
    df['cry_per_user_LRC_relation'] = df['cry_per_user']/df['LRC']
    sns.boxplot(x=df['cry_per_user_LRC_relation'])
    plt.show()
    Q1 = df['cry_per_user_LRC_relation'].quantile(0.25)
    Q3 = df['cry_per_user_LRC_relation'].quantile(0.75)
    IQR = Q3 - Q1
    upper_bound = Q3 + 1.5 * IQR
    outliers_cry_per_user_LRC_relation = df[(df['cry_per_user_LRC_relation'] > upper_bound)]
    display(outliers_cry_per_user_LRC_relation)
    # Есть выбросы сверху, но отток здесь в пределах разумного, т.е. высокая стоимость соответствует высокой сложности и это устраивает пользователей


    # 3. Есть ли шаги, где игроки уходят, но не платят? Возможно, слишком сложно — можно снизить сложность или снизить стоимость попытки.
    df['churn_cry_per_user_relation'] = df['churn'] / df['cry_per_user']
    sns.boxplot(x=df['churn_cry_per_user_relation'])
    plt.show()
    Q1 = df['churn_cry_per_user_relation'].quantile(0.25)
    Q3 = df['churn_cry_per_user_relation'].quantile(0.75)
    IQR = Q3 - Q1
    upper_bound = Q3 + 1.5 * IQR
    outliers_churn_cry_per_user_relation = df[(df['churn_cry_per_user_relation'] > upper_bound)]
    display(outliers_churn_cry_per_user_relation.sort_values(by='LRC', ascending=False))
    # Получили 76 шагов, уберём те, где отток 0,015 и более, т.к. мы уже взяли эту группу в работу, и проанализируем оставшиеся
    # Также нас не интересуют шаги с небольшим оттоком - 0,006 (это среднее значение по колонке) и менее
    outliers_churn_cry_per_user_relation_filtered = outliers_churn_cry_per_user_relation[
        (outliers_churn_cry_per_user_relation['churn'] < 0.015) & (outliers_churn_cry_per_user_relation['churn'] >= 0.006)]
    display(outliers_churn_cry_per_user_relation_filtered.sort_values(by='LRC', ascending=False))
    outliers_churn_cry_per_user_relation_filtered.sort_values(by='LRC', ascending=False).to_csv('output.csv', index=False)
    # Нашли 55 таких шагов и можем предложить повысить цену либо понизить уровень


    # 4. Отношение стоимости к количеству ушедших - что оно показывает? Есть ли выбросы и хороши ли они (высокий показатель - отлично, много платят, мало уходят
    # низкий показатель - плохо, ведь мало платят и много уходят
    df['cry_per_churn'] = df['cry_per_user'] / df['churn']
    sns.boxplot(x=df['cry_per_churn'])
    plt.show()
    # Уже видим, что выбросы только в большую сторону, значит, здесь нет проблемы, гипотезы строить не будем
    Q1 = df['cry_per_churn'].quantile(0.25)
    Q3 = df['cry_per_churn'].quantile(0.75)
    IQR = Q3 - Q1
    upper_bound = Q3 + 1.5 * IQR
    outliers_cry_per_churn = df[(df['cry_per_churn'] > upper_bound)]
    outliers_cry_per_churn.sort_values('churn', ascending=False).to_csv('output.csv', index=False)
    # Проверили размер оттоков здесь и убедились, что эти шаги нам не интересны (отток меньше 0,006)

    #ab_test.create_result()

    #Загружаем результат теста для дальнейшего анализа и интерпретации результата
    df_result = pd.read_csv('ab_test_churn_data.csv')
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


if __name__ == '__main__':
    main()