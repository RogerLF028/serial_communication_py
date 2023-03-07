
ANALOG_INPUT_SIZE = 16
ANALOG_OUTPUT_SIZE = 4
DIGITAL_INPUT_SIZE = 8
DIGITAL_OUTPUT_SIZE = 24
class ModuleInterface:

    def __init__(self, name, id):

        self.analog_input = [0 for x in range(ANALOG_INPUT_SIZE)]
        self.analog_output = [0 for x in range(ANALOG_OUTPUT_SIZE)]
        self.digital_input = [False for x in range(DIGITAL_INPUT_SIZE)]
        self.digital_output = [False for x in range(DIGITAL_OUTPUT_SIZE)]
        self. firmware = [0, 0, 0]

        self.digital_outputs_has_been_written = False
        self.analog_output1_has_been_written = False
        self.analog_output2_has_been_written = False
        self.analog_output3_has_been_written = False
        self.analog_output4_has_been_written = False

        print("chamada inicial dos modulos")
        print(self.analog_input)
        print(self.analog_output)
        print(self.digital_input)
        print(self.digital_output)

        self.name = name
        self.id = id