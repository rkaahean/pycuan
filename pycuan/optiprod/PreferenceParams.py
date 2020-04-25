import numpy as np
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s:%(name)s:%(message)s')

handler = logging.FileHandler('data/logs/PreferenceParams.log')
handler.setFormatter(formatter)

logger.addHandler(handler)


class PreferenceParams:
    """
    A class to pre-process the Preference Parameters.
    This class will:
    1. Generate functions which can compute the preference values for interpolated
    product values.
    2. Produce the product value itself.
    """

    def __init__(self, df, constants, interpolation_constant=1):
        """
        All pre-processing, cleaning should be done in this class.
        We are passing in data-frame for speed purposes, but all computation will be done in NumPy.
        """
        logger.log(logging.DEBUG, "\n")
        logger.log(logging.DEBUG, "Initializing the Class...")
        self._constants = constants
        self._INTERPOLATION = interpolation_constant

        self._data = self.set_processed_data(df)
        self._NAME_INDEX_MAP = self.set_name_index_map()

        self._data = self._data.values

        # TODO: Add a describe function of some sort that gives information about the computation.
        self._INTERPOLATED_PRODUCT_RANGES = self.compute_interpolated_product_range()
        self._INTERPOLATED_COST_RANGE = self.compute_interpolated_cost_range()

        self._INTERPOLATED_PRODUCT_CATALOG = self.compute_interpolated_product_catalog()
        self._INTERPOLATED_COST_CATALOG = self.compute_interpolated_cost_catalog()

    def compute_interpolated_product_range(self):
        """
        Get all possible attribute values for all possible features.
        """
        logger.log(logging.DEBUG, "Starting interpolation process for products...")
        return np.array(list(map(self.generate_range, self._constants.get_product_range())))

    def compute_interpolated_cost_range(self):
        """
        Get all possible cost values.
        """
        logger.log(logging.DEBUG, "Starting interpolation process for costs...")
        return np.array(list(map(self.generate_range, self._constants.get_cost_matrix())))

    def get_interpolation_cost_range(self):
        """
        Return the range of interpolated cost matrices.
        """
        return self._INTERPOLATED_COST_RANGE

    def generate_range(self, x):
        """
        Given the range, we will return all possible candidates for a given attribute.

        if interpolation_rate == x, then the range of products will have 2*n + 1 elements.

        TODO : AS of now, we cannot handle cases where RANGE is more than 3 different values.
                It has to be exactly 3.
        """
        logger.log(logging.DEBUG, 'Performing interpolation.')

        interpolation_rate = self.get_interpolation_rate()
        d = interpolation_rate + 1

        """
        Generate intermediate values between ranges. Then combine the two.
        The middle value will be repeated, and they need to be removed.
        """

        z = np.stack(np.linspace([x[0], x[1]], [x[1], x[2]], num=d), axis=1)
        z = np.concatenate(z)
        _, idx = np.unique(z, return_index=True)
        logger.log(logging.DEBUG, 'Completed interpolated. Length = {}'.format(len(idx)))

        return z[np.sort(idx)].tolist()

    def compute_interpolated_product_catalog(self):
        """
        Given that we know the range of products, we want to compute all possible products.
        We do importance_length - 1, because Brand cannot be interpolated, so it is being omitted.

        :return: A matrix of of different possible products.
        """
        logger.log(logging.DEBUG, "Creating the catalog of products...")
        product_ranges = self.get_interpolation_product_range()
        return np.stack(np.meshgrid(*product_ranges), -1).reshape(-1, self._constants.get_length_importance() - 1)

    def compute_interpolated_cost_catalog(self):
        """
        Computing the interpolated cost values for the corresponding interpolated products.

        :return: A matrix of of different possible costs.
        """
        logger.log(logging.DEBUG, "Creating the catalog of costs...")
        cost_ranges = self.get_interpolation_cost_range()
        return np.stack(np.meshgrid(*cost_ranges), -1).reshape(-1, self._constants.get_length_importance() - 1)

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

    def get_processed_data(self):
        """
        Getter function.
        :return: numpy array of preference data.
        """

        return self._data

    def set_processed_data(self, df):
        """
        Clean the data of any issues.
        Return NumPy array for faster computation.
        """
        logger.log(logging.DEBUG, "Processing data-frame...")

        df.columns = df.columns.str.strip()

        necessary_columns = sum(self._constants.get_feature_matrix().values(), [])
        df = df.loc[:, necessary_columns]

        logger.log(logging.DEBUG, "Finished processing data-frame")
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
        columns = self.get_processed_data().columns
        return {columns[i]: i for i in range(len(columns))}
