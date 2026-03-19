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
    
    showinfo(
    " Round Result",
    f"Computer chose: {computer_choice}\n\n{result}")
    score_label.configure(text=f"Score : {score} | Max Score : {max_score}")
    

root=ctk.CTk()

root.title("Rack Paper Scissor Game")
root.geometry("420x500")
root.resizable(False, False)

main_frame = ctk.CTkFrame(root, corner_radius=15)
main_frame.pack(padx=20, pady=20, fill="both", expand=True)

title_label = ctk.CTkLabel(
    main_frame,
    text="🎮 Rock Paper Scissors",
    font=("Arial", 26, "bold")
)
title_label.pack(pady=(10, 20))

score_label = ctk.CTkLabel(
    main_frame,
    text="Score: 0 | Max: 0",
    font=("Arial", 16)
)
score_label.pack()

button_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
button_frame.pack(pady=20)

for text in ["Rock","Paper","Scissor"]:
    btn = ctk.CTkButton(
    button_frame,
    text=f"✊ {text}",
    width=200,
    height=45,
    corner_radius=10,
    font=("Arial", 14, "bold"),
    command=lambda txt=text: check_condition(txt))

    btn.pack(pady=15)

root.mainloop()