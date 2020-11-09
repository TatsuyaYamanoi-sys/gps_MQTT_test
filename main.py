from machine import Pin,UART
import utime
import network
from umqtt.simple import MQTTClient

#======= connect to wifi access point =======#
SSID_NAME = "id"    # name
SSID_PASS = "pass"  # pass

def connect_wifi(ssid, passkey, timeout=10):
    wifi= network.WLAN(network.STA_IF)
    if wifi.isconnected() :
        print('already Connected.    connect skip')
        return wifi
    else :
        wifi.active(True)
        wifi.connect(ssid, passkey)
        while not wifi.isconnected() and timeout > 0:
            print('.')
            utime.sleep(1)
            timeout -= 1
    
    if wifi.isconnected():
        print('Connected')
        return wifi
    else:
        print('Connection failed!')
        return null

wifi = connect_wifi(SSID_NAME, SSID_PASS)
if not wifi :
    sys.exit(0)

print('wifi ok')
#======= MQTT =======#

server = "192.168.1.148"

c = MQTTClient("umqtt_client", server)
c.connect()
#c.disconnect()
print('MQTT ok')
#======= uart setting =======#

uart1 = UART(1,9600)
uart1.init(baudrate=9600,bits=8,parity=None,stop=1,rx=18,tx=19)
uart2 = UART(2,9600)
uart2.init(baudrate=9600,bits=8,parity=None,stop=1,rx=16,tx=17)
print('UART ok')
#======= GPS =======#


while True:        
    if (uart1.any()):       #uart1に何かデータが入ったら（.any()）以下を実行
        read_data = b''     #read_dataを空のbyte型data(b'')
        gps_line = b''      #gps_line 変数
        while read_data != b'\n':       #read_dataに改行が入るまでループ
            read_data = uart1.read(1)       #UARTで1byteずつ読む(.read(1))
            if(read_data):      #dataが入ったら以下を実行
                gps_line += read_data       #gps_line配列に1byteずつ読んだデータを入れる

        if(gps_line[:6] == b'$GPRMC'):      #gps_line配列の6番目までが(gps_line[:6])$GPRMCであれば以下を実行
            gps_str = gps_line.decode('utf-8')      #split()ではbytes型が変換出来ない為、gps_strを作成。.decode('utf-8')でstr型に変換。
            gps_parts = gps_str.split(',')      #split()でカンマ区切りの配列に変換
            uart2.write(gps_line)

            if(gps_parts[2] == 'A'):
                latitude = gps_parts[3]     #配列3番目の緯度を変数に代入
                longitude = gps_parts[5]    #配列5番目の経度

                uart2.write(latitude)
                uart2.write('\n\r')
                uart2.write(longitude)
                uart2.write('\n\r')
                
                c.publish(b"gps/test", latitude.encode('utf-8') + b',' + longitude.encode('utf-8'))
            else:
                uart2.write('No Data')
                c.publish(b"gps/test", b'GPS NoData')




#[;21]=<

    #gps_line = b''
    #rec_char = None

    #if (uart1.any()):
    #    while (rec_char != '\n'):

    #        rec_char = uart.read(1)

    #        gps_line += rec_char

    #uart2.write(gps_line)
    #uart2.write('ok\n\r')

    #uart2.write('\n\r')
    #uart2.write(uart1.read())

    #uart2.write('uart2test1')
    #uart2.write('uart2test2')

    #my_str = uart2.read()

    #if(my_str != None):
    #    uart2.write(my_str.encode('utf-8'))
    #    uart2.write(b'hello')

    #if (uart1.any()):
    #    uart2.write(uart1.readline())
    #    uart2.write('ok\n\r')

#while (rec_char != '\n'):
    #rec_char = uart1.read(1)
    #gps_line += rec_char
    #uart2.write(gps_line)