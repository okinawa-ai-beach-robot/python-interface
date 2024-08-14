# Setup of Jetson Orin Nano
Allow shutdown for all users
```
sudo sh -c "echo '%wheel ALL= NOPASSWD: /sbin/shutdown' >> /etc/sudoers"
sudo sh -c "echo '%wheel ALL= NOPASSWD: /usr/bin/systemctl poweroff' >> /etc/sudoers"
```
## System package install
Jetpack version used is: 5.1.2-b104
Currently installed version can be seen by executing `scripts/beachbot_get_jetpack_version`

Make sure the following software versions are present:
- Python 3.8.10
- 


```
sudo apt install build-essential 
sudo apt update
sudo apt install nvidia-jetpack
sudo apt install python3-pip
sudo pip3 install jetson-stats
sudo reboot
```

```
sudo apt-get install libjpeg-dev zlib1g-dev libpython3-dev libavcodec-dev libavformat-dev libswscale-dev libopenblas-base libopenmpi-dev
sudo apt-get install libopenblas-dev
```

add to bashrc:
```
export LD_LIBRARY_PATH=/usr/local/cuda/lib64
export PATH=$PATH:/usr/local/cuda/bin
```




## Pyton package install
Common packages:
```
sudo pip install Jetson.GPIO==2.1.6 #2.1.6. fizes gpio assignment issue: ValueError: Channel 32 is not a PWM
```

Pytorch:
Find packages on https://elinux.org/Jetson_Zoo#ONNX_Runtime

```
python3 -m pip install --no-cache torch-2.1.0a0+41361538.nv23.06-cp38-cp38-linux_aarch64.whl
```


Onnx runtime:
```
# libc++ incompatibility:
# wget https://nvidia.box.com/shared/static/zostg6agm00fb6t5uisw51qi6kpcuwzd.whl -O onnxruntime_gpu-1.17.0-cp38-cp38-linux_aarch64.whl
# sudo pip install onnxruntime_gpu-1.17.0-cp38-cp38-linux_aarch64.whl

# libc++ incompatibility:
# wget https://nvidia.box.com/shared/static/3fechcaiwbtblznlchl6dh8uuat3dp5r.whl -O onnxruntime_gpu-1.18.0-cp38-cp38-linux_aarch64.whl
# sudo pip install onnxruntime_gpu-1.18.0-cp38-cp38-linux_aarch64.whl


wget https://nvidia.box.com/shared/static/iizg3ggrtdkqawkmebbfixo7sce6j365.whl -O onnxruntime_gpu-1.16.0-cp38-cp38-linux_aarch64.whl
sudo pip install onnxruntime_gpu-1.16.0-cp38-cp38-linux_aarch64.whl
```
