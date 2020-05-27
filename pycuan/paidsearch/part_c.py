import numpy as np
import pandas as pd
import scipy.optimize as optimize
from pycuan.paidsearch.utils import number_of_clicks, expenditure, profit, total_expenditure, total_profit

expenditure_constraint = optimize.NonlinearConstraint(total_expenditure, 0, 3000)

init_values = np.array([17, 4.5, 11.5, 1.8])
res = optimize.minimize(total_profit, x0=init_values, constraints=expenditure_constraint)

print("Optimal bids and total profit",res.x, -total_profit(res.x))

ltv_conv = pd.read_excel('data/hw-kw-ltv-conv.rate-data.xlsx')
params = pd.read_csv('data/params.csv', index_col=0).T

alphas = params.iloc[:, 0].values
betas = params.iloc[:, 1].values
ltvs = ltv_conv.iloc[:, 1].values
conv_rates = ltv_conv.iloc[:, 2].values

data = {

}
for i in range(params.shape[0]):

    keyword = ltv_conv.iloc[i, 0]

    exp = expenditure(res.x[i], alphas[i], betas[i])
    prof = -profit(res.x[i], alphas[i], betas[i], ltvs[i], conv_rates[i])

    print(keyword, exp, prof)

    data[keyword] = [res.x[i], exp, prof]

pd.DataFrame(data).to_csv('data/partc.csv')