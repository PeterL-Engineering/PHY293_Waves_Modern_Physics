import matplotlib.pyplot as plt
import numpy as np
import scipy as scp
import math

def linear_fitter(x_inputs, y_inputs, y_uncertainties):
    """
    Function Description:
    Performs linear regression with chi-squared analysis on x-y data pairs to find
    the best-fit line y = mx + b and calculates associated statistics.
    
    Parameters:
    x_inputs (array_like): Array of x-values (independent variable).
    y_inputs (array_like): Array of y-values (dependent variable).
    y_uncertainties (array_like): Array of uncertainties in y-values.
    
    Returns:
    tuple: A tuple containing (m, b, m_stdrd_dev, b_stdrd_dev, y_variance, 
            chi_squared, reduced_chi_squared, p_value, residuals)
    """
    N = len(x_inputs)
    
    # Calculate delta
    delta = N * np.dot(x_inputs, x_inputs) - np.sum(x_inputs)**2
    
    # Calculate slope (m) and intercept (b)
    m = (N * np.dot(x_inputs, y_inputs) - np.sum(x_inputs) * np.sum(y_inputs)) / delta
    b = (np.sum(y_inputs) - m * np.sum(x_inputs)) / N
    
    # Calculate predicted values and residuals
    y_pred = b + m * x_inputs
    residuals = y_inputs - y_pred
    
    # Calculate y_variance (standard error of estimate)
    y_variance = np.sqrt(np.sum(residuals**2) / (N - 2))
    
    # Calculate standard errors
    m_stdrd_dev = np.sqrt((y_variance**2 * N) / delta)
    b_stdrd_dev = np.sqrt((y_variance**2 * np.dot(x_inputs, x_inputs)) / delta)
    
    # CHI-SQUARED CALCULATION
    # Calculate chi-squared
    chi_squared = np.sum(((y_inputs - y_pred) / y_uncertainties)**2)
    
    # Calculate reduced chi-squared (chi-squared per degree of freedom)
    degrees_of_freedom = N - 2  # 2 parameters (m and b)
    reduced_chi_squared = chi_squared / degrees_of_freedom
    
    # Calculate p-value (probability that chi-squared could be this large by chance)
    try:
        from scipy.stats import chi2
        p_value = 1 - chi2.cdf(chi_squared, degrees_of_freedom)
    except ImportError:
        # Fallback approximation if scipy is not available
        p_value = np.exp(-chi_squared / 2)  # Rough approximation
    
    return (m, b, m_stdrd_dev, b_stdrd_dev, y_variance, 
            chi_squared, reduced_chi_squared, p_value, residuals)

import matplotlib.pyplot as plt

def plot_V_vs_I(I_data, V_data, I_unc, V_unc, m, b, residuals, circuit_name):
    """
    Function Description:
    Plot V vs I with linear fit and residuals side-by-side
    """
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
    
    # Convert back to mA for better plotting
    I_data_mA = I_data * 1000
    I_unc_mA = I_unc * 1000
    
    # Left panel: V vs I with fit
    ax1.errorbar(I_data_mA, V_data, xerr=I_unc_mA, yerr=V_unc, fmt='o', 
                 capsize=3, label='Data with error bars')
    
    # Generate fit line
    I_fit = np.linspace(min(I_data), max(I_data), 100)
    V_fit = m * I_fit + b
    ax1.plot(I_fit * 1000, V_fit, 'r-', 
             label=f'Fit: V = ({m:.1f} Ω)I + ({b:.3f} V)')
    
    ax1.set_xlabel('Current I (mA)')
    ax1.set_ylabel('Voltage V (V)')
    ax1.set_title(f'{circuit_name}: V vs I')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # Right panel: Residuals
    ax2.axhline(y=0, color='r', linestyle='-', alpha=0.7, label='Zero line')
    ax2.errorbar(I_data_mA, residuals, xerr=I_unc_mA, yerr=V_unc, fmt='o', 
                 capsize=3, label='Residuals with error bars')
    ax2.set_xlabel('Current I (mA)')
    ax2.set_ylabel('Residuals (V)')
    ax2.set_title(f'Residuals (Std Dev: {np.std(residuals):.4f} V)')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    return fig

if __name__ == "__main__":

    "Circuit Option 1 Values"
    V1 = np.array([6.498, 6.500, 6.501, 6.501])  # V
    delta_V1 = np.array([0.005, 0.005, 0.005, 0.005])  # V
    I1 = np.array([63.67, 29.315, 0.241, 0.063]) / 1000.0  # A
    delta_I1 = np.array([0.18, 0.064, 0.051, 0.005]) / 1000.0  # A

    "Circuit Option 2 Values"
    V2 = np.array([6.386, 6.448, 6.501, 6.501])  # V
    delta_V2 = np.array([0.005, 0.005, 0.005, 0.005])  # V
    I2 = np.array([63.60, 29.322, 0.243, 0.065]) / 1000.0  # A
    delta_I2 = np.array([0.18, 0.064, 0.051, 0.005]) / 1000.0  # A

    # Circuit 1 Analysis: I vs V
    print("\n" + "="*50)
    print("CIRCUIT 1: V vs I ANALYSIS")
    print("="*50)

    # I is independent variable (x), V is dependent variable (y)
    x_circuit1 = I1
    y_circuit1 = V1
    x_unc_circuit1 = delta_I1
    y_unc_circuit1 = delta_V1

    results1 = linear_fitter(x_circuit1, y_circuit1, y_unc_circuit1)
    m1, b1, m_err1, b_err1, y_var1, chi2_1, red_chi2_1, p_value1, residuals1 = results1

    print(f"Slope: {m1:.3f} ± {m_err1:.3f} Ω (Expected: Load Resistance)")
    print(f"Intercept: {b1:.3f} ± {b_err1:.3f} V")
    print(f"Y-variance: {y_var1:.3f}")
    print(f"Chi-squared: {chi2_1:.3f}")
    print(f"Reduced chi-squared: {red_chi2_1:.3f}")
    print(f"p-value: {p_value1:.4f}")
    print(f"y-uncertainties:  {y_unc_circuit1}")

    if abs(red_chi2_1 - 1) < 0.5:
        print("Good fit: reduced chi-squared ≈ 1")
    elif red_chi2_1 > 1:
        print("Potential overestimation of uncertainties or poor fit")
    else:
        print("Potential underestimation of uncertainties or overfitting")

    # Circuit 2 Analysis: I vs V
    print("\n" + "="*50)
    print("CIRCUIT 2: V vs I ANALYSIS")
    print("="*50)

    # I is independent variable (x), V is dependent variable (y)
    x_circuit2 = I2
    y_circuit2 = V2
    x_unc_circuit2 = delta_I2
    y_unc_circuit2 = delta_V2

    results2 = linear_fitter(x_circuit2, y_circuit2, y_unc_circuit2)
    m2, b2, m_err2, b_err2, y_var2, chi2_2, red_chi2_2, p_value2, residuals2 = results2

    print(f"Slope: {m2:.3f} ± {m_err2:.3f} Ω (Expected: Load Resistance)")
    print(f"Intercept: {b2:.3f} ± {b_err2:.3f} V")
    print(f"Y-variance: {y_var2:.3f}")
    print(f"Chi-squared: {chi2_2:.3f}")
    print(f"Reduced chi-squared: {red_chi2_2:.3f}")
    print(f"p-value: {p_value2:.4f}")
    print(f"y-uncertainties:  {y_unc_circuit2}")

    if abs(red_chi2_2 - 1) < 0.5:
        print("Good fit: reduced chi-squared ≈ 1")
    elif red_chi2_2 > 1:
        print("Potential overestimation of uncertainties or poor fit")
    else:
        print("Potential underestimation of uncertainties or overfitting")

    # Plot both circuits
    print("\n" + "="*50)
    print("PLOTTING V vs I")
    print("="*50)

    # Plot Circuit 1
    fig1 = plot_V_vs_I(I1, V1, delta_I1, delta_V1, m1, b1, residuals1, "Circuit 1")
    plt.show()

    # Plot Circuit 2
    fig2 = plot_V_vs_I(I2, V2, delta_I2, delta_V2, m2, b2, residuals2, "Circuit 2")
    plt.show()