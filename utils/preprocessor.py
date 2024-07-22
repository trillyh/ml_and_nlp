
import nltk
from typing import List 
import re
import string
from nltk.tokenize import TweetTokenizer
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer

class Preprocessor:

    def preprocess(self, list_words: List[str]) -> List[List[str]]:
        list_words2 = list_words.copy()
        try:
            self.remove_unrelated(list_words2)
        except:
            print("Error occurred when removing unrealted word using Regex")

        print("Removed unrelated words")

        tokenized_list_words: List[List[str]] = []
        try:
            tokenized_list_words = self.tokenize(list_words2)
        except:
            print("Error occurred when tokenizing words")

        clean_list_words: List[List[str]] = []
        try:
            clean_list_words = self.remove_stopword_and_punctuation(tokenized_list_words) 
        except:
            print("Error occurred when tokenizing words")

        tokenized_list_words.clear() # free mem
        self.stem(clean_list_words)
        return clean_list_words

    def remove_unrelated(self, list_words: List[str]):
        for i in range(len(list_words)):
            words = list_words[i]
            clean_words = re.sub(r'^RT[\s]+', '', words)
            clean_words = re.sub(r'https?://[^\s\n\r]+', '', clean_words)
            clean_words = re.sub(r'#', '', clean_words)
            list_words[i] = clean_words

    def tokenize(self, list_words: List[str]) -> List[List[str]]:
        tokenized_list_words: List[List[str]] = []
        tokenizer = TweetTokenizer(preserve_case=False, strip_handles=True, reduce_len=True)
        for words in list_words:
            tokenized_list_words.append(tokenizer.tokenize(words))
        
        return tokenized_list_words
        
    def remove_stopword_and_punctuation(self, tokenized_list_words: List[List[str]]) -> List[List[str]]:
        # Import stopwords in English
        stopwords_english = stopwords.words("english")

        clean_lists_words: List[List[str]] = []
        for words in tokenized_list_words:
            inner_list_word = []
            for word in words:
                if (word not in stopwords_english
                    and word not in string.punctuation):
                    inner_list_word.append(word)
            clean_lists_words.append(inner_list_word)

        return clean_lists_words

    def stem(self, clean_list_words: List[List[str]]):
        stemmer = PorterStemmer()  
        for w in range(len(clean_list_words)):
            for i in range(len(clean_list_words[w])):
                clean_list_words[w][i] = stemmer.stem(clean_list_words[w][i])

"""
Use for testing
"""
if __name__ == "__main__":
    nltk.download('stopwords')
    preprocessor = Preprocessor()
    
    # Test data
    test_list = [
        "RT This is a tweet! Check out https://example.com #hashtag",
        "Another tweet @user with more text. Visit https://example.com for more info!",
        "Just a simple tweet."
    ]

    # Test remove_unrelated
    test_remove_unrelated = test_list.copy()
    preprocessor.remove_unrelated(test_remove_unrelated)
    print("After remove_unrelated:", test_remove_unrelated)
    
    # Test tokenize
    tokenized = preprocessor.tokenize(test_remove_unrelated)
    print("After tokenize:", tokenized)
    
    # Test remove_stopword_and_punctuation
    cleaned = preprocessor.remove_stopword_and_punctuation(tokenized)
    print("After remove_stopword_and_punctuation:", cleaned)

    preprocessor.stem(cleaned)
    print("After stem", cleaned)

    cleaned_list_words = preprocessor.preprocess(test_list.copy())
    print("All together", cleaned_list_words)
