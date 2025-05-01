OPP
===

Note: Board config does not load for solenoid wings prior to the wing being
physically installed. This is probably also true for incandescents.

Flashing
--------

First, install Python 2 and get to the directory with the cyflash script.

    pyenv install 2.7.18
    pyenv local 2.7.18
    pip install pyserial
    cd ./opp/Python/cyflash

Next, plug the board to USB while holding the button on the board to put
it in bootloader mode. The Blue LED should be flashing. Then run the
following command to flash the firmware. The serial port may be different,
check with `ls /dev/cu.*`.

    python -m cyflash.__main__ --serial /dev/cu.usbmodem101 \
        --serial_baudrate 115200 \
        ../../Creator/Gen2Images/Gen2.rev0.3.0.1.cyacd

Loading Config
--------------

First erase the config on the board. Ensure jumpers are set, but DO NOT
press the button on the board when plugging it in.

    opp/Python/Gen2Test
    python Gen2Test.py -port=/dev/cu.usbmodem101 -eraseCfg

Then copy the config to the Gen2Test directory. You can't do it from the
source directory due to the use of `__import__` in the opp script.

    opp/Python/Gen2Test
    cp /path/to/opp_board_config/06.py . 
    python Gen2Test.py -port=/dev/cu.usbmodem101 -saveCfg -loadCfg=06.py
