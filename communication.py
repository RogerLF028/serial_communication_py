import serial
import main
import module_interface
import protocol_interpreter
import asyncio
import time
from enum import Enum
from datetime import datetime

BLOCKING = 0x00
NON_BLOCKING = 0x01

mode_of_transmit = BLOCKING

#TAGs
#write
TAG_READ_FW_VERSION = 0x0E
TAG_READ_DIGITAL_OUTPUTS = 0x10
TAG_READ_ANALOG_OUTPUT_1 = 0x11
TAG_READ_ANALOG_OUTPUT_2 = 0x12
TAG_READ_ANALOG_OUTPUT_3 = 0x13
TAG_READ_ANALOG_OUTPUT_4 = 0x14
TAG_READ_TARGET_PEM_POWER = 0x15
TAG_READ_ANALOG_INPUT_BLOCK_A = 0x16
TAG_READ_ANALOG_INPUT_BLOCK_B = 0x17
TAG_READ_DIGITAL_INPUTS = 0x18
# write
TAG_WRITE_DIGITAL_OUTPUTS = 0x90
TAG_WRITE_ANALOG_OUTPUT_1 = 0x91
TAG_WRITE_ANALOG_OUTPUT_2 = 0x92
TAG_WRITE_ANALOG_OUTPUT_3 = 0x93
TAG_WRITE_ANALOG_OUTPUT_4 = 0x94
TAG_WRITE_TARGET_PEM_POWER = 0x95


# Equivalente ao Callback da interrupção de RX
def serial_rx_callback():
    # equivalente -> io_read(&SERIAL.io, &data_byte, 1)
    data_byte = protocol_interpreter.PI_receive_data_byte()
    protocol_interpreter.PI_protocol_organize_receive_data(data_byte)

    if protocol_interpreter.PI_message_arrived() is True:
        data, size, id_source = protocol_interpreter.PI_read_message()
        process_data_read(data, size, id_source)

def process_data_read(data, size, id_source):
    tag = data[0]
    data_info = data[1:size]
    # print("TAG: "+str(tag))
    if tag == TAG_READ_FW_VERSION:
        read_fw_version(data_info, id_source)
    elif tag == TAG_READ_DIGITAL_OUTPUTS:
        read_digital_outputs(data_info, id_source)
    elif tag == TAG_READ_DIGITAL_INPUTS:
        read_digital_inputs(data_info, id_source)
    else:
        print("TAG not found")
        return False
    return True
    # elif tag == TAG_READ_ANALOG_OUTPUT_1:
    # elif tag == TAG_READ_ANALOG_OUTPUT_2:
    # elif tag ==TAG_READ_ANALOG_OUTPUT_3:
    # elif tag == TAG_READ_ANALOG_OUTPUT_4:
    # elif tag == TAG_READ_TARGET_PEM_POWER:
    # elif tag == TAG_READ_ANALOG_INPUT_BLOCK_A:
    # elif tag == TAG_READ_ANALOG_INPUT_BLOCK_B:
    # elif tag == TAG_READ_DIGITAL_INPUTS:

def read_fw_version(data, id_source):
    firmware = [data[0], data[1], data[2]]
    main.update_firmware(firmware, id_source)

def read_digital_outputs(data, id_source):
    output = []
    for i in range(8):
        if data[0] >> i & 1 is True:
            output.append(True)
        else:
            output.append(False)
    for i in range(8):
        if data[1] >> i & 1 is True:
            output.append(True)
        else:
            output.append(False)
    for i in range(8):
        if data[2] >> i & 1 is True:
            output.append(True)
        else:
            output.append(False)
    main.update_digital_outputs(output, id_source)

def read_digital_inputs(data, id_source):
    input = []
    for i in range(8):
        if data[0] >> i & 1 is True:
            input.append(True)
        else:
            input.append(False)
    main.update_digital_inputs(input, id_source)

def request_data():
    data = [0x10, 0x07, 0x08]
    dest = 0x02
    protocol_interpreter.PI_send_message(data, len(data), dest)

def COM_read_FW(id_dest):
    data = []
    data.append(TAG_READ_FW_VERSION)
    #print(data)
    protocol_interpreter.PI_send_message(data, len(data), id_dest)

def COM_read_digital_outputs(id_dest):
    data=[]
    data.append(TAG_READ_DIGITAL_OUTPUTS)
    protocol_interpreter.PI_send_message(data, len(data), id_dest)
def COM_read_analog_outputs(id_dest):
    data=[]
    data.append(TAG_READ_ANALOG_OUTPUT_1)
    protocol_interpreter.PI_send_message(data, len(data), id_dest)
    data.append(TAG_READ_ANALOG_OUTPUT_2)
    protocol_interpreter.PI_send_message(data, len(data), id_dest)
    data.append(TAG_READ_ANALOG_OUTPUT_3)
    protocol_interpreter.PI_send_message(data, len(data), id_dest)
    data.append(TAG_READ_ANALOG_OUTPUT_4)
    protocol_interpreter.PI_send_message(data, len(data), id_dest)

def COM_read_analog_inputs(id_dest):
    data=[]
    data.append(TAG_READ_ANALOG_INPUT_BLOCK_A)
    protocol_interpreter.PI_send_message(data, len(data), id_dest)
    data.append(TAG_READ_ANALOG_INPUT_BLOCK_B)
    protocol_interpreter.PI_send_message(data, len(data), id_dest)

def COM_read_digital_inputs(id_dest):
    data=[]
    data.append(TAG_READ_DIGITAL_INPUTS)
    protocol_interpreter.PI_send_message(data, len(data), id_dest)


async def COM_communication():
    #print('Task Communication')
    while (True):
        while(protocol_interpreter.PI_has_message_to_transmit() is True):
            protocol_interpreter.PI_trasmit_message()
            #time.sleep(0.01)
            await asyncio.sleep(0)
        await asyncio.sleep(0.05)
    print("End task communication")


async def COM_receive_serial():
    #print('Task Monitoring Receive')
    protocol_interpreter.PI_set_serial_timeout(0.005)
    while (True):
        #print("Task receive")
        print("Init time Serial receive")
        print(datetime.utcnow().isoformat(sep=' ', timespec='milliseconds'))
        data_serial = protocol_interpreter.PI_is_message_receive()
        print("Final Time Serial receive")
        print(datetime.utcnow().isoformat(sep=' ', timespec='milliseconds'))
        if data_serial:
            print(data_serial)
            for data_byte in data_serial:
                #data_byte = protocol_interpreter.PI_receive_data_byte()
                protocol_interpreter.PI_protocol_organize_receive_data(data_byte)

                if protocol_interpreter.PI_message_arrived() is True:
                    data, size, id_source = protocol_interpreter.PI_read_message()
                    print("Data: "+ str(data)+" Size: "+str(size)+" Id: "+str(id_source))
                    if process_data_read(data, size, id_source) is False:
                        print("ERROR Tag")
            #serial_rx_callback()
            #data_serial.clear()
        #else:
            #print("x")
        await asyncio.sleep(0.005)
    print("End task receive serial")



async def print_test_async():
    while(True):
        print("Teste Async")
        await asyncio.sleep(3)

#asyncio.run(communication(), print_test_async())
#asyncio.run(print_test_async())

# async def main_communication():
#     await communication()
#     await print_test_async()
#     # await asyncio.wait([
#     #     communication(),
#     #     print_test_async()
#     # ])
#
# loop=asyncio.get_event_loop()
# loop.run_until_complete(main_communication())