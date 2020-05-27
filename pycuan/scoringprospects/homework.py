import pandas as pd
import numpy as np

from sklearn.linear_model import LogisticRegression
import matplotlib.pyplot as plt

import warnings
warnings.filterwarnings("ignore")

df = pd.read_excel('data/prospectscoringhw.xlsx', skiprows=2)
train_df = df.iloc[:200, :]
test_df = df.iloc[204:, :]

"""
Part 1
"""
model = LogisticRegression(solver='newton-cg', penalty='none')
x_train = train_df.iloc[:, :-1].values.astype('float64')
y_train = train_df.iloc[:, -1].values.astype('float64')
y_train = y_train.astype(int)
model.fit(x_train, y_train)

betas = np.append(model.intercept_, model.coef_)

"""
Part 2
"""

x_test = test_df.iloc[:, :-1].values.astype('float64')
pred_prob = model.predict_proba(x_test)[:, 1]
# print("Predicted Probability: ", pred_prob)

avg_response_rate = np.mean(train_df.iloc[:, -1].values)

"""
Part 3
"""

test_df['r'] = pred_prob
test_df['Lift'] = pred_prob/avg_response_rate
test_df = test_df.sort_values(by='Lift', ascending=False)


"""
Part 4
"""

plt.plot(test_df['r'].values)
plt.gcf().savefig('data/q4.png', dpi = 500)
#plt.show()

"""
Part 6
"""


plt.plot(np.cumsum(test_df['r'].values))
plt.gcf().savefig('data/q6.png', dpi = 500)
#plt.show()

"""
Part 8
"""

plt.figure()
print(test_df.iloc[:, -1].values)
plt.plot(np.cumsum(test_df['r'].values))
plt.plot(np.cumsum(test_df['y'].values))

plt.gcf().savefig('data/q8.png', dpi = 500)
plt.show()

print(list(enumerate(np.cumsum(test_df['y'].values))))