import numpy as np
import pandas as pd
import random
from scipy.optimize import curve_fit
from pycuan.workforce.utils import compute_ratio_revenue
from statistics import median
import json

"""
Importing all the data.
"""
computed_values = pd.read_json('data/computed_values.json')
margin = pd.read_excel('data/margin-revenue-salesforce.xlsx', index_col=0)
workforce_estimates = pd.read_excel('data/delphi-consensus-outputs.xlsx', index_col=0)
margin.columns = margin.columns.str.strip()

WORKFORCE_RANGE = np.linspace(100, 440, 11)
WORKFORCE_COST = 0.057

random.seed(4100142)
"""
Getting all the parameters related to Naprosyn.
"""
adbudg_min, adbudg_max, c, d = computed_values[computed_values['Drug'] == 'Naprosyn'].iloc[:, 1:].values[0]
profit_margin, orig_rev, org_sale = margin['Naprosyn'].values

"""
Getting the theta and covariance.
"""
proxy_for_infinity = 10
x = [0, 0.5, 1.0, 1.5, proxy_for_infinity]
y = workforce_estimates['Naprosyn'].values
theta_hat, varcov_theta_hat = curve_fit(
    compute_ratio_revenue,
    x,
    y
)

"""
Now we can do sampling, 500 times.
"""


def compute_utility(expected_value, std, ra=2.5):
    return expected_value - 0.5 * ra * (std ** 2)


data = {
    'sf': [],
    'mean': [],
    'median': [],
    'std_dev': [],
    'utility': []
}
multivariate_naprosyn_samples = np.random.multivariate_normal(theta_hat, varcov_theta_hat, size=500)
for sf in WORKFORCE_RANGE:
    profit_sf = []
    for sample in multivariate_naprosyn_samples:
        ratio_rev = compute_ratio_revenue(sf / org_sale, *sample)
        profit = ratio_rev * orig_rev * profit_margin - sf * WORKFORCE_COST
        profit_sf += [profit]

    mean, med, std_dev = np.mean(profit_sf), median(profit_sf), np.std(profit_sf)

    data['sf'] += [sf]
    data['mean'] += [mean]
    data['median'] += [med]
    data['std_dev'] += [std_dev]
    data['utility'] += [compute_utility(mean, std_dev)]

with open("data/partd_values.json", "w") as fp:
    json.dump(data, fp)
