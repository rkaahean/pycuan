import numpy as np
import pandas as pd
from pycuan.workforce.utils import compute_ratio_revenue
import json

computed_values = pd.read_json('data/computed_values.json')
margin = pd.read_excel('data/margin-revenue-salesforce.xlsx', index_col=0)
margin.columns = margin.columns.str.strip()

drugs = computed_values['Drug'].values

WORKFORCE_RANGE = np.linspace(0, 800, 100)
WORKFORCE_COST = 0.057

drug_profit_range = []
data = {
    'Drug': [],
    'workforce_optimal': [],
    'profit_optimal': []
}

for drug in drugs:

    profit_margin, orig_rev, orig_salesforce = margin[drug].values
    drug_params = computed_values[computed_values['Drug'] == drug]

    adb_min, adb_max, c, d = drug_params.iloc[:, 1:].values[0].tolist()

    sales_ratio_range = WORKFORCE_RANGE / orig_salesforce
    ratio_revenue = compute_ratio_revenue(sales_ratio_range, adb_min, adb_max, c, d)
    profit_range = ratio_revenue * orig_rev * profit_margin - WORKFORCE_RANGE * WORKFORCE_COST

    print('Optimal salesforce for {}: {}'.format(drug, WORKFORCE_RANGE[np.argmax(profit_range)]))

    data['Drug'] += [drug]
    data['workforce_optimal'] += [WORKFORCE_RANGE[np.argmax(profit_range)]]
    data['profit_optimal'] += [np.max(profit_range)]

with open('data/partb_values.json', 'w') as fp:
    json.dump(data, fp)



