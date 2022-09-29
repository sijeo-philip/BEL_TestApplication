#!/usr/bin/env python
import tkinter as tk
from tkinter import ttk
import webbrowser

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("PLL SETTING APPLICATION")
        self.geometry("750x800")
        self.resizable(0,0)

        self.registerR = []
        self.labels = []
        self.entries = []
        self.button1 = []
        self.button2 = []
        self.button3 = []

        self.info_icon = tk.PhotoImage(file='info.png')

        self.mainFrame = tk.Frame(self)
        self.mainFrame.pack(fill=tk.BOTH, expand=1)

        self.mainCanvas = tk.Canvas(self.mainFrame)
        self.mainCanvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

        self.scrollBar = ttk.Scrollbar(self.mainFrame, orient=tk.VERTICAL, command=self.mainCanvas.yview)
        self.scrollBar.pack(side=tk.RIGHT, fill=tk.Y)

        #Configure the Canvas
        self.mainCanvas.configure(yscrollcommand=self.scrollBar.set)
        self.mainCanvas.bind('<Configure>', lambda e: self.mainCanvas.configure(scrollregion= self.mainCanvas.bbox("all")))

        #Create Another Frame in the Canvas
        self.secondMainFrame = tk.Frame(self.mainCanvas)

        #Add that New Frame to a Window in the Canvas
        self.mainCanvas.create_window((0,0), window=self.secondMainFrame, anchor="nw")

        for i in range(11):
            self.registerR.append(tk.LabelFrame(self.secondMainFrame, width=100, highlightthickness=3, labelanchor='nw', text='Register R'+str(i)))
            self.registerR[i].pack(fill=tk.X, padx=5)

            self.labels.append(ttk.Label(self.registerR[i], text='R'+str(i)))
            self.labels[i].pack(side=tk.LEFT, padx=5)

            self.entries.append(ttk.Entry(self.registerR[i], width=50))
            self.entries[i].pack(side=tk.LEFT, padx=5)

            self.button1.append(ttk.Button(self.registerR[i], text="PLL1 Configure"))
            self.button1[i].pack(side=tk.LEFT, padx=5)

            self.button2.append(ttk.Button(self.registerR[i], text="PLL2 Configure"))
            self.button2[i].pack(side=tk.LEFT, padx=5)

            self.button3.append(ttk.Button(self.registerR[i], image=self.info_icon))
            self.button3[i].pack(side=tk.LEFT, padx=5)

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

        self.labels.append(ttk.Label(self.registerR[11], text='R' + str(13)))
        self.labels[11].pack(side=tk.LEFT, padx=5)

        self.entries.append(ttk.Entry(self.registerR[11], width=50))
        self.entries[11].pack(side=tk.LEFT, padx=5)

        self.button1.append(ttk.Button(self.registerR[11], text="PLL1 Configure", command=lambda:self.button1_clicked(13)))
        self.button1[11].pack(side=tk.LEFT, padx=5)

        self.button2.append(ttk.Button(self.registerR[11], text="PLL2 Configure", command=lambda:self.button2_clicked(13)))
        self.button2[11].pack(side=tk.LEFT, padx=5)

        self.button3.append(ttk.Button(self.registerR[11], image=self.info_icon, command=lambda:self.button2_clicked(13)))
        self.button3[11].pack(side=tk.LEFT, padx=5)

        self.registerR.append(tk.LabelFrame(self.secondMainFrame, width=100, highlightthickness=3, labelanchor='nw', text='Register R' + str(15)))
        self.registerR[12].pack(fill=tk.X, padx=5)

        self.labels.append(ttk.Label(self.registerR[12], text='R' + str(15)))
        self.labels[12].pack(side=tk.LEFT, padx=5)

        self.entries.append(ttk.Entry(self.registerR[12], width=50))
        self.entries[12].pack(side=tk.LEFT, padx=5)

        self.button1.append(ttk.Button(self.registerR[12], text="PLL1 Configure", command=lambda:self.button1_clicked(15)))
        self.button1[12].pack(side=tk.LEFT, padx=5)

        self.button2.append(ttk.Button(self.registerR[12], text="PLL2 Configure", command=lambda:self.button2_clicked(15)))
        self.button2[12].pack(side=tk.LEFT, padx=5)

        self.button3.append(ttk.Button(self.registerR[12], image=self.info_icon, command=lambda:self.button3_clicked(15)))
        self.button3[12].pack(side=tk.LEFT, padx=5)

        #self.statusBar = tk.Label(self, bd=1, relief='sunken', text='Disconnected', anchor='c')
        #self.statusBar.grid(sticky=tk.W+tk.E, row=13, ipady=10)

        self.registerMapButton = ttk.Button(self.secondMainFrame, text="Show Register Map", command=lambda :webbrowser.open_new("lmx2581_regmap.pdf"))
        self.registerMapButton.pack( padx=10, ipadx=5, ipady=5, anchor='w')

        self.statusBar = tk.Label(self.secondMainFrame, text= 'Disconnected', anchor='e', bd=1, relief=tk.SUNKEN)
        self.statusBar.pack(side=tk.BOTTOM, fill=tk.X, pady=1)

    def button1_clicked(self, value):
        print("Button1 {} is pressed\n".format(value))

    def button2_clicked(self, value):
        print("Button2 {} is pressed\n".format(value))

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
            webbrowser.open_new("lmx2581_2.pdf")
        elif ((value == 13) or (value == 15)):
            webbrowser.open_new("lmx2581_15.pdf")


    def register_data_capture(self):
        pass

if __name__ == '__main__':
    app = App()
    app.mainloop()

