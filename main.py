import module_interface
import communication
import asyncio
from datetime import datetime


#identificadores, id dos modulos
ID_PC = 0x01
ID_WATER_PURIFICATOR = 0x02
ID_ELECTROLIZER = 0x03
ID_MOTOR_SENSES = 0x04
ID_GAS_SENSES = 0x05
ID_PEM_POWER_CONTROL = 0x06


#ciar a lista de modulos, com nomes, id e indexes-----------------------------------------------------------------------
module_names = ["Purificador de Água", "Eletrolizador", "Interface Motor", "Potência-PEM", "Monitoramneto de Gases"]
module_id = [ID_WATER_PURIFICATOR, ID_ELECTROLIZER, ID_MOTOR_SENSES, ID_PEM_POWER_CONTROL, ID_GAS_SENSES]

list_modules=[]

for name in module_names:
    if name == "Purificador de Água":
        list_modules.append(module_interface.ModuleInterface(name, ID_WATER_PURIFICATOR))
        idxm_water_purificator = 0
    elif name == "Eletrolizador":
        list_modules.append(module_interface.ModuleInterface(name, ID_ELECTROLIZER))
        idxm_electrolizer = 1
    elif name == "Interface Motor":
        list_modules.append(module_interface.ModuleInterface(name, ID_MOTOR_SENSES))
        idxm_motor = 2
    elif name == "Potência-PEM":
        list_modules.append(module_interface.ModuleInterface(name, ID_PEM_POWER_CONTROL))
        idxm_pem = 3
    elif name == "Monitoramneto de Gases":
        list_modules.append(module_interface.ModuleInterface(name, ID_GAS_SENSES))
        idxm_gases = 4
#-----------------------------------------------------------------------------------------------------------------------

def update_firmware(firmware, id_source):
    index = module_id.index(id_source)
    #print("Index : "+str(index))
    #print("Module name Firmware Update: " + list_modules[index].name + " id:" + str(list_modules[index].id))
    list_modules[index].firmware = firmware
    #print("Update firmware")

def update_digital_outputs(outputs, id_source):
    index = module_id.index(id_source)
    list_modules[index].digital_output = outputs
    #print("Update digital outputs")

def update_digital_inputs(inputs, id_source):
    index = module_id.index(id_source)
    list_modules[index].digital_input = inputs
    #print("Update digital inputs")



#rotinas TASKs-------------------------------------------------------------------------------------
async def request_data_from_modules():
    #print('Task Request Data from Modules')
    # request_data()
    while (True):
        print("Init time")
        print(datetime.utcnow().isoformat(sep=' ', timespec='milliseconds'))
        for idx in range(len(list_modules)):
            #print(f"init at {time.strftime('%X')}")

            communication.COM_read_FW(list_modules[idx].id)
            #print(f"finished at {time.strftime('%X')}")

            await asyncio.sleep(0)
            communication.COM_read_digital_outputs(list_modules[idx].id)
            await asyncio.sleep(0)
            communication.COM_read_digital_inputs(list_modules[idx].id)
            await asyncio.sleep(0)
        print("Final Time")
        print(datetime.utcnow().isoformat(sep=' ', timespec='milliseconds'))
        #delay while
        await asyncio.sleep(0.5)
    print("End Requests")

async def print_test_async():
    while (True):
        print("Teste Async")
        await asyncio.sleep(0)

#--------------------------------------------------------------------------------------------------

#Task principal, roda as demais tasks--------------------------------------------------------------
async def main_tasks():
    #tasks = [request_data_from_modules(), communication.COM_receive_serial(), communication.COM_communication(), print_test_async()]
    tasks = [request_data_from_modules(), communication.COM_receive_serial(), communication.COM_communication()]
    res = await asyncio.gather(*tasks, return_exceptions=True)

    return res
    #await request_data_from_modules()
    #await communication.COM_communication()
    #await print_test_async()

#loop=asyncio.get_event_loop()
#loop.run_until_complete(main_communication())
#--------------------------------------------------------------------------------------------------

#main
if __name__ == '__main__':
    #list_modules=[]

    #list_modules.append(module_interface.ModuleInterface("Purificador de Água", communication.ID_WATER_PURIFICATOR))

    print("Module name: "+module_interface.ModuleInterface.name+" id:"+str(module_interface.ModuleInterface.id))

    for idx in range(len(list_modules)):
        print("Module name: "+list_modules[idx].name+" id:"+str(list_modules[idx].id))

    print("Module name: " + list_modules[idxm_pem].name + " id:" + str(list_modules[idxm_pem].id))


    res = asyncio.get_event_loop().run_until_complete(main_tasks())
    print(res)

    # while True:
    #
    #     for idx in range(len(list_modules)):
    #         print("Module name: " + list_modules[idx].name + " id:" + str(list_modules[idx].id))
    #     communication.COM_read_FW()


