
import nltk
from typing import List
import re
import string
from nltk.tokenize import TweetTokenizer
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer

class Preprocessor:

    def preprocess(self, words: str) -> List[str]:
        try:
            words = self.remove_unrelated(words)
        except:
            print("Error occurred when removing unrelated words using Regex")

        print("Removed unrelated words")

        try:
            tokenized_words = self.tokenize(words)
        except:
            print("Error occurred when tokenizing words")
            return [] # avoid unbound error

        try:
            clean_words = self.remove_stopword_and_punctuation(tokenized_words)
        except:
            print("Error occurred when removing stopwords and punctuation")
            return [] # avoid unbound error

        self.stem(clean_words)
        return clean_words

    def remove_unrelated(self, words: str) -> str:
        words = re.sub(r'^RT[\s]+', '', words)
        words = re.sub(r'https?://[^\s\n\r]+', '', words)
        words = re.sub(r'#', '', words)
        return words

    def tokenize(self, words: str) -> List[str]:
        tokenizer = TweetTokenizer(preserve_case=False, strip_handles=True, reduce_len=True)
        return tokenizer.tokenize(words)
        
    def remove_stopword_and_punctuation(self, tokenized_words: List[str]) -> List[str]:
        stopwords_english = set(stopwords.words("english"))
        clean_words = []
        for word in tokenized_words:
            if (word not in stopwords_english
                and word not in string.punctuation):
                clean_words.append(word)
        return clean_words

    def stem(self, clean_words: List[str]):
        stemmer = PorterStemmer()  
        for i in range(len(clean_words)):
            clean_words[i] = stemmer.stem(clean_words[i])

"""
Use for testing
"""
if __name__ == "__main__":
    nltk.download('stopwords')
    preprocessor = Preprocessor()
    
    # Test data
    test_tweet = "RT This is a tweet! Check out https://example.com #hashtag"
    test_tweets = [
        "RT This is a tweet! Check out https://example.com #hashtag",
        "Another tweet @user with more text. Visit https://example.com for more info!",
        "Just a simple tweet.",
        "RT Testing another tweet. Visit http://example.com #testing",
        "Here's a tweet with some #random #hashtags and a URL https://test.com",
        "Yet another tweet, RT it if you like! https://link.com",
        "Tweeting about #AI and #ML. Check this out https://ai.example.com",
        "RT This is great! #amazing https://great.com",
        "Learning Python is fun! Visit https://python.org",
        "This is the last test tweet! https://test.com #end"
    ]

    # Test single tweet
    print("\nSingle Tweet Test:")
    cleaned_words = preprocessor.preprocess(test_tweet)
    print("All together:", cleaned_words)

    # Test multiple tweets
    print("\nMultiple Tweets Test:")
    for i, tweet in enumerate(test_tweets):
        print(f"{i} {preprocessor.preprocess(tweet)}")
