import numpy as np


class Integrator:
    def __init__(self, step: float, eps: float=0) -> None:
        self._step = step
        self._eps = eps
        self._first_point_flag = True

    def _runge_kutta_2(self, x: float, v_1: float, v_2: float, step: float) -> np.array:
        c_1_1 = -500.005
        c_1_2 =  499.995
        c_2_1 =  499.995
        c_2_2 = -500.005

        k1_1 = c_1_1 * v_1 + c_1_2 * v_2
        k1_2 = c_2_1 * v_1 + c_2_2 * v_2
        k2_1 = c_1_1 * (v_1 + (step/3) * k1_1) + c_1_2 * (v_2 + (step/3) * k1_2)
        k2_2 = c_2_1 * (v_1 + (step/3) * k1_1) + c_2_2 * (v_2 + (step/3) * k1_2)
        k3_1 = c_1_1 * (v_1 + (2 * step/3) * k2_1) + c_1_2 * (v_2 + (2 * step/3) * k2_2)
        k3_2 = c_2_1 * (v_1 + (2 * step/3) * k2_1) + c_2_2 * (v_2 + (2 * step/3) * k2_2)

        x_next = x + step
        v_1_next = v_1 + (step/4) * (k1_1 + 3 * k3_1)
        v_2_next = v_2 + (step/4) * (k1_2 + 3 * k3_2)

        return np.array([x_next, v_1_next, v_2_next], dtype=np.longdouble)

    def next_point(self, x: float, v_1: float, v_2: float):
        if not self._first_point_flag:
            return self._runge_kutta_2(x, v_1, v_2, self._step)
        else:
            self._first_point_flag = False
            return np.array([x, v_1, v_2], dtype=np.longdouble)

    def next_point_with_step_control(self, x: float, v_1: float, v_2: float):
        if not self._first_point_flag:
            while True:
                old_step = self._step

                x_w, v_1_w, v_2_w  = self._runge_kutta_2(x, v_1, v_2, self._step)  # _w for whole(whole step)
                x_h_1, v_1_h_1, v_2_h_1  = self._runge_kutta_2(x, v_1, v_2, self._step / 2.0)  # _h for half step
                x_h_2, v_1_h_2, v_2_h_2  = self._runge_kutta_2(x_h_1, v_1_h_1, v_2_h_1, self._step / 2.0)

                delta = np.array([v_1_w - v_1_h_2, v_2_w - v_2_h_2], dtype=np.longdouble)
                error = np.linalg.norm(delta)

                if error > self._eps:
                    self._step /= 2.

                else:
                    x = x_w
                    v_1 = v_1_w
                    v_2 = v_2_w

                    if error < self._eps / (2 ** (3 + 1)):
                        self._step *= 2.

                    break
            return np.array([x, v_1, v_2], dtype=np.longdouble)
        else:
            self._first_point_flag = False
            return np.array([x, v_1, v_2], dtype=np.longdouble)
