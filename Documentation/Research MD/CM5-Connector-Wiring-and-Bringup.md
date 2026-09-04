# CM5 Connector Wiring and Bring-Up

Last updated: 2026-09-03

## System-level picture

The CM5 is the computer. It contains the processor, Linux bootloader, onboard
eMMC storage, Wi-Fi, Bluetooth, USB controller, UART, I2C, GPIO, and PCIe
controller. The carrier board does not need a separate microcontroller or
bridge chip for the planned design.

The two 100-pin connectors are board-to-board connectors. They transfer the
CM5 signals to copper traces on the carrier board. Those traces then connect to
power circuits, the programming connector, the debug connector, the camera,
and the Hailo-8L M.2 socket.

## Required external connections

```text
USB-C power connector
    -> protection and USB-PD circuitry
    -> 9V internal rail
    -> 5V regulator
    -> CM5 5V pins through the 100-pin connectors

CM5 USB 2.0 pins
    -> dedicated programming USB-C connector
    -> development computer running rpiboot/Mass Storage Gadget

CM5 nRPIBOOT
    -> accessible jumper or pushbutton to GND

CM5 debug UART
    -> three-pin connector: TX, RX, GND
    -> external 3.3V USB-to-UART adapter
```

The power USB-C and programming USB-C connectors have different jobs. Keeping
them separate avoids making the development computer responsible for powering
the complete carrier board and avoids mixing the USB-PD power path with the
CM5 USB recovery path.

## Initial flashing and normal boot

The full CM5 variant has factory-installed eMMC storage. It does not require a
physical SD-card socket.

```text
Hold nRPIBOOT low
    -> power the carrier board
    -> connect the programming USB-C cable to a host computer
    -> run rpiboot/Mass Storage Gadget
    -> CM5 eMMC appears as USB mass storage
    -> write Raspberry Pi OS with Raspberry Pi Imager
    -> release nRPIBOOT
    -> power-cycle the board
    -> CM5 boots Linux from eMMC
```

After the first successful boot, normal software development uses Wi-Fi and
SSH. USB recovery remains available if the eMMC image or boot configuration
becomes unusable.

## UART access

UART is a physical serial protocol and a software console. The carrier board
routes CM5 transmit, receive, and ground signals to an accessible connector:

```text
Carrier DEBUG_TX  -> USB-to-UART adapter RX
Carrier DEBUG_RX  <- USB-to-UART adapter TX
Carrier DEBUG_GND --- USB-to-UART adapter GND
```

The adapter converts the CM5's 3.3V UART signals to USB. On the development
computer it appears as a COM/serial port, which can be opened with a terminal
program. UART can show bootloader, kernel, and service messages when Wi-Fi,
SSH, or normal USB software is unavailable.

The UART connector is separate from the programming USB-C connector. A USB
virtual serial port may become available after Linux starts, but the separate
UART path is retained for early-boot diagnosis. Use a 3.3V USB-to-UART adapter;
do not connect a 5V UART adapter directly to the CM5.

## Communication interfaces used by this design

| Interface | Project use | Physical role |
|---|---|---|
| UART | CM5 boot and diagnostic console | Point-to-point TX/RX serial data |
| I2C | Camera configuration and control | Shared low-speed SDA/SCL bus |
| CSI-2 | Camera video | High-speed MIPI differential lanes |
| PCIe Gen 2 x1 | Hailo-8L communication | High-speed TX/RX link plus control signals |
| USB 2.0 | CM5 eMMC flashing and recovery | Host-to-CM5 programming path |
| SPI | Not currently required | Leave available only if a future device needs it |

I2C is the shared bus in this design. CSI-2 is not I2C: I2C configures the
camera, while CSI-2 carries the actual image data. The Hailo-8L does not use
SPI or I2C for its main data path; it communicates with the CM5 over PCIe.

## Bring-up order

1. Assemble the carrier board with the CM5 only.
2. Verify regulated 5V at the CM5 connector pins.
3. Use `nRPIBOOT` and the programming USB-C connector to flash the eMMC.
4. Release `nRPIBOOT` and confirm normal eMMC boot.
5. Confirm boot messages through the UART connector.
6. Confirm Wi-Fi and SSH.
7. Attach and test the camera power, I2C, and CSI-2 interface.
8. Attach and test the Hailo-8L M.2 interface and its local 3.3V rail.

## Pre-PCB Hailo validation

The Hailo-8L currently installed on the Raspberry Pi M.2 HAT+ can be tested on
a Raspberry Pi 5 before the custom carrier board is complete. Raspberry Pi's
current software guide requires a 64-bit Raspberry Pi OS installation,
up-to-date firmware, the Hailo driver/firmware, HailoRT, and TAPPAS software.
The basic verification command is:

```bash
hailortcli fw-control identify
```

The result should identify the device architecture as `HAILO8L`. A successful
Pi 5 test validates that the Hailo module itself, its power, PCIe connection,
firmware, runtime, and inference stack work. It does not replace testing the
custom CM5 PCIe routing. The Pi 5 AI Kit may be configured for PCIe Gen 3,
while the CM5 exposes a supported PCIe Gen 2 x1 interface.

Always disconnect power before connecting or removing the M.2 module or its
PCIe cable, and provide the Hailo module with its thermal pad/heatsink.

References:

- [Raspberry Pi CM5 datasheet](https://datasheets.raspberrypi.com/cm5/cm5-datasheet.pdf)
- [Raspberry Pi CM5 flashing documentation](https://www.raspberrypi.com/documentation/hardware/computemodule/raspberry-pi.html)
- [Raspberry Pi AI software documentation](https://www.raspberrypi.com/documentation/computers/ai.html)
- [Raspberry Pi AI Kit documentation](https://www.raspberrypi.com/documentation/accessories/ai-kit.html)
