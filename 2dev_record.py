"""
MIT License

Copyright (c) 2020, Henrik Blidh

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

https://github.com/hbldh/bleak

Modified for use with Blueberry test devices, 20220710
"""

import sys
import logging
import asyncio
import platform
import bitstring
import argparse
import time
import signal
import atexit
import datetime

from bleak import BleakClient 
from bleak import _logger as logger

from blueberry import Blueberry

global bby, bby_task, save_file

def save_csv(data_1,data_2,data_3):
    ms_device = data_1["ms_device"]
    ambient = data_1["ambient"]
    led740nm10mm = data_1["led740nm10mm"]
    led940nm10mm = data_1["led940nm10mm"]
    led850nm10mm = data_1["led850nm10mm"]
    led740nm27mm = data_1["led740nm27mm"]
    led940nm27mm = data_1["led940nm27mm"]
    led850nm27mm = data_1["led850nm27mm"]

    timeNow = time.time()

    save_file.write("{},{},{},{},{},{},{},{},{}\n".format(timeNow, ms_device, ambient, led740nm10mm, led940nm10mm, led850nm10mm, led740nm27mm, led940nm27mm, led850nm27mm))

    ms_device = data_2["ms_device"]
    ambient = data_2["ambient"]
    led740nm10mm = data_2["led740nm10mm"]
    led940nm10mm = data_2["led940nm10mm"]
    led850nm10mm = data_2["led850nm10mm"]
    led740nm27mm = data_2["led740nm27mm"]
    led940nm27mm = data_2["led940nm27mm"]
    led850nm27mm = data_2["led850nm27mm"]

    save_file.write("{},{},{},{},{},{},{},{},{}\n".format(timeNow+0.04, ms_device, ambient, led740nm10mm, led940nm10mm, led850nm10mm, led740nm27mm, led940nm27mm, led850nm27mm))

    ms_device = data_3["ms_device"]
    ambient = data_3["ambient"]
    led740nm10mm = data_3["led740nm10mm"]
    led940nm10mm = data_3["led940nm10mm"]
    led850nm10mm = data_3["led850nm10mm"]
    led740nm27mm = data_3["led740nm27mm"]
    led940nm27mm = data_3["led940nm27mm"]
    led850nm27mm = data_3["led850nm27mm"]

    save_file.write("{},{},{},{},{},{},{},{},{}\n".format(timeNow+0.08, ms_device, ambient, led740nm10mm, led940nm10mm, led850nm10mm, led740nm27mm, led940nm27mm, led850nm27mm))


async def main():
    global blueberry, blueberry_task, save_file

    parser = argparse.ArgumentParser()
    parser.add_argument("-a","--address", help="MAC address of the blueberry")
    parser.add_argument("-d", "--debug", help="debug", action='store_true')
    parser.add_argument("-u", "--type", help="timing type")
    parser.add_argument("-r", "--runname", help="runname")

    args = parser.parse_args()

    #get mac address from running list_devices.py
    #e.g. 2F313F76-893E-4119-A0C6-34CE77AA383B: blueberry-0C0D
    #use command to connect = python blueberry_connect_save_data.py -a 2F313F76-893E-4119-A0C6-34CE77AA383B
    mac = args.address
    #get time in readable format
    value = datetime.datetime.fromtimestamp(time.time())

    if mac == '3E8847D9-3D52-7A2F-B913-2FBD9F63ECF3':
        save_file = open("./data/{}/{}.csv".format(str(args.type), str(args.runname) + 'L'), "w+")
    elif mac == '737E96F8-345B-0B18-66D0-B72FF7301397':
        save_file = open("./data/{}/{}.csv".format(str(args.type), str(args.runname) + 'R'), "w+")

    save_file.write("timestamp,ms_device,ambient,740nm10mm,940nm10mm,850nm10mm,740nm27mm,940nm27mm,850nm27mm\n")
 
    #create blueberry instance
    blueberry = Blueberry(mac, callback=save_csv)

    #connect to and listen to notification from the blueberry
    blueberry_task = asyncio.create_task(blueberry.run())

    await blueberry_task
    save_file.close()

async def shutdown():
    global blueberry, blueberry_task
    await blueberry.stop()
    await blueberry_task


#create asyncio event loop and start program
loop = asyncio.get_event_loop()

#handle kill events (Ctrl-C)
for signame in ('SIGINT', 'SIGTERM'):
    loop.add_signal_handler(getattr(signal, signame), lambda: asyncio.ensure_future(shutdown()))
#start program loop
try:
    loop.run_until_complete(main())
finally:
    loop.close()

