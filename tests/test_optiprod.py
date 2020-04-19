import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pycuan.optiprod import PreferenceParams, ProductConstants, UtilityCompute

DATA = 'C:/Users/ranja/Desktop/Courses/Winter/Customer Analytics/Week 3/data'
df = pd.read_excel(DATA + '/mugs-preference-parameters-full.xlsx')

competitors = np.array([[0, 5, 7, 11, 14, 15],
                        [1, 4, 7, 10, 13, 16]])

constant_class = ProductConstants.ProductConstants()
constant_class.set_competition_catalog(competitors)
preference_class = PreferenceParams.PreferenceParams(df, constant_class)

utility_class = UtilityCompute.UtilityCompute(preference_class, 0.0139)
final_data = utility_class.get_competition_report()

plt.scatter(final_data['Market Share'], final_data['Expected Profit'], s=4)
plt.gca().set_xlabel("Market Share")
plt.gca().set_ylabel("Expected profit per customer")

plt.title("Interpolated product analysis")
plt.show()
print("Done.")
