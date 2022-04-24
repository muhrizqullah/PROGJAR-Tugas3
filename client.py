import sys
import socket

BUFFER_SIZE = 1024

FTP_PORT = 21
HOST = '192.168.2.4'
    
def getreply(f):
    line = f.readline()
    if not line:
        return 'EOF'
    print(f"{line}")
    code = line[:3]
    if line[3:4] == '-':
        while 1:
            line = f.readline()
            if not line: 
                break # Really an error
            print(f"{line}")
            if line[:3] == code and line[3:4] != '-': break
    return code, line

def getdata(r):
    while 1:
        data = r.recv(BUFFER_SIZE)
        if not data: 
            break
        print(data.decode())
    r.close()
    
def getcommand():
    try:
        while 1:
            line = input('ftp.py> ')
            if line: return line
    except EOFError:
        return ''

def getdataport(line):
    line = line.split("227 Entering Passive Mode (")
    line = line[1].split(').\n')
    line = line[0].split(',')
    p1 = int(line[4])
    p2 = int(line[5])
    FTP_DATA_PORT = p1 * 256 + p2
    return FTP_DATA_PORT

def senddata(r, filename):
    f = open(f"dataset/{filename}", 'rb')
    while True:
        read = f.read(BUFFER_SIZE)
        if not read:
            break
        r.send(read)
    f.close()
    r.close()

try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, FTP_PORT))
    f = s.makefile('r')

    r = None
    while True:
        code, line = getreply(f)
        if code in ('221', 'EOF'):
            break
        if code == '150':
            if line == "150 Ok to send data.\n":
                filename = cmd.split(' ')[1]
                filename = filename.rstrip('\n')
                print(filename)
                senddata(r, filename)
                code, line = getreply(f)
                r = None
            else:
                getdata(r)
                code, line = getreply(f)
                r = None
        if code == '227':
            r = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            r.connect((HOST, getdataport(line)))
        cmd = getcommand()
        if not cmd:
            break
        s.send((cmd + '\r\n').encode())
except KeyboardInterrupt:
    s.close()
    sys.exit(0)