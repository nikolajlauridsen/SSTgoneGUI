from tkinter import *
import os
import time
import sys


class SST(Frame):

    def __init__(self, master=None):
        Frame.__init__(self, master)
        # ---------- Initiate Frames ----------
        self.mainframe = Frame(root, padx=10, pady=8)
        self.mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
        self.mainframe.columnconfigure(0, weight=1)
        self.mainframe.rowconfigure(0, weight=1)
        self.button_frame = Frame(self.mainframe, padx=5, pady=5)
        self.button_frame.grid(column=0, row=3, columnspan=5)
        # -------- Displayed Variables --------
        self.hours = IntVar()
        self.minutes = IntVar()
        # --------- Various Variables ---------
        self.shutdown_time = None
        self.duration = None
        # -- Set defaults and create widgets --
        self.set_defaults()
        self.create_widgets()

    def create_widgets(self):
        # Title label
        Label(self.mainframe, text='Simple Sleep Timer').grid(column=0, row=1, columnspan=5, sticky=W+E)

        # Input
        # Hours
        Label(self.mainframe, text='Hours:')\
            .grid(column=1, row=2, sticky=E)

        Entry(self.mainframe, width=5, textvariable=self.hours)\
            .grid(column=2, row=2, sticky=W)

        # Minutes
        Label(self.mainframe, text='Minutes:')\
            .grid(column=3, row=2, sticky=E)

        Entry(self.mainframe, width=5, textvariable=self.minutes)\
            .grid(column=4, row=2, sticky=W)
        # Buttons
        Button(self.button_frame, text="Shutdown", command=self.run_timer,
               relief=FLAT).grid(column=1, row=0, sticky=W)

        Button(self.button_frame, text="Restart", command=self.restart_timer,
               relief=FLAT).grid(column=2, row=0, sticky=W+E)

        Button(self.button_frame, text="Cancel", command=self.stop_timer,
               relief=FLAT).grid(column=3, row=0, sticky=E)

        Button(self.button_frame, text="Exit", command=sys.exit,
               relief=FLAT).grid(column=4, row=0)
        # Button padding
        for child in self.button_frame.winfo_children():
            child.grid_configure(padx=8)

    def run_timer(self):
        """Calculate time to shutdown in seconds """
        self.duration = self.hours.get() * 3600 + self.minutes.get() * 60
        os.system('shutdown -s -t ' + str(self.duration))
        self.save_time()

    def restart_timer(self):
        self.duration = self.hours.get() * 3600 + self.minutes.get() * 60
        os.system('shutdown -s -t ' + str(self.duration))
        self.save_time()

    def stop_timer(self):
        os.system('shutdown -a')

    def set_defaults(self):
        self.hours.set(1)
        # self.minutes.set(30)

    # To be used later
    def save_time(self):
        self.shutdown_time = int(time.time() + int(self.duration))
        with open('data.txt', 'w') as time_file:
            time_file.write(str(self.shutdown_time))


root = Tk()
root.title('SST')
root.bind('<Escape>', sys.exit)

app = SST(master=root)

root.mainloop()