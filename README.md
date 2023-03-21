# Buzzah!
A simple and easy-to-build vibrotactile coordinated reset (vCR) device for Parkinson's disease sufferers.

## Background

"Vibrotactile coordinated reset" (vCR) is a novel treatment for symptoms of Parkinson's disease. It involves stimulating the fingertips of both hands with patterns of brief, mild vibration. Early research results are encouraging, and have made headlines around the world. Since the patterns of vibrations and other details about the vCR devices are documented, many in the P.D. community are experimenting with DIY versions.

## What is Buzzah!?

Many DIY implementations require technical proficiency: wiring, soldering small components, software installation, programming, etc. These requirements are substantial barriers to entry for non-technical users. The device presented here prioritizes ease of assembly over size/cost, eliminating most of the technical hurdles.

Buzzah! is:

- relatively inexpensive
- built from reliable, readily-available components
- assembled without special tools (minimal soldering)
- setup/configured without any special software

## Limitations

This is a work in progress, and only includes an electronics/firmware design. Adapting the device into a set of gloves, a "buzz board", or other physical form is up to the user. Those considerations are more personal and less technical...and definitely not my area of expertise.

## Parts

To build the guts of a Buzzah! device, you'll need:

- 1 x [Adafruit #4900](https://www.adafruit.com/product/4900) QT Py RP2040 Microcontroller
- 1 x [Adafruit #5626](https://www.adafruit.com/product/5626) 8-channel I2C Multiplexer
- **8** x [Adafruit #2305](https://www.adafruit.com/product/2305) Haptic Motor Controller
- **9** x [Adafruit #4210](https://www.adafruit.com/product/4210) Stemma QT cable, 100mm
- **8** x [Vybronics VG0832022D](https://www.vybronics.com/coin-vibration-motors/lra/v-g0832022d) Linear Resonant Actuator (LRA), 8mm diameter, 235Hz

These parts are available from many suppliers, but I prefer Digi-Key. If you want a single-click solution, here are shopping cart links for both Digi-Key USA and Canada (I don't get any kickbacks from Digi-Key...this is just a convenient way to load all the items into your cart):

- Digi-Key US: https://www.digikey.com/short/wwp9qvwc
- Digi-Key CA: https://www.digikey.ca/short/wwp9qvwc

While you wait for these parts to arrive, read on to understand how to assemble them, and what they do.

## Assembly

Here is a picture of the assembled parts of a Buzzah! device:

![Assembled Buzzah! Components](https://user-images.githubusercontent.com/382436/226647797-a104f5dc-2eab-44c7-af58-53cb1859483e.jpg)

In case the picture isn't self-explanatory:

- Connect a STEMMA QT cable between the microcontroller and the multiplexer's "middle" port.
- Connect a STEMMA QT cable between each remaining port on the multiplexer and a motor driver (either side is OK).

Connecting the motors to the motor drivers is the only step that requires work. Options include:

- Solder wires directly to the "+" and "-" pads on the drivers (polarity doesn't matter)
- Solder pins to each driver and add a matching connector to each motor (as pictured above)

In either case, basic soldering is required. I haven't found a solution that completely eliminates the need to solder some wires.

Adding connectors to each motor is a bit more work but facilitates both replacement and the addition of extension wires. The latter are required if you plan to install the motors in gloves and want to retain freedom of motion.

## Setup

To make the assembled parts do something useful, a tiny program ("firmware") must be loaded onto the microcontroller. As promised, this doesn't require any special tools. However, it does require following a few instructions carefully.

### Update/Upgrade the Microcontroller

- Visit [this page](https://circuitpython.org/board/adafruit_qtpy_rp2040/) and DOWNLOAD the latest "stable" release. 
- Plug the microcontroller into your computer.
- On the microcontroller, there are TWO very tiny buttons. HOLD DOWN the button CLOSEST to the USB port.
- WHILE HOLDING the first button, press and release the other button.
- CONTINUE TO HOLD the first button until your computer recognizes a new USB drive called "RPI-RP2".
- RELEASE the first button.
- Copy the "UF2" file to the "RPI-RP2" drive.

The "RPI-RP2" drive should disappear and a new drive called "CIRCUITPY" should appear.

### Load the Firmware

- Download and unzip the [latest release](https://github.com/kriswilk/buzzah/releases/latest) of the Buzzah! archive.
- Copy the `lib` folder to the CIRCUITPY drive, overwriting any existing files.
- Copy the `code.py` to the CIRCUITPY drive, overwriting the existing file.

As soon as you copy `code.py` to the USB drive (and assuming all your connections are correct), your Buzzah! device should come to life and start buzzing its motors.

## Using the Device

That's it! You no longer need to connect to a computer to use the device...simply plug it into a USB power source. If a new version of the Buzzah! firmware is released, you need only replace the `code.py` file on the CIRCUITPY drive. It will automatically take effect.

In the future, I'll add details about customizing the behaviour of the device by editing `code.py`. Until then, feel free to look at it yourself. It's only a handful of lines of CircuitPython code and, even for a beginner, is quite readable.

## Attribution

The files in the `lib` folder are provided for convenience. They are originally from [circuitpython.org](https://circuitpython.org) and are MIT licensed by [Adafruit](https://adafruit.com).

The pattern of vibration and general operation of this device are modelled after the published research of Dr. Peter Tass et al. (Stanford University).

## DISCLAIMER

I am neither a doctor nor a lawyer. The device described above is purely experimental. The research that it is based upon is ongoing, and the therapeutic effects (and/or SIDE EFFECTS!) of such a device are NOT fully understood. I do not claim that this device will improve anyone's symptoms, nor do I take responsibility for any harm that it may inadvertently cause.

If you choose to build a device such as this: (a) BEST WISHES and (b) USE IT AT YOUR OWN RISK.
