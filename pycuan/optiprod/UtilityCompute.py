import numpy as np
import pandas as pd


class UtilityCompute:
    """
    Main class where utility will be computed. The Product data is fed in from InterpolateCatalog.
    """

    def __init__(self, preference_params, C):
        """
        Initializing the class. Will be used for computing utility.
        More focus on performance.
        """

        self._param = preference_params
        self.C = C

    def get_preference_params(self):
        """
        Get preference parameter object.
        """
        return self._param

    def get_mapping(self):
        """
        Get Ranges of products, and mapping between index of product attr. and the index of the
        corresponding preference params.
        """
        PRODUCT_RANGES = self.get_preference_params().get_product_constant().get_range_product()

        N, ATTR_LEN = PRODUCT_RANGES.shape
        PREF_MAP = {i: np.array([ATTR_LEN * i, ATTR_LEN * i + 1, ATTR_LEN * i + 2]) for i in range(N)}

        return PRODUCT_RANGES, PREF_MAP

    def get_adj_val(self, arr, x):
        """
        Get index of array where the range could belong to. Also returns the ordering of the
        array. (Asc or Desc)
        Need to assert that x is in the range. I.e, if product value  = 29,
        range = [30, 10, 5], then return (0, 1)
        """
        if max(arr) == arr[0]:
            for i in range(len(arr) - 1):
                if arr[i] >= x >= arr[i + 1]:
                    return i, i + 1, True
        else:
            for i in range(len(arr) - 1):
                if arr[i] <= x <= arr[i + 1]:
                    return i, i + 1, False

    def interpolate_helper(self, x, product_range, pref_map):
        """
        Get preference parameters for a single attribute.
        Need to perform if else depending on the ordering of the array.
        Commented part gives a sort of cleaner solution, but still getting negative
        values.
        """

        data = self.get_preference_params().get_preference_data()

        IDX_RANGE_1, IDX_RANGE_2, rev = self.get_adj_val(product_range, x)
        if rev:
            PREF_RANGE_LOW, PREF_RANGE_HI = data[:, pref_map[[IDX_RANGE_1, IDX_RANGE_2]]].T
            scaling_ratio = (PREF_RANGE_HI - PREF_RANGE_LOW) \
                            / (product_range[IDX_RANGE_1] - product_range[IDX_RANGE_2])

            return PREF_RANGE_LOW + scaling_ratio * (product_range[IDX_RANGE_1] - x)
        else:
            PREF_RANGE_LOW, PREF_RANGE_HI = data[:, pref_map[[IDX_RANGE_1, IDX_RANGE_2]]].T
            scaling_ratio = (PREF_RANGE_HI - PREF_RANGE_LOW) \
                            / (product_range[IDX_RANGE_2] - product_range[IDX_RANGE_1])

            return PREF_RANGE_LOW + scaling_ratio * (x - product_range[IDX_RANGE_1])
        """
        PREF_RANGE_LOW, PREF_RANGE_HI = data[:, pref_map[[IDX_RANGE_1, IDX_RANGE_2]] ].T
        scaling_ratio = (PREF_RANGE_HI - PREF_RANGE_LOW) \
                    / ( (product_range[IDX_RANGE_1] - product_range[IDX_RANGE_2]) * ((-1) ** (1 * rev)) )
        return PREF_RANGE_LOW + scaling_ratio * (product_range[IDX_RANGE_1] - x)
        """

    def compute_interpolated_catalog_preferences(self):
        """
        Main compute function. Uses the three methods above.
        Spits out preferences for all customers for all products.
        (#of products, customer_length, #of unique attribute levels)

        NEED TO IMPROVE SPEED
        """
        PRODUCT_RANGES, PREF_MAP = self.get_mapping()
        products = self.get_preference_params().get_interpolation_product_catalog()
        pref_values = []

        for product in products:
            temp = []
            for i in range(len(product)):
                val = self.interpolate_helper(product[i], PRODUCT_RANGES[i], PREF_MAP[i])
                temp = temp + [val]
            pref_values = pref_values + [temp]

        self.set_interpolated_preferences(np.array(pref_values))

    def compute_utility(self):
        """
        Compute the utility.
        """
        pp = self.get_interpolated_preferences()
        pp = np.array([np.vstack([prd, [1] * prd.shape[1]]) for prd in pp])

        """
        Redundant loading of data
        """
        data = self.get_preference_params().get_preference_data()
        imp = data[:, -self.get_preference_params().get_product_constant().get_length_importance():]

        np.multiply(pp, np.expand_dims(imp.T, axis=0))
        utility = np.multiply(pp, np.expand_dims(imp.T, axis=0))

        final_product_utilities = np.average(np.sum(utility, axis=1), axis=1)

        # print(final_product_utilities)
        self.set_utility(final_product_utilities)
        # self.set_utility(utility)

    def get_competition_utility(self):
        """
        Compute the utility of the competitors.
        """

        data = self.get_preference_params().get_preference_data()
        competitors = self.get_preference_params().get_product_constant().get_competition_catalog()

        imp_len = self.get_preference_params().get_product_constant().get_length_importance()

        comp_util = []
        for i in range(len(competitors)):
            pref = np.multiply(data[:, competitors[i]], data[:, -imp_len:])
            pref = np.average(np.sum(pref, axis=1))
            comp_util = comp_util + [pref]

        return comp_util

    def get_competition_report(self):
        """
        Get final report!
        """
        self.compute_interpolated_catalog_preferences()
        self.compute_utility()

        competitors = self.get_competition_utility()
        cand_util = self.get_utility()

        C = self.C

        market_share = []
        for cand in cand_util:
            c_val = [x * C for x in [cand] + competitors]
            exp_val = np.exp(c_val)
            share = exp_val[0] / sum(exp_val)
            market_share = market_share + [share]

        cost_values = np.sum(self.get_preference_params().get_interpolation_cost_catalog(), axis=1)
        expected_profit = np.multiply(market_share, cost_values)
        df = pd.DataFrame({'Market Share': market_share, 'Margin': cost_values, 'Expected Profit': expected_profit})

        return df

    def set_utility(self, val):
        """
        Set the utility.
        """
        self._util = val

    def get_utility(self):
        """
        Return utility
        """
        return self._util

    def set_interpolated_preferences(self, val):
        """
        Store the values.
        """
        self._inter_prep = val

    def get_interpolated_preferences(self):
        """
        Get the interpolated preferences.
        """
        return self._inter_prep
