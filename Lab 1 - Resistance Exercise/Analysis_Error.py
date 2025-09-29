from Error_Propagation import multiplication, addition
import numpy as np

def calculate_uncertainty_R1(R_V, m1, dR_V, dm1):

    #calculate m1xrv
    mult1 = m1*R_V

    mult1_error = multiplication(
        x = m1, delta_x = dm1, 
        y = R_V, delta_y = dR_V,
        w = ones_array, delta_w = zeros_array

        z = mult1
    )

    sub2 = R_V - m1

    sub2_error = addition(
        delta_x = dm1,
        delta_y = dR_V
        delta_w = zeros_array
    )

    div3 = mult1 / sub2

    div3_error = multiplication(
        x = mult1, delta_x = mult1_error, 
        y = sub2, delta_y = sub2_error,
        w = ones_array, delta_w = zeros_array,

        z = div3
    )

    return div3, div3_error

def calculate_uncertainty_R2(R_A, dR_A, m2, dm2):

    mult1 = m2*R_A
    
    mult1_error = multiplication(
        x = m2, delta_x = dm2, 
        y = R_A, delta_y = dR_A, 
        w = ones_array, delta_w = zeros_array, 

        z = mult1
    )

    sub2 = R_A - m2

    sub2_error = addition(
        delta_x = dR_A, 
        delta_y = dm2, 
        delta_w = zeros_array
    )

    div3 = mult1/sub2

    div3_error = multiplication(
        x = mult1, delta_x = mult1_error, 
        y = sub2, delta_y = sub2_error, 
        w = ones_array, delta_w = zeros_array
    )

    return div3, div3_error

if __name__ == "__main__":
    R_V = 6.31*(10**6)
    m1 = -0.046
    dR_V = 4.62*(10**8)
    dm1 = 0.004
    R_A = 446.3
    dR_A = 3475.9
    m2 = -1.813
    dm2 = 0.003
    calculate_uncertainty_R1(R_V, m1, dR_V, dm1)
    calculate_uncertainty_R2(R_A, dR_A, m2, dm2)
    