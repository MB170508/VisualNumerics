import tkinter as tk
import tkinter.ttk as ttk
import tkinter.filedialog as fd
import tkinter.colorchooser as cc
from tkinter.constants import *
import tkinter.scrolledtext as st
from ns import *
import os

class FileTreeView:
    def __init__(self, parent):
        self.parent = parent
        self.treeObject = ttk.Treeview(self.parent.content, show="tree")
        tree = self.treeObject
        if self.parent.directory:
            self.listDir()
            tree.bind("<<TreeviewOpen>>", self.listDir)
            tree.bind("<<TreeviewClose>>", self.cleanDir)
            tree.bind("<<TreeviewSelect>>", self.parent.code.tabClick)
    
    def listDir(self, event=None):
        tree = self.treeObject
        if event:
            parent = " ".join(tree.item(tree.focus(), "tags"))
            tree.delete(tree.get_children(parent)[0])
        else:
            parent = ""
        for i in os.listdir(os.path.join(self.parent.directory, parent[1:])):
            if os.path.isdir(os.path.join(self.parent.directory, parent[1:], i)):
                tree.insert(parent, "end", parent+"/"+i, text=i, tags=parent+"/"+i)
                tree.insert(parent+"/"+i, "end")
            else:
                tree.insert(parent, "end", parent+"/"+i, text=i)
    
    def cleanDir(self, event):
        tree = self.treeObject
        parent = tree.item(tree.focus(), "tags")
        for i in tree.get_children(parent):
            tree.delete(i)
        tree.insert(parent, "end")
        
    def tabClick(self, event=None):
        pass

class CodeView:
    def __init__(self, parent):
        self.parent = parent
        self.codeObject = ttk.Notebook(self.parent.rightPane)
        code = self.codeObject
        self.untitledIndex = 0
        self.closeTab = tk.Frame(self.codeObject)
        self.tabs = {"Untitled-"+str(self.untitledIndex): st.ScrolledText(self.codeObject, wrap="none", undo=True)}
        self.tabs[f"Untitled-{self.untitledIndex}"].bind("<Key>",lambda e: self.currentTab.edit_modified(True))
        code.add(self.tabs["Untitled-0"], text=f"Untitled-{self.untitledIndex}")
        
        self.buttonFrame = tk.Frame(self.codeObject, width=10, height=5)
        
        code.add(self.closeTab, text="x")
        code.add(tk.Frame(self.codeObject), text="+")
        code.bind("<<NotebookTabChanged>>", self.tabClick)

    def tabClick(self, event=None):
        """Handles all tab onclick events - opening/closing tabs
        
        Args:
            event (tkinter.Event, optional): Tkinter event that called the function. Defaults to None.
        """
        topTabIndex = self.codeObject.index("end")-1
        self.currentTabIndex = self.codeObject.index("current")
        self.currentTabName = self.codeObject.tab(self.currentTabIndex, "text")
        self.currentTab = self.tabs[self.currentTabName] if self.currentTabName in self.tabs else None
        self.tabNames = [self.codeObject.tab(tab, "text") for tab in self.codeObject.tabs()]
        if event:
            # Open new Untitled tab
            if self.codeObject.index("current") == topTabIndex:
                self.untitledIndex = self.getUntitIndex()
                self.tabs.update({"Untitled-"+str(self.untitledIndex): st.ScrolledText(self.codeObject, wrap="none", undo=True)})
                self.codeObject.insert(topTabIndex, list(self.tabs.values())[-1], text=f"Untitled-{self.untitledIndex}")
                self.codeObject.select(topTabIndex)
            # Close tab
            elif self.currentTabName == "x":
                if len(self.tabNames) > 3:
                    self.tabs[self.tabNames[self.codeObject.index("current")-1]].destroy()
                    self.tabs.pop(self.tabNames[self.codeObject.index("current")-1])
                    self.codeObject.forget(self.codeObject.tabs()[self.codeObject.index("current")-1])
                    if self.codeObject.index("current") != 0: self.codeObject.select(self.codeObject.index("current")-1)
                    else: self.codeObject.select(self.codeObject.index("current")+1)
                else: self.codeObject.select(self.codeObject.index("current")-1)
            # Open selected file in new tab
            elif self.parent.tree.treeObject.focus()[1:] not in self.tabNames:
                fileName = self.parent.tree.treeObject.focus()[1:]
                if os.path.isfile(f"{self.parent.directory}/{fileName}"):
                    with open(f"{self.parent.directory}/{fileName}") as file:
                        self.tabs.update({fileName: st.ScrolledText(self.codeObject, wrap="none", undo=True)})
                        self.codeObject.insert(topTabIndex, list(self.tabs.values())[-1], text=self.parent.tree.treeObject.focus()[1:])
                        self.tabs[fileName].insert("1.0", chars=file.read())
                        self.codeObject.select(topTabIndex)
                self.parent.tree.treeObject.focus("")
            self.codeObject.insert("end", self.closeTab)
            self.codeObject.insert(self.codeObject.index("current")+1, self.closeTab)
        self.parent.runButton.lift()
        
    def getUntitIndex(self) -> int:
        """Returns the lowest unused integer for naming untitled tabs
        
        Returns:
            int: Lowest unused integer
        """
        for i in range(len(self.tabNames)-1):
            if f"Untitled-{i}" not in self.tabNames:
                return i
        #else: return len(self.tabNames)-2

class ConsoleView:
    def __init__(self, parent):
        self.parent = parent
        self.frame = tk.Frame(self.parent.rightPane)
        """self.consoleObject = st.ScrolledText(self.frame, wrap="none", height=10)
        self.consoleObject.pack(fill=BOTH, expand=True)
        self.consoleObject.insert("1.0", ">>> ")"""
        #self.consoleObject.config(state="disabled")
        
        self.entry = tk.Entry(self.frame)
        self.entry.pack(side=tk.BOTTOM, fill=tk.X)
        self.entry.bind('<Return>', self.inp)
        
        self.entry.insert(tk.END, ">>> ")
        self.entry.config(validate='key', validatecommand=(self.frame.register(lambda t: t.startswith(">>> ")), '%P'))
        
        self.consoleObject = st.ScrolledText(self.frame, height=10, borderwidth=0, state="disabled")
        self.consoleObject.pack(side=tk.BOTTOM, fill=tk.X)
    
    def out(self, *s, sep=" ", end="\n") -> str:
        """Writes text to the console field
        
        Args:
            sep (str, optional): String inserted bewteen values. Defaults to space.
            end (str, optional): String appended after the last value. Defaults to newline.
        
        Returns:
            str: The written text in the output format.
        """
        output = sep.join([str(i) for i in s])+end
        self.consoleObject.config(state="normal")
        self.consoleObject.insert("end", output)
        self.consoleObject.see(END)
        self.consoleObject.config(state="disabled")
        return output
    
    def inp(self, event, prompt=""):
        """Handles input from self.entry.

        Args:
            event (tkinter.Event): Event that called the function.
            prompt (str, optional): If specified is written into the console without trailing characters. Defaults to empty string.
        """
        output = self.consoleObject
        output['height'] += 1
        
        global tokenized_line, tokenized_code
        data = self.entry.get()[4:]
        if data.isnumeric():
            if data: tokenized_line=tokenizer(data.replace(" ",""))
            if tokenized_line == ["00"] or data == "": exe(self.out)
            elif tokenized_line != "-99": tokenized_code.append(tokenized_line)
        self.out(tokenized_line, tokenized_code)
        self.out(data)

class WindowMenu:
    def __init__(self, parent):
        self.parent = parent
        self.menuObject = tk.Menu(self.parent.root)
        
        self.fileMenu = tk.Menu(self.menuObject, tearoff=0)
        self.fileMenu.add_command(label="Open", command=self.parent.changeDir)
        self.fileMenu.add_command(label="Save", command=self.save)
        self.fileMenu.add_command(label="Save As", command=self.saveAs)
        self.fileMenu.add_separator()
        self.fileMenu.add_command(label="Exit", command=self.parent.root.quit)
        
        self.editMenu = tk.Menu(self.menuObject, tearoff=0)
        self.editMenu.add_command(label="Undo", command=self.undo)
        self.editMenu.add_command(label="Redo", command=self.redo)
        self.editMenu.add_separator()
        self.editMenu.add_command(label="Cut", command=self.cut)
        self.editMenu.add_command(label="Copy", command=self.copy)
        self.editMenu.add_command(label="Paste", command=self.paste)
        self.editMenu.add_command(label="Delete", command=self.delete)
        self.editMenu.add_separator()
        self.editMenu.add_command(label="Select All", command=self.selectAll)
        
        self.viewMenu = tk.Menu(self.menuObject, tearoff=0)
        self.viewMenu.add_command(label="Hide Console", command=self.toggleConsole)
        
        self.menuObject.add_cascade(label="File", menu=self.fileMenu)
        self.menuObject.add_cascade(label="Edit", menu=self.editMenu)
        self.menuObject.add_cascade(label="View", menu=self.viewMenu)
    
    def save(self):
        file = open(f"{self.parent.directory}/{self.parent.code.currentTabName}", "w+")
        file.write(self.parent.code.currentTab.get("1.0", "end")[:-1])
    def saveAs(self):
        file = fd.asksaveasfile()
        file.write(self.parent.code.currentTab.get("1.0", "end")[:-1])
    
    def undo(self):
        self.parent.code.currentTab.edit_undo()
    def redo(self):
        self.parent.code.currentTab.edit_redo()
    
    def cut(self):
        if self.parent.code.currentTab.tag_ranges("sel"):
            self.parent.code.currentTab.clipboard_clear()
            self.parent.code.currentTab.clipboard_append(self.parent.code.currentTab.get("sel.first", "sel.last")[:-1])
            self.parent.code.currentTab.delete("sel.first", "sel.last")
    def copy(self):
        if self.parent.code.currentTab.tag_ranges("sel"):
            self.parent.code.currentTab.clipboard_clear()
            self.parent.code.currentTab.clipboard_append(self.parent.code.currentTab.get("sel.first", "sel.last")[:-1])
    def paste(self):
        cursorPos = self.parent.code.currentTab.index("insert")
        self.parent.code.currentTab.insert(cursorPos, self.parent.code.currentTab.clipboard_get())
    def delete(self):
        if self.parent.code.currentTab.tag_ranges("sel"): self.parent.code.currentTab.delete("sel.first", "sel.last")
        else: self.parent.code.currentTab.delete("1.0","end")
    
    def selectAll(self):
        self.parent.code.currentTab.tag_add("sel", "1.0", "end")
    
    def toggleConsole(self):
        if len(self.parent.rightPane.panes()) > 1:
            self.parent.rightPane.remove(self.parent.console.frame)
            self.viewMenu.entryconfig(1, label="Show Console")
        else:
            self.parent.rightPane.add(self.parent.console.frame)
            self.viewMenu.entryconfig(1, label="Hide Console")

class MainWindow:
    def __init__(self, directory=None, title="VISUAL_NUMERICS.PY", width=800, height=600):
        self.root = tk.Tk()
        self.directory = directory
        self.width = width
        self.height = height
        self.root.title(title)
        self.root.geometry(f"{self.width}x{self.height}")
        
        self.content = ttk.PanedWindow(self.root, orient=tk.HORIZONTAL)
        self.content.pack(fill=BOTH, expand=True)
        
        self.rightPanel = tk.Frame(self.root)
        self.rightPane = ttk.PanedWindow(self.rightPanel, orient=tk.VERTICAL)
        self.rightPane.pack(fill=BOTH, expand=True)
        
        self.code = CodeView(self)
        self.tree = FileTreeView(self)
        self.console = ConsoleView(self)
        
        pixel = tk.PhotoImage(width=1, height=1)
        self.runButton = tk.Button(self.code.codeObject, text="▶", image=pixel, width=20, height=20, compound="c", command=self.run)
        self.runButton.pack(anchor=NE, padx=20, pady=23)
        
        self.rightPane.add(self.code.codeObject, weight=1)
        self.rightPane.add(self.console.frame)
        
        self.content.add(self.tree.treeObject)
        self.content.add(self.rightPanel, weight=1)
    
        self.menu = WindowMenu(self)
        self.root.config(menu=self.menu.menuObject)
        self.root.bind("<Control-o>", self.changeDir)                   
        
        """self.console.out("\n",
        "  _   _                 ____            _       _   \n",
        " | \\ | |_   _ _ __ ___ / ___|  ___ _ __(_)_ __ | |_ \n",
        " |  \\| | | | | '_ ` _ \\\\___ \\ / __| '__| | '_ \\| __|\n",
        " | |\\  | |_| | | | | | |___) | (__| |  | | |_) | |_ \n",
        " |_| \\_|\\__,_|_| |_| |_|____/ \\___|_|  |_| .__/ \\__|\n",
        "                                         |_|        "
        )"""
        self.root.mainloop()
    
    def run(self):
        """
        Runs the current python code in CodeView using exec().
        """
        exec(self.code.currentTab.get("1.0","end")[:-1].replace("print", "self.console.out").replace("input", "self.console.inp"))
    
    def changeDir(self, event=None, directory=None):
        """Changes the current working directory and refreshes FileTreeView.

        Args:
            event (tkinter.Event, optional): Event that called the function. Defaults to None.
            directory (str, optional): New working directory, if none, prompts the user with folder selection dialog. Defaults to None.
        """
        directory = fd.askdirectory(title="Select Directory") if not directory else self.directory
        self.directory = directory if directory != "" else self.directory
        self.tree.treeObject.delete(*self.tree.treeObject.get_children())
        self.tree.listDir()
    
    def openPreferences(self):
        """
        Open the preferences window.
        """
        pass
    
    def toggleConsole(self):
        """
        Hide or show the console.
        """
        if self.rightPane.index("end") == 1:
            self.rightPane.forget(self.console.consoleObject)
        else:
            self.rightPane.add(self.console.consoleObject)
        self.rightPane.update_idletasks()


MainWindow()

"""
if len(sys.argv) > 1: #File input from system arguments
    file = sys.argv[1].replace("\\","/")
    lines = [line.replace(" ","").rstrip() for line in open(file, encoding="utf-8").readlines() if line != "\n"]
    index = 1
    for i in lines:#Moves code from file to tokenized code
        tokenized_code.append(tokenizer(i))
        index+=1
    exe()#Runs the code
else: #Shell input from console
    while True:#Console loop

"""