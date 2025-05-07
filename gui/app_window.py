from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QComboBox, QLineEdit, QTextEdit
)
from PyQt5.QtCore import Qt
from protocols.uart import UARTSimulator
from gui.visualizer import WaveformVisualizer

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Protocol Visualizer")
        self.setGeometry(100, 100, 800, 600)
        self.uart_simulator = UARTSimulator()

        # Main layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout()
        central_widget.setLayout(layout)

        # Protocol selector and input
        protocol_layout = QHBoxLayout()
        self.protocol_combo = QComboBox()
        self.protocol_combo.addItems(["UART"])
        self.data_input = QLineEdit("0x41")
        self.format_combo = QComboBox()
        self.format_combo.addItems(["Hex", "Binary", "Decimal"])

        self.send_button = QPushButton("Send")
        self.step_button = QPushButton("Step")
        self.clear_button = QPushButton("Clear")

        protocol_layout.addWidget(QLabel("Protocol:"))
        protocol_layout.addWidget(self.protocol_combo)
        protocol_layout.addWidget(QLabel("Data:"))
        protocol_layout.addWidget(self.data_input)
        protocol_layout.addWidget(self.format_combo)
        protocol_layout.addWidget(self.send_button)
        protocol_layout.addWidget(self.step_button)
        protocol_layout.addWidget(self.clear_button)

        layout.addLayout(protocol_layout)

        # Waveform Visualizer
        self.visualizer = WaveformVisualizer()
        layout.addWidget(self.visualizer)

        # Explanation
        self.explanation = QLabel("Explanation will appear here.")
        layout.addWidget(self.explanation)

        # Log view
        self.log_view = QTextEdit()
        self.log_view.setReadOnly(True)
        layout.addWidget(QLabel("Log:"))
        layout.addWidget(self.log_view)

        # Connect button events
        self.send_button.clicked.connect(self.send_data)
        self.step_button.clicked.connect(self.step_data)
        self.clear_button.clicked.connect(self.clear_waveform)

    def send_data(self):
        data = self.data_input.text()
        format_type = self.format_combo.currentText()

        # Convert data based on format
        if format_type == "Hex":
            data = int(data, 16)
        elif format_type == "Binary":
            data = int(data, 2)
        elif format_type == "Decimal":
            data = int(data)

        # Validate data range (0-255)
        if not (0 <= data <= 255):
            self.log_view.append("Error: Data must be between 0 and 255.")
            return

        self.waveform_data = self.uart_simulator.generate_uart_waveform(data)
        self.visualizer.update_waveform(self.waveform_data)

        # Add Combined Labels (Start, LSB, MSB, Stop)
        self.visualizer.add_combined_labels(binary_value=bin(data)[2:].zfill(8))
        self.update_explanation(data)

    def step_data(self):
        if hasattr(self, 'waveform_data'):
            self.visualizer.step_waveform(self.waveform_data)

    def clear_waveform(self):
        self.visualizer.clear_waveform()
        self.log_view.clear()
        self.explanation.setText("Explanation will appear here.")

    def update_explanation(self, data):
        binary_value = bin(data)[2:].zfill(8)
        self.explanation.setText(
            f"Explanation:\n"
            f"Start Bit: The signal goes LOW to begin transmission.\n"
            f"Data Bits: Represent the binary value of the data ({hex(data)}) -> {binary_value}.\n"
            f"Stop Bit: The signal returns to HIGH (Idle)."
        )
