import sys, os
import numpy as np
from PyQt5 import QtGui, QtWidgets, QtCore, uic
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from Integrator.integrator import Integrator
from worker import Worker

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
        self.threadpool = QtCore.QThreadPool()

        self.plot_btn.clicked.connect(self.on_plot_btn_click)

    def update_progress_bar(self, value):
        self.progress_bar.setValue(value)

    def thread_complete(self, points_to_plot):
        self.plot.canvas.axes[0].clear()
        self.plot.canvas.axes[0].plot(points_to_plot.xs, points_to_plot.v_1s)
        self.plot.canvas.axes[0].plot(points_to_plot.xs, points_to_plot.v_2s)
        self.plot.canvas.axes[1].clear()
        self.plot.canvas.axes[1].plot(points_to_plot.xs, points_to_plot.u_1s)
        self.plot.canvas.axes[1].plot(points_to_plot.xs, points_to_plot.u_2s)

        self.plot.canvas.draw()

    def on_plot_btn_click(self) -> None:
        step = float(self.step_text_box.text())
        x_max = float(self.x_max_text_box.text())
        worker = Worker(step, x_max)
        worker.signals.finished.connect(self.thread_complete)
        worker.signals.progress.connect(self.update_progress_bar)

        self.threadpool.start(worker)


def main() -> None:
    app = QtWidgets.QApplication(sys.argv)
    window = Main_window()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
