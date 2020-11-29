import sys, os
import numpy as np
from PyQt5 import QtGui, QtWidgets, uic
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from Integrator.integrator import Integrator


class Main_window(QtWidgets.QMainWindow):
    def __init__(self) -> None:
        super(Main_window, self).__init__()
        script_dir = os.path.dirname(os.path.realpath(__file__))
        uic.loadUi(
            os.path.abspath(os.path.join(script_dir, os.pardir))  # Parent directory
            + os.path.sep
            + "resources"
            + os.path.sep
            + "main_window.ui",
            self,
        )
        self.addToolBar(NavigationToolbar(self.plot.canvas, self))
        self.setWindowIcon(QtGui.QIcon(
            os.path.abspath(os.path.join(script_dir, os.pardir))  # Parent directory
            + os.path.sep
            + "resources"
            + os.path.sep
            + "icon.png"))
        self.progress_bar.setValue(0)

        self.plot_btn.clicked.connect(self.on_plot_btn_click)

    def on_plot_btn_click(self) -> None:
        step = float(self.step_text_box.text())
        x_max = float(self.x_max_text_box.text())

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

            self.progress_bar.setValue(int((x_curr / x_max) * 100))

            xs = np.append(xs, x_curr)
            v_1s = np.append(v_1s, v_1)
            v_2s = np.append(v_2s, v_2)
            u_1s = np.append(u_1s, u_1)
            u_2s = np.append(u_2s, u_2)

        self.plot.canvas.axes[0].clear()
        self.plot.canvas.axes[0].plot(xs, v_1s)
        self.plot.canvas.axes[0].plot(xs, v_2s)
        self.plot.canvas.axes[1].clear()
        self.plot.canvas.axes[1].plot(xs, u_1s)
        self.plot.canvas.axes[1].plot(xs, u_2s)


        self.plot.canvas.draw()





def main() -> None:
    app = QtWidgets.QApplication(sys.argv)
    window = Main_window()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
