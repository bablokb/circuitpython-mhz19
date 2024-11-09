# -----------------------------------------------------------------------------
# CircuitPython library for the MHZ19 CO2 sensor.
#
# See:
#   - https://www.winsen-sensor.com/product/mh-z19c.html
#   - https://revspace.nl/MHZ19#Command_set
#
# This core of the code is from a Python implementation from:
# https://github.com/fdobrovolny/mh-zxx
#
# Adapted to CircuitPython with minor modifications by Bernhard Bablok
#
# Website: https://github.com/bablokb/circuitpython-mhz19
#
# -----------------------------------------------------------------------------

"""
MIT License

Copyright (c) 2024 Bernhard Bablok
Copyright (c) 2023 Filip Dobrovolný

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

try:
    from typing import List, Tuple, Union
    import busio
except ImportError:
    pass

class MHZ19:
    """
    Sensor for MH-Z16 and MH-Z19 CO2 sensors.
    """

    READ_CO2 = [0xFF, 0x01, 0x86, 0x00, 0x00, 0x00, 0x00, 0x00]
    ZERO_CALIBRATION = [0xFF, 0x01, 0x87, 0x00, 0x00, 0x00, 0x00, 0x00]
    SPAN_CALIBRATION = [0xFF, 0x01, 0x88, 0x00, 0x00, 0x00, 0x00, 0x00]
    AUTO_CALIBRATION = [0xFF, 0x01, 0x79, 0xA0, 0x00, 0x00, 0x00, 0x00]
    AUTO_CALIBRATION_OFF = [0xFF, 0x01, 0x79, 0x00, 0x00, 0x00, 0x00, 0x00]

    def __init__(
        self,
        uart: busio.UART
    ):
        """
        Setup CO2 sensor

        :param uart: the UART to use
        """
        self._uart = uart

    @staticmethod
    def _checksum(data: Union[bytes, List[int]]) -> int:
        """
        Calculate _checksum of the command.
        """
        return 0xFF - (sum(data[1:]) % 256) + 1

    def _write_command(self, command: List[int]):
        """
        Write command to the sensor.
        """
        self._uart.write(bytes(command) + bytes([self._checksum(command)]))

    def _read_response(self) -> bytes:
        """
        Read response from the sensor.
        """
        return self._uart.read(9)

    @property
    def co2(self) -> int:
        """
        Return CO2 concentration.
        """
        return self.read()[0]

    @property
    def temperature(self) -> float:
        """
        Return temperature.
        """
        return self.read()[1]

    @property
    def status(self) -> int:
        """
        Read status.
        """
        return self.read()[2]

    def read(self) -> Tuple[int, float, int, int]:
        """
        Read all values.

        :note: last value is auto calibration point, see
        :link: https://revspace.nl/MHZ19#Command_set

        :return: CO2 concentration, temperature, status, co2 auto calibration point
        """
        self._write_command(self.READ_CO2)
        response = self._read_response()
        if not response[0]:
            raise ValueError("No response")
        if response[0] != 0xFF or response[1] != 0x86:
            raise ValueError("Invalid response")
        if response[8] != self._checksum(response[:8]):
            raise ValueError("Invalid checksum")

        return (
            response[2] * 256 + response[3],
            response[4] - 40,
            response[5],
            response[6],
        )

    def zero_calibration(self):
        """
        Zero calibration.
        """
        self._write_command(self.ZERO_CALIBRATION)

    def span_calibration(self, span: int):
        """
        Span calibration.
        """
        command = self.SPAN_CALIBRATION.copy()
        command[3] = span // 256
        command[4] = span % 256
        self._write_command(command)

    @autocalibration.setter
    def autocalibration(self, state: bool):
        """
        Set auto calibration.
        """
        if state:
            self._write_command(self.AUTO_CALIBRATION)
        else:
            self._write_command(self.AUTO_CALIBRATION_OFF)
