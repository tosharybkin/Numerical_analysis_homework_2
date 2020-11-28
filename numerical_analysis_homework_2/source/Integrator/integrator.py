import numpy as np


class Integrator:
    def __init__(self, step: float) -> None:
        self._step = step
        self._first_point_flag = True

    def _runge_kutta_2(self, x: float, v_1: float, v_2: float) -> np.array:
        c_1_1 = -500.005
        c_1_2 =  499.995
        c_2_1 =  499.995
        c_2_2 = -500.005

        denominator_y = 1 - ((3 + (np.sqrt(3))) / 6) * self._step * (c_1_1 + c_1_2)
        denominator_u = 1 - ((3 + (np.sqrt(3))) / 6) * self._step * (c_2_1 + c_2_2)
        k1_y = (v_1 * c_1_1 + v_2 * c_1_2) / denominator_y
        k1_u = (v_1 * c_2_1 + v_2 * c_2_2) / denominator_u
        k2_y = (
            v_1 * c_1_1
            + v_2 * c_1_2
            + c_1_1 * self._step * (-1) * ((np.sqrt(3)) / 3) * k1_y
            + c_1_2 * self._step * (-1) * ((np.sqrt(3)) / 3) * k1_y
        ) / denominator_y
        k2_u = (
            v_1 * c_2_1
            + v_2 * c_2_2
            + c_2_1 * self._step * (-1) * ((np.sqrt(3)) / 3) * k1_u
            + c_2_2 * self._step * (-1) * ((np.sqrt(3)) / 3) * k1_u
        ) / denominator_u

        x_next = x + self._step
        v_1_next = v_1 + (self._step / 2) * (k1_y + k2_y)
        v_2_next = v_2 + (self._step / 2) * (k1_u + k2_u)

        return np.array([x_next, v_1_next, v_2_next], dtype=np.longdouble)

    def next_point(self, x: float, v_1: float, v_2: float):
        if not self._first_point_flag:
            return self._runge_kutta_2(x, v_1, v_2)
        else:
            self._first_point_flag = False
            return np.array([x, v_1, v_2], dtype=np.longdouble)
