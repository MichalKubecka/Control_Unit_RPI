# Control_Unit_RPI
Raspberry PI 5 - control unit

## Seznam knihoven:
* pymodbus verze vetsi nez 3 a mensi nez 4
* loguru
* rich
* gpiozero
* adafruit-circuitpython-pca9685
    * https://pypi.org/project/adafruit-circuitpython-pca9685/

## Setup
* python3 -m venv venv
* source /venv/bin/activate
* pip3 install -r requirements.txt
* make
* deactivate

## JSON protocol
```
    {
        "action": "reset_errors"
    }
```
```
    {
        "action": "set_value", 
        "device": "FrontLight", 
        "channel": 2, 
        "value": 128
    }
```
```
    {
        "action": "set_all", 
        "device": "FrontLight", 
        "value": 128
    }
```
```
    {
        "action": "set_channels", 
        "device": "FrontLight", 
        "values": [255, 128, 0, 0]
    }
```