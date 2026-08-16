# CM5 Programming and Boot Design

This document explains how the finished Watchdog carrier board will be
programmed, how the CM5 boots, and which programming connections must exist on
the PCB.

The important idea is that we are not programming a small microcontroller on
the carrier board. The CM5 is a complete Linux computer. We will install an
operating-system image onto the CM5's eMMC storage, then run the Watchdog
software as Linux services.

## The boot chain

The normal boot sequence is:

```text
Power applied
    ↓
CM5 boot ROM
    ↓
CM5 EEPROM bootloader
    ↓
eMMC boot partition
    ↓
Linux kernel and Device Tree
    ↓
systemd
    ↓
Watchdog services
```

The CM5 EEPROM bootloader decides where to look for an operating system. For
this board, the normal boot device should be the CM5's onboard eMMC. The
bootloader configuration, Linux kernel, Device Tree files, camera setup, and
application software all live in or are launched from the eMMC image.

The Hailo-8L is not what boots the board. It is a PCIe peripheral that Linux
initializes after the CM5 has booted. The camera is also initialized by Linux
after the camera driver and Device Tree configuration have loaded.

## Three ways to use the programming system

### Factory flashing

Factory flashing is used when the eMMC is blank or when a complete image needs
to be installed.

```text
Development PC
    │ USB data cable
    ▼
Programming connector on carrier board
    │ USB 2.0 D+/D−
    ▼
CM5 USB device interface
    │
nRPIBOOT held low during power-up
    ▼
CM5 USB boot mode
    ▼
eMMC appears to the PC as mass storage
```

The host computer runs Raspberry Pi's `rpiboot`/USB boot utility. The CM5
temporarily exposes its eMMC as a USB mass-storage device. The host then writes
the operating-system image to the eMMC.

After flashing:

1. Stop the flashing utility.
2. Remove the `nRPIBOOT` jumper or release the recovery switch.
3. Power-cycle the board.
4. The CM5 boots from eMMC.

The first image should contain Raspberry Pi OS 64-bit, the correct CM5 Device
Tree configuration, camera support, Hailo software, and a basic Watchdog
service.

### Normal development

Once the board has booted successfully, daily development should happen over
Wi-Fi:

```text
Developer PC ── Wi-Fi ── CM5
                         ├── SSH
                         ├── Git pull / file transfer
                         ├── service restart
                         └── application logs
```

The normal development loop is:

1. Build or edit the software on the development PC.
2. Transfer the new software to the CM5 with Git, `scp`, or a deployment
   script.
3. Restart the relevant `systemd` service.
4. View logs with `journalctl`.
5. Test the camera, Hailo-8L, and alarm/network behavior.

The CM5's eMMC should not be reflashed for every software change. Full image
flashing is for initial provisioning, operating-system changes, and recovery.

### Recovery and low-level debugging

If Linux, Wi-Fi, or the application fails, the board still needs a recovery
path. The board should therefore expose both:

- USB boot/recovery through `nRPIBOOT` and USB D+/D−
- A three-pin debug UART: TX, RX, and GND

The UART is useful before Linux has fully started. It can show bootloader
messages, kernel messages, and service failures. It is not a replacement for
USB eMMC flashing; it is the diagnostic path that tells us why flashing or
normal boot is failing.

## What must change in the PCB design

The carrier board needs the following programming hardware.

### 1. USB programming connection

The CM5 USB 2.0 data signals must reach an external host computer:

```text
USB programming connector
    ├── USB D+
    ├── USB D−
    ├── USB VBUS sense
    └── GND
```

The programming connector should include a low-capacitance USB ESD protector
placed close to the connector. Route D+ and D− as a controlled USB differential
pair according to the CM5 and stackup rules.

The connector's VBUS should be treated as USB presence/sense. It must not be
blindly tied to the carrier board's 5V rail, because the host computer and the
board's MP2329 converter would otherwise become competing 5V sources.

The exact VBUS-sense circuit should follow the CM5IO reference design. The
USB connector ground must connect directly to the board ground plane.

### 2. Separate power and programming roles

The selected front USB-C connector is primarily the 9V USB-PD power input.
Using that same connector as the only programming connector creates an awkward
bring-up case: a development PC may provide USB data but not enough power for
the complete carrier board, while a USB-PD charger provides power but is not a
development host.

The preferred design is therefore:

```text
Main USB-C       → USB-PD power input and normal USB data if desired
Separate port    → USB programming/recovery connection
```

If board area or cost prevents a second connector, expose USB D+, USB D−, VBUS
sense, and GND on a factory test connector or pogo-pad arrangement. This is
acceptable for manufacturing but less convenient during development.

### 3. `nRPIBOOT` recovery control

Add a jumper, pushbutton, or test pads that can pull `nRPIBOOT` to ground.
The normal state must leave `nRPIBOOT` released/high. The recovery state holds
it low during power-up.

Recommended schematic concept:

```text
3.3V
 │
10kΩ pull-up
 │
CM5 nRPIBOOT ───── jumper/test pad ───── GND
```

Do not permanently connect `nRPIBOOT` to ground. If it is permanently low, the
board will repeatedly enter USB recovery mode instead of booting normally from
eMMC.

The recovery control should be accessible with the CM5 installed. It should
not require removing the module or probing a hidden pad underneath it.

### 4. Debug UART

Expose this header or test-point group:

```text
DEBUG_UART_TX
DEBUG_UART_RX
GND
```

An optional fourth pin may provide a 3.3V reference, but the UART header should
not be used to power the board. Use a 3.3V USB-to-UART adapter; never connect a
5V UART adapter directly to the CM5 signals.

Keep the UART traces away from the MP2329 switching node and other noisy power
copper. The UART is low speed, so it does not need controlled-impedance routing,
but it does need a clean ground reference.

### 5. Reset and power control

Expose a reset/power-control button or test pad. This will allow us to:

- restart the CM5 without disconnecting USB-C power;
- test shutdown and wake behavior;
- recover from a hung application; and
- eventually implement a user-facing power button.

The power button should be connected according to the CM5IO reference design,
not treated as an arbitrary GPIO.

### 6. Status indicators

Reserve at least two LEDs or test points:

- board/CM5 power-good indication;
- activity or recovery indication.

The LEDs are especially useful before Wi-Fi and SSH are available. They should
not be connected directly to high-current power rails without the appropriate
resistors and should not load boot-critical signals.

## What the initial software image should contain

The first complete eMMC image should include:

1. Raspberry Pi OS 64-bit.
2. CM5 bootloader configuration with eMMC as the normal boot device.
3. The carrier-board Device Tree configuration.
4. Enabled CSI camera interface and I²C control bus.
5. Enabled PCIe interface for the Hailo-8L M.2 module.
6. HailoRT and the selected Hailo runtime packages.
7. Wi-Fi configuration and SSH access.
8. A serial console configuration for the debug UART.
9. A `watchdog-camera.service` systemd service.
10. Logging and a simple health/status command.

The first image should boot into a diagnostic mode before attempting the full
camera/AI application. That diagnostic mode should verify, in order:

```text
5V rail present
    ↓
CM5 booted
    ↓
Wi-Fi available
    ↓
Camera detected
    ↓
Hailo-8L detected over PCIe
    ↓
Application started
```

This makes hardware bring-up much easier than debugging the entire application
at once.

## Recommended development milestones

### Milestone 1: CM5-only boot

Before connecting the camera or Hailo-8L, prove that the carrier board can:

- power the CM5 with a stable 5V rail;
- enter USB boot mode;
- flash the eMMC;
- boot Raspberry Pi OS from eMMC; and
- produce UART output.

### Milestone 2: Carrier-board Linux configuration

Add and test:

- Wi-Fi;
- the Device Tree;
- the power-good and reset signals;
- the camera interface; and
- the programming/recovery controls.

### Milestone 3: Hailo-8L

Add the Hailo module and verify:

- the local 3.3V rail;
- power sequencing and reset timing;
- PCIe link detection;
- HailoRT device discovery; and
- a small inference test.

### Milestone 4: Watchdog application

Only after the hardware interfaces work independently should the full camera,
AI detection, Wi-Fi messaging, and alarm behavior be combined into the main
service.

## Firmware update plan

For the prototype:

```text
USB/rpiboot       Factory image and emergency recovery
SSH/Wi-Fi         Normal software development
UART              Boot and failure diagnosis
```

For a later production revision, add an update system with versioned releases,
rollback, and signed software. The USB recovery path should remain available
even after field-update support is added.

## Design decisions to lock before PCB layout

- Add a dedicated USB programming connector, or formally choose a factory
  pogo/test-pad method.
- Route CM5 USB D+/D− to that programming interface.
- Add accessible `nRPIBOOT` recovery control.
- Add the three-pin debug UART.
- Add reset/power control.
- Reserve status LEDs or test points.
- Copy the CM5IO USB VBUS-sense and USB boot circuitry before finalizing the
  schematic.
- Confirm the exact CM5 variant, especially the eMMC capacity and wireless
  option.

## References

- [Raspberry Pi Compute Module 5 datasheet](https://datasheets.raspberrypi.com/cm5/cm5-datasheet.pdf)
- [Raspberry Pi Compute Module documentation](https://www.raspberrypi.com/documentation/computers/compute-module.html)
- [Current carrier-board architecture notes](../documentation.md)
- [Power design explainer](power-design-explainer.md)
