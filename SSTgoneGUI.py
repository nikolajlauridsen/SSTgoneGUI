from tkinter import *
from datetime import datetime
import os
import time
import sys

# TODO: Clean up

class SST(Frame):

    def __init__(self, master=None):
        Frame.__init__(self, master)
        # ---------- Initiate Frames ----------
        self.mainframe = Frame(root, padx=10, pady=8).pack()
        # -------- Displayed Variables --------
        self.hours = IntVar()
        self.minutes = IntVar()
        # --------- Various Variables ---------
        self.shutdown_time = 0
        self.get_time()
        self.shut_time_string = StringVar()
        if self.timer_running():
            self.convert_time()
        self.duration = None
        # -- Set defaults and create widgets --
        self.set_defaults()
        self.create_widgets()

    def create_widgets(self):
        # Title label
        title = Label(self.mainframe, text='Simple Sleep Timer')
        status = Label(self.mainframe, textvariable=self.shut_time_string)

        # Input Frame
        entry_frame = Frame(self.mainframe, pady=8)
        # Hours
        Label(entry_frame, text='Hours:')\
            .grid(column=0, row=0, sticky=W)

        Entry(entry_frame, width=5, textvariable=self.hours)\
            .grid(column=1, row=0, sticky=E)

        # Add separator
        Frame(entry_frame, width=30)\
            .grid(column=2, row=0)

        # Minutes
        Label(entry_frame, text='Minutes:')\
            .grid(column=3, row=0, sticky=W)

        Entry(entry_frame, width=5, textvariable=self.minutes)\
            .grid(column=4, row=0, sticky=E)

        # Button frame
        button_frame = Frame(self.mainframe, padx=5, pady=5)
        Button(button_frame, text="Shutdown", command=self.run_timer,
               relief=FLAT).grid(column=0, row=0)

        Button(button_frame, text="Restart", command=self.restart_timer,
               relief=FLAT).grid(column=1, row=0)

        Button(button_frame, text="Cancel", command=self.stop_timer,
               relief=FLAT).grid(column=2, row=0)

        Button(button_frame, text="Exit", command=sys.exit,
               relief=FLAT).grid(column=3, row=0)
        # Button padding
        for child in button_frame.winfo_children():
            child.grid_configure(padx=8)

        # Pack it all
        title.pack()
        entry_frame.pack()
        status.pack()
        button_frame.pack()

    def run_timer(self):
        """Calculate time to shutdown in seconds """
        self.duration = self.hours.get() * 3600 + self.minutes.get() * 60
        os.system('shutdown -s -t ' + str(self.duration))
        self.shutdown_time = int(time.time() + int(self.duration))
        self.save_time()
        self.convert_time()

    def restart_timer(self):
        self.duration = self.hours.get() * 3600 + self.minutes.get() * 60
        os.system('shutdown -s -t ' + str(self.duration))
        self.shutdown_time = int(time.time() + int(self.duration))
        self.save_time()
        self.convert_time()

    def stop_timer(self):
        if self.timer_running():
            with open('data.txt', 'w') as time_file:
                time_file.write('0')
            self.duration = 0
            self.shutdown_time = 0
            self.shut_time_string.set('No timer set')
            os.system('shutdown -a')
        else:
            self.shut_time_string.set('Timer not running, start timer first')

    def set_defaults(self):
        self.hours.set(1)
        self.minutes.set(30)

    # To be used later
    def save_time(self):
        with open('data.txt', 'w') as time_file:
            time_file.write(str(self.shutdown_time))

    # Get the previous time stamp and save it in self.shutdown_time
    def get_time(self):
        data = open('data.txt', 'r').readlines()
        self.shutdown_time = int(data[0])

    def convert_time(self):
        stamp = datetime.fromtimestamp(self.shutdown_time)\
            .strftime('Shutting down at %H:%M on %d-%m')
        self.shut_time_string.set(stamp)

    def timer_running(self):
        if self.shutdown_time - time.time() < 0:
            self.shut_time_string.set('No timer set')
            return False
        else:
            return True

if __name__ == "__main__":
    root = Tk()
    root.title('SST')
    root.bind('<Escape>', sys.exit)

    app = SST(master=root)
    root.mainloop()
