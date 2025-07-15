import pandas as pd
from IPython.display import display
import seaborn as sns
from matplotlib import pyplot as plt
import result_data
import AB_test

def analysis():
    df.info()
    display(df)
    
    # Приведение типов данных
    df['SawStep'] = df['SawStep'].astype('int64')
    df['cry_per_user'] = df['cry_per_user'].astype('float')
    df['LRC'] = df['LRC'].astype('float')
    df['churn'] = df['churn'].astype('float')
    df.info()
    print(df.describe())
    
    # Проверка на дубликаты
    print(df.duplicated().sum())
    #Дубликатов не обнаружено

    # Ищем выбросы - они подскажут, есть ли проблемы в балансе твёрдой валюты и оттока
    sns.boxplot(x=df['SawStep'])
    plt.show()
    # Выбросов нет
    sns.boxplot(x=df['cry_per_user'])
    plt.show()
    # Выбросов нет
    sns.boxplot(x=df['LRC'])
    plt.show()
    # Выбросы по уровню сложности - очень маленький уровень сложности
    Q1 = df['LRC'].quantile(0.25)
    Q3 = df['LRC'].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    outliers = df[(df['LRC'] < lower_bound)]
    display(outliers)
    # Низкий уровень сложности, небольшое количество полученной игровой валюты и небольшой отток - всё логично и не вредит системе
    sns.boxplot(x=df['churn'])
    plt.show()
    # Выбросы в большую сторону наблюдаются, на этих шагах высокий отток, выведем информацию о них (в том числе в отдельный файл) и подумаем, как можно сократить отток на этих шагах
    Q1 = df['churn'].quantile(0.25)
    Q3 = df['churn'].quantile(0.75)
    IQR = Q3 - Q1
    upper_bound = Q3 + 1.5 * IQR
    outliers_churn = df[(df['churn'] > upper_bound)]
    display(outliers_churn)
    # Посмотрим средний отток и уровень сложности на этих шагах, затем сравним со средним оттоком и уровнем сложности по выборке (0,006 и 0,6162)
    print(outliers_churn.describe())
    # На данных шагах отток 0,018 при уровне сложности 0,7529
    # 1. Здесь могу предложить проверку с помощью A/B теста, уменьшится ли на этих шагах отток при снижении уровня сложности, например, на 0,03 единицы

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
    # Есть выбросы сверху, но отток здесь в пределах разумного, т.е. высокая стоимость соответствует высокой сложности и это устраивает пользователей, нет необходимости проводить дополнительный анализ

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
    # Получили 76 шагов, уберём те, где отток 0,015 и более, т.к. мы уже взяли эту группу в работу на первом шаге, и проанализируем оставшиеся
    # Также нас не интересуют шаги с небольшим оттоком - 0,006 (это среднее значение оттока по всей выборке) и менее
    outliers_churn_cry_per_user_relation_filtered = outliers_churn_cry_per_user_relation[
        (outliers_churn_cry_per_user_relation['churn'] < 0.015) & (outliers_churn_cry_per_user_relation['churn'] >= 0.006)]
    display(outliers_churn_cry_per_user_relation_filtered.sort_values(by='LRC', ascending=False))
    outliers_churn_cry_per_user_relation_filtered.sort_values(by='LRC', ascending=False).to_csv('output.csv', index=False)
    # Нашли 55 таких шагов и можем предложить повысить цену либо понизить уровень - можем провести ещё один А/В тест


    # 4. Отношение стоимости к количеству ушедших - что оно показывает? Есть ли выбросы и хороши ли они (высокий показатель - отлично, много платят, мало уходят, низкий показатель - плохо, ведь мало платят и много уходят
    df['cry_per_churn'] = df['cry_per_user'] / df['churn']
    sns.boxplot(x=df['cry_per_churn'])
    plt.show()
    # Уже видим, что выбросы только в большую сторону, значит, здесь нет проблемы и нет смысла в дальнейшем анализе
    Q1 = df['cry_per_churn'].quantile(0.25)
    Q3 = df['cry_per_churn'].quantile(0.75)
    IQR = Q3 - Q1
    upper_bound = Q3 + 1.5 * IQR
    outliers_cry_per_churn = df[(df['cry_per_churn'] > upper_bound)]
    outliers_cry_per_churn.sort_values('churn', ascending=False).to_csv('output.csv', index=False)
    # Проверили размер оттоков здесь и убедились, что эти шаги нам не интересны (отток меньше 0,006)


def main():
    df = pd.read_csv('input_data.csv', sep=';')

    # Запускаем анализ для определения возможных A/B тестов
    processing(df)

    # Генерируем результаты первого теста
    result_data.create_result()

    # Загружаем результат теста для дальнейшего анализа и интерпретации результата
    df_result = pd.read_csv('ab_test_churn_data.csv')
    
    # Проводим тест и делаем выводы
    AB_test.AB_test(df_result)


if __name__ == '__main__':
    main()
