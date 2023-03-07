import module_interface
from communication import Communication
import asyncio
import define_modules
from datetime import datetime

list_modules = []

for name in define_modules.module_names:
    if name == "Purificador de Água":
        list_modules.append(module_interface.ModuleInterface(name, define_modules.ID_WATER_PURIFICATOR))
        idxm_water_purificator = 0
    elif name == "Eletrolizador":
        list_modules.append(module_interface.ModuleInterface(name, define_modules.ID_ELECTROLIZER))
        idxm_electrolizer = 1
    elif name == "Interface Motor":
        list_modules.append(module_interface.ModuleInterface(name, define_modules.ID_MOTOR_SENSES))
        idxm_motor = 2
    elif name == "Potência-PEM":
        list_modules.append(module_interface.ModuleInterface(name, define_modules.ID_PEM_POWER_CONTROL))
        idxm_pem = 3
    elif name == "Monitoramneto de Gases":
        list_modules.append(module_interface.ModuleInterface(name, define_modules.ID_GAS_SENSES))
        idxm_gases = 4

print(list_modules)
print(len(list_modules))

communication = Communication(list_modules)


# -----------------------------------------------------------------------------------------------------------------------

# def update_firmware(firmware, id_source):
#     index = define_modules.module_id.index(id_source)
#     #print("Index : "+str(index))
#     #print("Module name Firmware Update: " + list_modules[index].name + " id:" + str(list_modules[index].id))
#     list_modules[index].firmware = firmware
#     #print("Update firmware")
#
# def update_digital_outputs(outputs, id_source):
#     index = define_modules.module_id.index(id_source)
#     list_modules[index].digital_output = outputs
#     #print("Update digital outputs")
#
# def update_digital_inputs(inputs, id_source):
#     index = define_modules.module_id.index(id_source)
#     list_modules[index].digital_input = inputs
#     #print("Update digital inputs")
#
# def update_analog_output(analog_output, idx, id_source):
#     index = define_modules.module_id.index(id_source)
#     list_modules[index].analog_output[idx] = analog_output
#
# def update_analog_input(analog_input, idx, id_source):
#     index = define_modules.module_id.index(id_source)
#     list_modules[index].analog_input[idx] = analog_input


# rotinas TASKs-------------------------------------------------------------------------------------
async def request_data_from_modules():
    print('Task Request Data from Modules')
    # request_data()
    communication.COM_read_FW(list_modules[0].id)
    while (True):
        # print("Init time")
        # print(datetime.utcnow().isoformat(sep=' ', timespec='milliseconds'))

        for idx in range(len(list_modules)):
            communication.COM_read_FW(list_modules[idx].id)
            await asyncio.sleep(0)
            communication.COM_read_digital_outputs(list_modules[idx].id)
            await asyncio.sleep(0)
            communication.COM_read_digital_inputs(list_modules[idx].id)
            await asyncio.sleep(0)
            communication.COM_read_analog_outputs(list_modules[idx].id)
            await asyncio.sleep(0)
            communication.COM_read_analog_inputs(list_modules[idx].id)
            await asyncio.sleep(0)
            await asyncio.sleep(0.1)
        # print("Final Time")
        # print(datetime.utcnow().isoformat(sep=' ', timespec='milliseconds'))
        # delay while
        await asyncio.sleep(0.2)
    print("End Requests")


async def print_info_modules():
    print('Task Print Infos')
    while True:
        for idx in range(len(communication.list_modules)):
            print("Module name: " + communication.list_modules[idx].name + " id:" + str(communication.list_modules[idx].id))
            print("     Analog Inputs: ")
            print(communication.list_modules[idx].analog_input)
            #for i in range(len(list_modules[idx].analog_input)):
                #print(list_modules[idx].analog_input[i])
        await asyncio.sleep(1)


async def update_list_modules():
    while (True):
        list_modules = communication.COM_read_list_modules()
        await asyncio.sleep(0.005)


async def print_test_async():
    while (True):
        print("Teste Async")
        await asyncio.sleep(2)


# --------------------------------------------------------------------------------------------------

# Task principal, roda as demais tasks--------------------------------------------------------------
async def main_tasks():
    # tasks = [request_data_from_modules(), communication.COM_receive_serial(), communication.COM_communication(), print_test_async()]
    tasks = [request_data_from_modules(), communication.COM_communication(), print_info_modules(),
             communication.COM_receive_serial(), update_list_modules()]
    # tasks = [request_data_from_modules(), communication.COM_receive_serial(), communication.COM_communication()]
    res = await asyncio.gather(*tasks, return_exceptions=True)
    return res
    # await request_data_from_modules()
    # await communication.COM_communication()
    # await print_test_async()


# loop=asyncio.get_event_loop()
# loop.run_until_complete(main_communication())
# --------------------------------------------------------------------------------------------------

# main
if __name__ == '__main__':
    # list_modules=[]

    # tasks = [request_data_from_modules(), communication.COM_receive_serial(), communication.COM_communication()]
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(main_tasks())
        loop.run_until_complete(loop.shutdown_asyncgens())
    finally:
        loop.close()

    # list_modules.append(module_interface.ModuleInterface("Purificador de Água", communication.ID_WATER_PURIFICATOR))

    print("Module name: " + module_interface.ModuleInterface.name + " id:" + str(module_interface.ModuleInterface.id))

    for idx in range(len(list_modules)):
        print("Module name: " + list_modules[idx].name + " id:" + str(list_modules[idx].id))

    print("Module name: " + list_modules[idxm_pem].name + " id:" + str(list_modules[idxm_pem].id))

    res = asyncio.get_event_loop().run_until_complete(main_tasks())
    print(res)

    # while True:
    #
    #     for idx in range(len(list_modules)):
    #         print("Module name: " + list_modules[idx].name + " id:" + str(list_modules[idx].id))
    #     communication.COM_read_FW()
