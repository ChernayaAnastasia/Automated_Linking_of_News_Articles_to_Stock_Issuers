# Automated Linking of Telegram News to Stock Issuers Using NLP Techniques

This project focuses on automatically linking news from Telegram channels to stock issuers using Natural Language Processing (NLP) techniques.

# Data
Data were collected using Telegram API and Moscow Exchange API from 26 most popular Telegram channels aimed at
investors, specifically those with the highest number of subscribers. 

Then data were annotated (linked to stock issures (or company's tickers)) using rule-based approach: with Regular Expression and list of company's names ('synonyms' or aliases).

Below is the extract from dataset with linked news:

![](https://github.com/ChernayaAnastasia/Screenshots/blob/master/raw_stock_news.png)

The table of aliases:

![](https://github.com/ChernayaAnastasia/Screenshots/blob/master/aliases.png)

For 189 companies there are 728 entries in the table. Some aliases were markes as *strong* meaning that a link between the news and the
company based on such an alias is considered reliable (most strong entries were the companies’ tickers). From more than 500,000 news articles, approximately 202,000 associations were identified. The resulting annotation created using rules was manually refined through text data analysis in pandas. EDA reveals the limitations of the rule-based approach. Some of them are below:

* false positives of regular expressions in links, e.g. MOEX ticker in every news with the link to MOEX site
  
* false posities in cases where a company was mentioned only as a source of information and had no further connection to the news, e.g:
  
the news *Лоукостер S7 в ближайшие годы не сможет потеснить Победу - ВТБ Капитал* gets the ticker of ВТБ банк

* homonymous company names
  
the news *Россия ударила по инфраструктуре крупнейшего хранилища газа на Украине. Там может храниться топливо для Европы - Лента* gets the ticker of Лента, retail company. 

* the alias table covers only aliases in their base form
  
* various spelling \ alternative naming of companies not covered
  
*Неожиданные слухи бродят по рынку насчет Белуги и Абрау. \nМногие уже написали в личку, просят прокомментировать что происходит. \n\nПока не очень понятно. Слухи комментировать не хочу. Что в реальности? Скоро узнаем.\n\n@bitkogan*

*Нижняя планка Яша* (about Яндекс)

* regular expressions cannot capture semantic relationships
  
*Банки в феврале увеличили выдачу ипотеки в 1,5 раза, в 2023г, объем продаж может превысить 5 трлн руб. - ВТБ* (construction companies such as LSR Group, Samolet, and PIK are related to this news because they are key players in the real estate market)

For now the news for top 2 channels (messages_grigorievspy', 'messages_newssmartlab') were checked and aggregated for baseline model. The distribution of 189 tickers is highly imbalanced. So the data were filtered focusing on the classes that have more than 1.5% representation. The entires with one word were also deleted because these are images with headlines. 

Below is the description of the final dataset used for training the baseline model


