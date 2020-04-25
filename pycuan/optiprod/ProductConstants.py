import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s:%(name)s:%(message)s')

handler = logging.FileHandler('data/logs/ProductConstants.log')
handler.setFormatter(formatter)

logger.addHandler(handler)


class ProductConstants:
    """
    A class defining all the constants. Semi generic.
    """

    def __init__(self, feature_matrix, product_ranges, cost_matrix, competition=False):
        """
        Constants related to product that will never change over time, unless intended to.
        """
        logger.log(logging.INFO, '\n')
        logger.log(logging.DEBUG, "Starting initialization...")

        self._FEATURE_MATRIX = feature_matrix
        self._PRODUCT_RANGE = product_ranges
        self._COST_MATRIX = cost_matrix
        self._IMPORTANCE_LEN = self.set_length_importance()

        if competition:
            logger.log(logging.DEBUG, "Assigned competition.")
            self._COMPETITION = competition

        logger.log(logging.DEBUG, "Completed Initialization.")

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

    def get_product_range(self):
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

        Error handling here if Im feature does not exist.
        """
        try:
            logger.log(logging.DEBUG, "Attempting to set importance length...")
            importance = self.get_feature_matrix()['Im']
        except KeyError:
            logger.exception("The importance variable in the feature matrix dictionary should have the key 'Im' ")
            # print("The importance key should be 'Im' in the feature matrix.")
        else:
            logger.log(logging.DEBUG, "Set importance length.")
            return len(importance)
