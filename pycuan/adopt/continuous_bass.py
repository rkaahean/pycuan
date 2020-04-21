def continuous_bass_func(t, p, q):
    """
    A function that returns the N(t), given A(t), p and q based on the
    Continuous Bass Model. Mainly used for the non linear optimization.
    """
    # M fixed in problem, but in general, it could be another variable to optimize too
    M = 100

    A_t = M * (1 - np.exp(- (p + q) * t)) / (1 + (q / p) * np.exp(- (p + q) * t))
    A_t_1 = M * (1 - np.exp(- (p + q) * (t - 1))) / (1 + (q / p) * np.exp(- (p + q) * (t - 1)))

    return A_t - A_t_1
