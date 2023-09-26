python3 nordicsemi/__main__.py -v dfu usb-serial -pkg ~/'builds/folium dongle/ota/Folium_Dongle-2-6-1-OTA-Image.zip' --port /dev/ttyACM0
# On Pi
sudo python3 pc-nrfutil/nordicsemi/__main__.py -v dfu usb-serial -pkg ~/Folium_Dongle-2-6-1-OTA-Image.zip --port /dev/ttyACM0
sudo python3 nordicsemi/__main__.py -v dfu usb-serial -pkg ~/Folium_Dongle-2-6-1-OTA-Image.zip --port /dev/ttyACM0
sudo pip3 install -r requirements-frozen.txt

sudo pip3 install pc_ble_driver_py
sudo pip3 install intelhex
sudo pip3 install protobuf
sudo pip3 install pyserial==3.5
sudo pip3 install pyspinel==1.0.3
sudo pip3 install PyYAML==5.4.1
sudo pip3 install tqdm==4.62.0
sudo pip3 install antlib==1.1b1
sudo pip3 install click==8.0.1
sudo pip3 install crcmod==1.7
sudo pip3 install ecdsa==0.17.0
sudo pip3 install intelhex==2.3.0
sudo pip3 install libusb1==1.9.3
sudo pip3 install pc-ble-driver-py
sudo pip3 install piccata==2.0.1
sudo pip3 install protobuf==3.17.3
