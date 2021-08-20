Emulate a 5G network deployment in comnetsemu.
Demonstrate distributed UPF deployment and slice-base UPF selection.

Tested Versions:
- Comnetsemu: v0.1.12 (downloaded the VM from here )
- UERANSIM: v3.1.9
- Open5gs: v2.3.2

## Build Instructions

Clone repository in the comnetsemu VM.

Build the necessary docker images:

```
cd ueransim
./build_ueransim.sh

cd ../open5gs
./build_5gc.sh
```

## Run experiments

### Start the network topology:
```
$ sudo python3 example1.py
```

The scenario includes 5 DockerHosts connected through a simple network.
- Host 1: Contains the user equipment with two PDU session active (sst=1 and sst=2).
- Host 2: Contains the gNB
- Host 3: Contains the UPF terminating the PDU session for the slice with sst=2 (container upf_mec)
- Host 4: Contains the UPF terminating the PDU session for the slice with sst=1 (container upf)
- Host 5: Contains the CP functions


### Test the environment

In two terminals start two tcpdump for both upf and upf_mec

``` 
$ ./start_tcpdump.sh upf
$ ./start_tcpdump.sh upf_mec
``` 

#### Latency test
Enter in the UE container:
``` 
# ./enter_container ue
``` 

Start ping test on the interfaces related to the two slices:
``` 
# ping -c 3 -n -I uesimtun0 www.google.com
# ping -c 3 -n -I uesimtun1 www.google.com
``` 



#### Bandwidth test

Enter in the UE container:
``` 
# ./enter_container.sh ue
``` 

Start bandwidth test leveraging the two slices:
``` 
iperf3 -c 10.45.0.1 -B 10.45.0.2 -t 5
iperf3 -c 10.46.0.1 -B 10.46.0.3 -t 5
``` 

Open the open5gs WebUI and change the DL/UL bandwidth for slice 1.

Update the PDU session in the UE.
```
# ./nr-cli imsi-001011234567895
$ ps-establish IPv4 --sst 1 --sd 1
$ status
```

Start again a bandwidth test in the UE leveraging the new PDU session:
``` 
iperf3 -c 10.45.0.1 -B 10.45.0.3 -t 5
```






