#!/usr/bin/python3
import tkinter as tk
from tkinter import filedialog as fd
from tkinter import messagebox as mb
import json
import os

class Window:
	def __init__(self,root):	#initializes Window class by placing the widgets and creating the StringVars
		self.root = root
		tk.Label(self.root, text="Input File").grid(row=0,column=0)
		tk.Button(self.root, text="Click to Open File", command=self.file_selection_callback).grid(row=1,column=0)
		tk.Label(self.root, text="Options").grid(row=0,column=1)
		
		self.filename = ""
		
		with open("resc/descriptions.json","r") as f:
			self.descriptions = json.load(f)
		
		self.description_panel = tk.Text(self.root)
		self.description_panel.grid(row=0,column=2,rowspan=6)

		self.trace_var = tk.StringVar()
		self.breakpoint_var = tk.StringVar()
		self.time_var = tk.StringVar()
		self.nanomites_var = tk.StringVar()
		self.elf_var = tk.StringVar()
		
		tk.Checkbutton(self.root, text="Trace Check", command=self.set_trace, variable=self.trace_var).grid(row=1,column=1)
		tk.Checkbutton(self.root, text="Breakpoint Check", command=self.set_breakpoint, variable=self.breakpoint_var).grid(row=2,column=1)
		tk.Checkbutton(self.root, text="Timing Check", command=self.set_time, variable=self.time_var).grid(row=3,column=1)
		tk.Checkbutton(self.root, text="Nanomites", command=self.set_nanomites, variable=self.nanomites_var).grid(row=4,column=1)
		tk.Checkbutton(self.root, text="ELF format obfuscation", command=self.set_elf_obfuscation, variable=self.elf_var).grid(row=5,column=1)
		
		tk.Button(self.root, text="Start obfuscating", command=self.start_obfuscating).grid(row=2,column=0)

	def file_selection_callback(self):	#starts file selection dialog and saves selected filename
		name = fd.askopenfilename()
		if name != "()":
			self.description_panel.delete("1.0","end")
			self.description_panel.insert("1.0","You opened a file: " + name)
			self.filename = name

	def change_description(self,selection):	#change description of panel
		self.description_panel.delete("1.0","end")
		self.description_panel.insert("1.0",self.descriptions[selection])

	def set_trace(self):	#set description of panel to tracing check
		if self.trace_var.get() == "1":
			self.change_description("trace")
		
	def set_breakpoint(self):	#set description of panel to breakpoint check
		if self.breakpoint_var.get() == "1":
			self.change_description("breakpoint")
	
	def set_time(self):	#set description of panel to timing check
		if self.time_var.get() == "1":
			self.change_description("time")
			
	def set_nanomites(self):	#set description of panel to nanomites
		if self.nanomites_var.get() == "1":
			self.change_description("nanomites")
	
	def set_elf_obfuscation(self):	#set description of panel to elf obfuscation
		if self.elf_var.get() == "1":
			self.change_description("elf_obfuscation")
			
	def start_obfuscating(self):	#function that gets executed when the "Start obfuscating" button is pressed. It decides which functions to run based on the check buttons
		if self.filename == "":
			mb.showinfo(title="File selection",message="Please select an input file")
		else:
			if self.trace_var.get() == "1" or self.breakpoint_var.get() == "1" or self.time_var.get() == "1":	#if a source level change has been selected
				if ".c" not in self.filename:
					mb.showinfo(title="File selection",message="Please provide C source file as input")
					return
				else:
					self.antianapy()
					self.compile()
					if self.nanomites_var.get() == "1" or self.elf_var.get() == "1":	#if a further elf level change has been selected
						self.elf_changes("$(pwd)/../antirevgui_output")
					self.end()

			elif self.nanomites_var.get() == "1" or self.elf_var.get() == "1":	#if elf level change has been selected
				with open(self.filename,"rb") as f:
					if f.read(4) != b"\x7fELF":
						mb.showinfo(title="File selection",message="Please provide ELF file as input")
					else:
						self.elf_changes()
						self.end()	
			
	def antianapy(self):	#applies source level changes by calling ANTIANAPY
		shell_string = "cd ANTIANAPY;./ANTIANAPY.py " + self.filename + " --non-interactive"
		if self.trace_var.get() == "1":
			shell_string += " --trace"
		if self.breakpoint_var.get() == "1":
			shell_string += " --breakpoint"
		if self.time_var.get() == "1":
			shell_string += " --time"
		os.system(shell_string)

	def compile(self):	#compiles output of ANTIANAPY and removes generated source file
		shell_string = "gcc " + self.filename[:-(len(self.filename.split("/")[-1].split(".")[0])+2)] + self.filename.split("/")[-1].split(".")[0] + "_antianapy.c" + " -o antirevgui_output"
		if self.time_var.get() == "1":
			shell_string += " -pthread"
		os.system(shell_string)
		shell_string = "rm " + self.filename[:-(len(self.filename.split("/")[-1].split(".")[0])+2)] + self.filename.split("/")[-1].split(".")[0] + "_antianapy.c"
		os.system(shell_string)
		
	def elf_changes(self,elf_name = ""):	#implements changes on ELF level by calling ELFREVGO and APAKER
		if elf_name == "":
			elf_name = self.filename
		if self.nanomites_var.get() == "1":
			shell_string = "cd APAKER;./add_nanomites.sh " + elf_name + " $(pwd)/../antirevgui_output"
			os.system(shell_string)
			elf_name = "$(pwd)/../antirevgui_output"
		if self.elf_var.get() == "1":
			shell_string = "cd ELFREVGO;./ELFREVGO -f " + elf_name + " -o $(pwd)/../antirevgui_output -t -n -b -e"
			os.system(shell_string)
	
	def end(self):	#displays name of output file
		self.description_panel.delete("1.0","end")
		self.description_panel.insert("1.0","Finished compiling your source file, you can find the output file under the name\nantirevgui_output in the current directory")
	

window = tk.Tk()
window.title("AntiRevGUI")
img = tk.Image("photo", file="images/laptop.png")	#sets app icon
window.tk.call("wm","iconphoto",window._w,img)
app = Window(window)
window.mainloop()

