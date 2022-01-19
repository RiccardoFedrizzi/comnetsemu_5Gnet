Emulate a 5G network deployment in comnetsemu.
Demonstrate distributed UPF deployment and slice-base UPF selection.

Tested Versions:
- Comnetsemu: v0.3.0 (Installed following either "Option 1" or "Option 3" from [here](https://git.comnets.net/public-repo/comnetsemu) )
- UERANSIM: v3.2.6
- Open5gs: v2.4.2

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

The scenario includes 5 DockerHosts as shown in the figure below.
The UE starts two PDU session one for each slice defined in the core network.

<img src="./images/topology.jpg" title="./images/topology.jpg" width=1000px></img>

Notice that at the first run the set-up should not work due to missing information in the 5GC.
To configure it we should leverage the WebUI by opening the following page in a browser on the host OS.
```
http://<VM_IP>:3000/
```

The configuration is as follows:

UE information:
- IMSI = 001011234567895
- USIM Type = OP
- Operator Key (OPc/OP) = 11111111111111111111111111111111
- key: '8baf473f2f8fd09487cccbd7097c6862'

Slice 1 configuration
- SST: 1
- SD: 000001
- Session-AMBR Downlink: 2 Mbps
- Session-AMBR Uplink: 2 Mbps

Slice 2 configuration
- SST: 1
- SD: 000001
- Session-AMBR Downlink: 10 Mbps
- Session-AMBR Uplink: 10 Mbps

The configuration should look like this:

<img src="./images/WebUI_config.JPG" title="./images/WebUI_config.JPG" width=800px></img>


### Test the environment

In two terminals start two tcpdump for both upf and upf_mec

``` 
$ ./start_tcpdump.sh upf
$ ./start_tcpdump.sh upf_mec
``` 

#### Latency test
Enter in the UE container:
``` 
# ./enter_container.sh ue
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
iperf3 -c 10.46.0.1 -B 10.46.0.2 -t 5
``` 

Open the open5gs WebUI and change the DL/UL bandwidth for slice 1.

Update the PDU session in the UE. Notice how the session is started specifying the slice, not the APN. The APN, and thus the associated UPF, is selected by the 5GC.

```
# ./nr-cli imsi-001011234567895
$ ps-establish IPv4 --sst 1 --sd 1
$ status
```

Start again a bandwidth test in the UE leveraging the new PDU session:
``` 
iperf3 -c 10.45.0.1 -B 10.45.0.3 -t 5
```


### Contact

Main maintainer:
- Riccardo Fedrizzi - rfedrizzi@fbk.eu




