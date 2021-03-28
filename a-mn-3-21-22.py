#Topology Substation 3-21-22
#!/usr/bin/python

from mininet.net import Mininet
from mininet.node import Node, Controller, RemoteController, OVSSwitch, OVSKernelSwitch, Host
from mininet.cli import CLI
from mininet.link import Intf, TCLink
from mininet.log import setLogLevel, info
from mininet.node import Node, CPULimitedHost
from mininet.util import irange,dumpNodeConnections
import time
import os



class LinuxRouter( Node ):
    "A Node with IP forwarding enabled."

    def config( self, **params ):
        super( LinuxRouter, self).config( **params )
        # Enable forwarding on the router
        self.cmd( 'sysctl net.ipv4.ip_forward=1' )

    def terminate( self ):
        self.cmd( 'sysctl net.ipv4.ip_forward=0' )
        super( LinuxRouter, self ).terminate()

def emptyNet():

    NODE2_IP='192.168.56.1'
    CONTROLLER_IP='127.0.0.1'

    net = Mininet( topo=None,
                   build=False)

    #c0 = net.addController( 'c0',controller=RemoteController,ip=CONTROLLER_IP,port=6633)
    net.addController('c0', port=6633)

    r0 = net.addHost('r0', cls=LinuxRouter, ip='100.0.0.1/16')
    r3 = net.addHost('r3', cls=LinuxRouter, ip='100.3.0.1/16')
    r21 = net.addHost('r21', cls=LinuxRouter, ip='100.21.0.1/16')
    r22 = net.addHost('r22', cls=LinuxRouter, ip='100.22.0.1/16')


    #Switch External Gateway
    s777 = net.addSwitch( 's777' )

    #Switch on Control Center
    s999 = net.addSwitch( 's999' )

    #Switch on Substation
    s31 = net.addSwitch( 's31' )
    s32 = net.addSwitch( 's32' )
    s33 = net.addSwitch( 's33' )
    s211 = net.addSwitch( 's211' )
    s212 = net.addSwitch( 's212' )
    s213 = net.addSwitch( 's213' )
    s221 = net.addSwitch( 's221' )
    s222 = net.addSwitch( 's222' )
    s223 = net.addSwitch( 's223' )

    # Add host-switch links in the same subnet
    net.addLink(s999, r0, intfName2='r0-eth1', params2={'ip': '100.0.0.1/16'})
    net.addLink(s31, r3, intfName2='r3-eth1', params2={'ip': '100.3.0.1/16'})
    net.addLink(s211, r21, intfName2='r21-eth1', params2={'ip': '100.21.0.1/16'})
    net.addLink(s221, r22, intfName2='r22-eth1', params2={'ip': '100.22.0.1/16'})

     # Add router-router link in a new subnet for the router-router connection
    net.addLink(r0, r3, intfName1='r0-eth3', intfName2='r3-eth2', params1={'ip': '200.3.0.1/24'}, params2={'ip': '200.3.0.2/24'})
    net.addLink(r0, r21, intfName1='r0-eth2', intfName2='r21-eth2', params1={'ip': '200.21.0.1/24'}, params2={'ip': '200.21.0.2/24'})
    net.addLink(r0, r22, intfName1='r0-eth4', intfName2='r22-eth2', params1={'ip': '200.22.0.1/24'}, params2={'ip': '200.22.0.2/24'})

    #Add Host on Control Center
    ccdb = net.addHost('ccdb', ip='100.0.0.11')
    cctl = net.addHost('cctl', ip='100.0.0.12')

    #Add Hosts on Substation 3
    s03m1 = net.addHost('s03m1', ip='100.3.0.11', cls=CPULimitedHost, cpu=.1)
    s03m2 = net.addHost('s03m2', ip='100.3.0.12', cls=CPULimitedHost, cpu=.1)
    s03m3 = net.addHost('s03m3', ip='100.3.0.13', cls=CPULimitedHost, cpu=.1)
    s03m4 = net.addHost('s03m4', ip='100.3.0.14', cls=CPULimitedHost, cpu=.1)
    s03m5 = net.addHost('s03m5', ip='100.3.0.15', cls=CPULimitedHost, cpu=.1)
    s03m6 = net.addHost('s03m6', ip='100.3.0.16', cls=CPULimitedHost, cpu=.1)
    s03m7 = net.addHost('s03m7', ip='100.3.0.17', cls=CPULimitedHost, cpu=.1)
    s03m8 = net.addHost('s03m8', ip='100.3.0.18', cls=CPULimitedHost, cpu=.1)
    s03m9 = net.addHost('s03m9', ip='100.3.0.19', cls=CPULimitedHost, cpu=.1)
    s03cpc = net.addHost('s03cpc', ip='100.3.0.21')
    s03db = net.addHost('s03db', ip='100.3.0.22')
    s03gw = net.addHost('s03gw', ip='100.3.0.23')

    #Add Hosts on Substation 21
    s21m1 = net.addHost('s21m1', ip='100.21.0.11', cls=CPULimitedHost, cpu=.1)
    s21m2 = net.addHost('s21m2', ip='100.21.0.12', cls=CPULimitedHost, cpu=.1)
    s21m3 = net.addHost('s21m3', ip='100.21.0.13', cls=CPULimitedHost, cpu=.1)
    s21m4 = net.addHost('s21m4', ip='100.21.0.14', cls=CPULimitedHost, cpu=.1)
    s21m5 = net.addHost('s21m5', ip='100.21.0.15', cls=CPULimitedHost, cpu=.1)
    s21m6 = net.addHost('s21m6', ip='100.21.0.16', cls=CPULimitedHost, cpu=.1)
    s21cpc = net.addHost('s21cpc', ip='100.21.0.21')
    s21db = net.addHost('s21db', ip='100.21.0.22')
    s21gw = net.addHost('s21gw', ip='100.21.0.23')

    #Add Hosts on Substation 17
    s22m1 = net.addHost('s22m1', ip='100.22.0.11', cls=CPULimitedHost, cpu=.1)
    s22m2 = net.addHost('s22m2', ip='100.22.0.12', cls=CPULimitedHost, cpu=.1)
    s22m3 = net.addHost('s22m3', ip='100.22.0.13', cls=CPULimitedHost, cpu=.1)
    s22m4 = net.addHost('s22m4', ip='100.22.0.14', cls=CPULimitedHost, cpu=.1)
    s22m5 = net.addHost('s22m5', ip='100.22.0.15', cls=CPULimitedHost, cpu=.1)
    s22m6 = net.addHost('s22m6', ip='100.22.0.16', cls=CPULimitedHost, cpu=.1)
    s22cpc = net.addHost('s22cpc', ip='100.22.0.21')
    s22db = net.addHost('s22db', ip='100.22.0.22')
    s22gw = net.addHost('s22gw', ip='100.22.0.23')

    # Link siwtch to switch
    net.addLink(s31,s32)
    net.addLink(s33,s32)
    net.addLink(s211,s212)
    net.addLink(s213,s212)
    net.addLink(s221,s222)
    net.addLink(s223,s222)

    # Link Control Center to Switch
    net.addLink(ccdb,s999, intfName1='ccdb-eth1', params1={'ip':'100.0.0.11/24'})
    net.addLink(cctl,s999, intfName1='cctl-eth1', params1={'ip':'100.0.0.12/24'})

    # Link Substation 03 Merging unit to Switch
    net.addLink(s03m1,s33, intfName1='s03m1-eth1', params1={'ip':'100.3.0.11/24'})
    net.addLink(s03m2,s33, intfName1='s03m2-eth1', params1={'ip':'100.3.0.12/24'})
    net.addLink(s03m3,s33, intfName1='s03m3-eth1', params1={'ip':'100.3.0.13/24'})
    net.addLink(s03m4,s33, intfName1='s03m4-eth1', params1={'ip':'100.3.0.14/24'})
    net.addLink(s03m5,s33, intfName1='s03m5-eth1', params1={'ip':'100.3.0.15/24'})
    net.addLink(s03m6,s33, intfName1='s03m6-eth1', params1={'ip':'100.3.0.16/24'})
    net.addLink(s03m7,s33, intfName1='s03m7-eth1', params1={'ip':'100.3.0.17/24'})
    net.addLink(s03m8,s33, intfName1='s03m8-eth1', params1={'ip':'100.3.0.18/24'})
    net.addLink(s03m9,s33, intfName1='s03m9-eth1', params1={'ip':'100.3.0.19/24'})  
    net.addLink(s03cpc,s32)
    net.addLink(s03db,s32)
    net.addLink(s03gw,s31, intfName1='s03gw-eth1', params1={'ip':'100.3.0.23/24'})
    
    # Link Substation 21 Merging unit to Switch
    net.addLink(s21m1,s213, intfName1='s21m1-eth1', params1={'ip':'100.21.0.11/24'}, cls=TCLink, bw=0.01 )
    net.addLink(s21m2,s213, intfName1='s21m2-eth1', params1={'ip':'100.21.0.12/24'}, cls=TCLink, bw=0.01 )
    net.addLink(s21m3,s213, intfName1='s21m3-eth1', params1={'ip':'100.21.0.13/24'}, cls=TCLink, bw=0.01 )
    net.addLink(s21m4,s213, intfName1='s21m4-eth1', params1={'ip':'100.21.0.14/24'}, cls=TCLink, bw=0.01 )
    net.addLink(s21m5,s213, intfName1='s21m5-eth1', params1={'ip':'100.21.0.15/24'}, cls=TCLink, bw=0.01 )
    net.addLink(s21m6,s213, intfName1='s21m6-eth1', params1={'ip':'100.21.0.16/24'}, cls=TCLink, bw=0.01 )
    net.addLink(s21cpc,s212)
    net.addLink(s21db,s212)
    net.addLink(s21gw,s211, intfName1='s21gw-eth1', params1={'ip':'100.21.0.23/24'})

    # Link Substation 22 Merging unit to Switch
    net.addLink(s22m1,s223, intfName1='s22m1-eth1', params1={'ip':'100.22.0.11/24'})
    net.addLink(s22m2,s223, intfName1='s22m2-eth1', params1={'ip':'100.22.0.12/24'})
    net.addLink(s22m3,s223, intfName1='s22m3-eth1', params1={'ip':'100.22.0.13/24'})
    net.addLink(s22m4,s223, intfName1='s22m4-eth1', params1={'ip':'100.22.0.14/24'})
    net.addLink(s22m5,s223, intfName1='s22m5-eth1', params1={'ip':'100.22.0.15/24'})
    net.addLink(s22m6,s223, intfName1='s22m6-eth1', params1={'ip':'100.22.0.16/24'}) 
    net.addLink(s22cpc,s222)
    net.addLink(s22db,s222)
    net.addLink(s22gw,s221, intfName1='s22gw-eth1', params1={'ip':'100.22.0.23/24'})


    # Link Host Control Center to External gateway
    net.addLink(ccdb,s777, intfName1='ccdb-eth0', params1={'ip':'10.0.0.11/16'})
    net.addLink(cctl,s777, intfName1='cctl-eth0', params1={'ip':'10.0.0.12/16'})

    # Link Host Substation 13 to switch to external gateway
    net.addLink(s03m1,s777, intfName1='s03m1-eth0', params1={'ip':'10.0.3.11/16'})
    net.addLink(s03m2,s777, intfName1='s03m2-eth0', params1={'ip':'10.0.3.12/16'})
    net.addLink(s03m3,s777, intfName1='s03m3-eth0', params1={'ip':'10.0.3.13/16'})
    net.addLink(s03m4,s777, intfName1='s03m4-eth0', params1={'ip':'10.0.3.14/16'})
    net.addLink(s03m5,s777, intfName1='s03m5-eth0', params1={'ip':'10.0.3.15/16'})
    net.addLink(s03m6,s777, intfName1='s03m6-eth0', params1={'ip':'10.0.3.16/16'})
    net.addLink(s03m7,s777, intfName1='s03m7-eth0', params1={'ip':'10.0.3.17/16'})
    net.addLink(s03m8,s777, intfName1='s03m8-eth0', params1={'ip':'10.0.3.18/16'})
    net.addLink(s03m9,s777, intfName1='s03m9-eth0', params1={'ip':'10.0.3.19/16'})
    net.addLink(s03gw,s777, intfName1='s03gw-eth0', params1={'ip':'10.0.3.23/16'})
    
    # Link Host Substation 10 to switch to external gateway
    net.addLink(s21m1,s777, intfName1='s21m1-eth0', params1={'ip':'10.0.21.11/16'})
    net.addLink(s21m2,s777, intfName1='s21m2-eth0', params1={'ip':'10.0.21.12/16'})
    net.addLink(s21m3,s777, intfName1='s21m3-eth0', params1={'ip':'10.0.21.13/16'})
    net.addLink(s21m4,s777, intfName1='s21m4-eth0', params1={'ip':'10.0.21.14/16'})
    net.addLink(s21m5,s777, intfName1='s21m5-eth0', params1={'ip':'10.0.21.15/16'})
    net.addLink(s21m6,s777, intfName1='s21m6-eth0', params1={'ip':'10.0.21.16/16'})
    net.addLink(s21gw,s777, intfName1='s21gw-eth0', params1={'ip':'10.0.21.23/16'})

    # Link Host Substation 11 to switch to external gateway
    net.addLink(s22m1,s777, intfName1='s22m1-eth0', params1={'ip':'10.0.22.11/16'})
    net.addLink(s22m2,s777, intfName1='s22m2-eth0', params1={'ip':'10.0.22.12/16'})
    net.addLink(s22m3,s777, intfName1='s22m3-eth0', params1={'ip':'10.0.22.13/16'})
    net.addLink(s22m4,s777, intfName1='s22m4-eth0', params1={'ip':'10.0.22.14/16'})
    net.addLink(s22m5,s777, intfName1='s22m5-eth0', params1={'ip':'10.0.22.15/16'})
    net.addLink(s22m6,s777, intfName1='s22m6-eth0', params1={'ip':'10.0.22.16/16'})
    net.addLink(s22gw,s777, intfName1='s22gw-eth0', params1={'ip':'10.0.22.23/16'})

    


    #Build and start Network ============================================================================
    net.build()
    net.addNAT(ip='10.0.0.250').configDefault()
    net.start()

    #Configure GRE Tunnel
    #s777.cmdPrint('ovs-vsctl add-port s777 s777-gre1 -- set interface s777-gre1 type=gre ofport_request=5 options:remote_ip='+NODE2_IP)
    #s777.cmdPrint('ovs-vsctl show')
    nat = net.get('nat0')
    nat.cmdPrint('ip link set mtu 1454 dev nat0-eth0')

    # Add routing for reaching networks that aren't directly connected
    info( net[ 'r0' ].cmd( 'ip route add 100.3.0.0/24 via 200.3.0.2 dev r0-eth3' ) )
    info( net[ 'r3' ].cmd( 'ip route add 100.0.0.0/24 via 200.3.0.1 dev r3-eth2' ) )

    info( net[ 'r0' ].cmd( 'ip route add 100.21.0.0/24 via 200.21.0.2 dev r0-eth2' ) )
    info( net[ 'r21' ].cmd( 'ip route add 100.0.0.0/24 via 200.21.0.1 dev r21-eth2' ) )

    info( net[ 'r0' ].cmd( 'ip route add 100.22.0.0/24 via 200.22.0.2 dev r0-eth4' ) )
    info( net[ 'r22' ].cmd( 'ip route add 100.0.0.0/24 via 200.22.0.1 dev r22-eth2' ) )

    info( net[ 's03m1' ].cmd( 'ip route add 100.0.0.0/24 via 100.3.0.1 dev s03m1-eth1' ) )
    info( net[ 's03m2' ].cmd( 'ip route add 100.0.0.0/24 via 100.3.0.1 dev s03m2-eth1' ) )
    info( net[ 's03m3' ].cmd( 'ip route add 100.0.0.0/24 via 100.3.0.1 dev s03m3-eth1' ) )
    info( net[ 's03m4' ].cmd( 'ip route add 100.0.0.0/24 via 100.3.0.1 dev s03m4-eth1' ) )
    info( net[ 's03m5' ].cmd( 'ip route add 100.0.0.0/24 via 100.3.0.1 dev s03m5-eth1' ) )
    info( net[ 's03m6' ].cmd( 'ip route add 100.0.0.0/24 via 100.3.0.1 dev s03m6-eth1' ) )
    info( net[ 's03m7' ].cmd( 'ip route add 100.0.0.0/24 via 100.3.0.1 dev s03m7-eth1' ) )
    info( net[ 's03m8' ].cmd( 'ip route add 100.0.0.0/24 via 100.3.0.1 dev s03m8-eth1' ) )
    info( net[ 's03m9' ].cmd( 'ip route add 100.0.0.0/24 via 100.3.0.1 dev s03m9-eth1' ) )

    info( net[ 's21m1' ].cmd( 'ip route add 100.0.0.0/24 via 100.21.0.1 dev s21m1-eth1' ) )
    info( net[ 's21m2' ].cmd( 'ip route add 100.0.0.0/24 via 100.21.0.1 dev s21m2-eth1' ) )
    info( net[ 's21m3' ].cmd( 'ip route add 100.0.0.0/24 via 100.21.0.1 dev s21m3-eth1' ) )
    info( net[ 's21m4' ].cmd( 'ip route add 100.0.0.0/24 via 100.21.0.1 dev s21m4-eth1' ) )
    info( net[ 's21m5' ].cmd( 'ip route add 100.0.0.0/24 via 100.21.0.1 dev s21m5-eth1' ) )
    info( net[ 's21m6' ].cmd( 'ip route add 100.0.0.0/24 via 100.21.0.1 dev s21m6-eth1' ) )

    info( net[ 's22m1' ].cmd( 'ip route add 100.0.0.0/24 via 100.22.0.1 dev s22m1-eth1' ) )
    info( net[ 's22m2' ].cmd( 'ip route add 100.0.0.0/24 via 100.22.0.1 dev s22m2-eth1' ) )
    info( net[ 's22m3' ].cmd( 'ip route add 100.0.0.0/24 via 100.22.0.1 dev s22m3-eth1' ) )
    info( net[ 's22m4' ].cmd( 'ip route add 100.0.0.0/24 via 100.22.0.1 dev s22m4-eth1' ) )
    info( net[ 's22m5' ].cmd( 'ip route add 100.0.0.0/24 via 100.22.0.1 dev s22m5-eth1' ) )
    info( net[ 's22m6' ].cmd( 'ip route add 100.0.0.0/24 via 100.22.0.1 dev s22m6-eth1' ) )
    
    info( net[ 'ccdb' ].cmd( 'ip route add 100.3.0.0/24 via 100.0.0.1 dev ccdb-eth1' ) )
    info( net[ 'ccdb' ].cmd( 'ip route add 100.21.0.0/24 via 100.0.0.1 dev ccdb-eth1' ) )
    info( net[ 'ccdb' ].cmd( 'ip route add 100.22.0.0/24 via 100.0.0.1 dev ccdb-eth1' ) )

    info( net[ 'cctl' ].cmd( 'ip route add 100.3.0.0/24 via 100.0.0.1 dev cctl-eth1' ) )
    info( net[ 'cctl' ].cmd( 'ip route add 100.21.0.0/24 via 100.0.0.1 dev cctl-eth1' ) )
    info( net[ 'cctl' ].cmd( 'ip route add 100.22.0.0/24 via 100.0.0.1 dev cctl-eth1' ) )
    
    info(os.system('ip addr add 100.0.0.99/24 dev s999'))
    info(os.system('ip link set s999 up'))

    #time.sleep(5)

    #info( net[ 's06db' ].cmd( 'python3 ascdb.py &amp' ) )


    CLI( net )
    net.stop()



if __name__ == '__main__':
    setLogLevel( 'info' )
    emptyNet()