import serial
import time
from .errors import _TypeError, _NotEnoughError, _MoreThanExpectedArgsError

byte = bytes
char = str

class ArduinoDevice:
    def __init__(self, com: str, baud_rate: int = 9600, timeout: int = 1000, encoding: str = "utf-8") -> None:
        if not isinstance(com, str):
            raise _TypeError("com", "str")
        
        if not isinstance(baud_rate, int):
            raise _TypeError("baud_rate", "int")
        
        if not isinstance(timeout, int):
            raise _TypeError("timeout", "int")
        
        if not isinstance(encoding, str):
            raise _TypeError("encoding", "str")

        self.__ready = False
        self.device = serial.Serial(com, baud_rate, timeout=timeout/1000)
        self.encoding = encoding
        time.sleep(2)
        self.__ready = True

    
    def available(self) -> int:
        return self.device.in_waiting
    
    def availableForWriting(self) -> int:
        return self.device.out_waiting()

    def end(self) -> None:
        self.device.close()
        return

    def find(self, target: char, length: int = 0) -> bool:
        if len(target) != 1 and isinstance(target, str):
            raise _TypeError("target", "char (one-length string)")
        
        if not isinstance(length, int):
            raise _TypeError("length", "int")

        target_byte = target.encode()

        while self.available():
            if self.read() == target_byte:
                return True
            
            if length and self.available() <= length:
                break

        return False

    def read(self) -> byte:
        if self.device.in_waiting == 0:
            raise _NotEnoughError("bytes")

        return self.device.read(1)
    
    def readBytes(self, buffer: list[byte], length: int) -> None:
        if not isinstance(buffer, list) or not all([isinstance(_, byte) for _ in buffer]):
            raise _TypeError("buffer", "list[byte]")
        
        if not isinstance(length, int):
            raise _TypeError("length", "int")
        
        start_len = len(buffer)

        for _ in range(length):
            if self.device.in_waiting == 0:
                raise _NotEnoughError("bytes")
            
            buffer.append(self.device.read(1))
        return start_len - len(buffer)

    def readBytesUntil(self, character: char, buffer: list[char | byte], length: int):
        if not isinstance(character, char) or len(character) != 1:
            raise _TypeError("character", "char (one-length string)")

        if not isinstance(buffer, list) or not (all([isinstance(_, char) and len(_) == 1 for _ in buffer]) or all([isinstance(_, byte) and len(byte) == 1 for _ in buffer])):
            raise _TypeError("buffer", "list[char] or list[byte]")

        if not isinstance(length, int):
            raise _TypeError("length", "int")
        
        if length <= 0:
            return 0

        start_len = len(buffer)

        while self.available()-length:
            read_byte = self.read().decode(self.encoding)
            buffer.append(read_byte)
            
            if read_byte == character:
                return start_len-len(buffer)
        else:
            return None
    

    def readString(self) -> str:
        if self.device.in_waiting == 0:
            raise _NotEnoughError("lines")
        
        return self.device.readline().decode(self.encoding).strip()
    
    def readStringUntil(self, terminator: char) -> str | None:
        if not isinstance(terminator, char) or len(terminator) != 1:
            raise _TypeError("terminator", "char (one-length string)")

        buffer = []
        while self.available():
            read_byte = self.read().decode(self.encoding)
            buffer.append(read_byte)
            
            if read_byte == terminator:
                return "".join(buffer)
        else:
            return None
    
    def print(self, val: any, format: str = "") -> None:
        if not isinstance(format, str) or len(format) not in [0, 3]:
            raise _TypeError("format", "format (3-or-0-length string)")
        
        if format:
            match format:
                case "DEC":
                    val = int(val)
                case "HEX":
                    val = hex(int(val))
                case "OCT":
                    val = oct(int(val))
                case "BIN":
                    val = bin(int(val))
        
        self.device.write(str(val).encode(self.encoding))
        return len(val)

    def println(self, val: any, format: str = "") -> None:
        if not isinstance(format, str) or len(format) not in [0, 3]:
            raise _TypeError("format", "format (3-or-0-length string)")

        val = val + "\r\n"
        self.print(val, format = format)
        return len(val)
    
    def setTimeout(self, time: int) -> None:
        if not isinstance(time, int):
            raise _TypeError("time", "int")
        
        self.device.timeout = time / 1000

    def write(self, *args):
        if len(args) == 0 or len(args) > 2:
            raise _MoreThanExpectedArgsError("write", 2, len(args))
        
        if len(args) == 1:
            if isinstance(args[1], int) and 0 <= args[1] <= 255:
                val = args[1]
                self.device.write(val)
                return 1
            elif isinstance(args[1], str):
                str_ = args[1]
                bytes_str = str_.encode(self.encoding)
                self.device.write(bytes_str)
                return len(bytes_str)
            else:
                raise _TypeError("val", "int or str")
        else:
            buf: list[char | byte] = args[1]
            len_: int = args[2]
            if not isinstance(buf, (list, str)) or (isinstance(buf, list) and not (all(isinstance(_, str) for _ in buf) or all(isinstance(_, int) and 0 <= _ <= 255 for _ in buf))):
                raise _TypeError("buf", "list[char | byte]")
            
            if not isinstance(len_, int):
                raise _TypeError("len", "int")
            
            if len_ > len(buf):
                raise _NotEnoughError("elements")
            
            if all([isinstance(_, str) for _ in buf]):
                str_buf = "".join(buf)
                self.device.write(str_buf.encode(self.encoding))
                return len(str_buf)
            else:
                bytes_buf = bytes(buf)
                self.device.write(bytes_buf)
                return len(bytes_buf)

    def __bool__(self) -> bool:
        return self.__ready