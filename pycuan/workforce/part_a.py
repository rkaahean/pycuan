import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import json

proxy_for_infinity = 10

workforce_estimates = pd.read_excel('data/delphi-consensus-outputs.xlsx', index_col=0)
drugs = workforce_estimates.columns

print("Implementing method 1...\n")

x = [0, 0.5, 1.0, 1.5, proxy_for_infinity]

for drug in drugs:
    y = workforce_estimates[drug].values
    y_lowest = y[0]
    y_highest = y[4]

    y_middle_three = y[1:4]
    x_middle_three = x[1:4]

    """
    def compute_response(sf, c, d):
        return 0.3 + (1.6 - 0.3) * (sf ** c) / (d + sf ** c)
    """

    # popt, _ = curve_fit(compute_response, x_middle_three, y_middle_three, p0=[1, 1])
    popt, _ = curve_fit(lambda sf, c, d: y_lowest + (y_highest - y_lowest) * (sf ** c) / (d + sf ** c),
                        x_middle_three, y_middle_three, p0=[1, 1])

    print('Drug: {}, c = {}, d = {}'.format(drug, popt[0], popt[1]))

print("\nImplementing method 2...")

data = {
    'Drug': [],
    'adbudg_min': [],
    'adbudg_max': [],
    'c': [],
    'd': []
}

for drug in drugs:
    y = workforce_estimates[drug].values
    y_lowest = y[0]
    y_highest = y[4]

    y_middle_three = y[1:4]
    x_middle_three = x[1:4]

    """
    def compute_response(sf, c, d):
        return 0.3 + (1.6 - 0.3) * (sf ** c) / (d + sf ** c)
    """

    # popt, _ = curve_fit(compute_response, x_middle_three, y_middle_three, p0=[1, 1])
    popt, _ = curve_fit(
        lambda sf, adbudg_min, adbudg_max, c, d: adbudg_min + (adbudg_max - adbudg_min) * (sf ** c) / (d + sf ** c),
        x, y, p0=[y_lowest, y_highest, 1, 1])

    data['Drug'] = data['Drug'] + [drug]

    data['adbudg_min'] = data['adbudg_min'] + [popt[0]]
    data['adbudg_max'] = data['adbudg_max'] + [popt[1]]

    data['c'] = data['c'] + [popt[2]]
    data['d'] = data['d'] + [popt[3]]

    print('Drug: {}, adbudg_min = {}, adbudg_max = {}, c = {}, d = {}'.format(drug, popt[0], popt[1], popt[2], popt[3]))

with open('data/computed_values.json', 'w') as fp:
    json.dump(data, fp)
