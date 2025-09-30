from Error_Propagation import multiplication, addition
import numpy as np

def calculate_uncertainty_R1(R_V, m1, dR_V, dm1):
    # Calculate m1 * R_V
    mult1 = m1 * R_V
    
    mult1_error = multiplication(
        x = m1, delta_x = dm1, 
        y = R_V, delta_y = dR_V,
        w = np.ones_like(m1), delta_w = np.zeros_like(m1),
        z = mult1
    )
    
    # Calculate R_V - m1
    sub2 = R_V - m1
    
    sub2_error = addition(
        delta_x = dR_V,
        delta_y = dm1,
        delta_w = np.zeros_like(m1)
    )
    
    # Calculate (m1 * R_V) / (R_V - m1)
    div3 = mult1 / sub2
    
    div3_error = multiplication(
        x = mult1, delta_x = mult1_error, 
        y = sub2, delta_y = sub2_error,
        w = np.ones_like(m1), delta_w = np.zeros_like(m1),
        z = div3
    )
    
    return div3, div3_error

def calculate_uncertainty_R2(R_A, dR_A, m2, dm2):
    # Calculate m2 + R_A
    R2_error = addition(
        delta_x = dR_A,
        delta_y = dm2,
        delta_w = np.zeros_like(m1)
    )

    R2 = - (m2 + R_A)

    return R2, R2_error

if __name__ == "__main__":
    R_V = 6.31*(10**6)
    m1 = -0.046
    dR_V = 4.62*(10**8)
    dm1 = 0.004
    R_A = 446.3
    dR_A = 3475.9
    m2 = -1.813
    dm2 = 0.003
    
    print("=== R1 Calculation ===")
    R1, R1_error = calculate_uncertainty_R1(R_V, m1, dR_V, dm1)
    print(f"Final R1 = {R1:.4e} ± {R1_error:.4e}")
    print()
    
    print("=== R2 Calculation ===")
    R2, R2_error = calculate_uncertainty_R2(R_A, dR_A, m2, dm2)
    print(f"Final R2 = {R2:.4e} ± {R2_error:.4e}")
    