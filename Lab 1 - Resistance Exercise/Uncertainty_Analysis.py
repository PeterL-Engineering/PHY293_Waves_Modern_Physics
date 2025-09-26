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

if __name__ == "__main__":

    "Circuit Option 1 Values"

    # All values in base SI units (Ohms, Volts, Amperes)
    R_li = np.array([100.32, 219.91, 26814.0, 101570.0])  # Ω
    delta_R_li = np.array([0.25, 0.49, 59.0, 250.0])  # Ω

    V1 = np.array([6.501, 6.501, 6.501, 6.501])  # V
    delta_V1 = np.array([0.005, 0.005, 0.005, 0.005])  # V

    # Convert mA to A
    I = np.array([63.67, 29.315, 0.241, 0.063]) / 1000.0  # A
    delta_I = np.array([0.18, 0.064, 0.051, 0.005]) / 1000.0  # A

    "Circuit Option 2 Values"

    V2 = np.array([6.386, 6.448, 6.501, 6.501])  # V
    delta_V2 = np.array([0.005, 0.005, 0.005, 0.005])  # V

    # Convert mA to A
    I2 = np.array([63.60, 29.322, 0.243, 0.065]) / 1000.0  # A
    delta_I2 = np.array([0.18, 0.064, 0.051, 0.005]) / 1000.0  # A