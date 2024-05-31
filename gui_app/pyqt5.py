import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
import pandas as pd


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Pandas Graph in PyQt")
        self.setGeometry(100, 100, 800, 600)

        layout = QVBoxLayout()
        self.central_widget = QWidget()
        self.central_widget.setLayout(layout)
        self.setCentralWidget(self.central_widget)

        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)

        # Create some sample data using pandas
        data = {'x': range(10), 'y': range(10, 0, -1)}
        self.df = pd.DataFrame(data)

        # Plot the data
        self.plot_data()

        # Label to display clicked point values
        self.label = QLabel(self)
        layout.addWidget(self.label)

        # Connect the mouse click event
        self.canvas.mpl_connect('button_press_event', self.on_click)

    def plot_data(self):
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        self.df.plot(x='x', y='y', ax=ax)
        ax.set_title('Pandas Plot in PyQt')
        ax.set_xlabel('X Axis')
        ax.set_ylabel('Y Axis')
        self.canvas.draw()

    def on_click(self, event):
        if event.inaxes:
            x = int(round(event.xdata))
            y = int(round(event.ydata))
            self.label.setText(f'Clicked point: ({x}, {y})')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
