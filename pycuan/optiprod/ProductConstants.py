class ProductConstants:
    """
    A class defining all the constants. Semi generic.
    """

    def __init__(self, feature_matrix, product_ranges, cost_matrix):
        """
        Constants related to product that will never change over time, unless intended to.
        """
        self._FEATURE_MATRIX = feature_matrix
        self._PRODUCT_RANGE = product_ranges
        self._COST_MATRIX = cost_matrix

        self._IMPORTANCE_LEN = self.set_length_importance()

    def get_length_importance(self):
        """
        Return length of the importance's
        """
        return self._IMPORTANCE_LEN

    def get_feature_matrix(self):
        """
        Returns the features matrix.
        """
        return self._FEATURE_MATRIX

    def get_range_product(self):
        """
        Return the range of products.
        """
        return self._PRODUCT_RANGE

    def get_cost_matrix(self):
        """
        Return the cost matrix
        """
        return self._COST_MATRIX

    def get_competition_catalog(self):
        """
        Return the competition catalog.
        NEEDS TO BE CALLED MANUALLY for now.
        """

        return self._COMPETITION

    def set_length_importance(self):
        """
        Return importance length. Importance feature always marked by 'Im'.
        Error handling here.
        """
        return len(self.get_feature_matrix()['Im'])

    def set_competition_catalog(self, arr):
        """
        Get competitor product details. Pass in the index of the preference_parameter columns.
        """

        self._COMPETITION = arr


