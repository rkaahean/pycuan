import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from factor_analyzer import FactorAnalyzer

cars_ar = pd.read_csv("data/cars.ar.csv", sep=",", index_col=0)

gof = []
for k in range(1, 11):
    fa = FactorAnalyzer(n_factors=k, rotation=None)
    fa_fit_out = fa.fit(cars_ar)
    fa_communalities = fa_fit_out.get_communalities()
    fa_gof = sum(fa_communalities)

    gof = gof + [fa_gof]

plt.plot(list(range(1, 11)), gof)
plt.xlabel("Values of k.")
plt.ylabel("Goodness of fit.")
plt.gcf().savefig('data/q3kchoose.png', dpi=500)
# plt.show()

# Difference in maps for k = 7 & k = 8?
print("As we can see, after about k = 8, the change in negligible.\n")

# How are these close to the regression coefficients? Documentation?
print("Reverting to k = 2.\n")

fa = FactorAnalyzer(n_factors=2, rotation=None)
fa_fit_out = fa.fit(cars_ar)
fa_communalities = fa_fit_out.get_communalities()
fa_scores = np.array(fa_fit_out.transform(cars_ar))
fa_factor_loadings = np.array(fa_fit_out.loadings_)

plt.figure()
plt.scatter(fa_scores[:, 0], fa_scores[:, 1])

SCALE = 1.5
for i in range(len(fa_communalities)):
    x = fa_factor_loadings[i, 0]
    y = fa_factor_loadings[i, 1]

    R_sq = fa_communalities[i]

    arrow_end_x = SCALE * R_sq * x / (np.sqrt(x ** 2 + y ** 2))
    arrow_end_y = SCALE * R_sq * y / (np.sqrt(x ** 2 + y ** 2))

    plt.arrow(0, 0, arrow_end_x, arrow_end_y, length_includes_head=True,
              head_width=0.08, head_length=0.0002)

# Again, need to add spacing to annotations. Need to resolve issue in Part A and Part B.

car_atr = list(cars_ar.index)
for i in range(len(car_atr)):
    plt.annotate(car_atr[i], fa_scores[i, :])
plt.axis('scaled')
plt.xlim(-2, 2)
plt.show()

