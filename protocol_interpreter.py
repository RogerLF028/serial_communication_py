import serial
from enum import Enum


# Definição da porta serial---------------------------------------------------------------------------------------------
HOST = "WINDOWS"
PORT_LINUX = '/dev/ttyUSB0'
PORT_WINDOWS = 'COM3'
BAUDRATE = 115200

# configuração da Serial
if HOST == "LINUX":
    serial_port = serial.Serial(
        port=PORT_LINUX, baudrate=BAUDRATE, bytesize=serial.EIGHTBITS, timeout=2, stopbits=serial.STOPBITS_ONE,
        parity=serial.PARITY_NONE,
    )
elif HOST == "WINDOWS":
    serial_port = serial.Serial(
        port=PORT_WINDOWS, baudrate=BAUDRATE, bytesize=serial.EIGHTBITS, timeout=2, stopbits=serial.STOPBITS_ONE,
        parity=serial.PARITY_NONE,
    )

serial_port.read_all()
serial_port.flush()
#-----------------------------------------------------------------------------------------------------------------------

id_communication = 0x01  # Id do PC

ID_ERROR = 0xFF

SIZE_PROTOCOL_HEADER = 7  # 4 sync + 1 dest_id + 1 source_id + 1 size
SIZE_CHECKSUM = 1

# Definição dos bytes de sincronismo
PROTOCOL_SYNC1 = 0xAE
PROTOCOL_SYNC2 = 0xCA
PROTOCOL_SYNC3 = 0xFE
PROTOCOL_SYNC4 = 0xEA


class StatesOfProtocol(Enum):
    SYNC1 = 0
    SYNC2 = 1
    SYNC3 = 2
    SYNC4 = 3
    DEST_ID = 4
    SOURCE_ID = 5
    SIZE = 6
    DATA = 7
    CHECKSUM = 8


protocol_state = StatesOfProtocol.SYNC1

BUFFER_SIZE = 50
QTY_PACKETS = 10 * 3


class DataMsgType:
    def __init__(self):
        self.data_msg_buffer = [0 for x in range(BUFFER_SIZE)]
        self.idx_data_msg = None
        self.data_size = None
        self.msg_check = False
        self.checksum = None
        self.source_id = None
        self.dest_id = None


# struct de msg transmitida
class DataToTransmitType:
    def __init__(self):
        self.tx_buffer = [0 for x in range(BUFFER_SIZE + SIZE_PROTOCOL_HEADER + SIZE_CHECKSUM)]
        self.data_size = None
        self.idx_tx = None


# lista de msg rx
message_rx = []
for i in range(QTY_PACKETS):
    message_rx.append(DataMsgType())
print(message_rx)
# lista de msg tx
message_tx = []
for i in range(QTY_PACKETS):
    message_tx.append(DataToTransmitType())
print(message_tx)

# rx
receive_packet = 0  # indice do pacote recebido na lista de msg
read_packet = 0  # indice do pacote lido na lista de msg
# tx
transmit_packet = 0  # indice do pacote a ser trasnmitido na lista de msg
write_packet = 0  # indice do pacote escrito na lista de msg

# seta o id (PC-Pyhton)
def PI_set_id_communication(id):
    global id_communication
    id_communication = id


# prepara uma mensagem para ser transmitida
# coloca o cabeçalho
# calcula checksum
def PI_send_message(data, size, dest):
    global write_packet
    clear_tx_buffer(write_packet)

    # cabeçalho
    message_tx[write_packet].tx_buffer[0] = PROTOCOL_SYNC1
    message_tx[write_packet].tx_buffer[1] = PROTOCOL_SYNC2
    message_tx[write_packet].tx_buffer[2] = PROTOCOL_SYNC3
    message_tx[write_packet].tx_buffer[3] = PROTOCOL_SYNC4
    message_tx[write_packet].tx_buffer[4] = dest
    message_tx[write_packet].tx_buffer[5] = id_communication
    message_tx[write_packet].tx_buffer[6] = size

    # data e checksum
    checksum = size
    for i in range(size):
        message_tx[write_packet].tx_buffer[i + SIZE_PROTOCOL_HEADER] = data[i]
        checksum += data[i]
    # checksum
    checksum = ((~checksum) + 1) & 0xFF
    message_tx[write_packet].tx_buffer[SIZE_PROTOCOL_HEADER + size] = checksum
    message_tx[write_packet].data_size = SIZE_PROTOCOL_HEADER + size + SIZE_CHECKSUM

    # print("Write packet:"+str(message_tx[write_packet].tx_buffer))

    # incrementa contagem de pacotes escrito - a ser enviado
    write_packet += 1
    if write_packet >= QTY_PACKETS:
        write_packet = 0
    # print(f"write_packet {write_packet}")


# trasnmite as mensagens inteira armazendas na lista de envio - blocking
def PI_trasmit_message():
    global transmit_packet, write_packet

    # vefirica se há diferença entre pacote transmitido e escrito
    if transmit_packet != write_packet:
        # envia o buffer de transmissão completo na usart
        # equivalente -> io_write(&SERIAL.io, message_tx[transmit_packet].tx_buffer, message_tx[transmit_packet].data_size)
        serial_port.write(message_tx[transmit_packet].tx_buffer[0:message_tx[transmit_packet].data_size])
        # print(message_tx[transmit_packet].tx_buffer[0:message_tx[transmit_packet].data_size])
        # print("Transmit packet:" + str(message_tx[transmit_packet].tx_buffer))
        # incrementa contagem de pacote enviado
        transmit_packet += 1
        if transmit_packet >= QTY_PACKETS:
            transmit_packet = 0
        # print(f"transmit_packet {transmit_packet}")

# Verifica se há msg para transmitir
def PI_has_message_to_transmit():
    if transmit_packet != write_packet:
        return True
    else:
        return False


# trasnmite as mensagens armazendas na lista de envio byte a byte - non blocking
def PI_transmit_message_byte_to_byte():
    global transmit_packet, write_packet
    # vefirica se há diferença entre pacote transmitido e escrito
    if transmit_packet != write_packet:
        # envia 1 byte do buffer de transmissão na usart
        # equivalente->io_write(&SERIAL.io, &message_tx[transmit_packet].tx_buffer[message_tx[transmit_packet].idx_tx],1)
        serial_port.write(message_tx[transmit_packet].tx_buffer[message_tx[transmit_packet].idx_tx])
        # incrmenta contador de bytes
        message_tx[transmit_packet].idx_tx += 1
        # verifica se já transmitiu todo o buffer
        if message_tx[transmit_packet].idx_tx > message_tx[transmit_packet].data_size:
            # incrementa contagem de pacote enviado
            transmit_packet += 1
            if transmit_packet >= QTY_PACKETS:
                transmit_packet = 0

# Lê um byte
def PI_receive_data_byte():
    data_byte = serial_port.read(1)
    return data_byte

# Lê uma sequencia de bytes
def PI_receive_data():
    data_bytes = serial_port.readline()
    size = len(data_bytes)
    return data_bytes, size


# Limpa a struct das mensagens recebidas
def clear_message_rx(packet):
    message_rx[packet].idx_data_msg = 0
    message_rx[packet].data_size = 0
    message_rx[packet].checksum = 0
    message_rx[packet].msg_check = False


# Limpa a struct das mensagens transmitidas
def clear_tx_buffer(packet):
    # print(f"Clear TX Buffer packet {packet}")
    message_tx[packet].tx_buffer = [0 for x in range(BUFFER_SIZE + SIZE_PROTOCOL_HEADER + SIZE_CHECKSUM)]
    message_tx[packet].idx_tx = 0
    message_tx[packet].data_size = 0


# verifica se recebeu uma mensagem (passou pelo checksum)
def PI_message_arrived():
    return message_rx[read_packet].msg_check


# Verifica se recebeu algo na serial, se sim retorna os dados recebidos
def PI_is_serial_receive():
    data = serial_port.readline()
    if data:
        return data
    else:
        return False

# Altera o valor de Timeout da Serial (timeout é blocking)
def PI_set_serial_timeout(time):
    serial_port.timeout = time


# lê uma mensagem, retorna o tamanho da msg
# tambem retorna o valor de id de origem da msg, junto com os dados da msg
def PI_read_message():
    # data, size, id_source = None
    global read_packet, receive_packet

    # vefirica se há diferença entre pacote recebido e lido
    if read_packet != receive_packet:
        # atualiza o tamanho da msg
        size = message_rx[read_packet].data_size
        # print("Size: "+str(size))
        # lê a msg do buffer rx
        data = message_rx[read_packet].data_msg_buffer[0:size]
        # print("Data: " + str(data))
        # Lê de qual id foi recebido a msg
        id_source = message_rx[read_packet].source_id
        # print("ID: " + str(id_source))
        # limpa a mensagem
        clear_message_rx(read_packet)
        # incrementa a contagem de msg lida
        read_packet += 1
        if read_packet >= QTY_PACKETS:
            read_packet = 0
    return data, size, id_source

# Função que realiza a interpretação do protocolo
def PI_protocol_organize_receive_data(data):
    global protocol_state, receive_packet

    # Sincronismo
    if protocol_state == StatesOfProtocol.SYNC1:
        if data == PROTOCOL_SYNC1:
            protocol_state = StatesOfProtocol.SYNC2
    elif protocol_state == StatesOfProtocol.SYNC2:
        if data == PROTOCOL_SYNC2:
            protocol_state = StatesOfProtocol.SYNC3
        else:
            protocol_state = StatesOfProtocol.SYNC1
    elif protocol_state == StatesOfProtocol.SYNC3:
        if data == PROTOCOL_SYNC3:
            protocol_state = StatesOfProtocol.SYNC4
        else:
            protocol_state = StatesOfProtocol.SYNC1
    elif protocol_state == StatesOfProtocol.SYNC3:
        if data == PROTOCOL_SYNC3:
            protocol_state = StatesOfProtocol.SYNC4
        else:
            protocol_state = StatesOfProtocol.SYNC1
    elif protocol_state == StatesOfProtocol.SYNC4:
        if data == PROTOCOL_SYNC4:
            protocol_state = StatesOfProtocol.DEST_ID
            # clear message
            clear_message_rx(receive_packet)
        else:
            protocol_state = StatesOfProtocol.SYNC1
    # fim do sincronismo
    # verificação de id
    elif protocol_state == StatesOfProtocol.DEST_ID:
        if data == id_communication:
            message_rx[receive_packet].dest_id = data
            protocol_state = StatesOfProtocol.SOURCE_ID
        else:
            protocol_state = StatesOfProtocol.SYNC1
    elif protocol_state == StatesOfProtocol.SOURCE_ID:
        message_rx[receive_packet].source_id = data
        protocol_state = StatesOfProtocol.SIZE
    # tamanho da msg
    elif protocol_state == StatesOfProtocol.SIZE:
        message_rx[receive_packet].data_size = data
        message_rx[receive_packet].checksum += data
        protocol_state = StatesOfProtocol.DATA
    # inicio dos dados
    elif protocol_state == StatesOfProtocol.DATA:
        message_rx[receive_packet].data_msg_buffer[message_rx[receive_packet].idx_data_msg] = data
        message_rx[receive_packet].checksum += data
        message_rx[receive_packet].idx_data_msg += 1
        if message_rx[receive_packet].idx_data_msg < message_rx[receive_packet].data_size:
            protocol_state = StatesOfProtocol.DATA
        else:
            message_rx[receive_packet].idx_data_msg = 0
            protocol_state = StatesOfProtocol.CHECKSUM
    elif protocol_state == StatesOfProtocol.CHECKSUM:
        if (((~message_rx[receive_packet].checksum) + 1) & 0xFF) == data:
            message_rx[receive_packet].msg_check = True
            # print('CheckSum OK!!');
            # incrementa contagem de pacote recebido
            receive_packet += 1
            if receive_packet >= QTY_PACKETS:
                receive_packet = 0
        protocol_state = StatesOfProtocol.SYNC1
    else:  # default
        protocol_state = StatesOfProtocol.SYNC1
