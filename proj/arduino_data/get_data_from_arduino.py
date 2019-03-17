import serial
import re
import datetime
import sqlite3
import time



output = " "
dev = serial.Serial('/dev/ttyUSB0')
TEMP_MAX = 30
TEMP_MIN = 15
LIGHT_MIN = 80
DB_NAME = 'arduino_log.db'


def parse_line(line):
    data = line.decode('utf-8')
    data = [i.strip() for i in data.split("=")]
    return (data[0], float(data[1]))

def check_conditions(data):
    if data[0] == 'Temperature':
        check_temp(data[1])
    elif data[0] == 'Humidity':
        #check_humidity(data[1])
        pass
    elif data[0] =='Light':
        check_light(data[1])

def check_temp(temp):
    if (temp > TEMP_MAX) or (temp < TEMP_MIN):
        print('temp outside of the optimal range')

def check_light(light):
    if (light < LIGHT_MIN):
        print('light outside of the optimal range')


def get_from_db(table, num_records):
    data = []
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('select * from %s order by date desc' % table)
    for i in range(num_records):
        data.append(c.fetchone())
    conn.close()
    return data


def write_to_db(table, date, value):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("INSERT INTO %s VALUES ('%s', %f)" % (table, date, value))
    conn.commit()
    conn.close()
    
def return_data(datapoints):
    return [parse_line(dev.readline()) for i in range(3 * datapoints)]
 
    
def log_conditions(file_path):    
    while True:
        now = time.time()
        line = dev.readline()
        data = parse_line(line)
        print("INSERT INTO %s VALUES (%s, %d)" % (data[0].lower(), str(datetime.datetime.now()) , data[1]))
        write_to_db(data[0].lower(), str(datetime.datetime.now()) , data[1])
        #print("TIME PASSED: {}".format(time.time() - now))
        
if __name__ == '__main__':
    log_conditions("/home/pi/Desktop/text.txt")

    
