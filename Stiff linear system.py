import sys
from math import sqrt
from matplotlib import pyplot as plt
import numpy as np
import pandas as pd 

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

    return np.array([x_next, y_next, u_next], dtype=np.longdouble)


def main() -> None:


    #? Initial conditions:
    x0 = 0
    y0 = 7
    u0 = 13
    xmax = 10

    #! User defined constants
    step = 0.001

    x, y, u = x0, y0, u0

    xs = np.array([], dtype=np.longdouble)
    ys = np.array([], dtype=np.longdouble)
    us = np.array([], dtype=np.longdouble)
    u_1s = np.array([], dtype=np.longdouble)
    u_2s = np.array([], dtype=np.longdouble)

    xs = np.append(xs, [x])
    ys = np.append(ys, [y])
    us = np.append(us, [u])
    u_1s = np.append(u_1s, [y])
    u_2s = np.append(u_2s, [u])

    data = []
    point = {'x_n': x, 'u_1': y, 'u_2': u, 'v_1': y, 'v_2': u, 'E_1': (y - y), 'E_2': (u - u), 'exp(-0,01*x)':np.exp(-x/100), 'exp(-1000*x)':np.exp(-1000*x)}
    data.append(point)

    x, y, u = RK2(x, y, u, step)

    # y -> u_1
    # u -> u_2

    while True:
        x, y, u = RK2(x, y, u, step)

        xs = np.append(xs, [x])
        ys = np.append(ys, [y])
        us = np.append(us, [u])
        u_1s =np.append(u_1s, [u_1])
        u_2s =np.append(u_2s, [u_2])

        if x > xmax:
            break


    fig, axs = plt.subplots(2, 1, figsize=(8, 8))
    plt.subplots_adjust(hspace=0.3)
    title = "Stiff system"
    fig.canvas.set_window_title(title)

    axs[0].plot(xs, ys, label = "v_1")
    axs[0].plot(xs, us, label = "v_2")
    axs[0].legend()
    axs[0].set_xlabel("x")
    axs[0].set_ylabel("v")

    axs[1].plot(xs, u_1s, label = "u_1")
    axs[1].plot(xs, u_2s, label = "u_2")
    axs[1].legend()
    axs[1].set_xlabel("x")
    axs[1].set_ylabel("u")

    df = pd.DataFrame(data)
    #print(df.to_string())

    with open('newfile.txt', 'w') as f:
        f.write(df.to_string())
    
    plt.show()

if __name__ == "__main__":
    main()
