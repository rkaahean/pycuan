import numpy as np
import pandas as pd

import matplotlib.pyplot as plt

computed_values = pd.read_json('data/computed_values.json')
margin = pd.read_excel('data/margin-revenue-salesforce.xlsx', index_col=0)
margin.columns = margin.columns.str.strip()

drugs = computed_values['Drug'].values


def compute_ratio_revenue(sf, adb_min, adb_max, c, d):
    return adb_min + (adb_max - adb_min) * (sf ** c) / (d + sf ** c)


WORKFORCE_RANGE = np.linspace(0, 800, 100)
WORKFORCE_COST = 0.057

drug_profit_range = []
for drug in drugs:

    profit_margin, orig_rev, orig_salesforce = margin[drug].values
    drug_params = computed_values[computed_values['Drug'] == drug]

    adb_min, adb_max, c, d = drug_params.iloc[:, 1:].values[0].tolist()

    base_profit = orig_rev * profit_margin - orig_salesforce * WORKFORCE_COST

    sales_ratio_range = WORKFORCE_RANGE / orig_salesforce
    ratio_revenue = compute_ratio_revenue(sales_ratio_range, adb_min, adb_max, c, d)
    profit_range = ratio_revenue * orig_rev * profit_margin - WORKFORCE_RANGE * WORKFORCE_COST

    print('Optimal salesforce for {}: {}'.format(drug, WORKFORCE_RANGE[np.argmax(profit_range)]))


