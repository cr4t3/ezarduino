# Arduino-Py

`arduino-py` is a Python library designed to simplify the connection between Python and Arduino devices through serial communication. It provides a Python-based reconstruction of Arduino's Serial class, making it easier to send and receive data between your Python scripts and Arduino projects.

---

## Features

- Easy-to-use class for managing Arduino devices over serial ports.
- Core functionality mirroring Arduino's `Serial` class.
- Support for:
  - Reading bytes and strings from Arduino.
  - Writing data to Arduino.
  - Checking available bytes and write readiness.
- Built-in support for encoding (default: UTF-8).

---

## Installation

### From GitHub
For now, you can clone the repository and install the library locally:

```bash
$ git clone https://github.com/your-repo/arduino-py.git
$ cd arduino-py
$ pip install .
```

### PyPI (Coming Soon)
Once published, you can install `arduino-py` via PyPI:

```bash
$ pip install arduino-py
```

---

## Usage

Here is a quick example to demonstrate the basic functionality of `arduino-py`:

### Example: Sending and Receiving Data
```python
from arduino_py import ArduinoDevice

# Connect to Arduino (adjust COM port and baud rate as necessary)
arduino = ArduinoDevice(com="COM3", baud_rate=9600)

# Send data to Arduino
arduino.printLn("Hello, Arduino!")

# Read data from Arduino
try:
    while arduino.available():
        print("Received:", arduino.readString())
except IndexError:
    print("No data available to read.")

# Close connection
arduino.end()
```

---

## API Reference

### `ArduinoDevice`
#### Initialization
```python
ArduinoDevice(com: str, baud_rate: int = 9600, timeout: int = 1, encoding: str = "utf-8")
```
- **com**: Serial port of the Arduino device (e.g., `"COM3"` or `"/dev/ttyUSB0"`).
- **baud_rate**: Communication speed (default: `9600`).
- **timeout**: Time in seconds to wait for a response (default: `1`).
- **encoding**: Encoding used for string communication (default: `UTF-8`).

#### Methods
- **`end()`**: Closes the serial connection.
- **`available()`**: Returns the number of bytes available for reading.
- **`availableForWriting()`**: Returns the number of bytes that can be written.
- **`readBytes(buffer: list, length: int)`**: Reads `length` bytes into a given buffer.
- **`read()`**: Reads a single byte.
- **`readString()`**: Reads a string from the Arduino (until a newline is received).
- **`print(text: str)`**: Sends a string to the Arduino.
- **`printLn(text: str)`**: Sends a string followed by a newline character.

---

## Contributing
We welcome contributions! If you would like to contribute to `arduino-py`, please follow these steps:

1. Fork the repository.
2. Create a new branch for your feature or bugfix.
3. Submit a pull request with a detailed description of your changes.

For issues, suggestions, or feedback, please open a GitHub Issue in the repository.

---

## Roadmap
Future plans include:
- Developing a corresponding Arduino library to complement `arduino-py` for even easier integration.
- Publishing to PyPI for streamlined installation.
- Add more methods to the ArduinoDevice class.

---

## License
This project is licensed under the MIT License. See the LICENSE file for details.

---

## Acknowledgments
Special thanks to the open-source community for inspiring this project. Let's make Arduino projects even more accessible with Python!

