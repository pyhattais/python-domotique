# Imports
import os
import glob
import time
import Led
from flask import render_template
from flask import Flask
from flask_socketio import SocketIO, send, emit
app = Flask(__name__)


class TemperatureSensor():

    def __init__(self, device_file='/sys/bus/w1/devices/28-01131a446afe/w1_slave'):
        os.system('modprobe w1-gpio')  # Allume le module 1wire
        os.system('modprobe w1-therm')
        self.device_file = device_file

    def read_temp_raw(self):
        f = open(self.device_file, 'r')  # Ouvre le fichier
        lines = f.readlines()  # Returns the text
        f.close()
        return lines

    # Lis la temperature
    def read_temp(self):
        lines = self.read_temp_raw()  # Lit le fichier de température
        # Tant que la première ligne ne vaut pas 'YES', on attend 0,2s
        # On relis ensuite le fichier
        while lines[0].strip()[-3:] != 'YES':
            time.sleep(0.2)
            lines = self.read_temp_raw()
        # On cherche le '=' dans la seconde ligne du fichier
        equals_pos = lines[1].find('t=')
        # Si le '=' est trouvé, on converti ce qu'il y a après le '=' en degrées celcius
        if equals_pos != -1:
            temp_string = lines[1][equals_pos + 2:]
            temp_c = float(temp_string) / 1000.0
            return round(temp_c, 1)

    def read_celcius(self):
        celcius = self.read_temp()
        if celcius < 15:
            lightb.on()
            lightr.off()
            return render_template('base.html')
        elif celcius > 30:
            lightb.off()
            lightr.on()
            return render_template('base.html')
        else:
            lightb.off()
            lightr.off()
            return render_template('base.html')

    def read_fahrenheit(self):
        fahrenheit = self.read_temp() * 1.8 + 32

        return self.read_fahrenheit()

    # On affiche la temérature tant que le script tourne
    def temperature_loop(self, socketio):
        while True:
            socketio.emit('temp', self.read_temp(), Broadcast=True)
            time.sleep(2)
