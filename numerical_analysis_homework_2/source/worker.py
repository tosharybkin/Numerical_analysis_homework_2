import sys, traceback
import numpy as np
from PyQt5.QtCore import QRunnable, QObject, pyqtSignal, pyqtSlot
from Integrator.integrator import Integrator


class Points_to_plot:
    def __init__(self, xs, v_1s, v_2s, u_1s, u_2s) -> None:
        self.xs = xs
        self.v_1s = v_1s
        self.v_2s = v_2s
        self.u_1s = u_1s
        self.u_2s = u_2s


class WorkerSignals(QObject):
    '''
    Defines the signals available from a running worker thread.

    Supported signals are:

    finished
        No data

    error
        `tuple` (exctype, value, traceback.format_exc() )

    result
        `object` data returned from processing, anything

    '''
    finished = pyqtSignal(Points_to_plot)
    error = pyqtSignal(tuple)
    progress = pyqtSignal(int)


class Worker(QRunnable):
    '''
    Worker thread

    Inherits from QRunnable to handler worker thread setup, signals and wrap-up.

    :param callback: The function callback to run on this worker thread. Supplied args and
                     kwargs will be passed through to the runner.
    :type callback: function
    :param args: Arguments to pass to the callback function
    :param kwargs: Keywords to pass to the callback function

    '''

    def __init__(self, step: float, x_max: float):
        super(Worker, self).__init__()
        # Store constructor arguments (re-used for processing)
        self.step = step
        self.x_max = x_max
        self.signals = WorkerSignals()

    @pyqtSlot()
    def run(self):
        '''
        Initialise the runner function with passed args, kwargs.
        '''

        step = self.step
        x_max = self.x_max

        xs   = np.array([], dtype=np.longdouble)
        v_1s = np.array([], dtype=np.longdouble)
        v_2s = np.array([], dtype=np.longdouble)
        u_1s = np.array([], dtype=np.longdouble)
        u_2s = np.array([], dtype=np.longdouble)

        x_curr = 0
        v_1 = 7
        v_2 = 13
        u_1 = 7
        u_2 = 13

        integrator = Integrator(step)

        while x_curr < x_max:
            x_curr, v_1, v_2 = integrator.next_point(x_curr, v_1, v_2)
            u_1 = -3 * np.exp(-1000 * x_curr) + 10 * np.exp(-x_curr / 100)
            u_2 = 3 * np.exp(-1000 * x_curr) + 10 * np.exp(-x_curr / 100)

            self.signals.progress.emit(int((x_curr / x_max) * 100))

            xs = np.append(xs, x_curr)
            v_1s = np.append(v_1s, v_1)
            v_2s = np.append(v_2s, v_2)
            u_1s = np.append(u_1s, u_1)
            u_2s = np.append(u_2s, u_2)

        self.signals.finished.emit(Points_to_plot(xs, v_1s, v_2s, u_1s, u_2s))
