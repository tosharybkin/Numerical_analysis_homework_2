import sys, os
import numpy as np
from PyQt5 import QtGui, QtWidgets, QtCore, uic
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QPalette, QColor
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
        pixmap = QPixmap(
            os.path.abspath(os.path.join(script_dir, os.pardir))  # Parent directory
            + os.path.sep
            + "resources"
            + os.path.sep
            + "system.png"
        )

        #pixmap = pixmap.scaled(400, 400, aspectRatioMode=QtCore.Qt.KeepAspectRatio)
        self.system_label.setPixmap(pixmap)
        self.system_label.setMask(pixmap.mask())
        self.threadpool = QtCore.QThreadPool()
        self.row_index = 0
        self.max_delta_u_v = 0

        self.plot_btn.clicked.connect(self.on_plot_btn_click)

    def update_progress_bar(self, value):
        self.progress_bar.setValue(value)

    def insert_table_row(self, row_index, row):
        self.table.insertRow(row_index)
        self.row_index = row_index

        for index, item in enumerate(row):
            self.table.setItem(row_index, index, QtWidgets.QTableWidgetItem(
                f"{item:.6e}"))

        if (delta_u_v := max(row[5], row[6])) > self.max_delta_u_v:
            self.max_delta_u_v = delta_u_v

    def thread_complete(self, points_to_plot):
        self.plot.canvas.axes[0].clear()
        self.plot.canvas.axes[0].plot(points_to_plot.xs, points_to_plot.v_1s, 'r')
        self.plot.canvas.axes[0].plot(points_to_plot.xs, points_to_plot.v_2s, 'g')
        self.plot.canvas.axes[0].legend(('v_1(x)', 'v_2(x)'),loc='upper right')
        self.plot.canvas.axes[0].set_title('Численное решение')
        self.plot.canvas.axes[0].set_xlabel("x")
        self.plot.canvas.axes[0].set_ylabel("v_1(x)/v_2(x)")

        self.plot.canvas.axes[1].clear()
        self.plot.canvas.axes[1].plot(points_to_plot.xs, points_to_plot.u_1s, 'r')
        self.plot.canvas.axes[1].plot(points_to_plot.xs, points_to_plot.u_2s, 'g')
        self.plot.canvas.axes[1].legend(('u_1(x)', 'u_2(x)'),loc='upper right')
        self.plot.canvas.axes[1].set_title('Истинное решение')
        self.plot.canvas.axes[1].set_xlabel("x")
        self.plot.canvas.axes[1].set_ylabel("u_1(x)/u_2(x)")

        self.plot.canvas.draw()

        self.max_delta_u_v_lbl.setText(f"{self.max_delta_u_v:.6e}")
        self.table.setVerticalHeaderLabels((str(i) for i in range(self.row_index + 1)))

    def on_plot_btn_click(self) -> None:

        self.max_delta_u_v = 0

        # Clear output table
        while (self.table.rowCount() > 0):
                self.table.removeRow(0)

        step = float(self.step_text_box.text())
        x_max = float(self.x_max_text_box.text())
        eps = float(self.eps_text_box.text())
        step_control_flag = self.step_control_check_box.isChecked()

        worker = Worker(step, x_max, eps, step_control_flag)
        worker.signals.finished.connect(self.thread_complete)
        worker.signals.progress.connect(self.update_progress_bar)
        worker.signals.insert_table_row.connect(self.insert_table_row)

        self.threadpool.start(worker)


def main() -> None:
    app = QtWidgets.QApplication(sys.argv)

    # Force the style to be the same on all OSs:
    app.setStyle("Fusion")

    # Now use a palette to switch to dark colors:
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor(53, 53, 53))
    palette.setColor(QPalette.WindowText, Qt.white)
    palette.setColor(QPalette.Base, QColor(25, 25, 25))
    palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
    palette.setColor(QPalette.ToolTipBase, Qt.black)
    palette.setColor(QPalette.ToolTipText, Qt.white)
    palette.setColor(QPalette.Text, Qt.white)
    palette.setColor(QPalette.Button, QColor(53, 53, 53))
    palette.setColor(QPalette.ButtonText, Qt.white)
    palette.setColor(QPalette.BrightText, Qt.red)
    palette.setColor(QPalette.Link, QColor(42, 130, 218))
    palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
    palette.setColor(QPalette.HighlightedText, Qt.black)
    app.setPalette(palette)

    window = Main_window()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
