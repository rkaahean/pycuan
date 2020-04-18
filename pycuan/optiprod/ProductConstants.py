class ProductConstants():
    """
    A class defining all the constants. Semi generic.

    """

    def __init__(self):
        """
        Constants related to product that will never change over time, unless intended to.
        """
        self.set_feature_matrix()
        self.set_length_importance()
        self.set_range_product()
        self.set_cost_matrix()

    def get_length_importance(self):
        """
        Return length of the importances
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

    def set_range_product(self):
        """
        Setting range of products. Add option to pass a dictionary?
        """
        RANGE_PRICE = np.array([30, 10, 5])
        RANGE_TIME_INSULATION = np.array([0.5, 1, 3])
        RANGE_CAPACITY = np.array([12, 20, 32])
        RANGE_CONTAINMENT = np.array([0, 0.5, 1])
        RANGE_CLEAN = np.array([7, 5, 2])

        self._PRODUCT_RANGE = np.array([RANGE_PRICE,
                                        RANGE_TIME_INSULATION,
                                        RANGE_CAPACITY,
                                        RANGE_CLEAN,
                                        RANGE_CONTAINMENT])

    def set_feature_matrix(self):
        """
        Setting the feature matrix
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
        self._FEATURE_MATRIX = FEATURE_MATRIX

    def set_length_importance(self):
        """
        Return importance length.
        """
        self._IMPORTANCE_LEN = len(self.get_feature_matrix()['Im'])

    def set_cost_matrix(self):
        """
        Setting the cost matrrix.
        """

        COST_PRICE = [30, 10, 5]
        COST_TIME_INSULATION = [-0.5, -1, -3]
        COST_CAPACITY = [-1, -2.6, -2.8]
        COST_CLEAN = [-1, -2.2, -3]
        COST_CONTAINMENT = [-0.5, -0.8, -1]

        self._COST_MATRIX = np.array([COST_PRICE,
                                      COST_TIME_INSULATION,
                                      COST_CAPACITY,
                                      COST_CLEAN,
                                      COST_CONTAINMENT])

    def get_cost_matrix(self):
        """
        Return the cost matrix
        """
        return self._COST_MATRIX

    def set_competition_catalog(self, arr):
        """
        Get competitor product details. Pass in the index of the preference_parameter columns.
        """

        self._COMPETITION = arr

    def get_competition_catalog(self):
        """
        Return the competition catalog.
        NEEDS TO BE CALLED MANUALLY for now.
        """

        return self._COMPETITION