import socket
import struct
import string

CONST = 0.58134
OFFSET_DATASHEET_25C = 827 #// 1422*CONST, from Datasheet
TEMP_COEFF = CONST * 4.2 #// From Datasheet
OFFSET_0C = OFFSET_DATASHEET_25C - (25 * TEMP_COEFF)

# open socket
socket_handler = socket.socket(socket.AF_INET6,socket.SOCK_DGRAM)
socket_handler.bind(('',2424))

def toHex(s):
    lst = []
    for ch in s:
        hv = hex(ord(ch)).replace('0x', '')
        if len(hv) == 1:
            hv = '0'+hv
        lst.append(hv)
    return reduce(lambda x,y:x+y, lst)

while True:
    
    # wait for a request
    #request,dist_addr = socket_handler.recvfrom(1024)
    data,dist_addr = socket_handler.recvfrom(1024)
 
    hisAddress     = dist_addr[0]
    hisPort        = dist_addr[1]
    macAddr        = dist_addr[0].split(':')
    #macAddr        = ":".join("%4X"%c for c in macAddr)
    #print "addr=%s" %macAddr
#    counter        = struct.unpack('<h',data)[0]
    counter,data1,data2,data3,data4         = struct.unpack('HHHHH',data)
    
    print 'len=%d, counter=%x, d1=%x, d2=%x, d3=%x, d4=%x' % (len(data),counter,data1,data2,data3,data4)
    #data1, int_temp
    #data2, ext_temp
    #data3, pyra
    #data4, volt

    pure_value = data1
    temp_volt = pure_value * CONST
    i_temp_real = (temp_volt - OFFSET_0C) / TEMP_COEFF
    print 'internal temp = %2.2f' % i_temp_real

    pure_value = data3
    temp_volt = pure_value * 1200 / 2048
    temp_real = (temp_volt - 0.1678) / 12.223
    print 'external temp = %2.2f' % temp_real

    pure_value = data2
    if (pure_value > 2047):
        pyra_real = 0
        print 'detect estimated pyra < 0'
    else:
        pyra_volt = pure_value * 1200 / 2048
        pyra_real = pyra_volt * 1000 / 1200
        print 'estimated pyra = %d' % pyra_real

    pure_value = data4
    i_volt_real = pure_value / 364.5
    print 'raw i_volt = %2.2f' % i_volt_real
    
    print 'received from [{0}]:{1} \
    '.format(hisAddress,hisPort)
