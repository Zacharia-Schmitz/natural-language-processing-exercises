def basic_clean(text):
    """
    This function takes in a string and applies some basic text cleaning to it:
    - Lowercase everything
    - Normalize unicode characters
    - Replace anything that is not a letter, number, whitespace or a single quote.
    """
    # Lowercase the text
    text = text.lower()
    
    # Normalize unicode characters
    text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('utf-8', 'ignore')
    
    # Replace anything that is not a letter, number, whitespace or a single quote
    text = re.sub(r"[^a-z0-9'\s]", '', text)
    
    return text

def tokenize(text):
    """
    This function takes in a string and tokenize all the words in the string.
    """
    # Create the tokenizer
    tokenizer = nltk.tokenize.ToktokTokenizer()
    
    # Use the tokenizer
    text = tokenizer.tokenize(text, return_str=True)
    
    return text

def stem(text):
    """
    This function takes in some text and return the text after applying stemming to all the words.
    """
    # Create the nltk stemmer object, then use it
    ps = nltk.porter.PorterStemmer()
    stems = [ps.stem(word) for word in text.split()]
    
    # Join our lists of words into a string again
    text_stemmed = ' '.join(stems)
    
    return text_stemmed

def lemmatize(text):
    """
    This function takes in some text and return the text after applying lemmatization to each word.
    """
    # Create the nltk lemmatizer object, then use it
    wnl = nltk.stem.WordNetLemmatizer()
    lemmas = [wnl.lemmatize(word) for word in text.split()]
    
    # Join our list of words into a string again
    text_lemmatized = ' '.join(lemmas)
    
    return text_lemmatized

def remove_stopwords(text, extra_words=None, exclude_words=None):
    """
    This function takes in some text and returns the text after removing all the stopwords.
    It defines two optional parameters, extra_words and exclude_words, which define any additional stop words to include,
    and any words that we don't want to remove.
    """
    # Get the list of stopwords
    stopword_list = stopwords.words('english')
    
    # Add any extra words to the stopword list
    if extra_words:
        stopword_list += extra_words
    
    # Remove any exclude words from the stopword list
    if exclude_words:
        stopword_list = [word for word in stopword_list if word not in exclude_words]
    
    # Tokenize the text
    words = text.split()
    
    # Remove the stopwords from the text
    filtered_words = [word for word in words if word not in stopword_list]
    
    # Join the filtered words back into a string
    filtered_text = ' '.join(filtered_words)
    
    return filtered_text

def preprocess_news_df(news_df: pd.DataFrame) -> pd.DataFrame:
    """
    Preprocesses the content column of a pandas DataFrame containing news articles.

    Parameters:
    news_df (pd.DataFrame): The pandas DataFrame containing the news articles.

    Returns:
    pd.DataFrame: The preprocessed pandas DataFrame containing the news articles.
    """
    # Rename the content column to original
    news_df = news_df.rename(columns={'content': 'original'})

    # Apply basic cleaning, tokenization, and stopword removal to the original column
    news_df['clean'] = news_df.original.apply(basic_clean).apply(tokenize).apply(remove_stopwords)

    # Apply stemming to the clean column
    news_df['stemmed'] = news_df.clean.apply(stem)

    # Apply lemmatization to the clean column
    news_df['lemmatized'] = news_df.clean.apply(lemmatize)

    # Select the desired columns
    news_df = news_df[['title', 'category','original', 'clean', 'stemmed', 'lemmatized']]

    return news_df

def preprocess_codeup_df(codeup_df: pd.DataFrame) -> pd.DataFrame:
    """
    Preprocesses the content column of a pandas DataFrame containing Codeup curriculum data.

    Parameters:
    codeup_df (pd.DataFrame): The pandas DataFrame containing the Codeup curriculum data.

    Returns:
    pd.DataFrame: The preprocessed pandas DataFrame containing the Codeup curriculum data.
    """
    # Rename the content column to original
    codeup_df = codeup_df.rename(columns={'content': 'original'})

    # Apply basic cleaning, tokenization, and stopword removal to the original column
    codeup_df['clean'] = codeup_df.original.apply(basic_clean).apply(tokenize).apply(remove_stopwords)

    # Apply stemming to the clean column
    codeup_df['stemmed'] = codeup_df.clean.apply(stem)

    # Apply lemmatization to the clean column
    codeup_df['lemmatized'] = codeup_df.clean.apply(lemmatize)

    # Select the desired columns
    codeup_df = codeup_df[['title', 'category','original', 'clean', 'stemmed', 'lemmatized']]

    return codeup_df