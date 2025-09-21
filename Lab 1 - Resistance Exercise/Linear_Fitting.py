import matplotlib.pyplot as plt
import numpy as np
import scipy as scp
import math

def linear_fitter(x_inputs, x_uncertainties, y_inputs, y_uncertainties):
    """
    Function Description:
    Performs linear regression with chi-squared analysis on x-y data pairs to find
    the best-fit line y = mx + b and calculates associated statistics.
    
    Parameters:
    x_inputs (array_like): Array of x-values (independent variable).
    x_uncertainties (array_like): Array of uncertainties in x-values.
    y_inputs (array_like): Array of y-values (dependent variable).
    y_uncertainties (array_like): Array of uncertainties in y-values.
    
    Returns:
    tuple: A tuple containing (m, b, m_stdrd_dev, b_stdrd_dev, coefficient_determination, 
            y_variance, chi_squared, reduced_chi_squared, p_value)
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
    
    # Calculate coefficient of determination (R²)
    y_mean = np.mean(y_inputs)
    total_variance = np.sum((y_inputs - y_mean)**2)
    residual_variance = np.sum(residuals**2)
    coefficient_determination = 1 - (residual_variance / total_variance)
    
    # CHI-SQUARED CALCULATION
    # Calculate chi-squared
    chi_squared = np.sum(((y_inputs - y_pred) / y_uncertainties)**2)
    
    # Calculate reduced chi-squared (chi-squared per degree of freedom)
    degrees_of_freedom = N - 2  # 2 parameters (m and b)
    reduced_chi_squared = chi_squared / degrees_of_freedom
    
    # Calculate p-value (probability that chi-squared could be this large by chance)
    try:
        from scp.stats import chi2
        p_value = 1 - chi2.cdf(chi_squared, degrees_of_freedom)
    except ImportError:
        # Fallback approximation if scipy is not available
        p_value = np.exp(-chi_squared / 2)  # Rough approximation
    
    return (m, b, m_stdrd_dev, b_stdrd_dev, coefficient_determination, 
            y_variance, chi_squared, reduced_chi_squared, p_value)

def chi_squared_goodness_of_fit(observed, expected, uncertainties):
    """
    Function Description:
    Calculates chi-squared goodness of fit between observed and expected values.
    
    Parameters:
    observed (array_like): Observed data values.
    expected (array_like): Expected/theoretical values.
    uncertainties (array_like): Uncertainties in observed values.
    
    Returns:
    tuple: (chi_squared, reduced_chi_squared, p_value, degrees_of_freedom)
    """
    chi_squared = np.sum(((observed - expected) / uncertainties)**2)
    degrees_of_freedom = len(observed) - 1  # Adjust based on constraints
    reduced_chi_squared = chi_squared / degrees_of_freedom
    
    try:
        from scp.stats import chi2
        p_value = 1 - chi2.cdf(chi_squared, degrees_of_freedom)
    except ImportError:
        p_value = np.exp(-chi_squared / 2)
    
    return chi_squared, reduced_chi_squared, p_value, degrees_of_freedom

def run_linear_fit():
    x = np.array([1, 2, 3, 4, 5])
    y = np.array([2.1, 3.9, 6.2, 8.1, 9.8])
    x_unc = np.array([0.1, 0.1, 0.1, 0.1, 0.1])
    y_unc = np.array([0.2, 0.2, 0.2, 0.2, 0.2])
    
    # Run the fitter
    results = linear_fitter(x, x_unc, y, y_unc)
    m, b, m_err, b_err, r2, y_var, chi2, red_chi2, p_value = results
    
    print(f"Slope: {m:.3f} ± {m_err:.3f}")
    print(f"Intercept: {b:.3f} ± {b_err:.3f}")
    print(f"R²: {r2:.4f}")
    print(f"Chi-squared: {chi2:.3f}")
    print(f"Reduced chi-squared: {red_chi2:.3f}")
    print(f"p-value: {p_value:.4f}")
    
    # Interpretation of reduced chi-squared
    if abs(red_chi2 - 1) < 0.5:
        print("Good fit: reduced chi-squared ≈ 1")
    elif red_chi2 > 1:
        print("Potential overestimation of uncertainties or poor fit")
    else:
        print("Potential underestimation of uncertainties or overfitting")

if __name__ == "__main__":
    run_linear_fit()