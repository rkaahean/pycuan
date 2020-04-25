from tests.optiprod.test_preference_params import *
from pycuan.optiprod.UtilityCompute import *

competitors = np.array([[0, 5, 7, 11, 14, 15],
                        [1, 4, 7, 10, 13, 16]])

"""
Need to add the competition feature.
Pass in indexes of the attributes in the preference parameters.
"""
product_constants = ProductConstants(FEATURE_MATRIX, PRODUCT_RANGES, COST_RANGES, competitors)
"""
Change the interpolation constant as required.
"""
preference_params = PreferenceParams(df, product_constants, interpolation_constant=1)

"""
C: the constant in the exponentiation phase. The formula for C is given as follows:
"""
C = 0.0139
utility_compute = UtilityCompute(preference_params, C)
df = utility_compute.get_competition_report()
print(df.head())
