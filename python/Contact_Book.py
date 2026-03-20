import customtkinter as ctk
from tkinter.messagebox import showerror,askyesno
import csv

class Ask_For_Text(ctk.CTkToplevel):
    def __init__(self, parent,title,default_name='',default_number=''):
        super().__init__(parent)
        self.result=(default_name,default_number)
        self.grab_set()

        self.geometry("350x300")
        self.resizable(False, False)
        self.grid_columnconfigure(0, weight=1)

        title = ctk.CTkLabel(self,text=title,font=("Segoe UI", 20, "bold"))
        title.grid(row=0, column=0, pady=(20,10))

        name_label = ctk.CTkLabel(self, text="Name", anchor="w")
        name_label.grid(row=1, column=0, sticky="w", padx=50)

        self.name_entry = ctk.CTkEntry(self,placeholder_text="Enter Name..",width=250)
        self.name_entry.grid(row=2, column=0, pady=10)

        if default_name:
            self.name_entry.insert(0,default_name)

        phone_label = ctk.CTkLabel(self, text="Phone Number", anchor="w")
        phone_label.grid(row=3, column=0, sticky="w", padx=50)

        self.number_entry = ctk.CTkEntry(self,placeholder_text="Enter a Phone Number",width=250)
        self.number_entry.grid(row=4, column=0, pady=10)

        if default_number:
            self.number_entry.insert(0,default_number)

        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.grid(row=5, column=0, pady=20)

        cancel_btn = ctk.CTkButton(btn_frame,text="Cancel",width=100,command=self.destroy)
        cancel_btn.grid(row=0, column=0, padx=10)

        save_btn = ctk.CTkButton(btn_frame,text="Save",width=100,command=self.save_task)
        save_btn.grid(row=0, column=1, padx=10)

    def save_task(self):
        name = self.name_entry.get().strip().title()
        number = self.number_entry.get().strip()

        self.result=(name,number)
        self.destroy()
    

class Element(ctk.CTkFrame):
    def __init__(self,parent ,name: str, phone_number : str):

        super().__init__(master=parent,width=500,height=100,corner_radius=20,fg_color="#1E293B")
        self.parent=parent
        self.name=name
        self.number=phone_number

        if phone_number.isdigit() and len(phone_number) < 9:
            showerror("Invalid Phone Number","Phone number cannot be digit or less than 9")
            return
        
        if not name:
            showerror(' Name not identified Error',"Kindly enter a Name task to continue")
            return

        self.name_label=ctk.CTkLabel(self,text=f"Name : {name.title()} | Phone : {phone_number}",
                          text_color="#94A3B8",font=("Segoe UI",18),width=400)
        self.name_label.grid(row=0,column=0,sticky="nswe",padx=10,pady=10)

        delete_btn=ctk.CTkButton(self,text="🗑",fg_color="#EF4444",
                                 hover_color="#DC2626",width=20,command=self.delete)
        delete_btn.grid(row=1,column=1,sticky="e",padx=5)

        edit_btn=ctk.CTkButton(self,text="Edit",fg_color="#10B981",
                               hover_color="#059669",command=self.update)
        edit_btn.grid(row=1,column=0,sticky="e",padx=5)

        self.pack(padx=10,pady=10)
        self.grid_propagate(False)
        self.show()
    
    def update(self):
        window=Ask_For_Text(self.parent,"Update the existing Contact",self.name,self.number)

        self.parent.wait_window(window)
        name,phone_number=window.result
        
        self.name_label.configure(text=f"Name : {name} | Phone : {phone_number}")
    
    def delete(self):
        Contact_Book.pop(self.name.lower())
        ELEMENTS.remove(self)
        self.destroy()
    
    def show(self):
        self.pack(padx=10,pady=10)
    
    def hide(self):
        self.pack_forget()

def fectch_the_corrsponding_element(name = "" ,number = "") -> Element|int:
    for element in ELEMENTS:
        if element.name.lower() == name:
            return element

        if element.number==number:
            return element
     
    return -1

def add_element():
    dialog=Ask_For_Text(root,title="Add a task ")
    root.wait_window(dialog)

    name,phone_number=dialog.result
   
    if (not phone_number.isdigit()) or (len(phone_number) < 9):
        showerror("Invalid Phone Number","Phone number cannot be digit or less than 9")
        return
        
    if not name:
        showerror(' Name not identified Error',"Kindly enter a Name task to continue")
        return

    name=name.lower()

    if name in Contact_Book :
        if Contact_Book[name]!=phone_number and askyesno("Confirmation","The Name already exists do you want to \n Replace ?"):
            element=fectch_the_corrsponding_element(name=name)
            if element!=-1:
                element.name_label.configure(text=f" Name : {name} | Phone : {phone_number}")
        
        if Contact_Book[name]==phone_number:
            return
    else:
        Contact_Book[name]=phone_number
        ELEMENTS.append(Element(root,name=name,phone_number=phone_number))

def search(event=None):
    entry=Search_bar.get().strip().lower()

    if len(entry)==0:
        reset()

    if entry.isdigit():
        for number in Contact_Book.values():
            if entry not in number:
                element=fectch_the_corrsponding_element(name=name)
                if element!=-1:
                    element.hide()

    
    else:
        for name in Contact_Book.keys():
            if entry not in name:
                element=fectch_the_corrsponding_element(name=name)
                if element!=-1:
                    element.hide()

def reset():
    Search_bar.delete(0,len(Search_bar.get().strip()))
    for element in ELEMENTS:
            element.show()


main_frame=ctk.CTk()
main_frame.geometry("600x500")
main_frame.title("Phone Book")

Search_Bar_Frame=ctk.CTkFrame(main_frame,height=30)
Search_Bar_Frame.pack(pady=5,padx=10,fill="both")

Search_bar = ctk.CTkEntry(Search_Bar_Frame,width=300,placeholder_text="Enter a Name or Phone Number")
Search_bar.pack(padx=10,pady=5,fill="both",side="left")

Search_bar.bind("<KeyRelease>",search)

Search_btn = ctk.CTkButton(Search_Bar_Frame,text="Search",command=search)
Search_btn.pack(padx=10,pady=5,fill="both",side="left")

Search_btn = ctk.CTkButton(Search_Bar_Frame,text="Reset",command=reset)
Search_btn.pack(padx=10,pady=5,fill="both",side="left")

root=ctk.CTkScrollableFrame(main_frame,orientation="vertical")
root.pack(expand=True,fill="both")

ELEMENTS=[]

with open("Contact Book.csv","a+",newline="") as file:
    file.seek(0)
    reader=list(csv.reader(file))

    Contact_Book={}

    for row in reader:
        if row:
            Contact_Book[row[0].lower()]=row[1]
            ELEMENTS.append(Element(root,row[0],row[1]))

add_button = ctk.CTkButton(main_frame,text="+",width=80,height=60,corner_radius=15,
                           font=("Segoe UI", 30, "bold"),bg_color="transparent",
                           fg_color="#3B82F6",hover_color="#2563EB",border_width=0,
                           command=add_element)

add_button.place(relx=1.0, rely=1.0, anchor="se", x=-20, y=-20)

main_frame.mainloop()

with open("Contact Book.csv","w") as file:
    writer=csv.writer(file)
    for contact in ELEMENTS:
        writer.writerow([contact.name,contact.number])

        

        
