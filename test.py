from lampsterble import Lampster
import asyncio
from base64 import b16encode

# def fix_byte_result(result):
#     return b16encode(result).decode('utf-8')


testdevice = Lampster("Lampster", True)
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

# print(fix_byte_result(result))

# result = asyncio.run(testdevice.read_rgb_value())
# print(fix_byte_result(result))

# result = asyncio.run(testdevice.read_ww_value())
# print(fix_byte_result(result))

result = asyncio.run(testdevice.read_mode())
print(result)


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