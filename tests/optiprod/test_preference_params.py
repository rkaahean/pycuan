from pycuan.optiprod.PreferenceParams import *
from pycuan.optiprod.ProductConstants import *

import numpy as np
import pandas as pd

"""
There are 4 major inputs that define the ProductConstants class:

1. The information regarding the features, and the columns it corresponds to in the data.
2. The ranges of the attributes of the products to be considered. 
3. The cost of production of each of the mentioned attributes.
4. The product specification of the competitors. (However, this is not a necessary step)
"""

"""
1. The matrix listing which features and the corresponding columns in the preference parameters data.
THE ORDER OF attributes is IMPORTANT.

IMPORTANCE'S MUST ALWAYS BE NAMED 'Im'.
"""
FEATURE_MATRIX = {
    'Pr': ['pPr30', 'pPr10', 'pPr05'],
    'In': ['pIn0.5', 'pIn1', 'pIn3'],
    'Cp': ['pCp12', 'pCp20', 'pCp32'],
    'Cl': ['pClD', 'pClF', 'pClE'],
    'Cn': ['pCnSl', 'pCnSp', 'pCnLk'],
    'Br': ['pBrA', 'pBrB', 'pBrC'],
    'Im': ['IPr', 'Iin', 'ICp', 'ICl', 'Icn', 'IBr']
}

"""
2. Passing an array of possible product specifications. The order in which the ranges are defined are IMPORTANT.
[30, 10, 5] & [5, 10, 30] for price are not equivalent. 
This is due to the matrix nature of computations, and that requires the all the attributes to follow the same order
found in the preference parameters data.

It is ALSO important to pass price as the first array, because price is the first element in the feature matrix.
The orders from feature matrix and product ranges SHOULD be the same.
"""
RANGE_PRICE = np.array([30, 10, 5])
RANGE_TIME_INSULATION = np.array([0.5, 1, 3])
RANGE_CAPACITY = np.array([12, 20, 32])
RANGE_CLEAN = np.array([7, 5, 2])
RANGE_CONTAINMENT = np.array([0, 0.5, 1])

PRODUCT_RANGES = np.array([RANGE_PRICE,
                           RANGE_TIME_INSULATION,
                           RANGE_CAPACITY,
                           RANGE_CLEAN,
                           RANGE_CONTAINMENT])

"""
3. Similar rules apply when passing the cost of the product. To ensure that computations work, 
add the cost price of the product as +ve numbers. Remaining numbers should be -ve, as they are costs of 
manufacturing the product.
"""

COST_PRICE = [30, 10, 5]
COST_TIME_INSULATION = [-0.5, -1, -3]
COST_CAPACITY = [-1, -2.6, -2.8]
COST_CLEAN = [-1, -2.2, -3]
COST_CONTAINMENT = [-0.5, -0.8, -1]

COST_RANGES = np.array([COST_PRICE,
                        COST_TIME_INSULATION,
                        COST_CAPACITY,
                        COST_CLEAN,
                        COST_CONTAINMENT])

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

preference_params = PreferenceParams(df, product_constants)

print("Setup completed.")

print("Product Range", preference_params.get_interpolation_product_range())
print("Product Catalog", preference_params.get_interpolation_product_catalog())

