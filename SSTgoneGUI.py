from tkinter import *
from tkinter import ttk
import os


def run_timer(*args):
    try:
        s = (int(hours.get())*3600) + (int(minutes.get())*60)
        os.system('shutdown -s -t ' + str(s))
    except ValueError:
        pass


def reboot(*args):
    try:
        s = (int(hours.get()) * 3600) + (int(minutes.get()) * 60)
        os.system('shutdown -r -t ' + str(s))
    except ValueError:
        pass


def cancel_shutdown(*args):
    os.system('shutdown -a')

root = Tk()
root.title('SST')

mainframe = ttk.Frame(root, padding="3 3 12 12")
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
mainframe.columnconfigure(0, weight=1)
mainframe.rowconfigure(0, weight=1)

# Variables
hours = StringVar()
minutes = StringVar()

# Widgets go here
ttk.Label(mainframe, text="Simple Sleep Timer").grid(column=3, row=1, sticky=N)

# Hours Entry
ttk.Label(mainframe, text="Hours:").grid(column=2, row=2, sticky=W)
hours_entry = ttk.Entry(mainframe, width=5, textvariable=hours)
hours_entry.grid(column=2, row=2, sticky=E)

# Minutes Entry
ttk.Label(mainframe, text="Minutes:").grid(column=3, row=2, sticky=W)
minutes_entry = ttk.Entry(mainframe, width=5, textvariable=minutes)
minutes_entry.grid(column=3, row=2, sticky=E)

# Shutdown Buttons
ttk.Button(mainframe, text="Shutdown", command=run_timer).grid(column=2, row=3, sticky=S)
ttk.Button(mainframe, text="Restart", command=reboot).grid(column=3, row=3, sticky=S)
ttk.Button(mainframe, text="Cancel Shutdown", command=cancel_shutdown).grid(column=4, row=3, sticky=S)


for child in mainframe.winfo_children(): child.grid_configure(padx=5, pady=5)

hours_entry.focus()
hours_entry.insert(0, "1")
minutes_entry.insert(0, "30")
root.bind('<Return>', run_timer)
root.bind('<Escape>', cancel_shutdown)

root.mainloop()
