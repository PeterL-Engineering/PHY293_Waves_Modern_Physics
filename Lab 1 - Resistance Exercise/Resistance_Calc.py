from Error_Propagation import multiplication, addition
import numpy as np

def calculate_uncertainty_R_A(V, I, dV, dI, dR_li):

    # Calculate term1 = V/I
    term1 = V / I
    
    # Uncertainty for V/I using multiplication function (division case)
    # For division V/I: we treat it as V * (1/I)
    # We need arrays of ones for the constant term (1) with zero uncertainty
    ones_array = np.ones_like(V)  # Array of ones with same length as V
    zeros_array = np.zeros_like(V)  # Array of zeros with same length as V

    term1_error = multiplication(
        x=V, delta_x=dV,
        y=I, delta_y=dI, 
        w=ones_array, delta_w=zeros_array,  # No third variable
        z=term1
    )
    
    # Uncertainty for the subtraction: R_A = term1 - R_li
    # For subtraction: δR_A = sqrt((δterm1)² + (δR_li)²)
    uncertainty = addition(term1_error, dR_li, zeros_array)
    
    return uncertainty

def calculate_uncertainty_R_V(V, I, R_li, dV, dI, dR_li):

    # Calculate components
    N = V * R_li  # Numerator value
    D1 = I * R_li  # First Denominator value  
    D = D1 - V     # Final Denominator
    Quotient = N / D  # Final R_V value
    
    # We need arrays of ones for the constant term (1) with zero uncertainty
    ones_array = np.ones_like(V)  # Array of ones with same length as V
    zeros_array = np.zeros_like(V)  # Array of zeros with same length as V

    # Uncertainty for numerator N = V * R_li
    dN = multiplication(
        x=V, delta_x=dV,
        y=R_li, delta_y=dR_li,
        w=ones_array, delta_w=zeros_array,
        z=N
    )
    
    # Uncertainty for D1 = I * R_li
    dD1 = multiplication(
        x=I, delta_x=dI, 
        y=R_li, delta_y=dR_li,
        w=ones_array, delta_w=zeros_array,
        z=D1
    )
    
    # Uncertainty for denominator D = D1 - V
    dD = addition(
        delta_x=dD1,
        delta_y=dV, 
        delta_w=zeros_array
    )
    
    # Uncertainty for quotient R_V = N / D
    uncertainty = multiplication(
        x=N, delta_x=dN,
        y=D, delta_y=dD, 
        w=ones_array, delta_w=zeros_array,
        z=Quotient
    )
    
    return uncertainty

if __name__ == "__main__":
    "Circuit Option 1 Values"

    # All values in base SI units (Ohms, Volts, Amperes)
    R_li = np.array([100.32, 219.91, 26814.0, 101570.0])  # Ω
    delta_R_li = np.array([0.25, 0.49, 59.0, 250.0])  # Ω

    V1 = np.array([6.501, 6.501, 6.501, 6.501])  # V
    delta_V1 = np.array([0.005, 0.005, 0.005, 0.005])  # V

    # Convert mA to A
    I1 = np.array([63.67, 29.315, 0.241, 0.063]) / 1000.0  # A
    delta_I1 = np.array([0.18, 0.064, 0.051, 0.005]) / 1000.0  # A

    "Circuit Option 2 Values"

    V2 = np.array([6.386, 6.448, 6.501, 6.501])  # V
    delta_V2 = np.array([0.005, 0.005, 0.005, 0.005])  # V

    # Convert mA to A
    I2 = np.array([63.60, 29.322, 0.243, 0.065]) / 1000.0  # A
    delta_I2 = np.array([0.18, 0.064, 0.051, 0.005]) / 1000.0  # A

    R_A = (V1 / I1) - R_li
    R_V = (V2 * R_li) / (I2 * R_li - V2)

    # print("Ammeter Resistances R_A (Ω):")
    # print(R_A)
    # print("\nVoltmeter Resistances R_V (Ω):")
    # print(R_V)

    # Calculate averages (excluding any unrealistic values)
    R_A_avg = np.mean(R_A)
    R_V_avg = np.mean(R_V)

    # print(f"\nAverage R_A: {R_A_avg:.1f} Ω")
    # print(f"Average R_V: {R_V_avg:.1f} Ω")

    dR_A = calculate_uncertainty_R_A(V1, I1, delta_V1, delta_I1, delta_R_li)
    dR_V = calculate_uncertainty_R_V(V2, I2, R_li, delta_V2, delta_I2, delta_R_li) 

    print("Ammeter Resistances Uncertaintiy dR_A (Ω):")
    print(dR_A)
    print("\nVoltmeter Resistances Uncertainty dR_V (Ω):")
    print(dR_V)

    dR_A_avg = np.average(dR_A)
    dR_V_avg = np.average(dR_V)

    print(f"\nAverage dR_A: {dR_A_avg:.1f} Ω")
    print(f"Average dR_V: {dR_V_avg:.1f} Ω")



