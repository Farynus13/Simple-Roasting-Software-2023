import minimalmodbus
import serial.tools.list_ports
from enum import Enum,IntEnum


BAUD_RATE_list = [1200,2400,4800,9600,19200,38400,57600,57800,115200]
BYTE_SIZE_list = [7,8]
PARITY_list = ['N','E','O']
STOP_BITS_list = [1,2]
MODBUS_FUNCTION_list = [1,2,3,4]
DIVIDER_list = [1/10,1/100]
MODE_list = ["C","F"]

class Modbus() :
    
    def __init__(self) :
        #setting default values
        self.drum_slave = None
        self.air_slave = None
        self.burner_slave = None

        self.et_slave = None
        self.bt_slave = None
        self.com_port = "COM9"
        self.baud_rate = 9600
        self.byte_size = 8
        self.parity = "N"
        self.stop_bits = 1
        self.timeout = 0.4
        self.__set_slave([1,2])
        self.__set_register([4096,4096])
        self.__set_modbus_function([3,3])
        self.__set_divider([1/10,1/10])
        self.__set_mode(["C","C"])
        # function for listing avaiable com ports
        # [comport.device for comport in serial.tools.list_ports.comports()]

    #setters
    def __set_com_port(self,com_port) :
        self.__com_port = com_port
    def __set_baud_rate(self,baud_rate) :
        self.__baud_rate = baud_rate
    def __set_byte_size(self,byte_size) :
        self.__byte_size = byte_size
    def __set_parity(self,parity) :
        self.__parity = parity
    def __set_stop_bits(self,stop_bits) :
        self.__stop_bits = stop_bits
    def __set_timeout(self,timeout) :
        self.__timeout = timeout
    def __set_slave(self,slave) :
        self.__slave = slave
    def __set_register(self,register) :
        self.__register = register
    def __set_modbus_function(self,modbus_function) :
        self.__modbus_function = modbus_function
    def __set_divider(self,divider) :
        self.__divider = divider
    def __set_mode(self,mode) :
        self.__mode = mode

    #getters
    def __get_com_port(self) :
        return self.__com_port
    def __get_baud_rate(self) :
        return self.__baud_rate
    def __get_byte_size(self) :
        return self.__byte_size
    def __get_parity(self) :
        return self.__parity
    def __get_stop_bits(self) :
        return self.__stop_bits
    def __get_timeout(self) :
        return self.__timeout
    def __get_slave(self) :
        return self.__slave
    def __get_register(self) :
        return self.__register
    def __get_modbus_function(self) :
        return self.__modbus_function
    def __get_divider(self) :
        return self.__divider
    def __get_mode(self) :
        return self.__mode

    #properties
    com_port = property(__get_com_port,__set_com_port)
    baud_rate = property(__get_baud_rate,__set_baud_rate)
    byte_size = property(__get_byte_size,__set_byte_size)
    parity = property(__get_parity,__set_parity)
    stop_bits = property(__get_stop_bits,__set_stop_bits)
    timeout = property(__get_timeout,__set_timeout)
    slave = property(__get_slave,__set_slave)
    register = property(__get_register,__set_register)
    modbus_function = property(__get_modbus_function,__set_modbus_function)
    divider = property(__get_divider,__set_divider)
    mode = property(__get_mode,__set_mode)

    def connect_slaves(self) :
        try:
            print("connecting slaves!")
            self.et_slave = minimalmodbus.Instrument(self.com_port,2,mode=minimalmodbus.MODE_RTU)
            self.bt_slave = minimalmodbus.Instrument(self.com_port,1,mode=minimalmodbus.MODE_RTU)
            self.air_slave = minimalmodbus.Instrument(self.com_port,5,mode=minimalmodbus.MODE_RTU)
            self.drum_slave = minimalmodbus.Instrument(self.com_port,4,mode=minimalmodbus.MODE_RTU)
            self.burner_slave = minimalmodbus.Instrument(self.com_port,3,mode=minimalmodbus.MODE_RTU)
            self.initialize_slave(self.et_slave)         
            self.initialize_slave(self.bt_slave)
            self.initialize_slave(self.air_slave)         
            self.initialize_slave(self.drum_slave)         
            self.initialize_slave(self.burner_slave)         

        except ValueError: 
            print("communication error!")

    def disconnect_slaves(self) :
        print("slaves released!")
        self.et_slave = None
        self.bt_slave = None
        self.air_slave = None
        self.drum_slave = None
        self.burner_slave = None

    def initialize_slave(self, slave) :
        slave.serial.baudrate = self.baud_rate
        slave.serial.bytesize = self.byte_size
        if self.parity == "N":
            slave.serial.parity = minimalmodbus.serial.PARITY_NONE
        elif self.parity == "O":
            slave.serial.parity = minimalmodbus.serial.PARITY_ODD
        elif self.parity == "E":
            slave.serial.parity = minimalmodbus.serial.PARITY_EVEN
        slave.serial.stopbits = self.stop_bits
        slave.serial.timeout = self.timeout
        slave.close_port_after_each_call = True
        slave.clear_buffers_before_ceach_transaction = True
        
    def read_temp(self,unit_id) :
        temp = -1.0 # if unit_id different than 1 or 2 reading will display -1.0
        if unit_id == 1 :
            try:
                temp = self.bt_slave.read_register(self.register[unit_id-1])
            except ValueError:
                print("problem connecting to registers")
        elif unit_id == 2 :
            try:
                temp = self.et_slave.read_register(self.register[unit_id-1])
            except ValueError:
                print("problem connecting to registers")
        return temp*self.divider[unit_id-1]
    
    def write_slave_register(self,unit_id,register,value):
        air_rules = unit_id == 5 & value >= 20 & value <= 50 
        drum_rules = unit_id == 4 & value >= 20 & value <= 50 
        burner_rules = unit_id == 3 & value >= 0 & value <= 100 
        if air_rules:
            self.air_slave.write_register(register,value*100)
        elif drum_rules : 
            self.drum_slave.write_register(register,value*100)
        elif burner_rules :
            print("fire)")