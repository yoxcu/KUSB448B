import json
import sys

def main():
    filename="KUSB448BInit"
    # Opening JSON file
    fi = open(filename+".json","r")

    # returns JSON object as
    # a dictionary
    data = json.load(fi)
    print("Found {} entrys.".format(len(data)))

    # Iterating through the json
    # list
    fo = open(filename+".hpp","w")
    fo.write("struct Transfer {\n    uint8_t bmRequestType;\n    uint8_t bRequest;\n    uint16_t wValue;\n    uint16_t wIndex;\n    std::vector <uint8_t> data;\n};\n\n")
    fo.write("std::vector <Transfer> {}Data{{\n".format(filename))
    pkgs=[]
    for i in range(len(data)):
        #print(data[i])
        bmRequestType=data[i]["_source"]["layers"]["Setup Data"]["usb.bmRequestType"]
        bRequest=hex(int(data[i]["_source"]["layers"]["Setup Data"]["usb.setup.bRequest"]))
        wValue=data[i]["_source"]["layers"]["Setup Data"]["usb.setup.wValue"]
        wIndex=hex(int(data[i]["_source"]["layers"]["Setup Data"]["usb.setup.wIndex"]))
        wLength=int(data[i]["_source"]["layers"]["Setup Data"]["usb.setup.wLength"])
        data_fragment=[]
        try:
            data_fragment=data[i]["_source"]["layers"]["Setup Data"]["usb.data_fragment"].split(":")
        except:
            print("No Data Found")
        if (wLength!=len(data_fragment)):
            print("Error wLength: {} != data length: {}".format(wLength,len(data_fragment)))
            return
        for i in range(len(data_fragment)):
            data_fragment[i]="0x{}".format(data_fragment[i])
        data_fragment=", ".join(data_fragment)
        wLength=hex(wLength)
        #print("bmRequestType: {}\nbRequest: {}\nwValue: {}\nwIndex: {}\nwLength: {}\ndata: {}".format(bmRequestType,bRequest,wValue,wIndex,wLength,data_fragment))
        pkgs.append("    {{{}, {}, {}, {}, {{\n        {}\n        }}\n    }}".format(bmRequestType,bRequest,wValue,wIndex,data_fragment))
    fo.write(",\n".join(pkgs))
    fo.write("\n};")
    # Closing file
    fi.close()
    fo.close()

if __name__ == "__main__":
    main()
