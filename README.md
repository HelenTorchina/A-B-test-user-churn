# A-B-test-user-churn

## 🇷🇺 Описание проекта

В файле Input_data.csv содержатся следующие данные о прохождении пользователями игры формата match-3:

SawStep - шаговые пилы с уровнем, который игрок должен выиграть, чтобы пройти дальше (номер шага указывает порядок отображения уровня у игрока), 
на каждом шаге пилы игроки проводят хард-валюту - cry_per_user, 
с каждого шага пилы уходят процент игроков - churn, 
каждый шаг имеет свою сложность для игрока - LRC (процент поражений от всех стартов на шаге).

### Цели проекта:
1. Проанализировать пилу с точки зрения баланса твердой валюты и оттока
2. Предложить A/B тест(-ы) с независимой гипотезой для улучшения баланса системы

### Этапы проекта:
1) В файле main_analysis.py происходит анализ исходного набора данных с точки зрения баланса валюты и оттока и предлагаются варианты A/B тестов

2) С помощью скрипта result_data.py генерируется результат теста - имитируем его проведение
Нулевая гипотеза: наше изменение (снижение уровня сложности или добавление бустера) не повлияет на отток пользователей
Альтернативная гипотеза: наше изменение вызовет значимое снижение оттока пользователей на проблемных уровнях

4) С помощью скрипта AB_test.py проводим анализ результата теста, основываясь на сгенерированных данных, и делаем краткий вывод

### Что ещё можно сделать?
Провести А/В тест для тех шагов, где игроки уходят и при этом мало платят, можно попробовать повысить уровень сложности или хотя бы стоимость и посмотреть, как изменится отток / какой выигрыш в стоимости можно получить

## 🇬🇧 Project Description
The Input_data.csv file contains data on user progression in a match-3 game involving a "SawStep" mechanic:

SawStep – levels with a gatekeeping mechanic that the player must beat to progress. Each step number represents the sequence of the player's level experience,
cry_per_user – amount of hard currency spent by a player on this level,
churn – percentage of users who abandon the game at this level,
LRC – level relative complexity, defined as the percentage of failures from all starts on that level

### Project Goals:
1. Analyze the balance between hard currency spending and user churn at different steps
2. Propose A/B test(s) with independent hypotheses to improve the system's balance

### Project Stages:
1) Main Analysis – main_analysis.py
Performs the core analysis of the initial dataset from the perspective of currency vs. churn balance, identifies problem steps, suggests hypotheses for A/B testing

2) Simulated A/B Test – result_data.py
Simulates the results of an A/B test
Null Hypothesis (H₀): The proposed change (e.g., lowering level difficulty or adding a booster) does not affect user churn
Alternative Hypothesis (H₁): The proposed change leads to a statistically significant reduction in churn on the problematic steps

3) Test Evaluation – AB_test.py
Analyzes the test results based on the generated data and provides a concise conclusion using statistical methods

### What else could be done?
You can conduct an A/B test for steps where players churn without paying much.
For these levels, try increasing difficulty or at least the cost per attempt, and observe whether churn increases or remains stable and what kind of gain in currency can be achieved from these changes
