import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
import pandas as pd

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("OANDA Data Viewer")
        self.setGeometry(100, 100, 800, 600)

        layout = QVBoxLayout()

        self.plot_button = QPushButton("Plot Data")
        self.plot_button.clicked.connect(self.plot_data)
        layout.addWidget(self.plot_button)

        self.graph_widget = QWidget()
        self.graph_layout = QVBoxLayout()
        self.graph_widget.setLayout(self.graph_layout)
        layout.addWidget(self.graph_widget)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def plot_data(self):
        # Fetch data from OANDA (replace this with your actual code to fetch data)
        data = {'Date': pd.date_range(start='2024-01-01', periods=100),
                'Value': pd.Series(range(100))}
        df = pd.DataFrame(data)

        # Plot the data
        fig, ax = plt.subplots()
        ax.plot(df['Date'], df['Value'])
        ax.set_title('OANDA Data')
        ax.set_xlabel('Date')
        ax.set_ylabel('Value')

        # Clear the previous graph layout
        for i in reversed(range(self.graph_layout.count())):
            self.graph_layout.itemAt(i).widget().setParent(None)

        # Add the new graph to the layout
        graph_canvas = FigureCanvas(fig)
        self.graph_layout.addWidget(graph_canvas)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
