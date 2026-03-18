import customtkinter as ctk
from tkinter.messagebox import showerror,showinfo
import random as rd

def animate_password(text, index=0):

    print('[info] enter animate_password method')

    if index <= len(text):
        result_entry.configure(state="normal")
        result_entry.delete(0, "end")
        result_entry.insert(0, text[:index])
        result_entry.configure(state="readonly")

        root.after(30, animate_password, text, index+1)

def copy_password():
    print("[info] entered copy_password method")
    root.clipboard_clear()
    root.clipboard_append(result_entry.get())
    copy_button.configure(text="Copied ✓", fg_color="#2ecc71")
    root.after(1500, lambda: copy_button.configure(text="Copy", fg_color="#1f6aa5"))

def generate_passward():
    global result_entry

    print("[info]: entered generate password method")

    vocab=""
    alphabets="abcdefghijklmnopqrstuvwxyz"

    vocab+="~`!@#$%^&*()/*-+;./,<>?0[]" if special_charater_needed.get() else ""
    vocab+=alphabets.upper() if upercase_needed.get() else ""
    vocab+=alphabets if lowercase_needed.get() else ""
    vocab+="0123456789" if number_needed.get() else ""

    if vocab=="":
        showerror("error","choose a feild/feilds for password")
        return
    
    try:
        entry=entry_box.get()

        if not entry:
            showinfo("Info","Pls enter the password lenght")
            return
        
        password_len=int(entry)
    
    except Exception as e:
        showerror("Error",str(e))
        return 
    
    password = []
    
    while len(password)<password_len:
        password.append(rd.choice(vocab))

    rd.shuffle(password)
    password = "".join(password)
    animate_password(password)
    flash_entry()

def flash_entry(count=0):
    colors = ["#2ecc71", "#27ae60"]  

    result_entry.configure(border_color=colors[count % 2])

    if count < 4:
        root.after(100, flash_entry, count+1)
    else:
        result_entry.configure(border_color="#444")

def create_checkbox(frame,text):
    btn=ctk.CTkCheckBox(frame,
                        text=text.title())
    btn.select()
    btn.pack(padx=10,pady=5,anchor='w')

    return btn

root=ctk.CTk()
root.geometry("600x600")
root.resizable(False,False)

main_frame=ctk.CTkFrame(root,400,400)
main_frame.pack(padx=50, pady=50, fill="both", expand=True)

main_frame.pack_propagate(False)

entry_frame=ctk.CTkFrame(main_frame,height=100,width=400)
entry_frame.pack(padx=10,pady=10)

entry_frame.pack_propagate(False)

entry_label=ctk.CTkLabel(entry_frame,100,30,20,text="Enter the number of characters:",font=("Arial",18))
entry_label.pack(pady=10,anchor="w",padx=10)

entry_box=ctk.CTkEntry(entry_frame,100,30)
entry_box.pack(pady=5,padx=30)

special_charater_needed=create_checkbox(main_frame,"Include special characters ")
number_needed=create_checkbox(main_frame,text="Include Numbers")
upercase_needed=create_checkbox(main_frame,text="Incude Uppercase letters")
lowercase_needed=create_checkbox(main_frame,text="Incude Lower case letters")

submit_button=submit_button = ctk.CTkButton(
    main_frame,
    text="Generate Password",
    fg_color="#ff4d4d",
    hover_color="#cc0000",
    command=generate_passward
)
submit_button.pack(pady=50,padx=10)


def on_press():
    submit_button.configure(scale=0.95)

def on_release():
    submit_button.configure(scale=1)

submit_button.bind("<ButtonPress>", lambda e: on_press())
submit_button.bind("<ButtonRelease>", lambda e: on_release())

result_frame = ctk.CTkFrame(main_frame)
result_frame.pack(pady=10, padx=10, fill="x")

result_entry = ctk.CTkEntry(result_frame, font=("Arial", 16))
result_entry.pack(side="left", fill="x", expand=True, padx=5, pady=5)

copy_button = ctk.CTkButton(result_frame, text="Copy", width=80,command=copy_password)
copy_button.pack(side="right", padx=5)

root.mainloop()