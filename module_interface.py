
class ModuleInterface:
    firmware = [0,0,0]
    name = "name"
    id = 0x00
    def __init__(self, name, id):
        analog_input = []
        for i in range(16):
            analog_input.append(0)
        #print(analog_input)

        analog_output = []
        for i in range(4):
            analog_output.append(0)
        #print(analog_output)

        digital_output = []
        for i in range(24):
            digital_output.append(False)
        #print(digital_output)

        digital_input = []
        for i in range(8):
            digital_input.append(False)
        #print(digital_input)

        self.name = name
        self.id=  id