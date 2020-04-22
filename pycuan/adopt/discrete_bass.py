import numpy as np


def get_bass_model(p, q, M, period=30):
    """
    Create a discrete bass model, given p, q & M.
    Return the new and cumulative adoptions. We provide a period argument,
    to indicate the number of time periods we want our bass model to be computed
    till. It is not inclusive of the last time period.
    """

    # Initializing the arrays
    A = [0] * period
    R = [0] * period
    F = [0] * period
    N = [0] * period

    # One important thing to note, is that the time period we start from is t = 0.
    # In many articles, you will see time starting from t = 1. They are both the
    # same for all intents and purposes. Starting with t = 0 makes life easier in
    # python, as indexing in python starts from 0 too.

    # We start with A(0) =0, and build up the values for t = 0 from the equations
    # formulated
    A[0] = 0
    R[0] = M
    F[0] = p
    N[0] = M * p

    # Recursion starts from next time step
    t = 1

    # Creating a helper function for recursion
    def get_bass_model_helper(A, R, F, N, t):

        # If we have reached the final period, return the values
        if t == period:
            return A, R, F, N
        else:

            # Else, just compute the values for t
            A[t] = N[t - 1] + A[t - 1]
            R[t] = M - A[t]
            F[t] = p + q * A[t] / M
            N[t] = F[t] * R[t]

            # compute values for the next time step
            return get_bass_model_helper(A, R, F, N, t + 1)

    A, R, F, N = get_bass_model_helper(A, R, F, N, t)

    # Converting to numpy arrays and returning.
    return np.array(N), np.array(A)


def extrapolate_bass(p, q, M, till_period, **kwargs):
    """
    A function to extrapolate till a certain period, from an
    existing N array (which is passed in **kwargs)
    """

    # Initializing the required arrays
    A = np.zeros(till_period)
    N = np.zeros(till_period)
    R = np.zeros(till_period)
    F = np.zeros(till_period)

    # Transferring the existing N values into the array.
    A[:len(kwargs['A'])] = kwargs['A']
    N[:len(kwargs['N'])] = kwargs['N']

    # The current length of the array. N(t-1) has been computed, Need
    # to resume from N(t)
    t = len(kwargs['A'])

    def extrapolate_bass_helper(A, R, F, N, t):
        """
        defining a recursive helper function for extrapolation.
        """

        # need to compute until till_period + 1
        if t == till_period:
            return N, F, R, A
        else:
            # main bass calculation

            A[t] = N[t - 1] + A[t - 1]
            R[t] = M - A[t]
            F[t] = p + q * A[t] / M
            N[t] = F[t] * R[t]
            return extrapolate_bass_helper(A, R, F, N, t + 1)

    N, F, R, A = extrapolate_bass_helper(A, R, F, N, t)
    return N, A


def discrete_bass_func(A_t, p, q, M):
    """
    A function that returns the N(t), given A(t), p and q based on the
    Discrete Bass Model. Mainly used for the non linear optimization.
    """

    # M fixed in problem, but in general, it could be another variable to optimize too.
    return M * p + (q - p) * A_t + (-q / M) * (A_t ** 2)






