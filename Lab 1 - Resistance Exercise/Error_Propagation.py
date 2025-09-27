import numpy as np

def multiplication(x, delta_x, y, delta_y, w, delta_w, z):
    """
    Function Description:
    Calculates the RMS uncertainty for multiplication and division operations using error propagation.
    
    Parameters:
    x (array_like): Array of values for input x.
    delta_x (array_like): Array of uncertainty values for x.
    y (array_like): Array of values for input y.
    delta_y (array_like): Array of uncertainty values for y.
    w (array_like): Array of values for input w.
    delta_w (array_like): Array of uncertainty values for w.
    z (array_like): Array of calculated output values.
    
    Returns:
    array_like: Array of RMS uncertainty values for z.
    """

    # Vectorized calculation - no loop needed!
    rel_x_sq = (delta_x / x) ** 2
    rel_y_sq = (delta_y / y) ** 2
    rel_w_sq = (delta_w / w) ** 2
    
    # Combined relative uncertainty
    rel_uncertainty = np.sqrt(rel_x_sq + rel_y_sq + rel_w_sq)
    
    # Convert to absolute uncertainty
    delta_z = z * rel_uncertainty

    return delta_z

def addition(delta_x, delta_y, delta_w):
    """
    Function Description:
    Calculates the RMS uncertainty for addition and subtraction operations.
    
    Parameters:
    delta_x (array_like): Array of uncertainty values for x.
    delta_y (array_like): Array of uncertainty values for y.
    delta_w (array_like): Array of uncertainty values for w.
    
    Returns:
    array_like: Array of RMS uncertainty values for z.
    """
    
    # Vectorized RMS calculation
    delta_z = np.sqrt(delta_x**2 + delta_y**2 + delta_w**2)
    
    return delta_z