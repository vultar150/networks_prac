#!/usr/bin/python

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import CPULimitedHost, OVSSwitch, Switch, RemoteController
from mininet.link import TCLink
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel
from mininet.cli import CLI
from time import sleep
import os
            
class MyTopo( Topo ):
    "Simple topology example."

    def build( self ):
        "Create custom topo."

        # Add hosts and switches
        leftHost = self.addHost( 'h1', ip='10.255.255.1/24' )
        middleHost = self.addHost( 'h2', ip='10.255.255.2/24' )
        rightHost = self.addHost( 'h3', ip='10.255.255.3/24' )

        leftSwitch = self.addSwitch( 's1' )
        middleSwitch = self.addSwitch('s2' )
        rightSwitch = self.addSwitch( 's3' )

        # Add links
        self.addLink( leftHost, leftSwitch )
        
        # s1->s2
        self.addLink( leftSwitch, middleSwitch, 
                      bw=1700, loss=0.00008, delay='140ms', max_queue_size=900)
    
        self.addLink( middleSwitch, middleHost )
        
        # s2->s3
        self.addLink( middleSwitch, rightSwitch,
                      bw=45, loss=2.3, delay='1.2ms', max_queue_size=95)
        
        self.addLink( rightSwitch, rightHost )        

def run_iperf(client, server, port, cong, experiment_num):
    server.cmd('killall iperf3')
    sleep(1) # make sure ports can be reused
    # -s: server
    # -p [port]: port
    # -f m: format in megabits
    # -i 1: measure every second
    if experiment_num == 1:
        cl, serv = 'h1', 'h2'
    elif experiment_num == 2:
        cl, serv = 'h2', 'h3'
    else:
        cl, serv = 'h1', 'h3'
        
    iperfServerOutput = "$PWD/" + "iperf_server_" + cong + "_" + cl + "_" + serv + ".txt"
    iperfClientOutput = "$PWD/" + "iperf_client_" + cong + "_" + cl + "_" + serv + ".txt"
    tcpProbeOutput = "$PWD/" + "tcp_probe_" + cong + "_" + cl + "_" + serv + ".txt"

    os.system("sudo rm {} {} {}".format(iperfServerOutput, iperfClientOutput, tcpProbeOutput))

    server.cmd('iperf3 -s -p {} -f m -i 1 --logfile {} &'.format(port, iperfServerOutput))
    sleep(3) # make sure all the servers start

    # start tcp_probe
    os.system('modprobe -r tcp_probe')
    os.system('modprobe tcp_probe port={} full=1'.format(port))
    os.system('dd if=/proc/net/tcpprobe > {} & echo $! > pid.txt'.format(tcpProbeOutput))
    
    client.cmd('iperf3 -c {} -f m -i 1 -p {} -C {} -t 65 --logfile {}'.format(server.IP(), port, cong, iperfClientOutput))
    server.cmd('killall iperf3')
    
    os.system('kill $(cat pid.txt)')
    os.system('wait $(cat pid.txt) 2>/dev/null')
    os.system('modprobe -r tcp_probe')
    os.remove('pid.txt')


topo = MyTopo()
net = Mininet( topo=topo,
               link=TCLink )

net.start()
h1, h2, h3 = net.get('h1', 'h2', 'h3')


# run_iperf(h1, h2, 5001, "reno", 1)
# run_iperf(h1, h2, 5001, "cubic", 1)

# run_iperf(h2, h3, 5001, "reno", 2)
# run_iperf(h2, h3, 5001, "cubic", 2)

# run_iperf(h1, h3, 5001, "reno", 3)
# run_iperf(h1, h3, 5001, "cubic", 3)
CLI(net)
net.stop()