# Automated Linking of Telegram News to Stock Issuers Using NLP Techniques

This project focuses on automatically linking news from Telegram channels to stock issuers using Natural Language Processing (NLP) techniques.

# Data
Data were collected using Telegram API and Moscow Exchange API from 26 most popular Telegram channels aimed at
investors, specifically those with the highest number of subscribers. 

Then data were annotated (linked to stock issures (or company's tickers)) using rule-based approach: with Regular Expression and list of company's names ('synonyms' or aliases).

Below is the extract from dataset with linked news:

![](https://github.com/ChernayaAnastasia/Screenshots/blob/master/raw_stock_news.png)

The table of aliases:

| Index | secid | search_string | is_strong |
|-------|-------|---------------|-----------|
| 149   | GAZP  | ГАЗПРОМ       | 0         |
| 150   | GAZP  | Gazprom       | 0         |
| 151   | GAZP  | GAZP          | 1         |


For 189 companies there are 728 entries in the table. Some aliases were marked as *strong* meaning that a link between the news and the
company based on such an alias is considered reliable (most strong entries were the companies’ tickers). From more than 500,000 news messages, 284,041 associations were identified. The resulting annotation created using rules was refined through exploratory data analysis in Pandas. Data analysis reveals the limitations of the rule-based approach. Some of them are below:

* false positives of regular expressions in links, e.g. MOEX ticker in every news with the link to Moscow Exchange site
  
* false posities in cases where a company was mentioned only as a source of information and had no further connection to the news, e.g:
  
the news *МНЕНИЕ: Лукойл хорошо заработал на дорогой нефти. Цель 5000 руб - Тинькофф* gets the ticker of Tinkoff bank

* homonymous company names
  
the news *Россия ударила по инфраструктуре крупнейшего хранилища газа на Украине. Там может храниться топливо для Европы - Лента* gets the ticker of Лента, retail company. 

* the alias table covers only aliases in their base form
  
* various spelling \ alternative naming of companies not covered
  
*Неожиданные слухи бродят по рынку насчет Белуги и Абрау. \nМногие уже написали в личку, просят прокомментировать что происходит. \n\nПока не очень понятно. Слухи комментировать не хочу. Что в реальности? Скоро узнаем.\n\n@bitkogan*

*Нижняя планка Яша* (about Яндекс)

* regular expressions cannot capture semantic relationships - only concrete names / keywords
  
*Банки в феврале увеличили выдачу ипотеки в 1,5 раза, в 2023г, объем продаж может превысить 5 трлн руб. - ВТБ* (construction companies such as LSR Group, Samolet, and PIK are related to this news because they are key players in the real estate market)

For now the news for top 2 channels (messages_grigorievspy', 'messages_newssmartlab') were checked and aggregated for baseline model. The distribution of 189 tickers is highly imbalanced. So the data were filtered focusing on the classes that have more than 1.5% representation. The entires with one word were also deleted because these are mostly images with short headlines with tickers. 

Below is the description of the final dataset used for training the baseline model:

| Description                   | Values            |
|-------------------------------|-------------------|
| Number of news                | 39638            |
| Number of tickers             | 24               |
| Number of telegram channels   | 2                |
| The earliest datetime value   | 2021-03-29 15:31:02 |
| The latest datetime value     | 2024-06-12 10:23:30 |


![](https://github.com/ChernayaAnastasia/Screenshots/blob/master/baseline_distribution.png)

| Split        | Number of Docs in Corpus | Number of Tokens | Size of Vocabulary |
|--------------|--------------------------|------------------|--------------------|
| Train        | 25368                    | 588295           | 21169             |
| Validation   | 6342                     | 147493           | 9582              |
| Test         | 7928                     | 180730           | 10087             |


Each row represents one message with news and it can be linked to more than one ticker. 

# Model

For now it is one simple model Logistic Regression with a TF-IDF vectorizer. 
We wrap LogisticRegression in MultiOutputClassifier when performing multi-label classification, where each instance can belong to multiple classes independently.

The model is fine-tuned through 10-fold cross-validation with GridSearchCV.

Params:

• C: 10

• Penalty: l2

• Solver: saga

The data was preprocessed. The preprocession included the following steps:

1. Delete irrelevant information: This involves removing tags (preventing
information leakage) and html links, stopwords (function words and
words common and specific to telegram channels) and punctuation marks
(while keeping hyphens inside words).
3. Remove multiple spaces. 
4. Substitute ’ё’ for ’е’.
5. Substitute all numbers with ’1’

**The metric is F1-macro score.**

# Results

| Label | Precision | Recall | F1-Score | Support |
|-------|-----------|--------|----------|---------|
| AFKS  | 1.00      | 0.96   | 0.98     | 465     |
| AFLT  | 1.00      | 0.93   | 0.96     | 348     |
| ASTR  | 1.00      | 0.94   | 0.97     | 259     |
| CHMF  | 1.00      | 0.84   | 0.92     | 245     |
| FESH  | 1.00      | 0.98   | 0.99     | 705     |
| GAZP  | 0.96      | 0.90   | 0.93     | 657     |
| LKOХ  | 0.98      | 0.74   | 0.84     | 258     |
| LSRG  | 1.00      | 0.93   | 0.96     | 522     |
| MAGN  | 1.00      | 0.88   | 0.93     | 235     |
| MOEX  | 0.98      | 0.88   | 0.93     | 272     |
| MVID  | 1.00      | 0.94   | 0.97     | 250     |
| NVTK  | 0.92      | 0.78   | 0.84     | 285     |
| PIKK  | 1.00      | 0.82   | 0.90     | 252     |
| PLZL  | 1.00      | 0.85   | 0.92     | 221     |
| POSI  | 0.99      | 0.96   | 0.97     | 236     |
| RNFT  | 1.00      | 0.98   | 0.99     | 655     |
| ROSN  | 0.95      | 0.81   | 0.87     | 367     |
| RTKM  | 1.00      | 0.96   | 0.98     | 255     |
| RUAL  | 1.00      | 0.89   | 0.94     | 275     |
| SBER  | 0.97      | 0.80   | 0.88     | 304     |
| SFIN  | 1.00      | 0.95   | 0.97     | 312     |
| SNGS  | 1.00      | 0.94   | 0.97     | 233     |
| VTBR  | 0.97      | 0.85   | 0.91     | 306     |
| YNDX  | 0.99      | 0.87   | 0.93     | 291     |

| Average        | Precision | Recall | F1-Score | Support |
|----------------|-----------|--------|----------|---------|
| Micro Avg      | 0.99      | 0.90   | 0.94     | 8206    |
| Macro Avg      | 0.99      | 0.89   | 0.93     | 8206    |
| Weighted Avg   | 0.99      | 0.90   | 0.94     | 8206    |
| Samples Avg    | 0.92      | 0.92   | 0.92     | 8206    |

| Model              | Vectorizer | F1 Macro Score | Predicting Time |
|--------------------|------------|----------------|-----------------|
| LogisticRegression | Tf-idf     | 0.934          | 0.54122 s       |


#### Predicting Stock Tickers from News Text Using a Pre-trained Model:

![](https://github.com/ChernayaAnastasia/Screenshots/blob/master/example_baseline.png)

# Author

**Chernaya Anastasia** - [Telegram](https://t.me/ChernayaAnastasia), [GitHub](https://github.com/ChernayaAnastasia)

# Links
[Report](https://drive.google.com/file/d/1-ImMnK1dKLTdvboOSXVte_eFUAKXgFYw/view?usp=sharing)

