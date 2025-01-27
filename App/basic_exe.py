# File: weather_risk_app.py

import sys
import pandas as pd
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QLabel, QLineEdit, QFileDialog, QVBoxLayout, QWidget, QMessageBox
)
from matplotlib.backends.backend_qt5agg import (
    FigureCanvasQTAgg as FigureCanvas
)
from matplotlib.figure import Figure


class WeatherRiskApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Set up the main window
        self.setWindowTitle("Weather Risk App")
        self.setGeometry(100, 100, 800, 600)

        # Main layout
        layout = QVBoxLayout()

        # Add a button to load the CSV file
        self.load_button = QPushButton("Load CSV File")
        self.load_button.clicked.connect(self.load_csv)
        layout.addWidget(self.load_button)

        # Input field for code_commune
        self.code_label = QLabel("Enter code_commune:")
        layout.addWidget(self.code_label)
        self.code_input = QLineEdit()
        layout.addWidget(self.code_input)

        # Search button
        self.search_button = QPushButton("Search and Plot")
        self.search_button.clicked.connect(self.search_and_plot)
        layout.addWidget(self.search_button)

        # Matplotlib canvas for plotting
        self.canvas = FigureCanvas(Figure(figsize=(8, 6)))
        layout.addWidget(self.canvas)
        self.ax = self.canvas.figure.add_subplot(111)

        # Set central widget
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        # Initialize variables
        self.df = None

    def load_csv(self):
        # Open a file dialog to select the CSV file
        file_name, _ = QFileDialog.getOpenFileName(self, "Open CSV File", "", "CSV Files (*.csv)")
        if file_name:
            try:
                self.df = pd.read_csv(file_name)
                QMessageBox.information(self, "Success", "CSV file loaded successfully!")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to load CSV: {e}")

    def search_and_plot(self):
        # Check if the CSV file is loaded
        if self.df is None:
            QMessageBox.warning(self, "Warning", "Please load a CSV file first.")
            return

        # Get the code_commune from input
        code_commune = self.code_input.text()
        if not code_commune:
            QMessageBox.warning(self, "Warning", "Please enter a code_commune.")
            return

        # Filter the data for the given code_commune
        filtered_data = self.df[self.df['code_commune'] == int(code_commune)]

        if filtered_data.empty:
            QMessageBox.warning(self, "Warning", f"No data found for code_commune: {code_commune}")
            return

        # Clear the previous plot
        self.ax.clear()

        # Ensure datetime is in proper format
        filtered_data['datetime'] = pd.to_datetime(filtered_data['datetime'])
        filtered_data = filtered_data.sort_values('datetime')

        # Plot the requested columns
        self.ax.plot(filtered_data['datetime'], filtered_data['rain_24'], label="Rain (24h)", marker='o', color='blue')
        self.ax.plot(filtered_data['datetime'], filtered_data['average_celsius'], label="Avg Temp (°C)", marker='s', color='red')
        self.ax.plot(filtered_data['datetime'], filtered_data['average_wind'], label="Avg Wind (km/h)", marker='^', color='green')
        self.ax.plot(filtered_data['datetime'], filtered_data['risk_level'], label="Risk Level", marker='d', color='orange')

        # Format the plot
        self.ax.set_title(f"Weather Data Over Time for {code_commune}")
        self.ax.set_xlabel("Datetime")
        self.ax.set_ylabel("Values")
        self.ax.legend()
        self.ax.grid(True)
        self.canvas.draw()


def main():
    app = QApplication(sys.argv)
    window = WeatherRiskApp()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
