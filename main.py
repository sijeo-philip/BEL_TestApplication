#!/usr/bin/env python
import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showinfo
import time
from token import EXACT_TOKEN_TYPES
from mcp2210 import Mcp2210, Mcp2210GpioDesignation, Mcp2210GpioDirection
import hid



class intF:
    connStatus = 0
    vid = 0x04D8
    pid = 0x00DE
    serailNumber = ""
    manufactuere = ""
    product = ""

PLL1 = 0
PLL2 = 1

try:
    h= hid.device()
    h.open(intF.vid, intF.pid)
    intF.manufactuere = h.get_manufacturer_string()
    intF.product = h.get_product_string()
    intF.serailNumber = h.get_serial_number_string()
    print("Manufacturer: {}".format(intF.manufactuere))
    print("Product: {}".format(intF.product))
    print("Serail No: {}".format(intF.serailNumber))

    mcp = Mcp2210(serial_number = intF.serailNumber, vendor_id= intF.vid, product_id= intF.pid)
    mcp.configure_spi_timing(chip_select_to_data_delay=0, last_data_byte_to_cs=0, delay_between_bytes=0)
    intF.connStatus = 1
except Exception as err:
    print("Device is not connected: {}".format(err))
    intF.connStatus = 0


class mcpAPI():
    def mcp_init():
        try:
            h= hid.device()
            h.open(intF.vid, intF.pid)
            intF.manufactuere = h.get_manufacturer_string()
            intF.product = h.get_product_string()
            intF.serailNumber = h.get_serial_number_string()
            print("Manufacturer: {}".format(intF.manufactuere))
            print("Product: {}".format(intF.product))
            print("Serail No: {}".format(intF.serailNumber))

            mcp = Mcp2210(serial_number = intF.serailNumber, vendor_id= intF.vid, product_id= intF.pid)
            mcp.configure_spi_timing(chip_select_to_data_delay=0, last_data_byte_to_cs=0, delay_between_bytes=0)
            intF.connStatus = 1
        except Exception as err:
            print("Device is not connected: {}".format(err))
            intF.connStatus = 0

    def gpio_mode(pin, value):
        mcp.set_gpio_designation(pin, Mcp2210GpioDesignation.GPIO)
        if 1 == value:
            mcp.set_gpio_direction(pin, Mcp2210GpioDirection.INPUT)
        elif 0 == value:
            mcp.set_gpio_direction(pin, Mcp2210GpioDirection.OUTPUT)

    def gpio_write(pin, value):
        mcp.set_gpio_output_value(pin, value)

    def gpio_read(pin):
        return mcp.get_gpio_value(pin)

    def spi_init(cs_pin):
        if(PLL1 == cs_pin):
            print("Initiating the PLL1...")
        else:
            print("Initiating the PLL2...")
        mcp.set_gpio_designation(cs_pin, Mcp2210GpioDesignation.CHIP_SELECT)

    def spi_write(cs_pin, payload):
        print("Sending Byte: {}\n".format(payload))
        tx_data = bytes(payload)
        rx_data = mcp.spi_exchange(tx_data, cs_pin_number=cs_pin)


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("PLL SETTING APPLICATION")
        self.geometry("600x700")

        self.registerR = []
        self.labels = []
        self.entries = []
        self.button1 = []
        self.button2 = []

        for i in range(11):
            self.registerR.append(tk.LabelFrame(self, width=100, highlightthickness=3, labelanchor='nw', text='Register R'+str(i)))
            self.registerR[i].grid(row=i, column=0, padx=20, ipadx=20)

            self.labels.append(ttk.Label(self.registerR[i], text='R'+str(i)))
            self.labels[i].grid(column=2, row=0)

            self.entries.append(ttk.Entry(self.registerR[i], width=50))
            self.entries[i].grid(column=3, row=0)

            self.button1.append(ttk.Button(self.registerR[i], text="PLL1 Configure"))
            self.button1[i].grid(column=4, row=0)

            self.button2.append(ttk.Button(self.registerR[i], text="PLL2 Configure"))
            self.button2[i].grid(column=5, row=0)

        self.button1[0]['command'] = lambda:self.button1_clicked(0)
        self.button2[0]['command'] = lambda:self.button2_clicked(0)

        self.button1[1]['command'] = lambda: self.button1_clicked(1)
        self.button2[1]['command'] = lambda: self.button2_clicked(1)

        self.button1[2]['command'] = lambda: self.button1_clicked(2)
        self.button2[2]['command'] = lambda: self.button2_clicked(2)

        self.button1[3]['command'] = lambda: self.button1_clicked(3)
        self.button2[3]['command'] = lambda: self.button2_clicked(3)

        self.button1[4]['command'] = lambda: self.button1_clicked(4)
        self.button2[4]['command'] = lambda: self.button2_clicked(4)

        self.button1[5]['command'] = lambda: self.button1_clicked(5)
        self.button2[5]['command'] = lambda: self.button2_clicked(5)

        self.button1[6]['command'] = lambda: self.button1_clicked(6)
        self.button2[6]['command'] = lambda: self.button2_clicked(6)

        self.button1[7]['command'] = lambda: self.button1_clicked(7)
        self.button2[7]['command'] = lambda: self.button2_clicked(7)

        self.button1[8]['command'] = lambda: self.button1_clicked(8)
        self.button2[8]['command'] = lambda: self.button2_clicked(8)

        self.button1[9]['command'] = lambda: self.button1_clicked(9)
        self.button2[9]['command'] = lambda: self.button2_clicked(9)

        self.button1[10]['command'] = lambda: self.button1_clicked(10)
        self.button2[10]['command'] = lambda: self.button2_clicked(10)

        self.registerR.append(tk.LabelFrame(self, width=100, highlightthickness=3, labelanchor='nw', text='Register R'+str(13)))
        self.registerR[11].grid(row=11, column=0, padx=20, ipadx=20)

        self.labels.append(ttk.Label(self.registerR[11], text='R' + str(13)))
        self.labels[11].grid(column=2, row=0)

        self.entries.append(ttk.Entry(self.registerR[11], width=50))
        self.entries[11].grid(column=3, row=0)

        self.button1.append(ttk.Button(self.registerR[11], text="PLL1 Configure", command=lambda:self.button1_clicked(13)))
        self.button1[11].grid(column=4, row=0)

        self.button2.append(ttk.Button(self.registerR[11], text="PLL2 Configure", command=lambda:self.button2_clicked(13)))
        self.button2[11].grid(column=5, row=0)

        self.registerR.append(tk.LabelFrame(self, width=100, highlightthickness=3, labelanchor='nw', text='Register R' + str(15)))
        self.registerR[12].grid(row=12, column=0, padx=20, ipadx=20)

        self.labels.append(ttk.Label(self.registerR[12], text='R' + str(15)))
        self.labels[12].grid(column=2, row=0)

        self.entries.append(ttk.Entry(self.registerR[12], width=50))
        self.entries[12].grid(column=3, row=0)

        self.button1.append(ttk.Button(self.registerR[12], text="PLL1 Configure", command=lambda:self.button1_clicked(15)))
        self.button1[12].grid(column=4, row=0)

        self.button2.append(ttk.Button(self.registerR[12], text="PLL2 Configure", command=lambda:self.button2_clicked(15)))
        self.button2[12].grid(column=5, row=0)

    def button1_clicked(self, value):
        print("Button1 {} is pressed\n".format(value))
        try:
            mcpAPI.spi_init(PLL1)
            mcpAPI.spi_write(PLL1, 255);
        except Exception as err:
            print("Device Connection Error: {}".format(err))
            #mcpAPI.mcp_init()
    
    time.sleep(1)
    def button2_clicked(self, value):
        print("Button2 {} is pressed\n".format(value))
        try:
            mcpAPI.spi_init(PLL2)
            mcpAPI.spi_write(PLL2, 255)
        except Exception as err:
            print("Device Connection Error: {}".format(err))
           # mcpAPI.mcp_init()
            
    def register_data_capture(self):
        pass
    
if __name__ == '__main__':
    app = App()
    app.mainloop()

