#include <iostream>
#include <libusb.h>
#include <vector>
#include "KUSB448BInit.hpp"

int main() {
    uint16_t vid=0x05e6;
    uint16_t pid=0xeeee;
    int interfaceNumber_=0;
    int timeout=5000;
    std::cout << "Trying to Init KUSB448B" << std::endl;
    libusb_device **devs = nullptr; //pointer to pointer of device, used to retrieve a list of devices
    int r = libusb_init(nullptr);
    if(r < 0) {
        std::cout<<"init error"<<std::endl;
        return 1;
    }
    std::cout<<"UsbSession created!"<<std::endl;
    ssize_t cnt = libusb_get_device_list(nullptr, &devs); //get the list of devices
    if(cnt < 0) {
        std::cout<<"device list error"<<std::endl;
        return 1;
    }

    std::cout<<cnt<<" Devices in list."<<std::endl;
    libusb_device_handle *dev_handle = libusb_open_device_with_vid_pid(nullptr, vid, pid);
    if(dev_handle == nullptr) {
        std::cout << "open error" << std::endl;
        return 1;
    }
    libusb_free_device_list(devs, cnt);
    std::cout<<"Device opened!"<<std::endl;

    //std::cout<<"Device reset"<<std::endl;
    if(libusb_kernel_driver_active(dev_handle, interfaceNumber_) == 1) { //find out if kernel driver is attached
        std::cout<<"Kernel Driver Active"<<std::endl;
        if(libusb_detach_kernel_driver(dev_handle, interfaceNumber_) == 0) //detach it
            std::cout<<"Kernel Driver Detached!"<<std::endl;
    }
    r = libusb_claim_interface(dev_handle, interfaceNumber_); //claim interface 0 (the first) of device (mine had jsut 1)
    if(r < 0) {
        std::cout << "claim error" << std::endl;
        return 1;
    }

    for (auto trf : KUSB448BInitData){
        r = libusb_control_transfer(dev_handle,trf.bmRequestType,trf.bRequest,trf.wValue,trf.wIndex,trf.data.data(),trf.data.size(),timeout);
        if (r != trf.data.size()){
            std::cout << "ctrl error: "<<r << std::endl;
            return 1;    }
    }



    libusb_exit(nullptr);
    return 0;
}
