import pandas as pd
import numpy as np

from scipy.optimize import minimize
from pycuan.paidsearch.utils import number_of_clicks, expenditure, profit

"""
Getting ltv, conv rate, parameters, bids
"""
ltv_conv = pd.read_excel('data/hw-kw-ltv-conv.rate-data.xlsx')
params = pd.read_csv('data/params.csv', index_col=0).T
bid_clicks = pd.read_csv(params.index[0], index_col=0)

data = {

}
for i in range(params.shape[0]):
    ltv, conv_rate = ltv_conv.iloc[i, 1:].values
    alpha, beta = params.iloc[i, :].values

    bid_range = np.linspace(bid_clicks.iloc[:, 0].max() / 2, 2 * bid_clicks.iloc[:, 0].max(), 10)
    """
    Creating a range of initial values to test from.
    """
    bid_opt = []
    for x_initial in bid_range:
        res = minimize(profit, x0=x_initial, args=(alpha, beta, ltv, conv_rate))
        bid_opt += [res.x]

    keyword = ltv_conv.iloc[i, 0]
    bid_final = np.mean(bid_opt)
    exp = expenditure(bid_final, alpha, beta)
    prof = -profit(bid_final, alpha, beta, ltv, conv_rate)
    data[keyword] = [exp, prof, bid_final]
    print("Keyword: {}, Expenditure: {}, Profit: {}, Optimal Bid: {}".format(keyword, exp, prof, bid_final))
pd.DataFrame(data).to_csv('data/partb.csv')




