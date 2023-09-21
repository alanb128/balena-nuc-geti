# balena-nuc-geti
Experimental Geti inferencing deployed to a NUC/x86 via balena

## Description
[Intel Geti](https://geti.intel.com/) is Intel’s new software platform for quickly building computer vision models. In this example project, we use the [balena platform](www.balena.io) to deploy a Geti model to an x86 device, where it instantly begins running inferences on a connected camera or RTSP stream. Optionally, you can connect an LED to the device which will illuminate when the selected object is detected by the camera.

The balena platform streamlines provisioning, updating and managing fleets of devices. We will use the device variables feature to change the configuration of the Geti model inferencing on-the-fly.

Once this project is running on the device, you can see the continuous inferencing output in the log window:

![Detection logging](https://raw.githubusercontent.com/alanb128/balena-nuc-geti/main/log-output.png)

## Requirements
You'll need an x86 device, a [balena account](https://dashboard.balena-cloud.com/signup) - free for up to 10 devices, and a USB drive/key to flash the device, along with flashing software such as [balenaEtcher](https://etcher.balena.io/).

We include an ML model but you can substitute your own. To perform inferences, you'll need a USB webcam or access to an RTSP stream.

To use the LED feature, you'll need:
- One Adafruit [FT232H Breakout](https://www.adafruit.com/product/2264) - General Purpose USB to GPIO
- One USB to USB C cable (like [this](https://www.adafruit.com/product/4474)) to connect the breakout to your PC
- One LED - any color, such as [this](https://www.adafruit.com/product/298)
- One 220 ohm [resistor](https://www.adafruit.com/product/2780) (+/- 100 ohms is fine)
- A small breadboard and some wire such as [this](https://www.amazon.com/eBoot-400-Point-Solderless-Breadboard-Flexible/dp/B071D7V9HD/) - or you can use a PCB/perfboard if you're comfortable soldering

![LED breadboard](https://raw.githubusercontent.com/alanb128/balena-nuc-geti/main/LED-breadboard.jpg)

Set up the breadboard or circuit as shown in the layout diagram on [this page](https://learn.adafruit.com/circuitpython-on-any-computer-with-ft232h/gpio).

## Setup
Set up your balena account, login, and then use the button below to create your fleet (of one or more devices) and deploy the code:

[![balena deploy button](https://www.balena.io/deploy.svg)](https://dashboard.balena-cloud.com/deploy?repoUrl=https://github.com/alanb128/balena-nuc-geti)

Then add a new device, flash the OS to your USB key, boot with that USB key and flash the X86 device. Make sure it is connected to the internet - it will then download the software and begin inferencing.

## Configuration

The video input source is set to a connected webcam by default. You can use the [device variable](https://docs.balena.io/learn/manage/variables/#device-variables) in the balenaCloud dashboard to set `VIDEO_INPUT` to an RTSP stream to use that instead. To switch back to a webcam, delete the `VIDEO_INPUT` variable or set it to `0` which is the first detected webcam.

If you have connected and wired the LED assembly, you can select the inference label that turns on the LED with the device variable `OBJECT_DETECT` which has a default value of `bird`.

The LED will stay on for three seconds after a detection and then turn off. To extend that time, set `LED_LAG_TIME` to an integer value for the number of seconds to remain on. Set the value to `0` to have it remain on indefinitely after a detection.

## Some takeaways

- This is an easy way to deploy Geti models to x86 devices

- A good example of how to perform IoT actions on certain object detections

- Ease of remotely re-configuring the device using variables on the web dashboard
