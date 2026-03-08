import customtkinter as ctk
from tkinter import messagebox
import csv

PADDING_X=20
PADDING_Y=10

DEFAULT_ELEMENT_HEIGHT=80
DEFAULT_ELEMENT_WIDTH=800-2*PADDING_X

TEXT_FONT="Arial"
TEXT_FONT_SIZE=28

DATE_FONT="Arial"
DATE_FONT_SIZE=15

TEXT_COLOR="white"

class Ask_For_Text(ctk.CTkToplevel):
    def __init__(self, parent, default_task="", default_duedate="",title=""):
        super().__init__(parent)
        self.result=(default_task,default_duedate)
        self.grab_set()

        self.geometry("350x220")
        self.resizable(False, False)
        self.grid_columnconfigure(0, weight=1)

        title = ctk.CTkLabel(self,text=title,font=("Segoe UI", 20, "bold"))
        title.grid(row=0, column=0, pady=(20,10))

        self.task_entry = ctk.CTkEntry(self,placeholder_text="Enter task...",width=250)
        self.task_entry.insert(0, default_task)
        self.task_entry.grid(row=1, column=0, pady=10)

        self.date_entry = ctk.CTkEntry(self,placeholder_text="Due date (e.g. 25 Mar)",width=250)
        self.date_entry.insert(0, default_duedate)
        self.date_entry.grid(row=2, column=0, pady=10)

        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.grid(row=3, column=0, pady=20)

        cancel_btn = ctk.CTkButton(btn_frame,text="Cancel",width=100,command=self.destroy)
        cancel_btn.grid(row=0, column=0, padx=10)

        save_btn = ctk.CTkButton(btn_frame,text="Save",width=100,command=self.save_task)
        save_btn.grid(row=0, column=1, padx=10)

        self.task_entry.focus()

    def save_task(self):
        task = self.task_entry.get()
        due = self.date_entry.get()

        if not task:
            messagebox.showerror(' Task not identified Error',"Kindly enter a valid task to continue")
            return

        self.result=(task,due)
        self.destroy()
    

class Element(ctk.CTkFrame):
    def __init__(self,parent,task="",due_date=None,color="yellow", task_state=0):
        super().__init__(parent,height=DEFAULT_ELEMENT_HEIGHT,
                         width=DEFAULT_ELEMENT_WIDTH,fg_color=color)
        
        self.parent=parent
        self.duedate=due_date
        self.text=task
        
        self.rowconfigure(0,weight=1)
        self.rowconfigure(1,weight=0)
        self.rowconfigure(2,weight=0)

        self.columnconfigure(0,weight=1)
        self.columnconfigure(1,weight=0)
        self.columnconfigure(2,weight=0)

        self.text_box=ctk.CTkCheckBox(self,text=task.title(),
                                text_color=TEXT_COLOR,font=(TEXT_FONT,TEXT_FONT_SIZE),
                                command=self.update_font)
        self.text_box.grid(row=1,column=0)

        if task_state==1:
            self.text_box.select()
            self.text_box.configure(font=(TEXT_FONT,TEXT_FONT_SIZE,"overstrike"))

        self.date=ctk.CTkLabel(self,text=f"Due Date : {due_date}",
                          text_color=TEXT_COLOR,font=(DATE_FONT,DATE_FONT_SIZE))
        self.date.grid(row=2,column=0,sticky="w",padx=10,pady=10)

        delete_btn=ctk.CTkButton(self,text="🗑",fg_color="red",width=20,command=self.delete)
        delete_btn.grid(row=2,column=2,sticky="e",padx=5)

        edit_btn=ctk.CTkButton(self,text="Edit",fg_color="green",command=self.edit)
        edit_btn.grid(row=2,column=1,sticky="e",padx=5)

        self.pack(padx=PADDING_X,pady=PADDING_Y)
        self.grid_propagate(False)
    
    def edit(self):
        dialog=Ask_For_Text(self.parent,default_task=self.text,default_duedate=self.duedate,
                            title="Edit task")
        root.wait_window(dialog)

        task,duedate=dialog.result
        self.text_box.configure(text=task.title())
        self.date.configure(text=duedate)
    
    def delete(self):
        if messagebox.askyesno("Confirmation","Do you want to Delete the task ?"):
            self.destroy()
            tasks.remove(self)
    
    def update_font(self):
        font=(TEXT_FONT,TEXT_FONT_SIZE)
        if self.text_box.get():font=font+("overstrike",)

        self.text_box.configure(font=font)

def add_element():
    dialog=Ask_For_Text(main,title="Add a task ")
    root.wait_window(dialog)

    task,duedate=dialog.result
    if task:
        tasks.append(Element(main,task,duedate))

file=open("python/To do list.csv","r",newline="")

root=ctk.CTk()
root.title("To Do List creator")
root.geometry("800x600")
root.resizable(False, False)

main=ctk.CTkScrollableFrame(root)
main.pack(expand=True,fill="both")

tasks=[]

for row in csv.reader(file):
    if row:
        tasks.append(Element(main,task=row[0],due_date=row[1],task_state=row[2]))

add_button = ctk.CTkButton(root,text="+",width=80,height=60,corner_radius=15,
                           font=("Segoe UI", 30, "bold"),bg_color="transparent",
                           fg_color="#3B82F6",hover_color="#2563EB",border_width=0,
                           command=add_element)

add_button.place(relx=1.0, rely=1.0, anchor="se", x=-20, y=-20)

file.close()
root.mainloop()

with open("python/To do list.csv","w",newline="") as file:
    writer=csv.writer(file)
    for task in tasks:
        writer.writerow([task.text,task.duedate,task.text_box.get()])

