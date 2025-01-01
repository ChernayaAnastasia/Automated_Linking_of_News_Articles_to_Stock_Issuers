import nltk
from nltk.corpus import stopwords
nltk.download("stopwords")

mystopwords = stopwords.words('russian')
sorted(mystopwords)[:5]

mystopwords.extend(
    [
        'это',
        'так',
        'из',
        'из-за',
        'на',
        'ок',
        'кстати',
        'который',
        'мочь',
        'весь',
        'еще',
        'также',
        'самый',
        'среди',
        'кроме',
        'ранее',
        'пока',
        'свой',
        'наш',
        'например',
        'поэтому',
        'очень',
        'однако',
        'затем',
        'именно',
        'поскольку'
    ]
)