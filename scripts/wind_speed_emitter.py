import socket
import sys
import time
import re

HOST = ''
PORT = 2094

def checksum(sentence):

    """ Remove any newlines """
    if re.search("\n$", sentence):
        sentence = sentence[:-1]

    nmeadata = sentence

    calc_cksum = 0
    for s in nmeadata:
        calc_cksum ^= ord(s)

    """ Return the nmeadata, the checksum from
        sentence, and the calculated checksum
    """
    return '{:02X}'.format(calc_cksum)

def generate_nmea(wind_speed):
    phrase = "IIMWV,000.0,R,"
    phrase += "%.1f" % wind_speed
    phrase += ",K,A"
    cksum = checksum(phrase)
    phrase += '*' + str(cksum)
    return '$' + phrase

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
print 'Socket created (PORT : %s)' % str(PORT)

try:
    s.bind((HOST, PORT))
except:
    print 'Bind failed'
    sys.exit()

s.listen(1)

conn, addr = s.accept()
print 'Connected with ' + addr[0] + ':' + str(addr[1])

while True:
    print "Wind speed nmea phrase : ", generate_nmea(20)
    conn.send(generate_nmea(20) + '\r\n')
    time.sleep(1)

s.close()
