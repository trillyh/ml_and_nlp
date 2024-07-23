import numpy as np

from typing import List

from .preprocessor import Preprocessor

class Frequency:
    """
    Input: 
        entries: List of entries
        labels: Labels for all entries (1 is positive, 0 is negative)
    Output:
        freqs: {(word, label): # word occured in that label}
    """
    def build_freqs(self, entries: List[str], labels): 
        preprocessor = Preprocessor()
        preprocess = preprocessor.preprocess
        # Squeeze labels to one dimension
        labels = np.squeeze(labels).tolist()

        freqs = {}

        for label, entry in zip(labels, entries):
            for word in preprocess(entry):
                pair = (word, label) 
                freqs[pair] = freqs.get(pair, 0) + 1
        return freqs


# For testing
if __name__ == "__main__":
    # Instantiate the Frequency class
    frequency = Frequency()
    # Test data
    entries = [
        "RT This is a tweet! Check out https://example.com #hashtag",
        "Another tweet @user with more text. Visit https://example.com for more info!",
        "Just a simple tweet.",
        "Learning Python is fun! Visit https://python.org",
    ]

    # Corresponding sentiment labels (1 for positive, 0 for negative)
    labels = np.array([[1], [0], [1], [0], [1], [1], [1], [1], [1], [1]])

    # Build frequencies
    freqs = frequency.build_freqs(entries, labels)

    # Print the frequency dictionary
    for key, value in freqs.items():
        print(f"{key}: {value}")
