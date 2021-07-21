#!/usr/bin/python3

from piclap import *
from gpiozero import LED
import _thread as thread
import pyaudio

class MY_Device(Device):
    def __init__(self, config, calibrate):
        self.config = config
        self.input = pyaudio.PyAudio()
        self.maxSamples = []
        self.__setInputDevice()
    
    def __setInputDevice(self):
        """Test for host api and input device support. If the supported host api and input device are available, default input device information is set"""
        if self.input.get_host_api_count() < 1:
            print("No supported PortAudio Host APIs are found in your system")
            sys.exit(1)
        if self.input.get_device_count() < 1:
            print("No input audio device is found in your system")
            sys.exit(1)
        self.defaultDevice = self.input.get_default_input_device_info()
        self.config.channels = int(self.defaultDevice['maxInputChannels'])
        self.config.rate = int(self.defaultDevice['defaultSampleRate'])



class My_Listener(Listener):
    def __init__(self, config=None, calibrate=True):
        self.config = config or Settings()
        self.claps = 0
        self.lock = thread.allocate_lock()
        self.device = MY_Device(self.config, calibrate)
        self.processor = SignalProcessor(method=self.config.method)
        self.confirm()

    def __myprintInfo(self):
        print("\n--------------------------------------------------------------\n")
        print("Default Device\t\t:", self.device.defaultDevice['name'])
        print("Channels\t\t:", self.config.channels)
        print("Chunk size\t\t:", self.config.chunk_size, "bytes")
        print("Rate\t\t\t:", self.config.rate, "Hz")
        print("Clap wait\t\t:", self.config.wait, "sec")
        print("Algorithm selected\t:", self.config.method.name)
        print("Threshold Value\t\t:", self.config.method.value, "\n")

    def confirm(self):
        self.__myprintInfo()
        print("Start now")

class Config(Settings):
    '''Describes custom configurations and action methods to be executed based
    on the number of claps detected.
    '''

    def __init__(self):
        super().__init__()
        self.rate = 44100           # Number of audio samples collected in 1 second
        self.chunk_size = 512       # Reduce as power of 2 if pyaudio overflow
        self.wait = 0.6             # Adjust wait between claps
        self.method.value = 6400    # Threshold value adjustment
        #self.method.value = 6368    # Threshold value adjustment
    
    def confirm(self):
        print("DDDDDDDDD")

    def on1Claps(self):
        '''Custom action for 1 claps'''
        print("Custom action for 1 claps")

    def on2Claps(self):
        '''Custom action for 2 claps'''
        print("Custom action for 2 claps")

    def on3Claps(self):
        '''Custom action for 3 claps'''
        print("Custom action for 3 claps")

    def on5Claps(self):
        '''Custom action for 5 claps'''
        print("Custom action for 5 claps")


def main():
    listener = My_Listener(Config(), calibrate=False)
    listener.start()


if __name__ == '__main__':
    main()
