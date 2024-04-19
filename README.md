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
*Coming Soon*


