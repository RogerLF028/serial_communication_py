import serial
# import main
import module_interface
import protocol_interpreter
import asyncio
import time
from enum import Enum
from datetime import datetime
import define_modules

BLOCKING = 0x00
NON_BLOCKING = 0x01

mode_of_transmit = BLOCKING

# TAGs
# write
TAG_READ_FW_VERSION = 0x0E
TAG_READ_DIGITAL_OUTPUTS = 0x10
TAG_READ_ANALOG_OUTPUT_1 = 0x11
TAG_READ_ANALOG_OUTPUT_2 = 0x12
TAG_READ_ANALOG_OUTPUT_3 = 0x13
TAG_READ_ANALOG_OUTPUT_4 = 0x14
TAG_READ_ANALOG_OUTPUTS = 0x15
TAG_READ_TARGET_PEM_POWER = 0x16
TAG_READ_ANALOG_INPUT_BLOCK_A = 0x17
TAG_READ_ANALOG_INPUT_BLOCK_B = 0x18
TAG_READ_ANALOG_INPUTS = 0x19
TAG_READ_DIGITAL_INPUTS = 0x1A

# write
TAG_WRITE_DIGITAL_OUTPUTS = 0x90
TAG_WRITE_ANALOG_OUTPUT_1 = 0x91
TAG_WRITE_ANALOG_OUTPUT_2 = 0x92
TAG_WRITE_ANALOG_OUTPUT_3 = 0x93
TAG_WRITE_ANALOG_OUTPUT_4 = 0x94
TAG_WRITE_TARGET_PEM_POWER = 0x95


class Communication:
    list_modules = []


    # Processo os dados recebidos na serial
    # Avalia a TAG e define o que será realizado
    def process_data_read(self, data, size, id_source):
        tag = data[0]
        data_info = data[1:size]
        # print("TAG: "+str(tag))
        if tag == TAG_READ_FW_VERSION:
            self.read_fw_version(data_info, id_source)
        elif tag == TAG_READ_DIGITAL_OUTPUTS:
            self.read_digital_outputs(data_info, id_source)
        elif tag == TAG_READ_DIGITAL_INPUTS:
            self.read_digital_inputs(data_info, id_source)
        elif tag == TAG_READ_ANALOG_OUTPUT_1:
            self.read_analog_output(data_info, 0, id_source)
        elif tag == TAG_READ_ANALOG_OUTPUT_2:
            self.read_analog_output(data_info, 1, id_source)
        elif tag == TAG_READ_ANALOG_OUTPUT_3:
            self.read_analog_output(data_info, 2, id_source)
        elif tag == TAG_READ_ANALOG_OUTPUT_4:
            self.read_analog_output(data_info, 3, id_source)
        elif tag == TAG_READ_ANALOG_OUTPUTS:
            self.read_analog_outputs(data_info, id_source)
        elif tag == TAG_READ_TARGET_PEM_POWER:
            print("Comando para o Sistema de potência")
        elif tag == TAG_READ_ANALOG_INPUT_BLOCK_A:
            self.read_analog_input_block_A(data_info, id_source)
        elif tag == TAG_READ_ANALOG_INPUT_BLOCK_B:
            self.read_analog_input_block_B(data_info, id_source)
        elif tag == TAG_READ_ANALOG_INPUTS:
            self.read_analog_inputs(data_info, id_source)
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

# Leitura---------------------------------------------------------------------------------------------------------------
    def read_fw_version(self, data, id_source):
        firmware = [data[0], data[1], data[2]]
        # main.update_firmware(firmware, id_source)
        index = define_modules.module_id.index(id_source)
        # print("Index : "+str(index))
        # print("Module name Firmware Update: " + list_modules[index].name + " id:" + str(list_modules[index].id))
        self.list_modules[index].firmware = firmware

    def read_digital_outputs(self, data, id_source):
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
        for i in range(8):
            if data[3] >> i & 1 is True:
                output.append(True)
            else:
                output.append(False)
        output.reverse()
        # main.update_digital_outputs(output, id_source)
        index = define_modules.module_id.index(id_source)
        self.list_modules[index].digital_output = output

    def read_digital_inputs(self, data, id_source):
        input = []
        for i in range(8):
            if data[0] >> i & 1 is True:
                input.append(True)
            else:
                input.append(False)
        # main.update_digital_inputs(input, id_source)
        index = define_modules.module_id.index(id_source)
        self.list_modules[index].digital_input = input

    def read_analog_output(self, data, idx, id_source):
        analog_out = ((data[0] << 8) & 0xFF) + ((data[1]) & 0xFF)
        # main.update_analog_output_1(analog_out, idx, id_source)
        index = define_modules.module_id.index(id_source)
        self.list_modules[index].analog_output[idx] = analog_out

    def read_analog_outputs(self, data, id_source):
        index = define_modules.module_id.index(id_source)
        analog_out1 = ((data[0] << 8) & 0xFF) + ((data[1]) & 0xFF)
        # main.update_analog_output_1(analog_out1, 0, id_source)
        self.list_modules[index].analog_output[0] = analog_out1
        analog_out2 = ((data[2] << 8) & 0xFF) + ((data[3]) & 0xFF)
        # main.update_analog_output_1(analog_out2, 1, id_source)
        self.list_modules[index].analog_output[1] = analog_out2
        analog_out3 = ((data[4] << 8) & 0xFF) + ((data[5]) & 0xFF)
        # main.update_analog_output_1(analog_out3, 2, id_source)
        self.list_modules[index].analog_output[2] = analog_out3
        analog_out4 = ((data[6] << 8) & 0xFF) + ((data[7]) & 0xFF)
        # main.update_analog_output_1(analog_out4, 3, id_source)
        self.list_modules[index].analog_output[3] = analog_out4

    def read_analog_input_block_A(self, data, id_source):
        #print("Bloco A")
        #print(data)
        for i in range(8):
            analog_input = ((data[(i * 2) + 1] << 8) & 0xFF00) + ((data[(i * 2) + 0]) & 0xFF)
            # main.update_analog_input(analog_input, i, id_source)
            self.update_analog_input(analog_input, i, id_source)

    def read_analog_input_block_B(self, data, id_source):
        for i in range(8):
            analog_input = ((data[(i * 2) + 1] << 8) & 0xFF00) + ((data[(i * 2) + 0]) & 0xFF)
            # main.update_analog_input(analog_input, i+8, id_source)
            self.update_analog_input(analog_input, i+8, id_source)

    def read_analog_inputs(self, data, id_source):
        for i in range(16):
            analog_input = ((data[(i * 2) + 1] << 8) & 0xFF00) + ((data[(i * 2) + 0]) & 0xFF)
            # main.update_analog_input(analog_input, i, id_source)
            self.update_analog_input(analog_input, i, id_source)

    def update_analog_input(self, analog_input, idx, id_source):
        #print("analog "+str(idx)+" : "+str(analog_input))
        index = define_modules.module_id.index(id_source)
        self.list_modules[index].analog_input[idx] = analog_input
# end Leitura-----------------------------------------------------------------------------------------------------------

# Requisição de Leitura-------------------------------------------------------------------------------------------------
    # Envios de comando para a serial
    def COM_read_FW(self, id_dest):
        data = []
        data.append(TAG_READ_FW_VERSION)
        protocol_interpreter.PI_send_message(data, len(data), id_dest)

    def COM_read_digital_outputs(self, id_dest):
        data = []
        data.append(TAG_READ_DIGITAL_OUTPUTS)
        protocol_interpreter.PI_send_message(data, len(data), id_dest)

    def COM_read_digital_inputs(self, id_dest):
        data = []
        data.append(TAG_READ_DIGITAL_INPUTS)
        protocol_interpreter.PI_send_message(data, len(data), id_dest)

    def COM_read_analog_output_1(self, id_dest):
        data = []
        data.append(TAG_READ_ANALOG_OUTPUT_1)
        protocol_interpreter.PI_send_message(data, len(data), id_dest)

    def COM_read_analog_output_2(self, id_dest):
        data = []
        data.append(TAG_READ_ANALOG_OUTPUT_2)
        protocol_interpreter.PI_send_message(data, len(data), id_dest)

    def COM_read_analog_output_3(self, id_dest):
        data = []
        data.append(TAG_READ_ANALOG_OUTPUT_3)
        protocol_interpreter.PI_send_message(data, len(data), id_dest)

    def COM_read_analog_output_4(self, id_dest):
        data = []
        data.append(TAG_READ_ANALOG_OUTPUT_4)
        protocol_interpreter.PI_send_message(data, len(data), id_dest)

    # def COM_read_analog_outputs(id_dest):
    #     data = []
    #     data.append(TAG_READ_ANALOG_OUTPUT_1)
    #     protocol_interpreter.PI_send_message(data, len(data), id_dest)
    #     data.append(TAG_READ_ANALOG_OUTPUT_2)
    #     protocol_interpreter.PI_send_message(data, len(data), id_dest)
    #     data.append(TAG_READ_ANALOG_OUTPUT_3)
    #     protocol_interpreter.PI_send_message(data, len(data), id_dest)
    #     data.append(TAG_READ_ANALOG_OUTPUT_4)
    #     protocol_interpreter.PI_send_message(data, len(data), id_dest)

    def COM_read_analog_outputs(self, id_dest):
        data = []
        data.append(TAG_READ_ANALOG_OUTPUTS)
        protocol_interpreter.PI_send_message(data, len(data), id_dest)

    def COM_read_analog_inputs(self, id_dest):
        data = []
        data.append(TAG_READ_ANALOG_INPUT_BLOCK_A)
        protocol_interpreter.PI_send_message(data, len(data), id_dest)
        data = []
        data.append(TAG_READ_ANALOG_INPUT_BLOCK_B)
        protocol_interpreter.PI_send_message(data, len(data), id_dest)

#end Requisção de leitura-----------------------------------------------------------------------------------------------

    # Função assincrona que realiza a transmissão de pacotes pela serial
    async def COM_communication(self):
        # print('Task Communication')
        # while (True):
        #     while(protocol_interpreter.PI_has_message_to_transmit() is True):
        #         protocol_interpreter.PI_trasmit_message()
        #         #time.sleep(0.01)
        #         await asyncio.sleep(0.005)
        #     await asyncio.sleep(0.05)
        # print("End task communication")
        while (True):
            protocol_interpreter.PI_trasmit_message()
            await asyncio.sleep(0.005)
        print("End task communication")

    # Função assincrona que monitora o recebimento de dados pela serial
    async def COM_receive_serial(self):
        # print('Task Monitoring Receive')
        protocol_interpreter.PI_set_serial_timeout(0.001)
        while (True):
            data_serial, size = protocol_interpreter.PI_receive_data()
            if size > 0:
                # print(data_serial)
                for data_byte in data_serial:
                    protocol_interpreter.PI_protocol_organize_receive_data(data_byte)

                    if protocol_interpreter.PI_message_arrived() is True:
                        data, size, id_source = protocol_interpreter.PI_read_message()
                        #print("Data: " + str(data) + " Size: " + str(size) + " Id: " + str(id_source))
                        if self.process_data_read(data, size, id_source) is False:
                            print("ERROR Tag")
            await asyncio.sleep(0.005)
        print("End task receive serial")

    async def print_test_async(self):
        while (True):
            print("Teste Async")
            await asyncio.sleep(3)


    def COM_read_list_modules(self):
        return self.list_modules

    def __init__(self, list_modules):

        self.list_modules = list_modules
        print(self.list_modules)
