**Problem**
System was suddenly reporting GPU memory overflow errors. Only of the GPUs was found by Nvidia Drivers. 

**Updating Driver & CUDA versions**

Remove the CUDA driver OS :

To remove CUDA Toolkit:

```sudo apt-get --purge remove "cuda" "cublas" "cufft" "cufile" "curand" "cusolver" "cusparse" "gds-tools" "npp" "nvjpeg" "nsight*" "nvvm"```

To remove NVIDIA Drivers:

```sudo apt-get --purge remove "nvidia" "libxnvctrl*"```

To clean up the uninstall:

```sudo apt-get autoremove```


To install cuda toolkit:
```

wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/x86_64/cuda-keyring_1.0-1_all.deb
sudo dpkg -i cuda-keyring_1.0-1_all.deb
sudo apt-get update
sudo apt-get -y install cuda
```

**Reports**

Thu Jan 25 00:07:29 2024       
+---------------------------------------------------------------------------------------+
| NVIDIA-SMI 545.23.08              Driver Version: 545.23.08    CUDA Version: 12.3     |
|-----------------------------------------+----------------------+----------------------+
| GPU  Name                 Persistence-M | Bus-Id        Disp.A | Volatile Uncorr. ECC |
| Fan  Temp   Perf          Pwr:Usage/Cap |         Memory-Usage | GPU-Util  Compute M. |
|                                         |                      |               MIG M. |
|=========================================+======================+======================|
|   0  Tesla T4                       On  | 00000000:00:03.0 Off |                    0 |
| N/A   41C    P0              26W /  70W |  10457MiB / 15360MiB |      0%      Default |
|                                         |                      |                  N/A |
+-----------------------------------------+----------------------+----------------------+
|   1  Tesla T4                       On  | 00000000:00:03.0 Off |                    0 |
| N/A   ERR!   P0              ERR! / ERR!|  10457MiB / 15360MiB |      0%      Default |
|                                         |                      |                  N/A |
+---------------------------------------------------------------------------------------+
| Processes:                                                                            |
|  GPU   GI   CI        PID   Type   Process name                            GPU Memory |
|        ID   ID                                                             Usage      |
|=======================================================================================|
|    0   N/A  N/A      1822      G   /usr/lib/xorg/Xorg                            4MiB |
|    0   N/A  N/A     39215      C   tritonserver                              10448MiB |
+---------------------------------------------------------------------------------------+


After updating everything to the latest drivers ( Driver Version: 545.23.08, CUDA Version: 12.3), nvidia-smi reported 2 gpus but one with status ERR. But after rebooting it was not showing. For now, everything is working fine with one gpu. After updating drivers, the nominal utilization is arount 6.5GB. I will keep checking it for now for any errors. We will keep you updated on next plans. 

**Status as of Jan 25, 2024**
*System is running end-to-end*

# nvidia-smi
Thu Jan 24 00:18:29 2024       
+---------------------------------------------------------------------------------------+
| NVIDIA-SMI 545.23.08              Driver Version: 545.23.08    CUDA Version: 12.3     |
|-----------------------------------------+----------------------+----------------------+
| GPU  Name                 Persistence-M | Bus-Id        Disp.A | Volatile Uncorr. ECC |
| Fan  Temp   Perf          Pwr:Usage/Cap |         Memory-Usage | GPU-Util  Compute M. |
|                                         |                      |               MIG M. |
|=========================================+======================+======================|
|   0  Tesla T4                       On  | 00000000:00:03.0 Off |                    0 |
| N/A   41C    P0              26W /  70W |  10457MiB / 15360MiB |      0%      Default |
|                                         |                      |                  N/A |
+---------------------------------------------------------------------------------------+
| Processes:                                                                            |
|  GPU   GI   CI        PID   Type   Process name                            GPU Memory |
|        ID   ID                                                             Usage      |
|=======================================================================================|
|    0   N/A  N/A      1822      G   /usr/lib/xorg/Xorg                            4MiB |
|    0   N/A  N/A     39215      C   tritonserver                              10448MiB |
+---------------------------------------------------------------------------------------+

# nvtop
Device 0 [Tesla T4] PCIe GEN 3@ 8x RX: 0.000 KiB/s TX: 0.000 KiB/s
 GPU 585MHz  MEM 5000MHz TEMP  42°C FAN N/A% POW  26 /  70 W
 GPU[                         0%] MEM[|||||||||||10.633Gi/15.000Gi]
   ┌────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
100│GPU0 %                                                                                                                                                                                      │
   │GPU0 mem%                                                                                                                                           
    PID USER DEV    TYPE  GPU        GPU MEM    CPU  HOST MEM Command                                                                                                                            
  39215 root   0 Compute   0%  10448MiB  68%     0%   1830MiB tritonserver --model-repository=/models --exit-on-error=false                                                                      
   1822  gdm   0 Graphic   0%      4MiB   0%     0%    131MiB /usr/lib/xorg/Xorg vt1 -displayfd 3 -auth /run/user/123/gdm/Xauthority -nolisten tcp -background none -noreset -keeptty -novtswitch

# docker ps
(base) ocr@eblict-gpu-04:~/ocr/core_ocr_services$ docker ps
CONTAINER ID   IMAGE                                   COMMAND                  CREATED          STATUS          PORTS                              NAMES
a23729bc8711   nvcr.io/nvidia/tritonserver:22.12-py3   "/opt/nvidia/nvidia_…"   19 minutes ago   Up 19 minutes   0.0.0.0:8000-8002->8000-8002/tcp   triton-server
4f2367701a05   python:3.10-slim                        "python3"                21 minutes ago   Up 21 minutes                                      python3.10-slim

# tmux list-sessions
(base) ocr@eblict-gpu-04:~/ocr/core_ocr_services$ tmux list-sessions
consumers: 1 windows (created Wed Jan 24 23:57:33 2024)
docker-triton: 1 windows (created Wed Jan 24 16:56:37 2024)
python-container: 1 windows (created Wed Jan 24 23:50:34 2024)
