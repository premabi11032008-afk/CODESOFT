import customtkinter as ctk
import random as rd
from tkinter.messagebox import showinfo

win_conditions={"Rock":"Scissor","Scissor":"Paper","Paper":"Rock"}
score,max_score=0,0

def check_condition(text:str)-> None:
    global score , max_score

    computer_choice=rd.choice(["Rock","Paper","Scissor"]) 

    if win_conditions[computer_choice]==text:
        result="Computer won ! No worry you will get next time"
        score=0
    
    elif win_conditions[text]==computer_choice:
        result=" You won Horray ! "

        score+=1
        max_score=max(score,max_score)
    
    else:
        result=" Game ends in Draw ."
    
    showinfo("Round Result",f"""
             
Computer Choosed : {computer_choice}

"""+result)
    score_label.configure(text=f"Score : {score}")
    max_score_label.configure(text=f" Max Score : {max_score}")
    

root=ctk.CTk()
root.title("Rack Paper Scissor Game")
root.geometry("400x400")

title_label = ctk.CTkLabel(
    root,
    text="Rock Paper Scissor Game ",
    font=("Arial", 24, "bold"),
    text_color="#e5e7eb"
)
title_label.pack(pady=(10, 20))

max_score_label = ctk.CTkLabel(
    root,
    text="Max Score : 0",
    font=("Arial", 14),
    text_color="#e5e7eb"
)
max_score_label.pack(pady=5)

score_label = ctk.CTkLabel(
    root,
    text="Score : 0",
    font=("Arial", 14),
    text_color="#e5e7eb"
)
score_label.pack(pady=5)

for text in ["Rock","Paper","Scissor"]:
    btn=ctk.CTkButton(root,text=text,command=lambda txt=text : check_condition(txt))
    btn.pack(pady=15)

root.mainloop()