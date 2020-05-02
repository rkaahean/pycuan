import pandas as pd
import numpy as np

import matplotlib.pyplot as plt

from pycuan.compmap.utils import COLLAPSE_WORDS, collapse_columns

reviews = pd.read_csv('data/reviews.csv')
bag_of_words = pd.read_csv('data/bag-of-words-representation.csv', index_col=0)

# Need to collapse similar words into 1 column.
WORD_LIST = list(bag_of_words.columns)

mod_bag_of_words = collapse_columns(bag_of_words, COLLAPSE_WORDS)
print(mod_bag_of_words.head())
