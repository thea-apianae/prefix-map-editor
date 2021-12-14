#import modules
from os.path import exists
import tkinter as tk
from tkinter import StringVar, ttk, messagebox as mb, filedialog as fd
from tkinter.constants import BROWSE
import webbrowser
import os
from PIL import Image, ImageTk

#create root window
root=tk.Tk()

#values for labels and comboboxes
boxyboys=[
    ["Prefix", 1, 1, 2, 2],
    ["Suffix", 3, 1, 4, 2]
]

#octaves
pnum=(
    "7",
    "6",
    "5",
    "4",
    "3",
    "2",
    "1"
)

#note names
plet=(
    "B",
    "A#",
    "A",
    "G#",
    "G",
    "F#",
    "F",
    "E",
    "D#",
    "D",
    "C#",
    "C"
)

#create empty list to populate
pitches=[]

#open image and create variable "fune", to reference in "aboutwindow"
img=Image.open("IMPORTANT.png").resize(
    (85, 85),
    Image.ANTIALIAS
)
fune=ImageTk.PhotoImage(img)

#populate list "pitches" with values
for pn in pnum:
    for pl in plet:
        p=pl + pn
        pitches.append(p)

#add scrollbar
sb=tk.Scrollbar()

#define setup of program
def setup():
    #customize root window to have title, not resizable, fixed geometry
    root.title("Prefix Map Editor v1.1")
    root.resizable(False, False)
    root.geometry("475x300")

    #create string variables for entry boxes
    etxt1=StringVar(value="")
    etxt2=StringVar(value="")

    #create string variables to retrieve input
    atxt1=StringVar(value="")
    atxt2=StringVar(value="")

    #add frame for pitchtree
    pframe=tk.Frame(root).grid(row=1, column=9)

    #create pitch tree with three columns, shows headings, uses scrollbar on y-axis, 
    #change select mode to BROWSE (one at a time)
    ptree=ttk.Treeview(pframe, 
        columns=("pitch", "prefix", "suffix"),
        show="headings",
        yscrollcommand=sb.set,
        selectmode=BROWSE
    )

    #add headings and columns to pitchtree
    ptree.heading("0",
        anchor="center",
        text="Pitch")
    ptree.column("0",
        width=50)
    ptree.heading("1",
        anchor="center",
        text="Prefix")
    ptree.column("1",
        width=50)
    ptree.heading("2",
        anchor="center",
        text="Suffix")
    ptree.column("2",
        width=50)

    #add scrollbar to grid
    sb.grid(row=0,
        column=12,
        rowspan=25,
        sticky="nsw"
    )

    #insert pitch values into rows of pitch tree
    for n in pitches:
        ptree.insert("", index=pitches.index(n), iid=pitches.index(n), values=n)

    #add pitch tree to grid
    ptree.grid(row=0, column=9, rowspan=25, columnspan=3)

    #set scrollbar command to the y-axis of the pitch tree
    sb.config(command=ptree.yview)

    #create string variables to retrieve combobox values
    cb1val=StringVar()
    cb2val=StringVar()
    cb3val=StringVar()
    cb4val=StringVar()

    #create combobox 1: add to root window, set text variable in order to retrieve later, "readonly" state
    #to not allow user to change values, set width to 4 characters, set options to pitches (earlier defined),
    #add to grid
    cb1=ttk.Combobox(root,
        textvariable=cb1val,
        state="readonly",
        width=4,
        values=pitches
    ).grid(row=2, column=1, padx=3, pady=1)

    #same thing but 2
    cb2=ttk.Combobox(root,
        textvariable=cb2val,
        state="readonly",
        width=4,
        values=pitches
    ).grid(row=2, column=3, padx=3, pady=1)

    #same thing but 3
    cb3=ttk.Combobox(root,
        textvariable=cb3val,
        state="readonly",
        width=4,
        values=pitches
    ).grid(row=4, column=1, padx=3, pady=1)

    #same thing but 4
    cb4=ttk.Combobox(root,
        textvariable=cb4val,
        state="readonly",
        width=4,
        values=pitches
    ).grid(row=4, column=3, padx=3, pady=1)

    #create first entry box in root window, with width of 5 characters, with variable to be used later, add to grid
    e1=tk.Entry(root,
        width=5,
        textvariable=etxt1
    ).grid(row=2, column=4, padx=3, pady=1)

    #same but 2
    e2=tk.Entry(root,
        width=5,
        textvariable=etxt2
    ).grid(row=4, column=4, padx=3, pady=1)

    #command for first "set" button. first gets the variable of the first entry box. if that value is "", or nothing,
    #it does not change anything. otherwise, it tries to use the values from the comboboxes to set the records
    #in pitch tree to "atxt1", the entry from the user. it is in the first column because this is the "prefix" option.
    #in the case that the user has not selected any values for the pitches, it shows an error requesting them to do 
    #so.
    #also, it doesn't work if the first combobox's value is after the second, but i don't really feel like fixing it.
    def setcmd1():
        atxt1=etxt1.get()
        if atxt1 == "":
            pass
        else:
            try:
                for n in pitches[pitches.index(cb1val.get()):pitches.index(cb2val.get())+1]:
                    for element in pitches:
                        if element == n:
                            item=pitches.index(n)
                            ptree.set(item, column=1, value=atxt1)
            except ValueError:
                mb.showerror(title="Error", message="Please select a pitch.")

    #same as before, but with the second version of things, and in the second column for the suffix.
    def setcmd2():
        atxt2=etxt2.get()
        if atxt2 == "":
            pass
        else:
            try:
                for n in pitches[pitches.index(cb3val.get()):pitches.index(cb4val.get())+1]:
                    for element in pitches:
                        if element == n:
                            item=pitches.index(n)
                            ptree.set(item, column=2, value=atxt2)
            except ValueError:
                mb.showerror(title="Error", message="Please select a pitch.")

    #command for button below pitch tree to "Clear Selected", which clears the selected row; applies to both prefix
    #and suffix columns.
    def clearsel():
        delsel=ptree.focus()
        ptree.set(item=delsel, column=1, value="")
        ptree.set(item=delsel, column=2, value="")

    #first "Set" button
    sbt1=tk.Button(root,
        text="Set",
        width=3,
        command=setcmd1
    ).grid(row=2, column=5, padx=3, pady=1)

    #second "Set" button
    sbt2=tk.Button(root,
        text="Set",
        width=3,
        command=setcmd2
    ).grid(row=4, column=5, padx=3, pady=1)

    #"Clear Selected" button underneath treeview
    clrbt=tk.Button(root,
        text="Clear Selected",
        command=clearsel,
        width=13
    ).grid(row=26, column=10, padx=1, pady=1)

    #define clearall command for later use
    def clearall():
        for item in ptree.get_children():
            ptree.delete(item)
        for n in pitches:
            ptree.insert("", index=pitches.index(n), iid=pitches.index(n), values=n)

    #defines creating a new file; first detects if there is a "prefix.map" already in the same folder. if there is,
    #it asks if you want to discard the contents of that file. if there is not, it creates a new file. the clearall
    #function is called when a new file is created and subsequently opened, with utf-8 encoding to allow for characters
    #outside of the latin alphabet.
    def new():
        if exists("prefix.map"):
            answer=mb.askyesno(title="New File Confirmation",
                message="Discard contents of the old file?"
            )
            if answer:
                clearall()
                f=open("prefix.map", "w+", encoding="utf8")
                for element in pitches:
                    f.write(element + "\n")
                f.close()
        else:
            clearall()
            f=open("prefix.map", "w+", encoding="utf8")
            for element in pitches:
                f.write(element + "\n")
            f.close()

    #defines selecting a pre-existing file. allows user to choose either .map files or any other kind, cause i'm
    #not really sure how to make it just the first one. a dialog pops up for file selection. if the user selects a
    #file, clearall is called to initialize the pitch tree. the file is opened in "r+" mode, as to not immediately
    #overwrite the contents, with utf-8 encoding for the same reason as before. the file is then read line by line
    #and added to list "a", which is then split by newlines in list "b". for each line in b, item is set to the index
    #of that line. if the value of item is greater than 83 (the amount of pitches+notes there are), it passes, as not
    #to return an error. in the other case, it tries to split the lines further by tabbed spaces and then copies those
    #values to the pitch tree. a try: except: statement is included to ensure that if an indexerror occurs, it will
    #keep working. the file is then closed.
    def selectfile():
        filetypes=(
            ("prefix map files", "*.map"),
            ("all files", "*.*")
        )
        openfile=fd.askopenfilename(
            title="Open",
            filetypes=(filetypes)
        )
        if openfile:
            clearall()
            a=""
            f=open(openfile, "r+", encoding="utf8")
            oflines=f.readlines()
            for line in oflines:
                a=a+line
            b=a.split("\n")
            for line in b:
                item=b.index(line)
                if item > 83:
                    pass
                else:
                    try:
                        pref=line.split("\t")[1]
                        ptree.set(item, column=1, value=pref)
                        suff=line.split("\t")[2]
                        ptree.set(item, column=2, value=suff)
                    except IndexError:
                        pass
            f.close()

    #defines saving as a file. a dialog is shown for the user to select what file they would like to save it as.
    #if the user chooses to save the file, it opens said file and gets the current values of the pitch tree. a for
    #loop is then executed wherein each value "i" in the pitch tree's get_children is set to info. then, it writes
    #the pitches to the fie, then the prefixes, then the suffixes. in the event that there is no prefix or suffix
    #value to be written, it writes either "\t" or "\n". after the loop is iterated through completely, it closes
    #the file.
    def saveasfile():
        filetypes=(
            ("prefix map files", "*.map"),
            ("all files", "*.*")
        )

        filename=fd.asksaveasfilename(
            title="Save As",
            filetypes=(filetypes)
        )
        if filename:
            f=open(filename, "w", encoding="utf8")
            xes=ptree.get_children("")
            for i in xes:
                info=ptree.set(i)
                f.write(info["pitch"] + "	")
                try:
                    f.write(info["prefix"] + "	")
                except KeyError:
                    f.write("	")
                try:
                    f.write(info["suffix"] + "\n")
                except KeyError:
                    f.write("\n")
            f.close()

    #creates the place for the menubar at the top.
    menubar=tk.Menu(root)
    root.config(menu=menubar)

    #creates file menu first. tearoff is disabled, which means the user cannot detach the menubar from its place.
    filemenu=tk.Menu(menubar,
        tearoff=False
    )
    #the "new" command is added.
    filemenu.add_command(
        label="New",
        command=new
    )
    #the "open" command is added.
    filemenu.add_command(
        label="Open",
        command=selectfile
    )
    #the "save as" command is added.
    filemenu.add_command(
        label="Save as...",
        command=saveasfile
    )

    #a seperator is added.
    filemenu.add_separator()

    #the "exit" command is added.
    filemenu.add_command(
        label="Exit",
        command=root.destroy
    )
    #the cascade is added, so that the previous commands are able to be viewed by hovering over the "File" menu.
    menubar.add_cascade(
        label="File",
        menu=filemenu
    )

    #defines readme for later usage.
    def readme():
        webbrowser.open("readme.txt")

    #defines the creation of the aboutwindow.
    def aboutwindow():
        #the window is added as a toplevel to the root window, titled "About". it is not resizable either, and is a
        #tool window, which means it cannot be minimized or maximized.
        about=tk.Toplevel(root)
        about.title("About")
        about.resizable(False, False)
        about.geometry("150x150")
        about.attributes("-toolwindow", True)
        
        #create and pack the first label widget.
        atxt1=StringVar()
        atxt1.set("Prefix Map Editor v1.1")
        aboutxt1=tk.Label(
            about,
            textvariable=atxt1
        ).pack()

        #create and pack the second label widget.
        atxt2=StringVar()
        atxt2.set("thea apianae 2021")
        aboutxt2=tk.Label(
            about,
            textvariable=atxt2
        ).pack()

        #add the image from before underneath the labels.
        aimage1=tk.Label(
            about,
            image=fune
        ).pack(pady=5)

    #creates the help menu.
    helpmenu=tk.Menu(menubar)
    helpmenu=tk.Menu(menubar,
        tearoff=False
    )

    #adds the readme option to the help menu.
    helpmenu.add_command(
        label="readme",
        command=readme
    )

    #adds the about option to the help menu.
    helpmenu.add_command(
        label="About",
        command=aboutwindow
    )

    #adds the cascade to the help menu.
    menubar.add_cascade(
        label="Help",
        menu=helpmenu
    )

    #uses elements from previous boxyboys to create the prefix and suffix labels, as well as the "-" between
    #comboboxes.
    for element in boxyboys:
        l1=tk.Label(root,
            text=element[0]
        ).grid(row=element[1], column=element[2], padx=3, pady=2)

        l2=tk.Label(root,
            text="-"
        ).grid(row=element[3], column=element[4], pady=1)

    #the first space, between the set buttons and the pitch tree.
    spacer1=tk.Label(root,
        text="",
        width=3
    ).grid(column=8)

    #the second spacer, at the top of the widgets.
    spacer2=tk.Label(root,
        text="",
        width=1
    ).grid()

    #the third spacer, to the left of the widgets.
    spacer3=tk.Label(root,
        text="",
    ).grid(row=0, column=0)

#executes setup.
setup()

#keeps the window running until otherwise destroyed.
root.mainloop()