#!/usr/bin/env python
from http.client import SERVICE_UNAVAILABLE
from logging import disable
from re import template
import tkinter as tk
from tkinter import ttk
import webbrowser
from tkinter import messagebox
import time
from token import EXACT_TOKEN_TYPES
from mcp2210 import Mcp2210, Mcp2210GpioDesignation, Mcp2210GpioDirection
import hid
import struct 

h = ""
mcp = ""

labelFont = ('Tahoma', 6)
spinboxFont= ('Tahoma', 6)


class intF:
    connStatus = 0
    vid = 0x04D8
    pid = 0x00DE
    serialNumber = ""
    manufactuere = ""
    product = ""
    PLL1 = 0
    PLL2 = 1

    #R0 values
    id_r0_value = ""
    frac_dither_r0_value = ""
    no_fcal_r0_value = ""
    plln_r0_value = ""
    pllnum_r0_value = ""

    #R1 values
    cpg_r1_value = ""
    vcosel_r1_value = ""
    pllnum_r1_value = ""
    frac_order_r1_value = ""
    pll_r_r1_value = ""

    #R2 Value
    osc2x_r2_value = ""
    cpp_r2_value = ""
    pllden_r2_value = ""

    #R3 value
    vcodiv_r3_value = ""
    outb_pwr_r3_value = ""
    outa_pwr_r3_value = ""
    outb_pd_r3_value = ""
    outa_pd_r3_value = ""

    #R4 value
    pfd_dly_r4_value = ""
    fl_frce_r4_value = ""
    fl_toc_r4_value = ""
    fl_cpg_r4_value = ""
    fl_cpg_bleed_r4_value = ""

    #R5 value
    outld_en_r5_value = ""
    oscfreq_r5_value = ""
    bufen_dis_r5_value = ""
    vco_sel_mode_r5_value = ""
    outb_mux_r5_value = ""
    outa_mux_r5_value = ""
    odly_r5_value = ""
    mode_r5_value = ""
    pwdn_mode_r5_value = ""
    reset_r5_value = ""

    #R6 value
    rd_diagnostics_r6_value = ""
    rdaddr_r6_value = ""
    uWirelock_r6_value = ""

    #R7 value
    fl_select_r7_value = ""
    fl_pinMode_r7_value = ""
    fl_inv_r7_value = ""
    muxout_select_r7_value = ""
    mux_inv_r7_value = ""
    muxout_pinmode_r7_value = ""
    ld_select_r7_value = ""
    ld_inv_r7_value = ""
    ld_pinmode_r7_value = ""

    #R8 R9 R10 values
    reg_r8_value = ""
    reg_r9_value = ""
    reg_r10_value = ""

    #R13 value
    dld_err_cnt_r13_value = "" 
    dld_pass_cnt_r13_value = ""
    dld_tol_r13_value = ""

    #R15 value
    vcocap_man_r15_value = ""
    vco_capcode_r15_value = ""
    
    #payloads
    spi_rxData = ""

try:
    h = hid.device()
    h.open(intF.vid, intF.pid)
    intF.manufactuere = h.get_manufacturer_string()
    intF.serialNumber = h.get_serial_number_string()
    intF.product = h.get_product_string()
    print("Manufactuere: {}".format(intF.manufactuere))
    print("Product: {}".format(intF.product))
    print("Serial Number: {}".format(intF.serialNumber))
    
    mcp = Mcp2210(serial_number=intF.serialNumber, vendor_id=intF.vid, product_id=intF.pid)
    mcp.configure_spi_timing(chip_select_to_data_delay=0, last_data_byte_to_cs=0, delay_between_bytes=0)
    intF.connStatus = 1

except Exception as err:
    print("Device is not Connected: {}".format(err))
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
        if(intF.PLL1 == cs_pin):
            print("Initiating the PLL1...")
        else:
            print("Initiating the PLL2...")
        mcp.set_gpio_designation(cs_pin, Mcp2210GpioDesignation.CHIP_SELECT)

    def spi_write(cs_pin, payload):
        print("Sending Byte: {}\n".format(payload))
        #tx_data = bytes(payload)
        intF.spi_rxData = payload
        #print(tx_data)
        #rx_data = mcp.spi_exchange(tx_data, cs_pin_number = cs_pin)
        #"""
        temp_txData = struct.unpack('4B', struct.pack('>I', payload))
        temp_txByteArrayData = bytearray()
        for i in range(len(temp_txData)):
            temp_txByteArrayData.append(temp_txData[i])
        temp_txByteData = bytes(temp_txByteArrayData)
        print( "Value of Temp txData: {}  leb: {}".format(temp_txData, len(temp_txData)))
        """
        for i in range(4):
            print("Temp_txData: {}".format(temp_txData[i]))
            rx_data = mcp.spi_exchange(bytes(temp_txData[i]), cs_pin_number=cs_pin)
            #rx_data = temp_txData.append(mcp.spi_exchange(temp_txData[i], cs_pin_number=cs_pin))
            print("SPI RX_Data: {}".format(rx_data))
        """
        rx_data = mcp.spi_exchange(temp_txByteData, cs_pin_number=cs_pin)
        print("SPI RX_DATA: {}".format(rx_data))
        #"""
        

    def spi_write_payload(button, value):
        print("Received value: {}\nButton: {}".format(value, button))
        if 0 == value:
            print("Reg: 0")
            tempList = [int(intF.id_r0_value.get()), int(intF.frac_dither_r0_value.get()), int(intF.no_fcal_r0_value.get()), int(intF.plln_r0_value.get()), int(intF.pllnum_r0_value.get())]
            print("ID: {}  Frac Dither: {}  No Fcal: {}  PLL No: {}  PLL Num: {}".format(tempList[0], tempList[1], tempList[2], tempList[3], tempList[4]))
            tempByte = 0
            tempByte = tempByte<<1|tempList[0]
            tempByte = tempByte<<2|tempList[1]
            tempByte = tempByte<<1|tempList[2]
            tempByte = tempByte<<12|tempList[3]
            tempByte = tempByte<<12|tempList[4]
            tempByte = tempByte<<4|int(value)
            print(tempByte)
            mcpAPI.spi_init(button)
            mcpAPI.spi_write(button, tempByte)

           
        elif 1 == value:
            print("Reg:  1")
            tempList = [int(intF.cpg_r1_value.get()), int(intF.vco_sel_mode_r5_value.get()), int(intF.pllnum_r0_value.get()), int(intF.frac_order_r1_value.get()), int(intF.pll_r_r1_value.get())]
            print("CPG: {}  VCO SEL: {}  PLL Num: {}  FRAC Order: {}  PLL R: {}".format(tempList[0], tempList[1], tempList[2], tempList[3], tempList[4]))
            tempByte = 0
            tempByte = tempByte<<5|tempList[0]
            tempByte = tempByte<<2|tempList[1]
            tempByte = tempByte<<10|tempList[2]
            tempByte = tempByte<<3|tempList[3]
            tempByte = tempByte<<8|tempList[4]
            tempByte = tempByte<<4|int(value)
            print(tempByte)
            mcpAPI.spi_init(button)
            mcpAPI.spi_write(button, tempByte)

        elif 2 == value:
            print("Reg:  2")
            tempList = [int(intF.osc2x_r2_value.get()), int(intF.cpp_r2_value.get()), int(intF.pllden_r2_value.get())]
            print("OSC 2X: {}  CPP: {}  PLL DEN: {}".format(tempList[0], tempList[1], tempList[2]))
            tempByte = 0
            tempByte = tempByte<<1|0
            tempByte = tempByte<<1|0
            tempByte = tempByte<<1|tempList[0]
            tempByte = tempByte<<1|0
            tempByte = tempByte<<1|tempList[1]
            tempByte = tempByte<<1|1
            tempByte = tempByte<<22|tempList[2]
            tempByte = tempByte<<4|int(value)
            print(tempByte)
            mcpAPI.spi_init(button)
            mcpAPI.spi_write(button, tempByte)

        elif 3 == value:
            print("Reg:  3")
            tempList = [int(intF.vcodiv_r3_value.get()), int(intF.outb_pwr_r3_value.get()), int(intF.outa_pwr_r3_value.get()), int(intF.outb_pd_r3_value.get()), int(intF.outa_pd_r3_value.get())]
            print("VCO Div: {}  OutB Pwr: {}  OutA Pwr: {}  OutB PD: {}  OutA PD: {}".format(tempList[0], tempList[1], tempList[2], tempList[3], tempList[4]))
            tempByte = 0
            tempByte = tempByte<<1|0
            tempByte = tempByte<<1|0
            tempByte = tempByte<<1|1
            tempByte = tempByte<<1|0
            tempByte = tempByte<<1|0
            tempByte = tempByte<<1|0
            tempByte = tempByte<<1|0
            tempByte = tempByte<<1|0
            tempByte = tempByte<<1|0
            tempByte = tempByte<<5|tempList[0]
            tempByte = tempByte<<6|tempList[1]
            tempByte = tempByte<<6|tempList[2]
            tempByte = tempByte<<1|tempList[3]
            tempByte = tempByte<<1|tempList[4]
            tempByte = tempByte<<4|int(value)
            print(tempByte)
            mcpAPI.spi_init(button)
            mcpAPI.spi_write(button, tempByte)

        elif 4 == value:
            print("Reg:  4")
            tempList = [int(intF.pfd_dly_r4_value.get()), int(intF.fl_frce_r4_value.get()), int(intF.fl_toc_r4_value.get()), int(intF.fl_cpg_r4_value.get()), int(intF.fl_cpg_bleed_r4_value.get())]
            print("PFD DLY: {}  FL FRCE: {}  FL TOC: {}  FL CPG: {}  CPG Bleed: {}".format(tempList[0], tempList[1], tempList[2], tempList[3], tempList[4]))
            tempByte = 0
            tempByte = tempByte<<3|tempList[0]
            tempByte = tempByte<<1|tempList[1]
            tempByte = tempByte<<12|tempList[2]
            tempByte = tempByte<<5|tempList[3]
            tempByte = tempByte<<1|1
            tempByte = tempByte<<6|tempList[4]
            tempByte = tempByte<<4|int(value)
            print(tempByte)
            mcpAPI.spi_init(button)
            mcpAPI.spi_write(button, tempByte)

        elif 5 == value:
            print("Reg:  5")
            tempList = [int(intF.outld_en_r5_value.get()), int(intF.oscfreq_r5_value.get()), int(intF.bufen_dis_r5_value.get()), int(intF.vco_sel_mode_r5_value.get()), int(intF.outb_mux_r5_value.get()), int(intF.outa_mux_r5_value.get()), int(intF.odly_r5_value.get()), int(intF.mode_r5_value.get()), int(intF.pwdn_mode_r5_value.get()), int(intF.reset_r5_value.get())]
            print("Out LDEN: {} Osc Freq: {}  Buf EN Dis: {}  VCO Sel Mode: {}  OutB Mux: {}  OutA Mux: {}  O Dly: {}  Mode: {}  Pw DN Mode: {}  Reset: {}".format(tempList[0], tempList[1], tempList[2], tempList[3], tempList[4], tempList[5], tempList[6], tempList[7], tempList[8], tempList[9]))
            tempByte = 0
            tempByte = tempByte<<7|0
            tempByte = tempByte<<1|tempList[0]
            tempByte = tempByte<<3|tempList[1]
            tempByte = tempByte<<1|tempList[2]
            tempByte = tempByte<<3|0
            tempByte = tempByte<<2|tempList[3]
            tempByte = tempByte<<2|tempList[4]
            tempByte = tempByte<<2|tempList[5]
            tempByte = tempByte<<1|tempList[6]
            tempByte = tempByte<<2|tempList[7]
            tempByte = tempByte<<3|tempList[8]
            tempByte = tempByte<<1|tempList[9]
            tempByte = tempByte<<4|int(value)
            print(tempByte)
            mcpAPI.spi_init(button)
            mcpAPI.spi_write(button, tempByte)

        elif 6 == value:
            print("Reg:  6")
            tempList = [int(intF.rd_diagnostics_r6_value.get()), int(intF.rdaddr_r6_value.get()), int(intF.uWirelock_r6_value.get())]
            print("RD Diagnostics: {}  RD AddrL: {}  uWire Lock: {}".format(tempList[0], tempList[1], tempList[2]))
            tempByte = 0
            tempByte = tempByte<<1|0
            tempByte = tempByte<<20|tempList[0]
            tempByte = tempByte<<1|1
            tempByte = tempByte<<1|0
            tempByte = tempByte<<4|tempList[1]
            tempByte = tempByte<<1|tempList[2]
            tempByte = tempByte<<4|int(value)
            print(tempByte)
            mcpAPI.spi_init(button)
            mcpAPI.spi_write(button, tempByte)

        elif 7 == value:
            print("Reg:  7")
            tempList = [int(intF.fl_select_r7_value.get()), int(intF.fl_pinMode_r7_value.get()), int(intF.fl_inv_r7_value.get()), int(intF.muxout_select_r7_value.get()), int(intF.mux_inv_r7_value.get()), int(intF.muxout_pinmode_r7_value.get()), int(intF.ld_select_r7_value.get()), int(intF.ld_inv_r7_value.get()), int(intF.ld_pinmode_r7_value.get())]
            print("FL Select: {}  FL Pinmode: {}  FL Inv: {}  Mux out Select: {}  Mux Inv: {}  Mux Out Pinmode: {}  LD Select: {}  LD Inv: {}  LD Pinmode: {}".format(tempList[0], tempList[1], tempList[2], tempList[3], tempList[4], tempList[5], tempList[6], tempList[7], tempList[8]))
            tempByte = 0
            tempByte = tempByte<<1|0
            tempByte = tempByte<<5|tempList[0]
            tempByte = tempByte<<3|tempList[1]
            tempByte = tempByte<<1|tempList[2]
            tempByte = tempByte<<5|tempList[3]
            tempByte = tempByte<<1|tempList[4]
            tempByte = tempByte<<3|tempList[5]
            tempByte = tempByte<<5|tempList[6]
            tempByte = tempByte<<1|tempList[7]
            tempByte = tempByte<<3|tempList[8]
            tempByte = tempByte<<4|int(value)
            print(tempByte)
            mcpAPI.spi_init(button)
            mcpAPI.spi_write(button, tempByte)

        elif 8 == value:
            print("Reg:  8")
            tempList = [int(intF.reg_r8_value.get())]
            print("R8: {}".format(tempList[0]))
            tempByte = 0
            tempByte = tempByte<<12|519
            tempByte = tempByte<<12|3547
            tempByte = tempByte<<4|15
            tempByte = tempByte<<4|int(value)
            print(tempByte)
            mcpAPI.spi_init(button)
            mcpAPI.spi_write(button, tempByte)

        elif 9 == value:
            print("Reg:  9")
            tempList = [int(intF.reg_r9_value.get())]
            print("R9: {}".format(tempList[0]))
            tempByte = 0
            tempByte = tempByte<<12|60
            tempByte = tempByte<<12|124
            tempByte = tempByte<<4|3
            tempByte = tempByte<<4|int(value)
            print(tempByte)
            mcpAPI.spi_init(button)
            mcpAPI.spi_write(button, tempByte)

        elif 10 == value:
            print("Reg: 10")  
            tempList = [int(intF.reg_r10_value.get())]
            print("R10: {}".format(tempList[0]))
            tempByte = 0
            tempByte = tempByte<<12|528
            tempByte = tempByte<<12|80
            tempByte = tempByte<<4|12
            tempByte = tempByte<<4|int(value)
            print(tempByte)
            mcpAPI.spi_init(button)
            mcpAPI.spi_write(button, tempByte)

        elif 13 == value:
            print("Reg:  13")
            tempList = [int(intF.dld_err_cnt_r13_value.get()), int(intF.dld_pass_cnt_r13_value.get()), int(intF.dld_tol_r13_value.get())]
            print("DLD Err Cnt: {}  DLD Pass Cnt: {}  DLD Tol: {}".format(tempList[0], tempList[1], tempList[2]))
            tempByte = 0
            tempByte = tempByte<<4|tempList[0]
            tempByte = tempByte<<10|tempList[1]
            tempByte = tempByte<<3|tempList[2]
            tempByte = tempByte<<11|1040
            tempByte = tempByte<<4|int(value)
            print(tempByte)
            mcpAPI.spi_init(button)
            mcpAPI.spi_write(button, tempByte)

        elif 15 == value:
            print("Reg:  15")
            tempList = [int(intF.vcocap_man_r15_value.get()), int(intF.vco_capcode_r15_value.get())]
            print("VCO Cap Man: {}  VCO Cap Code: {}".format(tempList[0], tempList[1]))
            tempByte = 0
            tempByte = tempByte<<19|4351
            tempByte = tempByte<<1|tempList[0]
            tempByte = tempByte<<8|tempList[1]
            tempByte = tempByte<<4|int(value)
            print(tempByte)
            mcpAPI.spi_init(button)
            mcpAPI.spi_write(button, tempByte)

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("PLL SETTING APPLICATION")
        self.geometry("850x600")
        #self.resizable(0,0)

        self.registerR = []
        self.labels = []
        self.entries = []
        self.button1 = []
        self.button2 = []
        self.button3 = []

        self.info_icon = tk.PhotoImage(file='info.png')

        self.mainFrame = tk.Frame(self, width=700, height=700)
        self.mainFrame.pack(fill=tk.BOTH, expand=1)

        self.mainCanvas = tk.Canvas(self.mainFrame)
        self.mainCanvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

        self.scrollBar_updwn = ttk.Scrollbar(self.mainFrame, orient=tk.VERTICAL, command=self.mainCanvas.yview)
        self.scrollBar_updwn.pack(side=tk.RIGHT, fill=tk.Y)


        id_r0_var = tk.IntVar()
        intF.id_r0_value = id_r0_var
        frac_dither_r0_var = tk.IntVar()
        intF.frac_dither_r0_value = frac_dither_r0_var
        no_fcal_r0_var = tk.IntVar()
        intF.no_fcal_r0_value = no_fcal_r0_var
        plln_r0_var = tk.IntVar()
        intF.plln_r0_value = plln_r0_var
        pllnum_r0_var = tk.IntVar()
        intF.pllnum_r0_value = pllnum_r0_var

        cpg_r1_var = tk.IntVar()
        intF.cpg_r1_value = cpg_r1_var
        vcosel_r1_var = tk.IntVar()
        intF.vcosel_r1_value = vcosel_r1_var
        pllnum_r1_var = tk.IntVar()
        intF.pllnum_r1_value = pllnum_r1_var
        frac_order_r1_var = tk.IntVar()
        intF.frac_order_r1_value = frac_order_r1_var
        pll_r_r1_var = tk.IntVar()
        intF.pll_r_r1_value = pll_r_r1_var

        osc2x_r2_var = tk.IntVar()
        intF.osc2x_r2_value = osc2x_r2_var
        cpp_r2_var = tk.IntVar()
        intF.cpp_r2_value = cpp_r2_var
        pllden_r2_var = tk.IntVar()
        intF.pllden_r2_value = pllden_r2_var

        vcodiv_r3_var = tk.IntVar()
        intF.vcodiv_r3_value = vcodiv_r3_var
        outb_pwr_r3_var = tk.IntVar()
        intF.outb_pwr_r3_value = outb_pwr_r3_var
        outa_pwr_r3_var = tk.IntVar()
        intF.outa_pwr_r3_value = outa_pwr_r3_var
        outb_pd_r3_var = tk.IntVar()
        intF.outb_pd_r3_value = outb_pd_r3_var
        outa_pd_r3_var = tk.IntVar()
        intF.outa_pd_r3_value = outa_pd_r3_var

        pfd_dly_r4_var = tk.IntVar()
        intF.pfd_dly_r4_value = pfd_dly_r4_var
        fl_frce_r4_var = tk.IntVar()
        intF.fl_frce_r4_value = fl_frce_r4_var
        fl_toc_r4_var = tk.IntVar()
        intF.fl_toc_r4_value = fl_toc_r4_var
        fl_cpg_r4_var = tk.IntVar()
        intF.fl_cpg_r4_value = fl_cpg_r4_var
        cpg_bleed_r4_var = tk.IntVar()
        intF.fl_cpg_bleed_r4_value = cpg_bleed_r4_var

        outld_en_r5_var = tk.IntVar()
        intF.outld_en_r5_value = outld_en_r5_var
        oscfreq_r5_var = tk.IntVar()
        intF.oscfreq_r5_value = oscfreq_r5_var
        bufen_dis_r5_var = tk.IntVar()
        intF.bufen_dis_r5_value = bufen_dis_r5_var
        vco_sel_mode_r5_var = tk.IntVar()
        intF.vco_sel_mode_r5_value = vco_sel_mode_r5_var
        outb_mux_r5_var = tk.IntVar()
        intF.outb_mux_r5_value = outb_mux_r5_var
        outa_mux_r5_var = tk.IntVar()
        intF.outa_mux_r5_value = outa_mux_r5_var
        odly_r5_var = tk.IntVar()
        intF.odly_r5_value = odly_r5_var
        mode_r5_var = tk.IntVar()
        intF.mode_r5_value = mode_r5_var
        pwdn_mode_r5_var = tk.IntVar()
        intF.pwdn_mode_r5_value = pwdn_mode_r5_var
        reset_r5_var = tk.IntVar()
        intF.reset_r5_value = reset_r5_var

        rd_diagnostics_r6_var = tk.IntVar()
        intF.rd_diagnostics_r6_value = rd_diagnostics_r6_var
        rdaddr_r6_var = tk.IntVar()
        intF.rdaddr_r6_value = rdaddr_r6_var
        uWirelock_r6_var = tk.IntVar()
        intF.uWirelock_r6_value = uWirelock_r6_var

        fl_select_r7_var = tk.IntVar()
        intF.fl_select_r7_value = fl_select_r7_var
        fl_pinmode_r7_var = tk.IntVar()
        intF.fl_pinMode_r7_value = fl_pinmode_r7_var
        fl_inv_r7_var = tk.IntVar()
        intF.fl_inv_r7_value = fl_inv_r7_var
        muxout_select_r7_var = tk.IntVar()
        intF.muxout_select_r7_value = muxout_select_r7_var
        mux_inv_r7_var = tk.IntVar()
        intF.mux_inv_r7_value = mux_inv_r7_var
        muxout_pinmode_r7_var = tk.IntVar()
        intF.muxout_pinmode_r7_value = muxout_pinmode_r7_var
        ld_select_r7_var = tk.IntVar()
        intF.ld_select_r7_value = ld_select_r7_var
        ld_inv_r7_var = tk.IntVar()
        intF.ld_inv_r7_value = ld_inv_r7_var
        ld_pinmode_r7_var = tk.IntVar()
        intF.ld_pinmode_r7_value = ld_pinmode_r7_var

        reg_value_r8 = tk.IntVar()
        intF.reg_r8_value = reg_value_r8
        reg_value_r9 = tk.IntVar()
        intF.reg_r9_value = reg_value_r9
        reg_value_r10 = tk.IntVar()
        intF.reg_r10_value = reg_value_r10

        dld_err_cnt_r13_var = tk.IntVar()
        intF.dld_err_cnt_r13_value = dld_err_cnt_r13_var
        dld_pass_cnt_r13_var = tk.IntVar()
        intF.dld_pass_cnt_r13_value = dld_pass_cnt_r13_var
        dld_tol_r13_var = tk.IntVar()
        intF.dld_tol_r13_value = dld_tol_r13_var

        vcocap_man_r15_var = tk.IntVar()
        intF.vcocap_man_r15_value = vcocap_man_r15_var
        vco_capcode_r15_var = tk.IntVar()
        intF.vco_capcode_r15_value = vco_capcode_r15_var

        #Configure the Canvas
        self.mainCanvas.configure(yscrollcommand=self.scrollBar_updwn.set)
        self.mainCanvas.bind('<Configure>', lambda e: self.mainCanvas.configure(scrollregion= self.mainCanvas.bbox("all")))

        #Create Another Frame in the Canvas
        self.secondMainFrame = tk.Frame(self.mainCanvas)

        #Add that New Frame to a Window in the Canvas
        self.mainCanvas.create_window((0,0), window=self.secondMainFrame, anchor="nw")



        #Adding Widgets to the Second Main Frame
        for i in range(11):
            self.registerR.append(tk.LabelFrame(self.secondMainFrame, width=100, highlightthickness=3, labelanchor='nw', text='Register R'+str(i)))
            self.registerR[i].pack(fill=tk.X, padx=5, ipady= 10)

            self.button1.append(ttk.Button(self.registerR[i], text="PLL1 Configure"))
            self.button1[i].pack(side=tk.RIGHT, padx=5)

            self.button2.append(ttk.Button(self.registerR[i], text="PLL2 Configure"))
            self.button2[i].pack(side=tk.RIGHT, padx=5)

            self.button3.append(ttk.Button(self.registerR[i], image=self.info_icon))
            self.button3[i].pack(side=tk.RIGHT, padx=5)

        #REGISTER R0
        #Single Bit ID
        self.id_label_r0 = ttk.Label(self.registerR[0], text="ID", justify=tk.LEFT, font=labelFont)
        self.id_label_r0.pack(padx=5, side=tk.LEFT, pady=5)

        self.id_r0 = ttk.Spinbox(self.registerR[0], from_=0, to=1, font=spinboxFont, width= 3, textvariable=id_r0_var)
        self.id_r0.pack(padx=1, pady=2, side=tk.LEFT)
        id_r0_var.set(self.id_r0.cget("from"))
        self.id_r0.bind('<FocusOut>', lambda e: self.validate_value(self.id_r0, id_r0_var))


        #3 BIT FRAC DITHER SETTING
        self.fracdither_label_r0 = ttk.Label(self.registerR[0], text="FRAC DITHER", justify=tk.LEFT, font=labelFont)
        self.fracdither_label_r0.pack(padx=5, side=tk.LEFT, pady=5)

        self.frac_dither_r0 = ttk.Spinbox(self.registerR[0], from_=0, to=3, font=spinboxFont, width=3, textvariable=frac_dither_r0_var)
        self.frac_dither_r0.pack(padx= 1, pady=2, side=tk.LEFT)
        frac_dither_r0_var.set(self.frac_dither_r0.cget("from"))
        self.frac_dither_r0.bind('<FocusOut>', lambda e: self.validate_value(self.frac_dither_r0, frac_dither_r0_var))

        #SINGLE BIT NO_FCAL SETTING
        self.nofcal_label_r0 = ttk.Label(self.registerR[0], text="NO_FCAL", justify=tk.LEFT,font= labelFont)
        self.nofcal_label_r0.pack(padx=5, side=tk.LEFT, pady=5)

        self.no_fcal_r0 = ttk.Spinbox(self.registerR[0], from_=0, to=1, font=spinboxFont, width=3, textvariable=no_fcal_r0_var)
        self.no_fcal_r0.pack(padx=1, side=tk.LEFT, pady=2)
        no_fcal_r0_var.set(self.no_fcal_r0.cget("from"))
        self.no_fcal_r0.bind('<FocusOut>', lambda e: self.validate_value(self.no_fcal_r0, no_fcal_r0_var))

        #12 BIT PLL_N SETTING
        self.plln_label_r0 = ttk.Label(self.registerR[0], text='PLL_N0', justify=tk.LEFT, font = labelFont)
        self.plln_label_r0.pack(padx=5, side=tk.LEFT, pady=5)

        self.plln_r0 = ttk.Spinbox(self.registerR[0], from_=0, to=4095, font=spinboxFont, width=5, textvariable=plln_r0_var)
        self.plln_r0.pack(padx=5, side=tk.LEFT, pady=2)
        plln_r0_var.set(self.plln_r0.cget("from"))
        self.plln_r0.bind('<FocusOut>', lambda e: self.validate_value(self.plln_r0, plln_r0_var))

        #12BIT PLL_NUM SETTING
        self.pllnum_label_r0 = ttk.Label(self.registerR[0], text='PLL_NUM', justify=tk.LEFT, font=labelFont)
        self.pllnum_label_r0.pack(padx=5, side=tk.LEFT, pady=5)

        self.pllnum_r0 = ttk.Spinbox(self.registerR[0], from_=0, to=4095, font=spinboxFont, width=5, textvariable=pllnum_r0_var)
        self.pllnum_r0.pack(padx=5, side=tk.LEFT, pady=2)
        pllnum_r0_var.set(self.pllnum_r0.cget("from"))
        self.pllnum_r0.bind('<FocusOut>', lambda e: self.validate_value(self.pllnum_r0, pllnum_r0_var))

        #R1 REGISTER
        #5 BIT CPG SETTING
        self.cpg_label_r1 = ttk.Label(self.registerR[1], text="CPG", justify=tk.LEFT, font=labelFont)
        self.cpg_label_r1.pack(padx=5, side=tk.LEFT, pady=5)

        self.cpg_r1 = ttk.Spinbox(self.registerR[1], from_=0, to=31, font=spinboxFont, width=3, textvariable=cpg_r1_var)
        self.cpg_r1.pack(padx=5, side=tk.LEFT, pady=2)
        cpg_r1_var.set(self.cpg_r1.cget("from"))
        self.cpg_r1.bind('<FocusOut>', lambda e: self.validate_value(self.cpg_r1, cpg_r1_var))

        #2BIT VCO_SEL
        self.vcosel_label_r1 = ttk.Label(self.registerR[1], text="VCO_SEL", justify=tk.LEFT, font= labelFont)
        self.vcosel_label_r1.pack(padx=5, side=tk.LEFT, pady=5)

        self.vco_sel_r1 = ttk.Spinbox(self.registerR[1], from_=0, to=3, font=spinboxFont, width=3, textvariable=vcosel_r1_var)
        self.vco_sel_r1.pack(padx=5, side=tk.LEFT, pady=2)
        vcosel_r1_var.set(self.vco_sel_r1.cget("from"))
        self.vco_sel_r1.bind('<FocusOut>', lambda e: self.validate_value(self.vco_sel_r1, vcosel_r1_var))

        #10BIT PLL_NUM
        self.pllnum_label_r1 = ttk.Label(self.registerR[1], text="PLL_NUM", justify=tk.LEFT, font=labelFont)
        self.pllnum_label_r1.pack(padx=5, side=tk.LEFT, pady=5)

        self.pllnum_r1 = ttk.Spinbox(self.registerR[1], from_=0, to=1023, font=spinboxFont, width=5, textvariable=pllnum_r1_var)
        self.pllnum_r1.pack(padx=5, side=tk.LEFT, pady=2)
        pllnum_r1_var.set(self.pllnum_r1.cget("from"))
        self.pllnum_r1.bind('<FocusOut>', lambda e: self.validate_value(self.pllnum_r1, pllnum_r1_var))

        #2 BIT FRAC_ORDER
        self.frac_order_label_r1 = ttk.Label(self.registerR[1], text="FRAC_ORDER", justify=tk.LEFT, font=labelFont)
        self.frac_order_label_r1.pack(padx=5, side=tk.LEFT, pady=5)

        self.frac_order_r1 = ttk.Spinbox(self.registerR[1], from_=0, to=3, font=spinboxFont, width=3, textvariable=frac_order_r1_var)
        self.frac_order_r1.pack(padx=5, side=tk.LEFT, pady=2)
        frac_order_r1_var.set(self.frac_order_r1.cget("from"))
        self.frac_order_r1.bind('<FocusOut>', lambda e: self.validate_value(self.frac_order_r1, frac_order_r1_var))

        #8 BIT PLL_R
        self.pllr_label_r1 = ttk.Label(self.registerR[1], text="PLL_R", justify=tk.LEFT, font=labelFont)
        self.pllr_label_r1.pack(padx=5, side=tk.LEFT, pady=5)

        self.pllr_r1 = ttk.Spinbox(self.registerR[1], from_=0, to=255, font=spinboxFont, width=5, textvariable=pll_r_r1_var)
        self.pllr_r1.pack(padx=5, side=tk.LEFT, pady=2)
        pll_r_r1_var.set(self.pllr_r1.cget("from"))
        self.pllr_r1.bind('<FocusOut>', lambda e: self.validate_value(self.pllr_r1, pll_r_r1_var))

        #REGISTER R2
        #1 BIT OSC_2X
        self.osc2x_label_r2 = ttk.Label(self.registerR[2], text="OSC_2X", justify=tk.LEFT, font=labelFont)
        self.osc2x_label_r2.pack(padx=5, side=tk.LEFT, pady=5)

        self.osc2x_r2 = ttk.Spinbox(self.registerR[2], from_=0, to=1, font=spinboxFont, width=3, textvariable=osc2x_r2_var)
        self.osc2x_r2.pack(padx=5, side=tk.LEFT, pady=2)
        osc2x_r2_var.set(self.osc2x_r2.cget("from"))
        self.osc2x_r2.bind('<FocusOut>', lambda e: self.validate_value(self.osc2x_r2, osc2x_r2_var))

        #1 BIT CPP
        self.cpp_label_r2 = ttk.Label(self.registerR[2], text="CPP", justify=tk.LEFT, font=labelFont)
        self.cpp_label_r2.pack(padx=5, side=tk.LEFT, pady=5)

        self.cpp_r2 = ttk.Spinbox(self.registerR[2], from_=0, to=1, font=spinboxFont, width=3, textvariable=cpp_r2_var)
        self.cpp_r2.pack(padx=5, side=tk.LEFT, pady=2)
        cpp_r2_var.set(self.cpp_r2.cget("from"))
        self.cpp_r2.bind('<FocusOut>', lambda e: self.validate_value(self.cpp_r2, cpp_r2_var))

        #22 BIT PLL_DEN
        self.pll_den_label_r2 = ttk.Label(self.registerR[2], text="PLL_DEN", justify=tk.LEFT, font=labelFont)
        self.pll_den_label_r2.pack(padx=5, side=tk.LEFT, pady=5)

        self.pll_den_r2 = ttk.Spinbox(self.registerR[2], from_=0, to=4194303, font=spinboxFont, width=10, textvariable=pllden_r2_var)
        self.pll_den_r2.pack(padx=5, side=tk.LEFT, pady=2)
        pllden_r2_var.set(self.pll_den_r2.cget("from"))
        self.pll_den_r2.bind('<FocusOut>', lambda e: self.validate_value(self.pll_den_r2, pllden_r2_var))

        #REGISTER R3
        #5 BIT VCO_DIV
        self.vco_div_label_r3 = ttk.Label(self.registerR[3], text="VCO_DIV", justify=tk.LEFT, font=labelFont)
        self.vco_div_label_r3.pack(padx=5, side=tk.LEFT, pady=5)

        self.vco_div_r3 = ttk.Spinbox(self.registerR[3], from_=0, to=31, font=spinboxFont, width=3, textvariable=vcodiv_r3_var)
        self.vco_div_r3.pack(padx=5, side=tk.LEFT, pady=2)
        vcodiv_r3_var.set(self.vco_div_r3.cget("from"))
        self.vco_div_r3.bind('<FocusOut>', lambda e: self.validate_value(self.vco_div_r3, vcodiv_r3_var))

        #6 BIT OUTB_PWR
        self.outb_pwr_label_r3 = ttk.Label(self.registerR[3], text="OUTB_PWR", justify=tk.LEFT, font=labelFont)
        self.outb_pwr_label_r3.pack(padx=5, side=tk.LEFT, pady=5)

        self.outb_pwr_r3 = ttk.Spinbox(self.registerR[3], from_=0, to=63, font=spinboxFont, width=3, textvariable=outb_pwr_r3_var)
        self.outb_pwr_r3.pack(padx=5, side=tk.LEFT, pady=2)
        outb_pwr_r3_var.set(self.outb_pwr_r3.cget("from"))
        self.outb_pwr_r3.bind('<FocusOut>', lambda e: self.validate_value(self.outb_pwr_r3, outb_pwr_r3_var))

        #6 BIT OUTA_PWR
        self.outa_pwr_label_r3 = ttk.Label(self.registerR[3], text="OUTA_PWR", justify=tk.LEFT, font=labelFont)
        self.outa_pwr_label_r3.pack(padx=5, side=tk.LEFT, pady=5)

        self.outa_pwr_r3 = ttk.Spinbox(self.registerR[3], from_=0, to=63, font=spinboxFont, width=3, textvariable=outa_pwr_r3_var)
        self.outa_pwr_r3.pack(padx=5, side=tk.LEFT, pady=2)
        outa_pwr_r3_var.set(self.outa_pwr_r3.cget("from"))
        self.outa_pwr_r3.bind('<FocusOut>', lambda e: self.validate_value(self.outa_pwr_r3, outa_pwr_r3_var))

        #1 BIT OUTB_PD
        self.outb_pd_label_r3 = ttk.Label(self.registerR[3], text='OUTB_PD', justify=tk.LEFT, font=labelFont)
        self.outb_pd_label_r3.pack(padx=5, side=tk.LEFT, pady=5)

        self.outb_pd_r3 = ttk.Spinbox(self.registerR[3], from_=0, to=1, font=spinboxFont, width=3, textvariable=outb_pd_r3_var)
        self.outb_pd_r3.pack(padx=5, side=tk.LEFT, pady=2)
        outb_pd_r3_var.set(self.outb_pd_r3.cget("from"))
        self.outb_pd_r3.bind('<FocusOut>', lambda e: self.validate_value(self.outb_pd_r3, outb_pd_r3_var))

        #1 BIT OUTA_PD
        self.outa_pd_label_r3 = ttk.Label(self.registerR[3], text="OUTA_PD", justify=tk.LEFT, font=labelFont)
        self.outa_pd_label_r3.pack(padx=5, side=tk.LEFT, pady=5)

        self.outa_pd_r3 = ttk.Spinbox(self.registerR[3], from_=0, to=1, font=spinboxFont, width=3, textvariable=outa_pd_r3_var)
        self.outa_pd_r3.pack(padx=5, side=tk.LEFT, pady=2)
        outa_pd_r3_var.set(self.outa_pd_r3.cget("from"))
        self.outa_pd_r3.bind('<FocusOut>', lambda e: self.validate_value(self.outa_pd_r3, outa_pd_r3_var))

        #REGISTER4
        #3 BIT PFD_DLY
        self.pfd_dly_label_r4 = ttk.Label(self.registerR[4], text='PFD_DLY', justify=tk.LEFT, font=labelFont)
        self.pfd_dly_label_r4.pack(padx=5, side=tk.LEFT, pady=5)

        self.pfd_dly_r4 = ttk.Spinbox(self.registerR[4], from_=0, to=7, font=spinboxFont, width=3, textvariable=pfd_dly_r4_var)
        self.pfd_dly_r4.pack(padx=5, side=tk.LEFT, pady=2)
        pfd_dly_r4_var.set(self.pfd_dly_r4.cget("from"))
        self.pfd_dly_r4.bind('<FocusOut>', lambda e: self.validate_value(self.pfd_dly_r4, pfd_dly_r4_var))

        #1 BIT FL_FRCE
        self.fl_frce_label_r4 = ttk.Label(self.registerR[4], text='FL_FRCE', justify=tk.LEFT, font=labelFont)
        self.fl_frce_label_r4.pack(padx=5, side=tk.LEFT, pady=5)

        self.fl_frce_r4 = ttk.Spinbox(self.registerR[4], from_=0, to=1, font=spinboxFont, width=3, textvariable=fl_frce_r4_var)
        self.fl_frce_r4.pack(padx=5, side=tk.LEFT, pady=2)
        fl_frce_r4_var.set(self.fl_frce_r4.cget("from"))
        self.fl_frce_r4.bind('<FocusOut>', lambda e: self.validate_value(self.fl_frce_r4, fl_frce_r4_var))

        #12 BIT FL_TOC
        self.fl_toc_label_r4 = ttk.Label(self.registerR[4], text='FL_TOC', justify=tk.LEFT, font=labelFont)
        self.fl_toc_label_r4.pack(padx=5, side=tk.LEFT, pady=5)

        self.fl_toc_r4 = ttk.Spinbox(self.registerR[4], from_=0, to=4095, font=spinboxFont, width=3, textvariable=fl_toc_r4_var)
        self.fl_toc_r4.pack(padx=5, side=tk.LEFT, pady=2)
        fl_toc_r4_var.set(self.fl_toc_r4.cget("from"))
        self.fl_toc_r4.bind('<FocusOut>', lambda e: self.validate_value(self.fl_toc_r4, fl_toc_r4_var))

        #5 BIT FL_CPG
        self.fl_cpg_label_r4 = ttk.Label(self.registerR[4], text='FL_CPG', justify=tk.LEFT, font=labelFont)
        self.fl_cpg_label_r4.pack(padx=5, side=tk.LEFT, pady=5)

        self.fl_cpg_r4 = ttk.Spinbox(self.registerR[4], from_=0, to=31, font=spinboxFont, width=3, textvariable=fl_cpg_r4_var)
        self.fl_cpg_r4.pack(padx=5, side=tk.LEFT, pady=2)
        fl_cpg_r4_var.set(self.fl_cpg_r4.cget("from"))
        self.fl_cpg_r4.bind('<FocusOut>', lambda e: self.validate_value(self.fl_cpg_r4, fl_cpg_r4_var))

        #6 BIT CPG_BLEED
        self.cpg_bleed_label_r4 = ttk.Label(self.registerR[4], text='CPG_BLEED', justify=tk.LEFT, font=labelFont)
        self.cpg_bleed_label_r4.pack(padx=5, side=tk.LEFT, pady=5)

        self.cpg_bleed_r4 = ttk.Spinbox(self.registerR[4], from_=0, to=63, font=spinboxFont, width=3, textvariable=cpg_bleed_r4_var)
        self.cpg_bleed_r4.pack(padx=5, side=tk.LEFT, pady=2)
        cpg_bleed_r4_var.set(self.cpg_bleed_r4.cget("from"))
        self.cpg_bleed_r4.bind('<FocusOut>', lambda e: self.validate_value(self.cpg_bleed_r4, cpg_bleed_r4_var))

        #REGISTER R5
        #1 BIT OUT_LDEN
        self.out_lden_label_r5 = ttk.Label(self.registerR[5], text='OUT_LDEN', justify=tk.LEFT, font=labelFont)
        self.out_lden_label_r5.pack(padx=5, side=tk.LEFT, pady=5)

        self.out_lden_r5 = ttk.Spinbox(self.registerR[5], from_=0, to=1, font=spinboxFont, width=3, textvariable=outld_en_r5_var)
        self.out_lden_r5.pack(padx=5, side=tk.LEFT, pady=2)
        outld_en_r5_var.set(self.out_lden_r5.cget("from"))
        self.out_lden_r5.bind('<FocusOut>', lambda e: self.validate_value(self.out_lden_r5, outld_en_r5_var))

        #3 BIT OSC_FREQ
        self.osc_freq_label_r5 = ttk.Label(self.registerR[5], text='OSC_FREQ', justify=tk.LEFT, font=labelFont)
        self.osc_freq_label_r5.pack(padx=5, side=tk.LEFT, pady=5)

        self.osc_freq_r5 = ttk.Spinbox(self.registerR[5], from_=0, to=7, font=spinboxFont, width=3, textvariable=oscfreq_r5_var)
        self.osc_freq_r5.pack(padx=5, side=tk.LEFT, pady=2)
        oscfreq_r5_var.set(self.osc_freq_r5.cget("from"))
        self.osc_freq_r5.bind('<FocusOut>', lambda e: self.validate_value(self.osc_freq_r5, oscfreq_r5_var))

        #1 BIT BUFEN_DIS
        self.bufen_dis_label_r5 = ttk.Label(self.registerR[5], text='BUFEN_DIS', justify=tk.LEFT, font=spinboxFont)
        self.bufen_dis_label_r5.pack(padx=5, side=tk.LEFT, pady=5)

        self.bufen_dis_r5 = ttk.Spinbox(self.registerR[5], from_=0, to=1, font=spinboxFont, width=3, textvariable=bufen_dis_r5_var)
        self.bufen_dis_r5.pack(padx=5, side=tk.LEFT, pady=2)
        bufen_dis_r5_var.set(self.bufen_dis_r5.cget("from"))
        self.bufen_dis_r5.bind('<FocusOut>', lambda e: self.validate_value(self.bufen_dis_r5, bufen_dis_r5_var))

        #2 BIT VCO_SEl_MODE
        self.vcosel_mode_label_r5 = ttk.Label(self.registerR[5], text='VCO_SEL_MODE', justify=tk.LEFT, font=labelFont)
        self.vcosel_mode_label_r5.pack(padx=5, side=tk.LEFT, pady=5)

        self.vcosel_mode_r5 = ttk.Spinbox(self.registerR[5], from_=0, to=3, font=spinboxFont, width=3, textvariable=vco_sel_mode_r5_var)
        self.vcosel_mode_r5.pack(padx=5, side=tk.LEFT, pady=2)
        vco_sel_mode_r5_var.set(self.vcosel_mode_r5.cget("from"))
        self.vcosel_mode_r5.bind('<FocusOut>', lambda e: self.validate_value(self.vcosel_mode_r5, vco_sel_mode_r5_var))

        #2 BIT OUTB_MUX
        self.outb_mux_label_r5 = ttk.Label(self.registerR[5], text='OUTB_MUX', justify=tk.LEFT, font=labelFont)
        self.outb_mux_label_r5.pack(padx=5, side=tk.LEFT, pady=5)

        self.outb_mux_r5 = ttk.Spinbox(self.registerR[5], from_=0, to=3, font=spinboxFont, width=3, textvariable=outb_mux_r5_var)
        self.outb_mux_r5.pack(padx=5, side=tk.LEFT, pady=2)
        outb_mux_r5_var.set(self.outb_mux_r5.cget("from"))
        self.outb_mux_r5.bind('<FocusOut>', lambda e: self.validate_value(self.outb_mux_r5, outb_mux_r5_var))

        # 2 BIT OUTA_MUX
        self.outa_mux_label_r5 = ttk.Label(self.registerR[5], text='OUTA_MUX', justify=tk.LEFT, font=labelFont)
        self.outa_mux_label_r5.pack(padx=5, side=tk.LEFT, pady=5)

        self.outa_mux_r5 = ttk.Spinbox(self.registerR[5], from_=0, to=3, font=spinboxFont, width=3, textvariable=outa_mux_r5_var)
        self.outa_mux_r5.pack(padx=5, side=tk.LEFT, pady=2)
        outa_mux_r5_var.set(self.outa_mux_r5.cget("from"))
        self.outa_mux_r5.bind('<FocusOut>', lambda e: self.validate_value(self.outa_mux_r5, outa_mux_r5_var))

        #1 BIT O_DLY
        self.odly_label_r5 = ttk.Label(self.registerR[5], text='O_DLY', justify=tk.LEFT, font=labelFont)
        self.odly_label_r5.pack(padx=5, side=tk.LEFT, pady=5)

        self.odly_r5 = ttk.Spinbox(self.registerR[5], from_=0, to=1, font=spinboxFont, width=2, textvariable=odly_r5_var)
        self.odly_r5.pack(padx=5, side=tk.LEFT, pady=2)
        odly_r5_var.set(self.odly_r5.cget("from"))
        self.odly_r5.bind('<FocusOut>', lambda e: self.validate_value(self.odly_r5, odly_r5_var))

        #2 BIT MODE
        self.mode_label_r5 = ttk.Label(self.registerR[5], text='MODE', justify=tk.LEFT, font=labelFont)
        self.mode_label_r5.pack(padx=5, side=tk.LEFT, pady=5)

        self.mode_r5 = ttk.Spinbox(self.registerR[5], from_=0, to=3, font=spinboxFont, width=3, textvariable=mode_r5_var)
        self.mode_r5.pack(padx=5, side=tk.LEFT, pady=2)
        mode_r5_var.set(self.mode_r5.cget("from"))
        self.mode_r5.bind('<FocusOut>', lambda e: self.validate_value(self.mode_r5, mode_r5_var))

        #3BIT PWDN_MODE
        self.pwdn_mode_label_r5 = ttk.Label(self.registerR[5], text='PWDN_MODE', justify=tk.LEFT, font=labelFont)
        self.pwdn_mode_label_r5.pack(padx=5, side=tk.LEFT, pady=5)

        self.pwdn_mode_r5 = ttk.Spinbox(self.registerR[5], from_=0, to=7, font=spinboxFont, width=3, textvariable=pwdn_mode_r5_var)
        self.pwdn_mode_r5.pack(padx=5, side=tk.LEFT, pady=2)
        pwdn_mode_r5_var.set(self.pwdn_mode_r5.cget("from"))
        self.pwdn_mode_r5.bind('<FocusOut>', lambda e: self.validate_value(self.pwdn_mode_r5, pwdn_mode_r5_var))

        #1 BIT RESET
        self.reset_label_r5 = ttk.Label(self.registerR[5], text='RESET', justify=tk.LEFT, font=labelFont)
        self.reset_label_r5.pack(padx=5, side=tk.LEFT, pady=5)

        self.reset_r5 = ttk.Spinbox(self.registerR[5], from_=0, to=1, font=spinboxFont, width=2, textvariable=reset_r5_var)
        self.reset_r5.pack(padx=5, side=tk.LEFT, pady=2)
        reset_r5_var.set(self.reset_r5.cget("from"))
        self.reset_r5.bind('<FocusOut>', lambda e: self.validate_value(self.reset_r5, reset_r5_var))

        #REGISTER R6
        #20 BIT RD_DIAGNOSTICS
        self.rd_diagnostics_label_r6 = ttk.Label(self.registerR[6], text='RD_DIAGNOSTICS', justify=tk.LEFT, font=labelFont)
        self.rd_diagnostics_label_r6.pack(padx=5, side=tk.LEFT, pady=5)

        self.rd_diagnostics_r6 = ttk.Spinbox(self.registerR[6], from_=0, to=1048575, font=spinboxFont, width=10, textvariable=rd_diagnostics_r6_var)
        self.rd_diagnostics_r6.pack(padx=5, side=tk.LEFT, pady=2)
        rd_diagnostics_r6_var.set(self.rd_diagnostics_r6.cget("from"))
        self.rd_diagnostics_r6.bind('<FocusOut>', lambda e: self.validate_value(self.rd_diagnostics_r6, rd_diagnostics_r6_var))

        #4 BIT RDADDR
        self.rdaddr_label_r6 = ttk.Label(self.registerR[6], text='RDADDR', justify=tk.LEFT, font=labelFont)
        self.rdaddr_label_r6.pack(padx=5, side=tk.LEFT, pady=5)

        self.rdaddr_r6 = ttk.Spinbox(self.registerR[6], from_=0, to=15, font=spinboxFont, width=3, textvariable=rdaddr_r6_var)
        self.rdaddr_r6.pack(padx=5, side=tk.LEFT, pady=2)
        rdaddr_r6_var.set(self.rdaddr_r6.cget("from"))
        self.rdaddr_r6.bind('<FocusOut>', lambda e: self.validate_value(self.rdaddr_r6, rdaddr_r6_var))

        #1 BIT uWIRE_LOCK
        self.uWIRE_label_r6 = ttk.Label(self.registerR[6], text='uWIRE_LOCK', justify=tk.LEFT, font=labelFont)
        self.uWIRE_label_r6.pack(padx=5, side=tk.LEFT, pady=5)

        self.uWIRE_LOCK_r6 = ttk.Spinbox(self.registerR[6], from_=0, to=1, font=spinboxFont, width=2, textvariable=uWirelock_r6_var)
        self.uWIRE_LOCK_r6.pack(padx=5, side=tk.LEFT, pady=2)
        uWirelock_r6_var.set(self.uWIRE_LOCK_r6.cget("from"))
        self.uWIRE_LOCK_r6.bind('<FocusOut>', lambda e: self.validate_value(self.uWIRE_LOCK_r6, uWirelock_r6_var))

        #REGISTER R7
        #5 BIT FL_SELECT
        self.fl_select_label_r7 = ttk.Label(self.registerR[7], text='FL_SELECT', justify=tk.LEFT, font=labelFont)
        self.fl_select_label_r7.pack(padx=5, side=tk.LEFT, pady=5)

        self.fl_select_r7 = ttk.Spinbox(self.registerR[7], from_=0, to=31, font=spinboxFont, width=3, textvariable=fl_select_r7_var)
        self.fl_select_r7.pack(padx=5, side=tk.LEFT, pady=2)
        fl_select_r7_var.set(self.fl_select_r7.cget("from"))
        self.fl_select_r7.bind('<FocusOut>', lambda e: self.validate_value(self.fl_select_r7, fl_select_r7_var))

        #3 BIT FL_PINMODE
        self.fl_pinmode_label_r7 = ttk.Label(self.registerR[7], text='FL_PINMODE', justify=tk.LEFT, font=labelFont)
        self.fl_pinmode_label_r7.pack(padx=5, side=tk.LEFT, pady=5)

        self.fl_pinmode_r7 = ttk.Spinbox(self.registerR[7], from_=0, to=7, font=spinboxFont, width=3, textvariable=fl_pinmode_r7_var)
        self.fl_pinmode_r7.pack(padx=5, side=tk.LEFT, pady=2)
        fl_pinmode_r7_var.set(self.fl_pinmode_r7.cget("from"))
        self.fl_pinmode_r7.bind('<FocusOut>', lambda e: self.validate_value(self.fl_pinmode_r7, fl_pinmode_r7_var))

        #1BIT FL_INV
        self.fl_inv_label_r7 = ttk.Label(self.registerR[7], text='FL_INV', justify=tk.LEFT, font=labelFont)
        self.fl_inv_label_r7.pack(padx=5, side=tk.LEFT, pady=5)

        self.fl_inv_r7 = ttk.Spinbox(self.registerR[7], from_=0, to=1, font=spinboxFont, width=2, textvariable=fl_inv_r7_var)
        self.fl_inv_r7.pack(padx=5, side=tk.LEFT, pady=2)
        fl_inv_r7_var.set(self.fl_inv_r7.cget("from"))
        self.fl_inv_r7.bind('<FocusOut>', lambda e: self.validate_value(self.fl_inv_r7, fl_inv_r7_var))

        #5 BIT MUXOUT_SELECT
        self.muxout_select_label_r7 = ttk.Label(self.registerR[7], text='MUXOUT_SELECT', justify=tk.LEFT, font=labelFont)
        self.muxout_select_label_r7.pack(padx=5, side=tk.LEFT, pady=5)

        self.muxout_select_r7 = ttk.Spinbox(self.registerR[7], from_=0, to=31, font=spinboxFont, width=3, textvariable=muxout_select_r7_var)
        self.muxout_select_r7.pack(padx=5, side=tk.LEFT, pady=2)
        muxout_select_r7_var.set(self.muxout_select_r7.cget("from"))
        self.muxout_select_r7.bind('<FocusOut>', lambda e: self.validate_value(self.muxout_select_r7, muxout_select_r7_var))

        #1 BIT MUX_INV
        self.mux_inv_label_r7 = ttk.Label(self.registerR[7], text='MUX_INV', justify=tk.LEFT, font=labelFont)
        self.mux_inv_label_r7.pack(padx=5, side=tk.LEFT, pady=5)

        self.mux_inv_r7 = ttk.Spinbox(self.registerR[7], from_=0, to=1, font=spinboxFont, width=2, textvariable=mux_inv_r7_var)
        self.mux_inv_r7.pack(padx=5, side=tk.LEFT, pady=2)
        mux_inv_r7_var.set(self.mux_inv_r7.cget("from"))
        self.mux_inv_r7.bind('<FocusOut>', lambda e: self.validate_value(self.mux_inv_r7, mux_inv_r7_var))

        #3BIT MUXOUT_PINMODE
        self.muxout_pinmode_label_r7 = ttk.Label(self.registerR[7], text='MUXOUT_PINMODE', justify=tk.LEFT, font=labelFont)
        self.muxout_pinmode_label_r7.pack(padx=5, side=tk.LEFT, pady=5)

        self.muxout_pinmode_r7 = ttk.Spinbox(self.registerR[7], from_=0, to=7, font=spinboxFont, width=3, textvariable=muxout_pinmode_r7_var)
        self.muxout_pinmode_r7.pack(padx=5, side=tk.LEFT, pady=2)
        muxout_pinmode_r7_var.set(self.muxout_pinmode_r7.cget("from"))
        self.muxout_pinmode_r7.bind('<FocusOut>', lambda e: self.validate_value(self.muxout_pinmode_r7, muxout_pinmode_r7_var))

        #5BIT LD_SELECT
        self.ld_select_label_r7 = ttk.Label(self.registerR[7], text='LD_SELECT', justify=tk.LEFT, font=labelFont)
        self.ld_select_label_r7.pack(padx=5, side=tk.LEFT, pady=5)

        self.ld_select_r7 = ttk.Spinbox(self.registerR[7], from_=0, to=31, font=spinboxFont, width=3, textvariable=ld_select_r7_var)
        self.ld_select_r7.pack(padx=5, side=tk.LEFT, pady=2)
        ld_select_r7_var.set(self.ld_select_r7.cget("from"))
        self.ld_select_r7.bind('<FocusOut>', lambda e: self.validate_value(self.ld_select_r7, ld_select_r7_var))

        #1 BIT LD_INV
        self.ld_inv_label_r7 = ttk.Label(self.registerR[7], text='LD_INV', justify=tk.LEFT, font=labelFont)
        self.ld_inv_label_r7.pack(padx=5, side=tk.LEFT, pady=5)

        self.ld_inv_r7 = ttk.Spinbox(self.registerR[7], from_=0, to=1, font=spinboxFont, width=2, textvariable=ld_inv_r7_var)
        self.ld_inv_r7.pack(padx=5, side=tk.LEFT, pady=2)
        ld_inv_r7_var.set(self.ld_inv_r7.cget("from"))
        self.ld_inv_r7.bind('<FocusOut>', lambda e: self.validate_value(self.ld_inv_r7, ld_inv_r7_var))

        #3BIT LD_PINMODE
        self.ld_pinmode_label_r7 = ttk.Label(self.registerR[7], text='LD_PINMODE', justify=tk.LEFT, font=labelFont)
        self.ld_pinmode_label_r7.pack(padx=5, side=tk.LEFT, pady=5)

        self.ld_pinmode_r7 = ttk.Spinbox(self.registerR[7], from_=0, to=7, width=3, font=spinboxFont, textvariable=ld_pinmode_r7_var)
        self.ld_pinmode_r7.pack(padx=5, side=tk.LEFT, pady=2)
        ld_pinmode_r7_var.set(self.ld_pinmode_r7.cget("from"))
        self.ld_pinmode_r7.bind('<FocusOut>', lambda e: self.validate_value(self.ld_pinmode_r7, ld_pinmode_r7_var))

        #REGISTER R8
        self.entry_r8 = ttk.Label(self.registerR[8],text="0 0 1 0 0 0 0 0 0 1 1 1 1 1 0 1 1 1 0 1 1 0 1 1 1 1 1 1", relief=tk.SUNKEN, font=('Helvetica', 10) )
        self.entry_r8.pack(padx=5, side=tk.LEFT, pady=5)

        #REGISTER R9
        self.entry_r9 = ttk.Label(self.registerR[9], text="0 0 0 0 0 0 1 1 1 1 0 0 0 1 1 1 1 1 0 0 0 0 0 0 0 0 1 1", relief=tk.SUNKEN, font=('Helvetica', 10))
        self.entry_r9.pack(padx=5, side=tk.LEFT, pady=5)

        #REGISTER R10
        self.entry_r10 = ttk.Label(self.registerR[10], text="0 0 1 0 0 0 0 1 0 0 0 0 0 0 0 0 0 1 0 1 0 0 0 0 1 1 0 0", relief=tk.SUNKEN, font=('Helvetica', 10))
        self.entry_r10.pack(padx=5, side=tk.LEFT, pady=5)

        self.button1[0]['command'] = lambda:self.button1_clicked(0)
        self.button2[0]['command'] = lambda:self.button2_clicked(0)
        self.button3[0]['command'] = lambda :self.button3_clicked(0)

        self.button1[1]['command'] = lambda: self.button1_clicked(1)
        self.button2[1]['command'] = lambda: self.button2_clicked(1)
        self.button3[1]['command'] = lambda: self.button3_clicked(1)

        self.button1[2]['command'] = lambda: self.button1_clicked(2)
        self.button2[2]['command'] = lambda: self.button2_clicked(2)
        self.button3[2]['command'] = lambda: self.button3_clicked(2)

        self.button1[3]['command'] = lambda: self.button1_clicked(3)
        self.button2[3]['command'] = lambda: self.button2_clicked(3)
        self.button3[3]['command'] = lambda: self.button3_clicked(3)

        self.button1[4]['command'] = lambda: self.button1_clicked(4)
        self.button2[4]['command'] = lambda: self.button2_clicked(4)
        self.button3[4]['command'] = lambda: self.button3_clicked(4)

        self.button1[5]['command'] = lambda: self.button1_clicked(5)
        self.button2[5]['command'] = lambda: self.button2_clicked(5)
        self.button3[5]['command'] = lambda: self.button3_clicked(5)

        self.button1[6]['command'] = lambda: self.button1_clicked(6)
        self.button2[6]['command'] = lambda: self.button2_clicked(6)
        self.button3[6]['command'] = lambda: self.button3_clicked(6)

        self.button1[7]['command'] = lambda: self.button1_clicked(7)
        self.button2[7]['command'] = lambda: self.button2_clicked(7)
        self.button3[7]['command'] = lambda: self.button3_clicked(7)

        self.button1[8]['command'] = lambda: self.button1_clicked(8)
        self.button2[8]['command'] = lambda: self.button2_clicked(8)
        self.button3[8]['command'] = lambda: self.button3_clicked(8)

        self.button1[9]['command'] = lambda: self.button1_clicked(9)
        self.button2[9]['command'] = lambda: self.button2_clicked(9)
        self.button3[9]['command'] = lambda: self.button3_clicked(9)

        self.button1[10]['command'] = lambda: self.button1_clicked(10)
        self.button2[10]['command'] = lambda: self.button2_clicked(10)
        self.button3[10]['command'] = lambda: self.button3_clicked(10)

        self.registerR.append(tk.LabelFrame(self.secondMainFrame, width=100, highlightthickness=3, labelanchor='nw', text='Register R'+str(13)))
        self.registerR[11].pack(fill=tk.X, padx=5)

        # REGISTER 13
        # 4 BIT DLD_ERR_CNT
        self.dlderr_cnt_label_r13 = ttk.Label(self.registerR[11], text='DLD_ERR_CNT', justify=tk.LEFT, font=labelFont)
        self.dlderr_cnt_label_r13.pack(padx=5, side=tk.LEFT, pady=5)

        self.dlderr_cnt_r13 = ttk.Spinbox(self.registerR[11], from_=0, to=15, font=spinboxFont, width=3,
                                          textvariable=dld_err_cnt_r13_var)
        self.dlderr_cnt_r13.pack(padx=5, side=tk.LEFT, pady=2)
        dld_err_cnt_r13_var.set(self.dlderr_cnt_r13.cget("from"))
        self.dlderr_cnt_r13.bind('<FocusOut>', lambda e: self.validate_value(self.dlderr_cnt_r13, dld_err_cnt_r13_var))

        # 10 BIT DLD_PASS_CNT
        self.dldpass_cnt_label_r13 = ttk.Label(self.registerR[11], text='DLD_PASS_CNT', justify=tk.LEFT, font=labelFont)
        self.dldpass_cnt_label_r13.pack(padx=5, side=tk.LEFT, pady=5)

        self.dldpass_cnt_r13 = ttk.Spinbox(self.registerR[11], from_=0, to=1023, font=spinboxFont, width=5,
                                           textvariable=dld_pass_cnt_r13_var)
        self.dldpass_cnt_r13.pack(padx=5, side=tk.LEFT, pady=2)
        dld_pass_cnt_r13_var.set(self.dldpass_cnt_r13.cget("from"))
        self.dldpass_cnt_r13.bind('<FocusOut>',
                                  lambda e: self.validate_value(self.dldpass_cnt_r13, dld_pass_cnt_r13_var))

        # 3 BIT DLD_TOL
        self.dldtol_label_r13 = ttk.Label(self.registerR[11], text='DLD_TOL', justify=tk.LEFT, font=labelFont)
        self.dldtol_label_r13.pack(padx=5, side=tk.LEFT, pady=5)

        self.dldtol_r13 = ttk.Spinbox(self.registerR[11], from_=0, to=7, font=spinboxFont, width=3,
                                      textvariable=dld_tol_r13_var)
        self.dldtol_r13.pack(padx=5, side=tk.LEFT, pady=2)
        dld_tol_r13_var.set(self.dldtol_r13.cget("from"))
        self.dldtol_r13.bind('<FocusOut>', lambda e: self.validate_value(self.dldtol_r13, dld_tol_r13_var))

        self.button1.append(ttk.Button(self.registerR[11], text="PLL1 Configure", command=lambda: self.button1_clicked(13)))
        self.button1[11].pack(side=tk.RIGHT, padx=5)

        self.button2.append(ttk.Button(self.registerR[11], text="PLL2 Configure", command=lambda:self.button2_clicked(13)))
        self.button2[11].pack(side=tk.RIGHT, padx=5)

        self.button3.append(ttk.Button(self.registerR[11], image=self.info_icon, command=lambda: webbrowser.open_new("lmx2581_15.pdf")))
        self.button3[11].pack(side=tk.RIGHT, padx=5)

        self.registerR.append(tk.LabelFrame(self.secondMainFrame, width=100, highlightthickness=3, labelanchor='nw', text='Register R' + str(15)))
        self.registerR[12].pack(fill=tk.X, padx=5)

        # REGISTER R15
        # 1 BIT VCO_CAP_MAN
        self.vcocap_man_label_r15 = ttk.Label(self.registerR[12], text='VCO_CAP_MAN', justify=tk.LEFT, font=labelFont)
        self.vcocap_man_label_r15.pack(padx=5, side=tk.LEFT, pady=5)

        self.vcocap_man_r15 = ttk.Spinbox(self.registerR[12], from_=0, to=1, font=spinboxFont, width=2,
                                          textvariable=vcocap_man_r15_var)
        self.vcocap_man_r15.pack(padx=5, side=tk.LEFT, pady=2)
        vcocap_man_r15_var.set(self.vcocap_man_r15.cget("from"))
        self.vcocap_man_r15.bind('<FocusOut>', lambda e: self.validate_value(self.vcocap_man_r15, vcocap_man_r15_var))

        # 8BIT VCO_CAPCODE
        self.vcocap_code_label_r15 = ttk.Label(self.registerR[12], text='VCO_CAPCODE', justify=tk.LEFT, font=labelFont)
        self.vcocap_code_label_r15.pack(padx=5, side=tk.LEFT, pady=5)

        self.vcocap_code_r15 = ttk.Spinbox(self.registerR[12], from_=0, to=255, font=spinboxFont, width=5,
                                           textvariable=vco_capcode_r15_var)
        self.vcocap_code_r15.pack(padx=5, side=tk.LEFT, pady=2)
        vco_capcode_r15_var.set(self.vcocap_code_r15.cget("from"))
        self.vcocap_code_r15.bind('<FocusOut>',
                                  lambda e: self.validate_value(self.vcocap_code_r15, vco_capcode_r15_var))

        self.button1.append(ttk.Button(self.registerR[12], text="PLL1 Configure", command=lambda: self.button1_clicked(15)))
        self.button1[12].pack(side=tk.RIGHT, padx=5)

        self.button2.append(ttk.Button(self.registerR[12], text="PLL2 Configure", command=lambda: self.button2_clicked(15)))
        self.button2[12].pack(side=tk.RIGHT, padx=5)

        self.button3.append(ttk.Button(self.registerR[12], image=self.info_icon, command=lambda: webbrowser.open_new("lmx2581_15.pdf")))
        self.button3[12].pack(side=tk.RIGHT, padx=5)

        self.registerMapButton = ttk.Button(self.secondMainFrame, text="Show Register Map", command=lambda :webbrowser.open_new("lmx2581_regmap.pdf"))
        self.registerMapButton.pack(padx=10, ipadx=5, ipady=5, anchor='w', side=tk.LEFT)

        self.connectButton = ttk.Button(self.secondMainFrame, text="Connect", command=self.ConnectDevice)
        self.connectButton.pack(padx= 10, ipadx=5, ipady=5, anchor='e', side=tk.RIGHT)

        if intF.connStatus == 0:
            self.statusBar = tk.Label(self, text= 'Disconnected', anchor='e', bd=1, relief=tk.SUNKEN)
        else:
            self.statusBar = tk.Label(self, text= 'Connected', anchor='e', bd=1, relief=tk.SUNKEN)
        self.statusBar.pack(side=tk.BOTTOM, fill=tk.X, pady=1)



    def button1_clicked(self, value):
        print("Button1 {} is pressed".format(value))
        if 1 == intF.connStatus:
            print("Writing SPI: ")
            mcpAPI.spi_write_payload(intF.PLL1, value)
            messagebox.showinfo(messagebox.INFO, "0x%x is sent to R%d of PLL1" %(intF.spi_rxData, value))
        else:
            print("Device is Not Connected")

    def button2_clicked(self, value):
        print("Button2 {} is pressed".format(value))
        if 1 == intF.connStatus:
            print("Writing SPI: ")
            mcpAPI.spi_write_payload(intF.PLL2, value)
            messagebox.showinfo(messagebox.INFO, "0x%x is sent to R%d of PLL2" %(intF.spi_rxData, value))
        else:
            print("Device is Not Connected")

    def button3_clicked(self, value):
        if (value == 0):
            webbrowser.open_new("lmx2581_0.pdf")
        elif (value == 1):
            webbrowser.open_new("lmx2581_1.pdf")
        elif (value == 2):
            webbrowser.open_new("lmx2581_2.pdf")
        elif (value == 3):
            webbrowser.open_new("lmx2581_3.pdf")
        elif (value == 4):
            webbrowser.open_new("lmx2581_4.pdf")
        elif (value == 5):
            webbrowser.open_new("lmx2581_5.pdf")
        elif (value == 6):
            webbrowser.open_new("lmx2581_6.pdf")
        elif ((value == 7) or (value == 8) or (value == 9) or (value == 10)):
            webbrowser.open_new("lmx2581_7.pdf")
        elif ((value == 13) or (value == 15)):
            webbrowser.open_new("lmx2581_15.pdf")

    def ConnectDevice(self):
        pass

    def register_data_capture(self):
        pass

    def validate_value(self, object, var):

        try:
            currentValue = object.get()
            if (int(currentValue) > object.cget("to")):
                var.set(object.cget("to"))
            elif (int(currentValue) < object.cget("from")):
                var.set(object.cget("from"))
        except:
            messagebox.showinfo("error", "Enter a Valid Integer Value")



if __name__ == '__main__':
    app = App()
    app.mainloop()

