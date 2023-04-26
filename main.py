import module_interface
from communication import Communication
import asyncio
import define_modules
from datetime import datetime

# Criação da lista de Modulos de Interface------------------------------------------------------------------------------
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

# print(list_modules)

# Cria o objeto da comunicação, envia a lista de objetos modulos
communication = Communication(list_modules)


# -----------------------------------------------------------------------------------------------------------------------


# rotinas TASKs---------------------------------------------------------------------------------------------------------

# Realiza a requisição de dados dos Modulos (loop)
async def request_data_from_modules():
    sleep = 0.04
    print('Task Request Data from Modules')
    # request_data()
    communication.COM_read_FW(list_modules[0].id)
    while (True):
        # print("Init time")
        # print(datetime.utcnow().isoformat(sep=' ', timespec='milliseconds'))

        # for idx in range(len(list_modules)):
        #     communication.COM_read_FW(list_modules[idx].id)
        #     await asyncio.sleep(sleep)
        #     communication.COM_read_digital_outputs(list_modules[idx].id)
        #     await asyncio.sleep(sleep)
        #     communication.COM_read_digital_inputs(list_modules[idx].id)
        #     await asyncio.sleep(sleep)
        #     communication.COM_read_analog_outputs(list_modules[idx].id)
        #     await asyncio.sleep(sleep)
        #     communication.COM_read_analog_inputs(list_modules[idx].id)
        #     await asyncio.sleep(sleep)
        #     communication.COM_write_analog_output_1(list_modules[idx].id, 125)
        #     await asyncio.sleep(sleep)
        #     communication.COM_write_analog_output_2(list_modules[idx].id, 150)
        #     await asyncio.sleep(sleep)
        #     #communication.COM_write_digital_outputs(list_modules[idx].id, 15794115)
        #     communication.COM_write_digital_outputs(list_modules[idx].id, 15790320)
        #     await asyncio.sleep(1)
        #     communication.COM_write_digital_outputs(list_modules[idx].id, 986895)
        #     await asyncio.sleep(1)
        #     await asyncio.sleep(2*sleep)

        idx=idxm_water_purificator
        communication.COM_read_FW(list_modules[idx].id)
        await asyncio.sleep(sleep)
        communication.COM_read_digital_outputs(list_modules[idx].id)
        await asyncio.sleep(sleep)
        communication.COM_read_digital_inputs(list_modules[idx].id)
        await asyncio.sleep(sleep)
        communication.COM_read_analog_outputs(list_modules[idx].id)
        await asyncio.sleep(sleep)
        communication.COM_read_analog_inputs(list_modules[idx].id)
        await asyncio.sleep(sleep)
        communication.COM_write_analog_output_1(list_modules[idx].id, 125)
        await asyncio.sleep(sleep)
        communication.COM_write_analog_output_2(list_modules[idx].id, 150)
        await asyncio.sleep(sleep)
        #communication.COM_write_digital_outputs(list_modules[idx].id, 90)
        communication.COM_write_digital_outputs(list_modules[idx].id, 15790320)
        await asyncio.sleep(1)
        communication.COM_write_digital_outputs(list_modules[idx].id, 986895)
        await asyncio.sleep(1)
        await asyncio.sleep(2*sleep)
        # print("Final Time")
        # print(datetime.utcnow().isoformat(sep=' ', timespec='milliseconds'))
        # delay while
        await asyncio.sleep(0.5)
    print("End Requests")


# Printa informações dos modulos (teste)
async def print_info_modules():
    print('Task Print Infos')
    while True:
        for idx in range(len(list_modules)):
            print("Module name: " + list_modules[idx].name + " id:" + str(list_modules[idx].id))
            print("     Analog Inputs: ")
            print(list_modules[idx].analog_input)
            # for i in range(len(list_modules[idx].analog_input)):
            # print(list_modules[idx].analog_input[i])
        await asyncio.sleep(1)


# Atualiza a lista de modulos a partir das modificações da lista pela Comunicação
# não necessario, pois o obejeto alterado em comunicação é o meemo enviado????
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
    # Cria lista de tarefas
    # tasks = [request_data_from_modules(), communication.COM_receive_serial(), communication.COM_communication(), print_test_async()]
    tasks = [request_data_from_modules(), communication.COM_communication(), print_info_modules(),
             communication.COM_receive_serial()]
    # tasks = [request_data_from_modules(), communication.COM_receive_serial(), communication.COM_communication()]
    res = await asyncio.gather(*tasks, return_exceptions=True)
    return res


# --------------------------------------------------------------------------------------------------

# main
if __name__ == '__main__':

    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(main_tasks())
        loop.run_until_complete(loop.shutdown_asyncgens())
    finally:
        loop.close()
