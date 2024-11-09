Introduction to the MHZ19 CO2 Sensor
====================================

The MHZ19 is a small and cheap CO2 sensor based on NDIR
(non-dispersive infrared) detection from Zhengzhou Winsen Electronics
Technology Co., Ltd.

The sensor supports UART, PWM and ADC output. This driver only implements
the UART interface.

UART logic levels are 3V3. The power supply of the device *must* be in the
range of 4.9-5.1V, otherwise the CO2 readings will be off. It is highly
recommended to add a buck-bust converter between the power supply and the
sensor to stabilize the input voltage.

The code of this driver is the CircuitPython port of
<https://github.com/fdobrovolny/mh-zxx>. Changes are minor, mainly passing
the uart object to the constructor and defining properties and setters.


Dependencies
============

There are no dependencies: the driver only uses plain `busio.UART` read and
write methods.


Installing from PyPI
====================

*Note: currently, the package is not yet available from PyPI*.

On supported GNU/Linux systems like the Raspberry Pi, you can install the driver locally `from
PyPI <https://pypi.org/project/circuitpython-mhz19/>`_. To install for current user:

.. code-block:: shell

    pip3 install circuitpython-mhz19

To install system-wide (this may be required in some cases):

.. code-block:: shell

    sudo pip3 install circuitpython-mhz19

To install in a virtual environment in your current project:

.. code-block:: shell

    mkdir project-name && cd project-name
    python3 -m venv .venv
    source .venv/bin/activate
    pip3 install circuitpython-mhz19


Usage Notes
===========

See `examples//mhz19_simpletest.py` for a basic usage example.


Documentation
=============

For information on building library documentation, please check out `this guide <https://learn.adafruit.com/creating-and-sharing-a-circuitpython-library/sharing-our-docs-on-readthedocs#sphinx-5-1>`_.


Contributing
============

Contributions are welcome! This project follows Adafruit's `Code of Conduct
<https://github.com/bablokb/circuitpython_mhz19/blob/main/CODE_OF_CONDUCT.md>`_
before contributing to help this project stay welcoming.
