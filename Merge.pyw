import tkinter as tk
from tkinter.filedialog import askopenfilename, asksaveasfilename
from PyPDF2 import PdfFileMerger, PdfFileReader

class MergerGUI:
    
    MAIN_FONT = "helvetica 11 bold"
    LIST_FONT = "helvetica 10 bold"
    COLOR = "#DBECEE"

    def __init__(self, root):
        
        '''
        GUI initialization
        '''

        self.root = root
        self.root.title("PDF Merger")
        self.root.resizable(False, False)
        self.root.option_add("*Font", MergerGUI.MAIN_FONT)
        self.root.option_add("*Background", MergerGUI.COLOR)
        self.root.config(bg=MergerGUI.COLOR)

        screenW = root.winfo_screenwidth()
        screenH = root.winfo_screenheight()
        windowW = root.winfo_reqwidth()
        windowH = root.winfo_reqheight()
		
        positionR = int((screenW - windowW) / 2)
        positionD = int((screenH - windowH) / 2)
        root.geometry("+{}+{}".format(positionR, positionD))

        self.upButton = tk.Button(text="\u2b9d", command=self.swapUp)
        self.upButton.grid(row=0, column=3, columnspan=1, sticky='nsew')

        self.downButton = tk.Button(text="\u2b9f", command=self.swapDown)
        self.downButton.grid(row=1, column=3, columnspan=1, sticky='nsew')

        self.fileList = tk.Listbox(root, width=0, height=0, selectmode='extended', font=MergerGUI.LIST_FONT)
        self.fileList.grid(row=0, column=0, rowspan=2, columnspan=3, sticky="nsew")

        self.addButton = tk.Button(root, text="Add File", command=self.add)
        self.addButton.grid(row=2, column=0, columnspan=2, sticky="nswe")

        self.removeButton = tk.Button(root, text="Remove File", command=self.remove)
        self.removeButton.grid(row=2, column=2, columnspan=2, sticky="nswe")

        self.mergeButton = tk.Button(root, text="Merge Files", command=self.merge)
        self.mergeButton.grid(row=3, columnspan=4, sticky="nswe")
		

    # Add a file to merge
    def add(self):
        self.root.update()
        file = askopenfilename()
        if file != "":
            if not self.isPDF(file):
                return
            else:
                self.fileList.insert(self.fileList.size() + 1, file)

    # Remove a file to merge
    def remove(self):
        selected = [int(selection) for selection in self.fileList.curselection()[-1::-1]]
        for index in selected:
            self.fileList.delete(index)
        for selection in selected:
            if selection < self.fileList.size():
                self.fileList.selection_set(selection)

    # Swap the order of two files to merge
    def swap(self, dir):
        if dir == -1:
            selected = [int(selection) for selection in self.fileList.curselection()][-1::-1]
        else:
            selected = [int(selection) for selection in self.fileList.curselection()]
        if ((0 in selected and dir == 1) or (self.fileList.size() - 1 in selected and dir == -1)):
            return
        newSelect = []
        for index in selected:
            neighbor = index - dir
            i, n = self.fileList.get(index), self.fileList.get(neighbor)
            self.fileList.delete(index), self.fileList.insert(index, n)
            self.fileList.delete(neighbor), self.fileList.insert(neighbor, i)
            newSelect.append(neighbor)
        for selection in newSelect:
            self.fileList.selection_set(selection)
    
    # Move a file up the queue
    def swapUp(self):
        self.swap(1)

    # Move a file down the queue and save to the specified file name
    def swapDown(self):
        self.swap(-1)
    
    # Merge the selected files
    def merge(self):
        merger = PdfFileMerger()
        files = self.fileList.get(0, self.fileList.size())
        for file in files:
            with open(file, 'rb') as f:
                merger.append(PdfFileReader(f))
            f.close()
        self.root.update()
        destination = asksaveasfilename()
        if destination == "":
            return
        else:
            if not self.isPDF(destination):
                destination += ".pdf"
            merger.write(destination)
    
    # Return true if the file name is a PDF
    def isPDF(self, filename):
        return filename[-4:] == ".pdf"

if __name__ == '__main__':
    root = tk.Tk()
    MergeGUI = MergerGUI(root)
    root.mainloop()
