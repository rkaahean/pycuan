import numpy as np
import pandas as pd
from pycuan.workforce.utils import compute_ratio_revenue
import scipy.optimize as optimize
import json

computed_values = pd.read_json('data/computed_values.json')
margin = pd.read_excel('data/margin-revenue-salesforce.xlsx', index_col=0)
partb_values = pd.read_json('data/partb_values.json')

margin.columns = margin.columns.str.strip()
drugs = computed_values['Drug'].values

WORKFORCE_COST = 0.057


def negative_profit(share):
    """
    This should give the negative profit of all 8 drugs combined.
    :param share: Share of each drug. The sum should always be # of Total salesforce workers.
    :return: -ve profit across all drugs for a particular split.
    """

    i = 0
    profit = []
    for drug in drugs:
        profit_margin, orig_rev, orig_salesforce = margin[drug].values
        drug_params = computed_values[computed_values['Drug'] == drug]

        adb_min, adb_max, c, d = drug_params.iloc[:, 1:].values[0].tolist()

        sales_ratio_range = share[i] / orig_salesforce
        ratio_revenue = compute_ratio_revenue(sales_ratio_range, adb_min, adb_max, c, d)
        profit_range = ratio_revenue * orig_rev * profit_margin - share[i] * WORKFORCE_COST

        i += 1
        profit += [profit_range]

    return -sum(profit)


n_drugs = 8
total_salesforce_size = 700
lower_bound = 0
x0 = np.ones(n_drugs) * total_salesforce_size / n_drugs
sum_constraint_object = optimize.LinearConstraint(np.ones((1, n_drugs)), lower_bound, total_salesforce_size)
bounds_object = optimize.Bounds(lower_bound, np.inf)

optimizer_output = optimize.minimize(negative_profit, x0, method='SLSQP', bounds=bounds_object,
                                     constraints=sum_constraint_object)

drug_share = optimizer_output['x']
i = 0

data = {
    'Drug': [],
    'Optimal Salesforce': [],
    'Optimal Profit': [],
    'Salesforce Change': [],
    'Profit Change': []
}

for drug in drugs:
    drug_workforce_optimal, drug_profit_optimal = partb_values[partb_values['Drug'] == drug].iloc[:, 1:] \
        .values[0] \
        .tolist()
    overall_optimal_drug_workforce = drug_share[i]

    profit_margin, orig_rev, orig_salesforce = margin[drug].values
    adb_min, adb_max, c, d = computed_values[computed_values['Drug'] == drug].iloc[:, 1:].values[0].tolist()

    salesforce_ratio = overall_optimal_drug_workforce / orig_salesforce
    ratio_revenue = compute_ratio_revenue(salesforce_ratio, adb_min, adb_max, c, d)
    profit = ratio_revenue * orig_rev * profit_margin - overall_optimal_drug_workforce * WORKFORCE_COST

    print('Drug: {}, Optimal Salesforce: {}, Optimal profit: {}, Salesforce change: {}%, Profit change: {}%'.format(
        drug,
        overall_optimal_drug_workforce,
        profit,
        (drug_workforce_optimal - overall_optimal_drug_workforce) / drug_workforce_optimal * 100,
        (drug_profit_optimal - profit) / drug_profit_optimal * 100))

    data['Drug'] += [drug]
    data['Optimal Salesforce'] += [overall_optimal_drug_workforce]
    data['Optimal Profit'] += [profit]
    data['Salesforce Change'] += [
        (drug_workforce_optimal - overall_optimal_drug_workforce) / drug_workforce_optimal * 100]
    data['Profit Change'] += [(drug_profit_optimal - profit) / drug_profit_optimal * 100]

    i += 1

with open('data/partc_values.json', 'w') as fp:
    json.dump(data, fp)
