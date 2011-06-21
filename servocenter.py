import serial

def calc_checksum(data):
    """
    Calculate data checksum
    """
    checksum = 0
    for byte in data:
        checksum += ord(byte)
    return (checksum % 239) + 1

class ServoController(object):
    def __init__(self, comm, baud):
        """
        Create a ServoController and open the serial port
        """
        self.ser=serial.Serial(comm, baud, timeout=1)

    def close(self):
        """
        Close the serial port
        """
        self.ser.close()

    def read(self, size=1):
        """
        Read the specified number of bytes (blocking)
        """
        return self.ser.read(size)

    def read_buffered(self):
        """
        Read buffered data
        """
        data=''
        buff=self.read()
        while buff:
            data+=buff
            buff=self.read()
        return data

    def board_command(self, boardid, command, data=''):
        """
        Send a command with data to the specified board
        """
        commandstr = '%c%c%s' % (chr(boardid%16+240),
            chr(command), data)
        commandstr += chr(calc_checksum(commandstr))
        # send the packet
        self.ser.write(commandstr)

    def servo_command(self, boardid, servonum, command, data=''):
        """
        Send a servo command with data to the specified board and servo
        """
        self.board_command(boardid, command, '%c%s' \
            % (chr(15 if servonum==15 else servonum%15), data))

    # Begin methods for each command available to the board

    def quick_move(self, boardid, servonum, servopos):
        self.servo_command(boardid, servonum, 0, 
            chr(200 if servopos==200 else servopos%200))

    def scaled_quick_move(self, boardid, servonum, servopos):
        self.servo_command(boardid, servonum, 1,
            chr(100 if servopos==100 else servopos%100))

    def servo_enable(self, boardid, servonum):
        self.servo_command(boardid, servonum, 2)

    def servo_disable(self, boardid, servonum):
        self.servo_command(boardid, servonum, 3)

    def set_min(self, boardid, servonum, servopos):
        self.servo_command(boardid, servonum, 4,
            chr(200 if servopos==200 else servopos%200))

    def set_max(self, boardid, servonum, servopos):
        self.servo_command(boardid, servonum, 5,
            chr(200 if servopos==200 else servopos%200))

    def set_start(self, boardid, servonum, servopos):
        self.servo_command(boardid, servonum, 6,
            chr(200 if servopos==200 else servopos%200))

    def set_maximum_speed(self, boardid, servonum, maxspeed):
        self.servo_command(boardid, servonum, 7,
            chr(200 if maxspeed==200 else maxspeed%200))

    def set_minimum_to_current(self, boardid, servonum):
        self.servo_command(boardid, servonum, 8)

    def set_maximum_to_current(self, boardid, servonum):
        self.servo_command(boardid, servonum, 9)

    def set_start_to_current(self, boardid, servonum):
        self.servo_command(boardid, servonum, 10)

    def get_current_position(self, boardid, servonum):
        self.servo_command(boardid, servonum, 11)
        return ord(self.read())

    def get_min_position(self, boardid, servonum):
        self.servo_command(boardid, servonum, 12)
        return ord(self.read())

    def get_max_position(self, boardid, servonum):
        self.servo_command(boardid, servonum, 13)
        return ord(self.read())

    def get_start_position(self, boardid, servonum):
        self.servo_command(boardid, servonum, 14)
        return ord(self.read())

    def get_max_speed(self, boardid, servonum):
        self.servo_command(boardid, servonum, 15)
        return ord(self.read())

    def move_raw(self, boardid, servonum, servopos, servospeed):
        self.servo_command(boardid, servonum, 16,
            '%c%c' % (chr(200 if servopos==200 else servopos%200),
            chr(100 if servospeed==100 else servospeed%100)))

    def move_raw_cw(self, boardid, servonum, servopos, servospeed):
        self.servo_command(boardid, servonum, 17,
            '%c%c' % (chr(200 if servopos==200 else servopos%200),
            chr(100 if servospeed==100 else servospeed%100)))

    def move_raw_ccw(self, boardid, servonum, servopos, servospeed):
        self.servo_command(boardid, servonum, 18,
            '%c%c' % (chr(200 if servopos==200 else servopos%200),
            chr(100 if servospeed==100 else servospeed%100)))

    def move_scaled(self, boardid, servonum, servopos, servospeed):
        self.servo_command(boardid, servonum, 19,
            '%c%c' % (chr(100 if servopos==100 else servopos%100),
            chr(100 if servospeed==100 else servospeed%100)))

    def move_scaled_cw(self, boardid, servonum, servopos, servospeed):
        self.servo_command(boardid, servonum, 20,
            '%c%c' % (chr(100 if servopos==100 else servopos%100),
            chr(100 if servospeed==100 else servospeed%100)))

    def move_scaled_ccw(self, boardid, servonum, servopos, servospeed):
        self.servo_command(boardid, servonum, 21,
            '%c%c' % (chr(100 if servopos==100 else servopos%100),
            chr(100 if servospeed==100 else servospeed%100)))

    def set_pulse_width_min(self, boardid, pulsewidth):
        self.board_command(boardid, 22,
            chr(239 if pulsewidth==239 else pulsewidth%239))

    def set_pulse_width_min(self, boardid, pulsewidth):
        self.board_command(boardid, 23,
            chr(239 if pulsewidth==239 else pulsewidth%239))

    def servo_invert(self, boardid, servonum):
        self.servo_command(boardid, servonum, 24)

    def servo_uninvert(self, boardid, servonum):
        self.servo_command(boardid, servonum, 25)

    def show_settings(self, boardid):
        self.board_command(boardid, 235)
        return self.read_buffered()

    def commit_settings(self, boardid):
        self.board_command(boardid, 236)

    def load_factory_settings(self, boardid):
        self.board_command(boardid, 237)

    def reset_as_startup(self, boardid):
        self.board_command(boardid, 238)

    def display_version(self, boardid):
        self.board_command(boardid, 239)
        return self.read_buffered()

