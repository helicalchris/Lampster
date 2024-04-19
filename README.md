# Python Lampster Library and test harness

This library control a Lampster light, which otherwise is only possible via an app

## Understanding the BLE commands for Lampster

before I wrote the library I dod quite a lot of work to understand the BLE commands

NB This doesn't yet include the wake up and timed sleep function as I havent quite figured that out yet

### Mode Setting
> UUID: 01FF5554-BA5E-F4EE-5CA1-EB1E5E4B1CE0  Handle: 0x0021
>On=192 (0xC0) 
>Off=64(0x40) 
>Lock Light %?=0xC8. 
>RGB Mode?=0xA0 might be A8
>White mode might be 0xC8
>Overdrive?=0x20
>“All off??” 0xB0 or 0x28
> Support: Write and Read of UUID

### White Colour Setting
> UUID: 01FF5556-BA5E-F4EE-5CA1-EB1E5E4B1CE0 Handle: 0x0025
> White Mode Intensity 2xhex pairs 00-64
> Support: Write and Read of UUID

### RGB Colour Setting
>01ff5559-ba5e-f4ee-5ca1-eb1e5e4b1ce0 Handle: 0x002a
>RGB Intensity 3xhex pairs 00-64 (0-100%)
> Support: Write and Read of UUID

### imers
>Wake Up Tomer UUID
>01ff5561ba5ef4ee5ca1eb1e5e4b1ce0 Handle: 0x0038
> *Wake Timer On Settings TBC*
>
> 01ff5562ba5ef4ee5ca1eb1e5e4b1ce0 Handle: 0x003c
> *Wake Timer Off Settings TBC*

## Library Usage
*Coming Soon*


