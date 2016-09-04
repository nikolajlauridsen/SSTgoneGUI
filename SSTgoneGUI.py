from tkinter import *
from datetime import datetime
import os
import time
import sys


class SST(Frame):

    def __init__(self, master=None):
        Frame.__init__(self, master)
        # ---------- Initiate Frames ----------
        self.mainframe = Frame(root, padx=10, pady=8).pack()
        # -------- Displayed Variables --------
        self.hours = IntVar()
        self.minutes = IntVar()
        self.shut_time_string = StringVar()
        # --------- Various Variables ---------
        self.shutdown_time = 0
        self.duration = None
        # -- Set defaults and create widgets --
        self.set_defaults()
        self.create_widgets()
        # -- If timer is running, set status --
        if self.timer_running():
            self.set_status()

    def create_widgets(self):
        """Create all the widgets, keeps __init__ short-ish"""
        # Labels
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
        Button(button_frame, text="Shutdown", command=self.shutdown_timer,
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

    def shutdown_timer(self):
        """Start the timer, for a shutdown event."""
        self.duration = self.hours.get() * 3600 + self.minutes.get() * 60
        os.system('shutdown -s -t ' + str(self.duration))
        self.save_time()
        self.set_status()

    def restart_timer(self):
        """Set the timer for a restart event."""
        self.duration = self.hours.get() * 3600 + self.minutes.get() * 60
        os.system('shutdown -s -t ' + str(self.duration))
        self.save_time()
        self.set_status()

    def stop_timer(self):
        """Stop and reset the timer."""
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
        """Set hour/minute defaults."""
        self.hours.set(1)
        self.minutes.set(30)

    def save_time(self):
        """Calculate shutdown time and save to file."""
        self.shutdown_time = int(time.time() + int(self.duration))
        with open('data.txt', 'w') as time_file:
            time_file.write(str(self.shutdown_time))

    # Get the previous time stamp and save it in self.shutdown_time
    def get_time(self):
        """Read the shutdown time from the file."""
        data = open('data.txt', 'r').readlines()
        self.shutdown_time = int(data[0])

    def set_status(self):
        """Set the status line to display the shutdown time."""
        stamp = datetime.fromtimestamp(self.shutdown_time)\
            .strftime('Shutting down at %H:%M on %d-%m')
        self.shut_time_string.set(stamp)

    def timer_running(self):
        """Check whether the timer is running or not."""
        self.get_time()
        if self.shutdown_time - time.time() < 0:
            self.shut_time_string.set('No timer set')
            return False
        else:
            return True

if __name__ == "__main__":
    root = Tk()
    app = SST(master=root)
    root.title('SST GUI')
    root.bind('<Escape>', sys.exit)
    root.mainloop()
