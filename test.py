from lampsterble import Lampster
import asyncio

testdevice = Lampster("Lampster", True)
#testdevice = Lampster("C0:00:00:01:65:45")

# try:
#     asyncio.run(testdevice.set_power(True))
#     print("Power is on")
# except:
#     print("Power change to on failed")


# try:
#     asyncio.run(testdevice.set_rgb_mode())
#     print("mode is RGB")
# except:
#     print("Mode change to RGB failed")

# try:
#     asyncio.run(testdevice.set_rgb_value(90,135,250,100))
#     print("Colour is set")
# except:
#     print("RGB change to new value failed")

# result = asyncio.run(testdevice.read_mode())

# try:
#     result = asyncio.run(testdevice.read_rgb_value())
#     print(result)
# except:
#     print("RAG Value Read Failed")


# try:
#     result = asyncio.run(testdevice.read_ww_value())
#     print(result)
# except:
#     print("WW Value Read Failed")

#Basic test without try so exceptions are visible
result = asyncio.run(testdevice.set_power(False))
print(result)
