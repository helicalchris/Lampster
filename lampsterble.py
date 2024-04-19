
#01FF5554-BA5E-F4EE-5CA1-EB1E5E4B1CE0  0x0021
#Mode
#On/off? 
#On=192 (0xC0) 
#Off=64(0x40) 
#Lock Light %?=0xC8. 
#RGB Mode?=0xA0 might be A8
#White mode might be 0xC8
#Overdrive?=0x20
#“All off??” 0xB0 or 0x28
#
#01FF5556-BA5E-F4EE-5CA1-EB1E5E4B1CE0 0x0025
#White Mode Intensity 2xhex pairs 00-64
#
#
#01ff5559-ba5e-f4ee-5ca1-eb1e5e4b1ce0 0x002a
#RGB Intensity 3xhex pairs 00-64 (0-100%)
#
#
#
#01ff5561ba5ef4ee5ca1eb1e5e4b1ce0 0x0038
#Wake Timer On Settings
#
#01ff5562ba5ef4ee5ca1eb1e5e4b1ce0 0x003c
#Wake Timer Off Settings



import asyncio

from bleak import BleakScanner
from bleak import BleakClient
from base64 import b16encode
import bleak_retry_connector

class Lampster:
    
    #rgb and ww channel values
    r = 0
    g = 0
    b = 0
    ww = 0
    wc = 0

    #this setting changes how you connect to Lampster
    #Most OS work fine with MAC address but MacOS doesnt, and needs to search for the device which is a bit rubbish but it only supports UUIDs not MACs
    #Left in for testing the library on MacOS but beware that because of this for some reason on MacOS sending >1 command per connection sometimes fails
    #Set at init but documented here to be clear on usage
    connect_with_name = False
    
    def __init__(self, nameofdevice, connectwithname = False):
        self.device_name = nameofdevice
        self.connect_with_name = connectwithname
        

    async def _connect_to_lampster(self):
        #if we are connecting by name, finds the device, otherwise just returns the mac to be used as a param for BleakClient
        bledevice = None
        #See note above about connect_with_name usage
        if self.connect_with_name: 
            bledevice = (await BleakScanner.find_device_by_name(self.device_name))
        else:
            bledevice = (await BleakScanner.find_device_by_address(self.device_name))
        if bledevice == None: return None

        try:
            client = await bleak_retry_connector.establish_connection(
                        client_class = BleakClient, 
                        device = bledevice, 
                        name = bledevice.address,
                    )
            return client
        except Exception as e:
            raise ConnectionError("Error when connecting to Lampster BLE device, address: %s\n%s", bledevice.address, str(e))
        
    async def set_rgb_mode(self):
        async with BleakClient(await self._connect_to_lampster()) as client:
            #Set mode to RGB
            output_modergb = await client.write_gatt_char("01ff5554-ba5e-f4ee-5ca1-eb1e5e4b1ce0",bytes.fromhex("a0"))


    async def set_rgb_value(self, rval, gval, bval, brightness):
        #Lampster does not have brightness.  Brightness is set by the intensity of each channel
        #Each channel is a percentage 0-100, not 0-255 which is what you pass in as parameters.
        #Pass in brightness as 1-100% (int)


        rval = int(rval)
        gval = int(gval)
        bval = int(gval)
        brightness = int(brightness)

        if not 1 <= brightness <=100: brightness = 100
        if not 0 <= rval <= 255: rval = 255
        if not 0 <= gval <= 255: gval = 255
        if not 0 <= bval <= 255: bval = 255

        #Logic:
        # i) the colour value sent to function is 0-255 but the light uses 0-100, so divide by 2.5 to convet
        # ii) the brightness is acually done by adjusting the colour by the percent brightness, so take adjusted colour number above and multiply by brightness percentage
        self.r = (rval/2.5) * (brightness/100)
        self.g = (gval/2.5) * (brightness/100)
        self.b = (bval/2.5) * (brightness/100)

        async with BleakClient(await self._connect_to_lampster()) as client:
                    #Set RGB : convert each of the three values to hex, and pad to 2 chars if only one
                    rgbstring = hex(int(self.r))[2:].zfill(2) + hex(int(self.g))[2:].zfill(2) + hex(int(self.b))[2:].zfill(2)
                    output_setrgb = await client.write_gatt_char("01ff5559-ba5e-f4ee-5ca1-eb1e5e4b1ce0",bytes.fromhex(rgbstring))

    async def set_ww_mode(self):
        async with BleakClient(await self._connect_to_lampster()) as client:
            #Set mode to WW
            output_modeww = await client.write_gatt_char("01ff5554-ba5e-f4ee-5ca1-eb1e5e4b1ce0",bytes.fromhex("c8"))            

    async def set_ww_value(self, wwval, wcval, brightness):
        #Lampster does not have brightness.  Brightness is set by the intensity of each channel
        #Each channel is a percentage 0-100, not 0-255 which is what you pass in as parameters
        #Pass in brightness as 1-100% (int)

        wwval = int(wwval)
        wcval = int(wcval)
        brightness = int(brightness)

        if not 1 <= brightness <=100: brightness = 100
        if not 0 <= wwval <= 255: wwval = 255
        if not 0 <= wcval <= 255: wcval = 255

        #Logic:
        # i) the colour value sent to function is 0-255 but the light uses 0-100, so divide by 2.5 to convet
        # ii) the brightness is acually done by adjusting the colour by the percent brightness, so take adjusted colour number above and multiply by brightness percentage
        self.ww = (wwval/2.5) * (brightness/100)
        self.wc = (wcval/2.5) * (brightness/100)

        async with BleakClient(await self._connect_to_lampster()) as client:
            #Set WW : convert each of the two values to hex, and pad to 2 chars if only one
            wwstring = hex(int(self.ww))[2:].zfill(2) + hex(int(self.wc))[2:].zfill(2)
            output_setww = await client.write_gatt_char("01ff5556-ba5e-f4ee-5ca1-eb1e5e4b1ce0",bytes.fromhex(wwstring))           

    async def set_power(self, powerstate):
        #Set flags to whether we ought to turn power on or off
        #Note we can only have one flag on, we cant turn device on and off not both
        if powerstate: 
            async with BleakClient(await self._connect_to_lampster()) as client:
                output_on = await client.write_gatt_char("01ff5554-ba5e-f4ee-5ca1-eb1e5e4b1ce0", bytes.fromhex("c0"))
        else: 
            async with BleakClient(await self._connect_to_lampster()) as client:
                output_off = await client.write_gatt_char("01ff5554-ba5e-f4ee-5ca1-eb1e5e4b1ce0", bytes.fromhex("40"))

    async def read_mode(self):

        client = await self._connect_to_lampster()

        async with client:
            result = (await client.read_gatt_char("01ff5554-ba5e-f4ee-5ca1-eb1e5e4b1ce0"))
            return b16encode(result).decode('utf-8')
        

    async def read_rgb_value(self):
        async with BleakClient(await self._connect_to_lampster()) as client:
            result = (await client.read_gatt_char("01ff5559-ba5e-f4ee-5ca1-eb1e5e4b1ce0"))
            return b16encode(result).decode('utf-8')
        
    async def read_ww_value(self):
        async with BleakClient(await self._connect_to_lampster()) as client:
            result = (await client.read_gatt_char("01ff5556-ba5e-f4ee-5ca1-eb1e5e4b1ce0"))
            return b16encode(result).decode('utf-8')