import serial
import serial_protocol
import asyncio

BLOCKING = 0x00
NON_BLOCKING = 0x01

mode_of_transmit = BLOCKING;



# Equivalente ao Callback da interrupção de RX
def serial_rx_callback_irq():
    # equivalente -> io_read(&SERIAL.io, &data_byte, 1)
    data_byte = serial_protocol.SP_receive_data_byte()
    serial_protocol.SP_protocol_organize_receive_data(data_byte)

    if serial_protocol.SP_message_arrived() is True:
        data, size, id_source = serial_protocol.SP_read_message()
        # process_data_read(data, size, id_source)


def request_data():
    data = [0x10, 0x07, 0x08]
    dest = 0x02
    serial_protocol.SP_send_message(data, len(data), dest)


async def communication():
    print('Olá ...')
    print('... Mundo!')
    #request_data()
    while (True):
        request_data()
        serial_protocol.SP_trasmit_message()
        await asyncio.sleep(2)
    print("End")

async def print_test_async():
    while(True):
        print("Teste Async")
        await  asyncio.sleep(3)

#asyncio.run(communication(), print_test_async())
#asyncio.run(print_test_async())

async def main():
    await communication()
    await print_test_async()
    # await asyncio.wait([
    #     communication(),
    #     print_test_async()
    # ])

loop=asyncio.get_event_loop()
loop.run_until_complete(main())