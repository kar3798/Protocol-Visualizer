import pyqtgraph as pg
from PyQt5.QtWidgets import QWidget, QVBoxLayout


class WaveformVisualizer(QWidget):
    def __init__(self):
        super().__init__()
        self.text_items = None
        self.plot_curve = None
        self.plot_widget = None
        self.waveform_data = None
        self.init_ui()
        self.current_step = 0  # Track the current step

    def init_ui(self):
        layout = QVBoxLayout()
        self.plot_widget = pg.PlotWidget()
        layout.addWidget(self.plot_widget)
        self.setLayout(layout)

        # Initial empty plot
        self.plot_widget.setTitle("UART Timing Diagram")
        self.plot_widget.setYRange(-0.5, 1.5)
        self.plot_widget.showGrid(x=True, y=True)
        self.plot_curve = self.plot_widget.plot([], [], pen="g")
        self.text_items = []  # To store labels
        self.waveform_data = []

    def update_waveform(self, waveform):
        """
        Updates the plot with the full waveform data.
        """
        self.waveform_data = waveform
        self.current_step = 0  # Reset step counter
        self.plot_complete_waveform()

    def plot_complete_waveform(self):
        """
        Draw the complete waveform immediately.
        """
        x_values = list(range(len(self.waveform_data)))
        y_values = [item[1] for item in self.waveform_data]

        self.plot_curve.setData(x_values, y_values)
        self.add_waveform_labels()

    def step_waveform(self, waveform):
        """
        Draw the waveform one step at a time.
        """
        if self.current_step >= len(waveform):
            return  # No more steps to draw

        if self.current_step == 0:
            self.clear_waveform()

        # Draw up to the current step
        x_values = list(range(self.current_step + 1))
        y_values = [waveform[i][1] for i in x_values]
        self.plot_curve.setData(x_values, y_values)

        # Add label for the current step
        label_text, _, label_color = waveform[self.current_step]
        text_item = pg.TextItem(label_text, color=label_color, anchor=(0.5, 1.5))
        text_item.setPos(self.current_step, waveform[self.current_step][1] + 0.2)
        self.plot_widget.addItem(text_item)
        self.text_items.append(text_item)

        # Move to the next step
        self.current_step += 1

    def clear_waveform(self):
        """
        Clears the waveform from the screen.
        """
        self.plot_curve.setData([], [])
        for text_item in self.text_items:
            self.plot_widget.removeItem(text_item)
        self.text_items.clear()
        self.current_step = 0

    def add_waveform_labels(self):
        """
        Adds labels for the waveform data (Start, Data, Stop Bits).
        """
        # Clear previous labels
        for text_item in self.text_items:
            self.plot_widget.removeItem(text_item)
        self.text_items.clear()

        # Add label for each segment
        for i, (label, value, color) in enumerate(self.waveform_data):
            text_item = pg.TextItem(label, color=color, anchor=(0.5, 1.5))
            text_item.setPos(i, value + 0.2)
            self.text_items.append(text_item)
            self.plot_widget.addItem(text_item)

    def add_combined_labels(self, binary_value):
        """
        Adds combined labels for Start, Data (LSB to MSB), and Stop.
        :param binary_value: The binary string (8 bits) to be labeled.
        """
        # Clear any previous labels
        for text_item in self.text_items:
            self.plot_widget.removeItem(text_item)
        self.text_items.clear()

        # Add Start Bit Label
        start_text = pg.TextItem("Start", color="green", anchor=(0.5, 1.5))
        start_text.setPos(0, 1)
        self.plot_widget.addItem(start_text)
        self.text_items.append(start_text)

        # Reversing the Bit Order
        reversed_bits = binary_value[::-1]

        # Add Data Bit Labels (LSB to MSB)
        for i, bit in enumerate(reversed_bits):
            color = "cyan" if i == 0 else "magenta" if i == 7 else "yellow"
            label = "LSB" if i == 0 else "MSB" if i == 7 else f"Bit {i + 1}"
            text = f"{label}: {bit}"

            text_item = pg.TextItem(text, color=color, anchor=(0.5, 1.5))
            text_item.setPos(i + 1, 1)  # Slightly above the waveform
            self.plot_widget.addItem(text_item)
            self.text_items.append(text_item)

        # Add Stop Bit Label
        stop_text = pg.TextItem("Stop", color="red", anchor=(0.5, 1.5))
        stop_text.setPos(len(binary_value) + 1, 1)
        self.plot_widget.addItem(stop_text)
        self.text_items.append(stop_text)

