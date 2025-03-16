import nltk
from nltk.corpus import brown
from collections import Counter
import string

# Download corpus if not already present
nltk.download("brown")
nltk.download("wordnet")

# Load words from the Brown corpus
words = brown.words()

# Normalize words (lowercase, remove punctuation)
words = [word.lower() for word in words if word.isalpha()]

# Count word frequencies
word_freq = Counter(words)

# Get the 5000 most common words
most_common_words = word_freq.most_common(5000)
antonyms = []

for i in range(len(most_common_words)):
    for syn in wordnet.synsets(most_common_words[i]):
        for l in syn.lemmas():
            if l.antonyms():
                antonyms.append(l.antonyms()[0].name())
            else:
                antonyms.append("--")
