import numpy as np


class PreferenceParams():
    """
    A class to preprocess the Preference Parameters.
    This class will:
    1. Generate functions which can compute the preference values for interpolated
    product valus.
    2. Produce the product value itself.
    """

    def __init__(self, df, constants, interpolation_constant=1):
        """
        All preprocessing, cleaning should be done in this class.
        We are passing in dataframe for speed purposes, but all computation will be done in NumPy.
        """
        self._data = df
        self._constants = constants
        self._INTERPOLATION = interpolation_constant

        self._data = self.get_process_dataframe()
        self.set_name_index_map()

        self._data = self._data.values

        self._INTERPOLATED_PRODUCT_RANGES = self.perform_interpolate_product_range()
        self._INTERPOLATED_COST_RANGE = self.perform_interpolate_cost_range()

        self._INTERPOLATED_PRODUCT_CATALOG = self.perform_interpolate_product_catalog()
        self._INTERPOLATED_COST_CATALOG = self.perform_interpolate_cost_catalog()

    def perform_interpolate_product_range(self):
        """
        Get all possible attribute values for all possible features.
        """

        return np.array(list(map(self.generate_range, self._constants.get_range_product())))

    def perform_interpolate_cost_range(self):
        """
        Get all possible cost values.
        """

        return np.array(list(map(self.generate_range, self._constants.get_cost_matrix())))

    def get_interpolation_cost_range(self):
        """
        Return the range of interpolated cost matrices.
        """
        return self._INTERPOLATED_COST_RANGE

    def generate_range(self, x):
        """
        Given the range, we will return all possible candidates for a given attribute.
        """
        d = 0.5 * self.get_interpolation_rate() + 1
        z = np.stack(np.linspace([x[0], x[1]], [x[1], x[2]],
                                 num=int(d + 3 / 2)), axis=1)
        z = np.concatenate(z)
        _, idx = np.unique(z, return_index=True)
        return z[np.sort(idx)].tolist()

    def perform_interpolate_product_catalog(self):
        """
        Given that we know the range of products, we want to compute all possible produdcts.
        """
        x0, x1, x2, x3, x4 = tuple(self.get_interpolation_product_range())
        return np.stack(np.meshgrid(x0, x1, x2, x3, x4), -1).reshape(-1, 5)

    def perform_interpolate_cost_catalog(self):
        x0, x1, x2, x3, x4 = tuple(self.get_interpolation_cost_range())
        return np.stack(np.meshgrid(x0, x1, x2, x3, x4), -1).reshape(-1, 5)

    def get_interpolation_product_catalog(self):
        """
        Return the entire catalog.
        """
        return self._INTERPOLATED_PRODUCT_CATALOG

    def get_interpolation_product_range(self):
        """
        Just return the ranges of products interpolated.
        """
        return self._INTERPOLATED_PRODUCT_RANGES

    def get_interpolation_cost_catalog(self):
        """
        Return the range of all possible costs.
        """
        return self._INTERPOLATED_COST_CATALOG

    def get_preference_data(self):
        """
        Get an instance of the Product Constants.
        """
        return self._data

    def get_process_dataframe(self):
        """
        Clean the data of any issues.
        """
        df = self._data
        df.columns = df.columns.str.strip()

        necessary_columns = sum(self._constants.get_feature_matrix().values(), [])
        df = df.loc[:, necessary_columns]

        return df

    def get_importance_values(self):
        """
        Return only the importance values.
        """
        return self._data.loc[:, self._constants.get_feature_matrix()['Im']].to_dict()

    def get_interpolation_rate(self):
        """
        Return interpolation rate
        """
        return self._INTERPOLATION

    def get_name_index_map(self):
        """
        Returns a dictionary of the name index mapping.
        """
        return self._NAME_INDEX_MAP

    def get_product_constant(self):
        """
        Return the constants object.
        """
        return self._constants

    def set_name_index_map(self):
        """
        Mapping from name to index
        """
        columns = self.get_process_dataframe().columns
        self._NAME_INDEX_MAP = {columns[i]: i for i in range(len(columns))}
