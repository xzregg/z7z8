import subprocess
import os,sys
import pty
import tty
import time


def test():
    pid,child_fd = pty.fork()
    if pid == 0 :
        os.system('ssh 192.168.112.109')
    else:
        print os.getpid()
        while 1:
            ret = os.read(child_fd, 65536)
            if ret :
                print '*%s'%ret
                d = raw_input()
                os.write(child_fd,'%s\n'%d)
                time.sleep(0.5)
            else:
            #os.write(child_fd, '123456\n')
                print '-'
                time.sleep(1)


if __name__ == '__main__':
    test()