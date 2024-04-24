# Python Lampster Library and test harness

This library control a Lampster light, which otherwise is only possible via an app

## Understanding the BLE commands for Lampster

Before I wrote the library I did quite a lot of work to understand the BLE commands

NB This doesn't yet include the wake up and timed sleep function as I havent quite figured that out yet

### Mode Setting
> **UUID:** 01FF5554-BA5E-F4EE-5CA1-EB1E5E4B1CE0  Handle: 0x0021
> 
> **Modes**
> - On Mode (write: turns light on; read: last action was to turn light on) Hex C0 (Decimal 192 = 0xC0) 
> - Off Mode (write: turns light off; read: light is off) Hex 40 (Decimal 64 = 0x40) 
> - RGB Mode (Write: sets mode: read: is current mode) Hex A0
> - White mode (Write: sets mode: read: is current mode) Hex C8
> - *Modes below are the ones I haven't quite figured out yet...*
> - Lock Light Hex C8. 
> - Overdrive Hex 20
> - Alternative off - seems to work when C0 doesn't - Hex 28 however B0 seems to do something similar
>
> **Support:** Write and Read of UUID

### White Colour Setting
> **UUID:** 01FF5556-BA5E-F4EE-5CA1-EB1E5E4B1CE0 Handle: 0x0025
> 
> White Mode Intensity 
> 
> Format is 2 x hex pairs each with hex value 00-64 concatenated (eg 0145)
> 
> Note: The values provided are warm white then cold white LED intensity.  The values used are not typical RGB 0-255 values.  Each is a value 0-100, which is actually an intensity value for each set of LEDs.  As such it isnt really colour temperature.  The library takes the 0-255 pair of values provided for normal WW, and scales each value in line with the brightnes (ie percentage intensity 0-100%).  This is a bit odd, and a bit rubbish, but its how it works
> 
> **Support:** Write and Read of UUID

### RGB Colour Setting
> **UUID:** 01ff5559-ba5e-f4ee-5ca1-eb1e5e4b1ce0 Handle: 0x002a
> 
> RGB Intensity 
> 
> Format: 3 x hex pairs each with value 00-64 (concatenated as a single string (eg 142235) 
> 
> Note: The values used are not typical RGB 0-255 values.  Each is a value 0-100, which is actually an intensity value for each set of LEDs.  As such it isnt really RGB.  The library takes the 0-255 tuple provided for normal RGB, and scales each value in line with the brightnes (ie percentage intensity 0-100%).  This is a bit odd, and a bit rubbish, but its how it works
> 
> **Support:** Write and Read of UUID

### Timers
> Wake Up Tomer UUID
> 
> **UUID:** 01ff5561ba5ef4ee5ca1eb1e5e4b1ce0 Handle: 0x0038
> 
> *Wake Timer On Settings TBC*
>
> Sleep Timer
> 
> **UUID:** 01ff5562ba5ef4ee5ca1eb1e5e4b1ce0 Handle: 0x003c
> 
> *Wake Timer Off Settings TBC*

## Library Usage

The library requires bleak and bleak_retry_connector, both of which can be installed by pip

Once you import the lampsterble library, you just create a Lampster object

```
light = Lampster("Lampster", True)
light = Lampster("C0:00:00:01:65:45")
```

The first parameter is the name of the device, which can be the actual name or a MAC address.  The library works on Mac and non-Mac systems, the difference beign that on Macs you can't connect by MAC address you have to find the device by name instead (by name is a universal approach but is a little slower).  If you are connecting using a name, inform the object by adding a second paraneter of True which switches the mode to connect-by-name.

The library can then be used by making calls.  If you are using within a wider application that is already using async and await calls (such as Home Assistant) then you can just call with await pre-pended, but for a test harnesslike test.py in the repo you need to wrap the calls in an asyncio.run() in order to handle the async element of the library.

```
#Read the current mode
light.read_mode()  #returns 2 hex characters - see UUID text above

#Read the current RGB value (intensity of the R G and B LEDs)
light.read_rgb_value()  #returns 6 hex characters - see UUID text above

#Read the current white light value (intensity of cold and warm LEDs)
light.read_ww_value()   #returns 4 hex characters - see UUID text above

#Turn device on
light.set_power(True)

#Turn device off
light.set_power(False)

#Set to RGB Mode
light.set_rgb_mode()

#Set RGB value (see note about read and intesity in main text above)
light.set_rgb_value(red_value_0_255, green_value_0_255, blue_colour_0_255, brightness_percentage)

#Set warm - cold white mode
light.set_ww_mode()

#Set white colour value
light.set_ww_value(warm_value_0_255, cold_value_0_255, brightness_percentage)
```


