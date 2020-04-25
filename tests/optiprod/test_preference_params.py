from pycuan.optiprod.PreferenceParams import *
from tests.optiprod.test_product_constants import *

import pandas as pd
"""
Test run.
"""
product_constants = ProductConstants(FEATURE_MATRIX, PRODUCT_RANGES, COST_RANGES)

"""
Preference Params testing.
"""
df = pd.read_excel('data/mugs-preference-parameters-full.xlsx')

# Pass only the preference values and the importance's.
# Everything else should be dropped.
df = df.iloc[:, 1:]

preference_params = PreferenceParams(df, product_constants, interpolation_constant=1)

# print("Product Range", preference_params.get_interpolation_product_range())
# print("Product Catalog", preference_params.get_interpolation_product_catalog())
