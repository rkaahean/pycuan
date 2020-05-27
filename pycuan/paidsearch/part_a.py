import pandas as pd
import numpy as np
import glob
import matplotlib.pyplot as plt

from scipy.optimize import curve_fit
from pycuan.paidsearch.utils import number_of_clicks

keywords = glob.glob('data/clicksdata*')

data = {

}
for keyword in keywords:

    df = pd.read_csv(keyword)
    alpha_range = np.linspace(df.iloc[:, 2].max() / 2, 2 * df.iloc[:, 2].max(), 10)
    beta_range = 0.69 / alpha_range

    params = []
    for bounds in list(zip(alpha_range, beta_range)):
        popt, _ = curve_fit(number_of_clicks, df.iloc[:, 1].values, df.iloc[:, 2].values,
                            bounds=(0, np.inf), p0=list(bounds))

        params += [popt]
    data[keyword] = np.mean(np.array(params), axis=0)
print(data)
pd.DataFrame(data).to_csv('data/params.csv')