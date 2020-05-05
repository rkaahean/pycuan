import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
from factor_analyzer import FactorAnalyzer
from sklearn.decomposition import LatentDirichletAllocation

from pycuan.compmap.utils import COLLAPSE_WORDS, collapse_columns

reviews = pd.read_csv('data/reviews.csv')
bag_of_words = pd.read_csv('data/bag-of-words-representation.csv', index_col=0)

# Need to collapse similar words into 1 column.
WORD_LIST = list(bag_of_words.columns)

mod_bag_of_words = collapse_columns(bag_of_words, COLLAPSE_WORDS)
mod_bag_of_words['asin'] = reviews['asin']

"""
One of the problems is that, there are different number of reviews for each of the
50 products. Summing them up would not be a great solution. Averaging is a better choice.
"""
mean_mod_bow = mod_bag_of_words.groupby(['asin']).mean()

fa = FactorAnalyzer(n_factors=2, rotation=None)
fa_fit_out = fa.fit(mean_mod_bow)
fa_communalities = fa_fit_out.get_communalities()
fa_scores = np.array(fa_fit_out.transform(mean_mod_bow))
fa_factor_loadings = np.array(fa_fit_out.loadings_)

SCALE = 4
brand_attrs = list(mod_bag_of_words.columns)
for i in range(len(fa_communalities)):
    x = fa_factor_loadings[i, 0]
    y = fa_factor_loadings[i, 1]

    R_sq = fa_communalities[i]

    arrow_end_x = SCALE * R_sq * x / (np.sqrt(x ** 2 + y ** 2))
    arrow_end_y = SCALE * R_sq * y / (np.sqrt(x ** 2 + y ** 2))

    plt.arrow(0, 0, arrow_end_x, arrow_end_y, length_includes_head=True,
              head_width=0.08, head_length=0.0002)
    plt.annotate(brand_attrs[i], (arrow_end_x, arrow_end_y))


plt.scatter(fa_scores[:, 0], fa_scores[:, 1])
plt.axis('scaled')
plt.gcf().savefig('data/q4factor.png', dpi=500)
plt.show()

"""
But for LDA, it is better to do a summation (for some reason).
"""
sum_mod_bow = mod_bag_of_words.groupby(['asin']).sum()

lda = LatentDirichletAllocation(n_components=2, random_state=0)
transformed_bow = lda.fit_transform(mean_mod_bow)

plt.scatter(transformed_bow[:, 0], transformed_bow[:, 1])
plt.gcf().savefig('data/q4lda.png', dpi=500)
plt.show()


