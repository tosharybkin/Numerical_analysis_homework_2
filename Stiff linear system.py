import sys
from math import sqrt
import numpy as np
from matplotlib import pyplot as plt

C1_1 = -500.005
C1_2 = 499.995
C2_1 = 499.995
C2_2 = -500.005


def RK2(x, y, u, step) -> np.array:

    denominator_y = 1 - ((3 + (sqrt(3)))/6) * step * (C1_1 + C1_2)
    denominator_u = 1 - ((3 + (sqrt(3)))/6) * step * (C2_1 + C2_2)
    k1_y = (y * C1_1 + u * C1_2)/denominator_y 
    k1_u = (y * C2_1 + u * C2_2)/denominator_u
    k2_y = (y * C1_1 + u * C1_2 + C1_1 * step * (-1) * ((sqrt(3))/3) * k1_y + C1_2 * step * (-1) * ((sqrt(3))/3) * k1_y )/denominator_y 
    k2_u = (y * C2_1 + u * C2_2 + C2_1 * step * (-1) * ((sqrt(3))/3) * k1_u + C2_2 * step * (-1) * ((sqrt(3))/3) * k1_u )/denominator_u

    x_next = x + step
    y_next = y + (step/2) * (k1_y + k2_y)
    u_next = u + (step/2) * (k1_u + k2_u)

    return np.array([x_next, y_next, u_next])


def main() -> None:

    #? Initial conditions:
    x0 = 0
    y0 = 7
    u0 = 13
    xmax = 100

    #! User defined constants
    step = 0.001

    x, y, u = x0, y0, u0
    xs = np.array([])
    ys = np.array([])
    us = np.array([])


    while True:
        
        x, y, u = RK2(x, y, u, step)
                
        xs = np.append(xs, [x])
        ys = np.append(ys, [y])
        us = np.append(us, [u])

        if x > xmax:
            break


    plt.plot(xs, ys, xs, us)

    plt.show()


if __name__ == "__main__":
    main()
