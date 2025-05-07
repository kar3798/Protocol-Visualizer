class UARTSimulator:
    def __init__(self):
        self.baud_rate = 9600  # Can be adjusted later

    def generate_uart_waveform(self, data: int):
        """
        Generates UART waveform data (start, data bits, stop).
        :param data: Integer value of the data byte (0-255)
        :return: List of tuples [(label, value, color)]
        """
        if not (0 <= data <= 255):
            raise ValueError("Data must be an integer between 0 and 255.")

        waveform = []

        # Start Bit (Low) - Green
        waveform.append(("Start", 0, "green"))

        # Data Bits (8 bits, LSB first) - Yellow
        for i in range(8):
            bit = (data >> i) & 1
            waveform.append((f"Data {i+1}", bit, "yellow"))

        # Stop Bit (High) - Red
        waveform.append(("Stop", 1, "red"))

        return waveform
