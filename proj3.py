"""cs244 google increase initial cwnd replication project"""
from mininet.topo import Topo
from mininet.node import CPULimitedHost
from mininet.link import TCLink
from mininet.net import Mininet
from mininet.log import lg, info
from mininet.util import dumpNodeConnections
from mininet.cli import CLI
from subprocess import Popen, PIPE
from time import sleep, time
from multiprocessing import Process
from argparse import ArgumentParser
import sys
import os
import math
import numpy as np

parser = ArgumentParser(description="fastopen")
parser.add_argument('--bw','-b',
                    type=float,
                    help="Bandwidth of links (kbp/s)",
                    default=1000)

parser.add_argument('--rtt','-r',
                    type=float,
                    help="Link propagation delay (ms)",
                    default=70)

parser.add_argument('--init_cwnd','-c',
                    help="Initial window size",
                    type=int,
                    default=3)

parser.add_argument('--dir',
                    help='Directory to store outputs',
                    default='results')

args = parser.parse_args()

class Initialcwnd_Topo(Topo):
    def build(self, n = 2):
        for i in range(n):
            host = self.addHost('h%s' % (i + 1))
        
        switch = self.addSwitch('s0')
        self.addLink('h1', switch, bw = 500, delay = str(args.rtt / 2) + 'ms') # server
        self.addLink('h2', switch, bw = args.bw / 1000) # curl client (short-lived flow)

def modify_initial_cwnd(net):
    # Windows 7 have average rwnd = 41KB = 27.3 segments
    h1 = net.get('h1')
    ip_route = h1.cmd('ip route show')
    h1.cmd('ip route change %s initcwnd %d initrwnd %d mtu 1500' % (ip_route.strip(), args.init_cwnd, 27))

    h2 = net.get('h2')
    ip_route = h2.cmd('ip route show')
    h2.cmd('ip route change %s initcwnd %d initrwnd %d mtu 1500' % (ip_route.strip(), args.init_cwnd, 27))

def start_webserver(net):
    h1 = net.get('h1')
    h1.popen('python2 webserver.py', shell = True)
    sleep(1)

def get_web_transfer_time(net):
    h1 = net.get('h1')
    h2 = net.get('h2')
   
    save_curl_file = open(args.dir + '/cwnd%d_rtt%d_bw%d.txt' % (args.init_cwnd, args.rtt, args.bw), 'w')
    print("Running test for init_window = %d and rtt = %d and bw = %d" % (args.init_cwnd, args.rtt, args.bw))
    save_curl_file.write(h2.cmd('curl -o /dev/null -s -w %%{time_total} %s' % (h1.IP())))
    save_curl_file.write('\n')
    save_curl_file.close()

if __name__ == "__main__":
     if not os.path.exists(args.dir):
         os.makedirs(args.dir)
     topo = Initialcwnd_Topo()
     os.system("sysctl -w net.ipv4.tcp_congestion_control=cubic > /dev/null")
     net = Mininet(topo = topo,host = CPULimitedHost, link = TCLink)
     net.start()
     modify_initial_cwnd(net)
     start_webserver(net)
     get_web_transfer_time(net)
    
     net.stop()
     Popen("pgrep -f webserver.py | xargs kill -9", shell = True).wait()
