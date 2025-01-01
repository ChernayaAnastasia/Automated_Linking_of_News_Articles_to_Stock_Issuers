import re
import nltk
import emoji
from string import punctuation
from pymorphy3 import MorphAnalyzer


RUBBISH_PATTERN = r'Читать.+|Подключить бота-шпиона:?'
PATTERN_TAG = r'#\S+|\$[A-Z]{4}' #для тэгов тикеров, которые могут вводится через $
LINKS_PATTERN  = r"https?://\S+"

# Removes specific patterns of text defined in RUBBISH_PATTERN, such as prompts for external actions.
def remove_rubbish(text):
    return re.sub(RUBBISH_PATTERN, '', text)

# Removes links matching the pattern defined in LINKS_PATTERN (e.g., "http://example.com").
def remove_links(text):
    return re.sub(LINKS_PATTERN, '', text)

# Replaces emojis in the text with a space using the emoji library.
def remove_emojis(text):
    return emoji.replace_emoji(text, " ")

# Removes tags like hashtags or ticker symbols defined in PATTERN_TAG.
def remove_tags(text):
    return re.sub(PATTERN_TAG, '', text)

# Replaces numeric tokens in the text with the digit '1'.
def replace_numbers(text):
    return re.sub(r'\d+', '1', text)

# Removes punctuation from the text while preserving hyphens inside words.
def remove_punctuation(text):
    text = text.translate(str.maketrans('', '', punctuation.replace('-', '') + '”„“«»†*\—/\\‘’'))
    text = re.sub(r'-(?=\s)', '', text)  # Remove standalone hyphens.
    return text

# Applies a sequence of cleaning operations to preprocess the text.
def clean_text(text):
    if not isinstance(text, str):
        return text
    else:
        text = re.sub(r'ё', 'е', text)  # Normalize Cyrillic "ё" to "е".
        text = remove_emojis(text)
        text = re.sub(r'\*+', '', text)  # Remove excess asterisks.
        text = remove_rubbish(text)
        text = remove_links(text)
        text = remove_tags(text)
        text = replace_numbers(text)
        text = re.sub(r'\n|\xa0', ' ', text)  # Replace newlines and non-breaking spaces.
        text = re.sub(r'\s{2,}', ' ', text)  # Remove extra spaces.
        text = remove_punctuation(text)
        text = text.strip()
        text = re.sub(r'^[+\-*/=<>!?\s]+$', '', text)  # Remove special characters-only lines.
        return text

# Tokenizes text into words based on a regex pattern, removing standalone numeric tokens.
def tokenize(text, regex=re.compile("[а-яa-zё\d-]+", re.IGNORECASE)):
    try:
        tokens = regex.findall(text)
        tokens = [(re.sub(r'^\d+$', '', token)) for token in tokens]  # Remove numeric tokens.
        tokens = [token for token in tokens if token.strip()]  # Remove empty tokens.
        return tokens
    except:
        return []

# Lemmatizes a list of tokens using pymorphy3 to find their normal forms.
def pymorphy_lemmatizer(tokens, pymorphy=MorphAnalyzer()):
    return [pymorphy.parse(token)[0].normal_form for token in tokens]

# Removes stopwords from a list of lemmas.
def remove_stopwords(lemmas, stopwords):
    return [w for w in lemmas if not w in stopwords]

# Combines tokenization, lemmatization, and optional stopword removal into a single function.
def lemmatize(text, delete_stopwords=True, stopwords=None):
    tokens = tokenize(text)
    lemmas = pymorphy_lemmatizer(tokens)
    lemmas = [re.sub('ё', 'е', lemma) for lemma in lemmas]  # Normalize "ё" to "е".

    if delete_stopwords and stopwords is not None:
        lemmas = remove_stopwords(lemmas, stopwords=stopwords)

    return ' '.join(lemmas)

# Applies preprocessing and optional lemmatization or tokenization to a DataFrame column 'text'.
def preprocess_text(df, stopwords=None, delete_stopwords=True, make_lemmatization=True):
    df['text_cleaned'] = df.text.progress_apply(clean_text)  # Clean text.
    if make_lemmatization:
        df['lemmas'] = df['text_cleaned'].progress_apply(
            lambda x: lemmatize(x, stopwords=stopwords, delete_stopwords=delete_stopwords)
        )  # Lemmatize if required.
    else:
       df['tokens'] = df['text_cleaned'].progress_apply(tokenize)  # Tokenize if lemmatization is skipped.
    return df


# Removes empty strings which can be found after text normalization
def remove_empty_strings(data, column):
    data = data[data[column].str.strip().ne('')]
    return data

