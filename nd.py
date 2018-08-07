import numpy as np


def nondom(Z, axis=1):
    """
    Return a list of indices of the non-dominated points in the set `Z`.
    Parameters
    ----------
    Z : numpy.ndarray
        The set from which to determine the non-dominated points.
    axis : int, optional
        The axis along which to determine the non-dominated points (default=1).
    Returns
    -------
    list
        The indices of the non-dominated points in `Z`.
    Notes
    -----
    This function assumes that lower values are dominating.
    
    Examples
    --------
    >>> import numpy as np
    >>> from nondom import nondom
    >>> N = 500  # Number of points in X.
    >>> D = 2  # Number of dimensions.
    >>> X = np.random.randn(N, D)
    >>> A = nondom(X)  # Indices of the non-dominated points.
    """
    nondominated = []
    for n, z in enumerate(Z):
        # Count the number of points that dominate `z`.
        ndominators = \
            np.sum(np.all(Z <= z, axis=axis) & np.any(Z < z, axis=axis))

        # If `z` doesn't have any dominators, then it must be non-dominated!
        if ndominators == 0:
            nondominated.append(n)

    return nondominated
