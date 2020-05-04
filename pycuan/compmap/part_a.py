import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from sklearn.manifold import MDS

cars_od = pd.read_csv("data/cars.dissimilarity.csv", sep=",", index_col=0)

stress = []
for k in range(1, 9):
    mds = MDS(n_components=k, metric=True, max_iter=1000, eps=1e-9, dissimilarity="precomputed", n_jobs=1)
    mdf_fit_out = mds.fit(cars_od)
    stress = stress + [mdf_fit_out.stress_]

plt.plot(list(range(1, 9)), stress)
plt.xlabel("Values of k.")
plt.ylabel("Stress.")
plt.title(" k = 2 is the optimal number of components.")
plt.gcf().savefig('data/q1kchoose.png', dpi=500)

print("Clearly, beyond k = 2, the values change barely, if at all. PART 1 Completed.\n")

"""
Part 2
"""
print("Assuming k = 2.")

mds = MDS(n_components=2, metric=True, max_iter=1000, eps=1e-9, dissimilarity="precomputed", n_jobs=1)
mds_fit_out = mds.fit(cars_od)
coods = np.array(mds_fit_out.embedding_)

car_name = list(cars_od.columns)

plt.figure()
plt.scatter(coods[:, 0], coods[:, 1])

for i in range(len(car_name)):
    plt.annotate(car_name[i], coods[i, :])
plt.tight_layout()
plt.axis('square')
plt.gcf().savefig('data/q1plot.png', dpi=500)
plt.show()








