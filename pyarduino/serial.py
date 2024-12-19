import serial
import time

byte = bytes

class ArduinoDevice:
    def __init__(self, com: str, baud_rate: int = 9600, timeout: int = 1, encoding: str = "utf-8") -> None:
        self.__ready = False
        self.device = serial.Serial(com, baud_rate, timeout=timeout)
        self.encoding = encoding
        time.sleep(2)
        self.__ready = True

    def end(self) -> None:
        self.device.close()
        return
    
    def available(self) -> int:
        return self.device.in_waiting()
    
    def availableForWriting(self) -> int:
        return self.device.out_waiting()

    def readBytes(self, buffer: list, length: int) -> None:
        for _ in range(length):
            if self.device.in_waiting == 0:
                raise IndexError("Not available bytes to read.")
            
            buffer.append(self.device.read(1))
        return

    def read(self) -> byte:
        if self.device.in_waiting == 0:
            raise IndexError("Not available bytes to read.")

        return self.device.read(1)

    def readString(self) -> str:
        if self.device.in_waiting == 0:
            raise IndexError("Not available lines to read.")
        
        return self.device.readline().decode(self.encoding).strip()
    
    def print(self, text: str) -> None:
        self.device.write((text).encode(self.encoding))

    def printLn(self, text: str) -> None:
        self.print(text + "\n")

    def __bool__(self) -> bool:
        return self.__ready