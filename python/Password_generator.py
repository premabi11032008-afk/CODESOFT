import customtkinter as ctk
from tkinter.messagebox import showerror,showinfo
import random as rd

def update_length(value):
    length_label.configure(text=f"Length: {int(value)}")

show_password = False

def toggle_password():
    global show_password
    show_password = not show_password

    if show_password:
        result_entry.configure(show="")
        eye_button.configure(text="🙈")  
    else:
        result_entry.configure(show="*")
        eye_button.configure(text="👁️")  

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
    
    password_len = int(length_slider.get())
    
    password = []
    
    while len(password)<password_len:
        password.append(rd.choice(vocab))

    rd.shuffle(password)
    password = "".join(password)
    animate_password(password)

def create_checkbox(frame,text):
    btn=ctk.CTkCheckBox(frame,
                        text=text.title())
    btn.select()
    btn.pack(padx=10,pady=5,anchor='w')

    return btn

root=ctk.CTk()
root.geometry("600x600")
root.resizable(False,False)

main_frame=ctk.CTkFrame(root,400,400,fg_color="#111827",corner_radius=20,
    border_width=1,
    border_color="#1f2937")
main_frame.pack(padx=50, pady=50, fill="both", expand=True)

main_frame.pack_propagate(False)

title_label = ctk.CTkLabel(
    main_frame,
    text="Password Generator",
    font=("Arial", 24, "bold"),
    text_color="#e5e7eb"
)
title_label.pack(pady=(10, 20))

controls_frame = ctk.CTkFrame(main_frame, fg_color="#020617")
controls_frame.pack(padx=20, pady=10, fill="x")

length_slider = ctk.CTkSlider(controls_frame, from_=4, to=100, number_of_steps=100,command=update_length)
length_slider.set(10)
length_slider.pack(pady=(0, 10), padx=20, fill="x")

length_label = ctk.CTkLabel(controls_frame, text="Length: 12", font=("Arial", 14))
length_label.pack()

special_charater_needed=create_checkbox(controls_frame,"Include special characters ")
number_needed=create_checkbox(controls_frame,text="Include Numbers")
upercase_needed=create_checkbox(controls_frame,text="Incude Uppercase letters")
lowercase_needed=create_checkbox(controls_frame,text="Incude Lower case letters")

submit_button=submit_button = ctk.CTkButton(
    main_frame,
    text="Generate Password",
    fg_color="#22c55e",
    hover_color="#16a34a",
    text_color="black",
    command=generate_passward
)
submit_button.pack(pady=30,padx=10)

result_frame = ctk.CTkFrame(main_frame)
result_frame.pack(pady=20, padx=10, fill="x")

result_entry = ctk.CTkEntry(result_frame, font=("Arial", 16), fg_color="#020617",
    border_color="#22c55e",
    text_color="#22c55e",
    show="*")
result_entry.pack(side="left", fill="x", expand=True, padx=5, pady=5)

eye_button = ctk.CTkButton(result_frame, text="👁️", width=50,  fg_color="#111827",
    hover_color="#1f2937",command=toggle_password)
eye_button.pack(side="right", padx=5)

copy_button = ctk.CTkButton(result_frame, text="Copy", width=80,command=copy_password,
    fg_color="#38bdf8",
    hover_color="#0ea5e9",
    text_color="black"
)
copy_button.pack(side="right", padx=5)


root.mainloop()