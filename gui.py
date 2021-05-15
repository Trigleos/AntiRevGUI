import tkinter as tk
from tkinter import filedialog as fd
from tkinter import messagebox as mb
import json
import os

class Window:
	def __init__(self,root):
		self.root = root
		tk.Label(self.root, text='Input File').grid(row=0,column=0)
		tk.Button(self.root, text='Click to Open File', command=self.file_selection_callback).grid(row=1,column=0)
		tk.Label(self.root, text='Options').grid(row=0,column=1)
		self.filename_entry = tk.Entry(self.root)
		self.filename_entry.grid(row=2,column=0)
		
		self.filename = ""
		
		with open("descriptions.json","r") as f:
			self.descriptions = json.load(f)
		
		self.description_panel = tk.Text(self.root)
		self.description_panel.grid(row=0,column=2,rowspan=2)

		self.trace_var = tk.StringVar()
		self.breakpoint_var = tk.StringVar()
		self.time_var = tk.StringVar()
		
		tk.Checkbutton(self.root, text='Trace Check',command=self.set_trace, variable=self.trace_var).grid(row=1,column=1)
		tk.Checkbutton(self.root, text='Breakpoint Check',command=self.set_breakpoint, variable=self.breakpoint_var).grid(row=2,column=1)
		tk.Checkbutton(self.root, text='Timing Check',command=self.set_time, variable=self.time_var).grid(row=3,column=1)
		
		tk.Button(self.root, text='Start obfuscating', command=self.start_obfuscating).grid(row=4,column=0,columnspan=3)

	def file_selection_callback(self):
		name = fd.askopenfilename()
		if name != "()":
			self.filename_entry.delete("0","end")
			self.filename_entry.insert("0",name)
			self.filename = name

	def change_description(self,selection):
		self.description_panel.delete("1.0","end")
		self.description_panel.insert("1.0",self.descriptions[selection])

	def set_trace(self):
		if self.trace_var.get() == "1":
			self.change_description("trace")
		
	def set_breakpoint(self):
		if self.breakpoint_var.get() == "1":
			self.change_description("breakpoint")
	
	def set_time(self):
		if self.time_var.get() == "1":
			self.change_description("time")
			
	def start_obfuscating(self):
		if self.filename == "":
			mb.showinfo(title="File selection",message="Please select an input file")
		else:
			if self.trace_var.get() == "1" or self.breakpoint_var.get() == "1" or self.time_var.get() == "1":
				if ".c" not in self.filename:
					print("Please provide C source file")
					return
				else:
					self.antianapy()
					self.compile()
			
	def antianapy(self):
		shell_string = "cd ANTIANAPY;./ANTIANAPY.py " + self.filename + " --non-interactive"
		if self.trace_var.get() == "1":
			shell_string += " --trace"
		if self.breakpoint_var.get() == "1":
			shell_string += " --breakpoint"
		if self.time_var.get() == "1":
			shell_string += " --time"
		os.system(shell_string)

	def compile(self):
		shell_string = "gcc " + self.filename.split("/")[-1].split(".")[0] + "_antianapy.c" + " -o antirevgui_output"
		if self.time_var.get() == "1":
			shell_string += " -pthread"
		os.system(shell_string)

window = tk.Tk()
app = Window(window)
window.mainloop()

