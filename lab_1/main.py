"""
Lab 1
Language detection
"""


def tokenize(text: str) -> list or None:
    """
    Splits a text into tokens, converts the tokens into lowercase,
    removes punctuation and other symbols from words
    :param text: a text
    :return: a list of lower-cased tokens without punctuation
    """
    if not isinstance(text, str):
        return None
    text = text.lower()
    preprocessed = ''
    for symbol in text:
        if symbol.isalnum() or symbol == ' ':
            preprocessed += symbol
    tokens = preprocessed.split()
    return tokens


def remove_stop_words(tokens: list, stop_words: list) -> list or None:
    """
    Removes stop words
    :param tokens: a list of tokens
    :param stop_words: a list of stop words
    :return: a list of tokens without stop words
    """
    if not isinstance(tokens, list) or not isinstance(stop_words, list):
        return None
    tokens = [token for token in tokens if token not in stop_words]
    return tokens

def calculate_frequencies(tokens: list) -> dict or None:
    """
    Calculates frequencies of given tokens
    :param tokens: a list of tokens
    :return: a dictionary with frequencies
    """
    if not isinstance(tokens, list):
        return None
    for word in tokens:
        if not isinstance(word, str):
            return None
    freq_dict = {}
    for token in tokens:
        if token in freq_dict:
            freq_dict[token] += 1
        else:
            freq_dict[token] = 1
    return freq_dict

def get_top_n_words(freq_dict: dict, top_n: int) -> list or None:
    """
    Returns the most common words
    :param freq_dict: a dictionary with frequencies
    :param top_n: a number of the most common words
    :return: a list of the most common words
    """
    if not isinstance(freq_dict, dict) or not isinstance(top_n, int):
        return None
    freq_dict_sort = sorted(freq_dict.items(), key=lambda i: i[1], reverse=True)
    if freq_dict_sort == []:
        return []
    new_freq_list = []
    for element in freq_dict_sort:
        new_freq_list.append(element[0])
        top_words = new_freq_list[:top_n]
    return top_words

def create_language_profile(language: str, text: str, stop_words: list) -> dict or None:
    """
    Creates a language profile
    :param language: a language
    :param text: a text
    :param stop_words: a list of stop words
    :return: a dictionary with three keys – name, freq, n_words
    """
    if not isinstance(language, str) or \
            not isinstance(text, str) or \
            not isinstance(stop_words,list):
        return None
    if len(text) == 0:
        return None
    profile = {}
    profile['name'] = language
    freq = calculate_frequencies(remove_stop_words(tokenize(text),stop_words))
    profile['freq'] = freq
    n_words = len(freq)
    profile['n_words'] = n_words
    return profile

def compare_profiles(unknown_profile: dict, profile_to_compare: dict, top_n: int) -> float or None:
    """
    Compares profiles and calculates the distance using top n words
    :param unknown_profile: a dictionary
    :param profile_to_compare: a dictionary
    :param top_n: a number of the most common words
    :return: the distance
    """
    if not isinstance(unknown_profile, dict) or \
            not isinstance(profile_to_compare, dict) or \
            not isinstance(top_n, int):
        return None
    count = 0
    top_n_words_profile_to_compare = get_top_n_words(profile_to_compare['freq'],top_n)
    top_n_words_unknown_profile = get_top_n_words(unknown_profile['freq'], top_n)
    len_top_n_words_unknown_profile = len(top_n_words_unknown_profile)
    for word in top_n_words_profile_to_compare:
        if len(top_n_words_profile_to_compare) == len(top_n_words_unknown_profile) and \
                (word in top_n_words_unknown_profile):
            share_of_common_frequency_words = float(1)
        else:
            for word_profile_to_compare in top_n_words_profile_to_compare:
                if word_profile_to_compare in top_n_words_unknown_profile:
                    count += 1
            share_of_common_frequency_words = round(count / len_top_n_words_unknown_profile,2)
        return share_of_common_frequency_words

def detect_language(unknown_profile:dict, profile_1:dict, profile_2:dict, \
                    top_n:int) -> str or None:
    """
    Detects the language of an unknown profile
    :param unknown_profile: a dictionary
    :param profile_1: a dictionary
    :param profile_2: a dictionary
    :param top_n: a number of the most common words
    :return: a language
    """
    if not isinstance(unknown_profile, dict) or not isinstance(profile_1,dict):
        return None
    share_of_common_words_with_profile_1 = compare_profiles(unknown_profile,profile_1,top_n)
    share_of_common_words_with_profile_2 = compare_profiles(unknown_profile,profile_2,top_n)
    if share_of_common_words_with_profile_1 > share_of_common_words_with_profile_2:
        language = profile_1['name']
    elif share_of_common_words_with_profile_1 < share_of_common_words_with_profile_2:
        language = profile_2 ['name']
    else:
        all_languages = [profile_1['name'], profile_2['name']]
        language = all_languages.sort()[0]
    return language

