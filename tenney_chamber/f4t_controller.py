import socket
import time
import errno
import multiprocessing as mp

class F4T_Controller:

    def __init__(self, ip_address="192.168.1.14", port=5025):

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM )
        self.sock.connect( ( ip_address, port) )
        self.sock.sendall("*IDN?")
        self.name = self.sock.recv(1024)
        print("You are connected to: %s "%self.name )

    def set_temperature( self, value):
        scpi_command = ":SOURCE:CLOOP1:SPOINT %s"%value
        self.sock.sendall(scpi_command)
        print("Temperature is set to %s"%value )

    def set_humidity( self, value):
        scpi_command = ":SOURCE:CLOOP2:SPOINT %s"%value
        self.sock.sendall(scpi_command)
        print("Humidity is set to %s"%value )

    def get_temperature(self):
        scpi_command_get_temp = ":SOURCE:CLOOP1:PVALUE?"
        self.sock.sendall(scpi_command_get_temp)

        try:
            tempValue = self.sock.recv(1024)
        #except socket.error as (code, msg):
        except:
            #while code != errno.EINTR:
            #    return -273.0
            return -273.0

        tempValue = tempValue.split("\n")[0]
        if tempValue is "":
            tempValue = -273.0

        return float(tempValue)


    def get_humidity(self):
        scpi_command_get_humi = ":SOURCE:CLOOP2:PVALUE?"
        self.sock.sendall(scpi_command_get_humi)

        try:
            humiValue = self.sock.recv(1024)
        #except socket.error as (code, msg):
        except:
            #while code != errno.EINTR:
                #return -1.0
            return -1.0

        humiValue = humiValue.split("\n")[0]
        return float(humiValue)

    def check_temperature(self, value):
        while abs(self.get_temperature()-float(value))>=3:
            time.sleep(5)
            continue

    def log_temp_humi_to_file(self, output_name="temp_humi.txt", duration=3600*10, show_plot=True):
        output_name = "start_time_%s_%s"%(int(time.time()), output_name)
        output = open(output_name, "w")
        output.write("timestamp, temp, humi, \n")
        _start_time = time.time()
        _end_time = _start_time + duration

        temperature_plot = ""
        humidity_plot = ""
        proc_list = []

        if show_plot:
            from stas_plot_tool import generic_plot
            temperature_plot = generic_plot.Generic_Plot("Time", "Temperature")
            humidity_plot = generic_plot.Generic_Plot("Time", "Humidity")

            tempPlot_proc = mp.Process(target=temperature_plot.draw, args=(1,))
            tempPlot_proc.start()
            proc_list.append( tempPlot_proc )

            humiPlot_proc = mp.Process(target=humidity_plot.draw, args=(2,))
            humiPlot_proc.start()
            proc_list.append( humiPlot_proc )


        while True:
            current_time = time.time()
            if current_time >= _end_time:
                break
            else:
                tempValue = self.get_temperature()
                humiValue = self.get_humidity()
                if tempValue<=-273.0:continue
                if humiValue<=-1.0:continue
                output.write("%s, %s, %s\n"%(current_time, tempValue, humiValue) )
                #print("%s, %s, %s\n"%(current_time, tempValue, humiValue) )
                output.flush()
                if show_plot:
                    temperature_plot.updateValue( current_time, tempValue )
                    humidity_plot.updateValue( current_time, humiValue )
                time.sleep(1)
        output.close()
        if not proc_list:
            pass
        else:
            for item in proc_list:
                item.join()
