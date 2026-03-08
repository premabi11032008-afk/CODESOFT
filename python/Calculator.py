import customtkinter as ctk
from tkinter import messagebox

BUTTON_HEIGHT=70
BUTTON_WIDTH=70

class Calculator(ctk.CTk):
    def __init__(self):
        super().__init__()

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("green")

        self.expression=""
        self.expression_label=""

        self.title("Calculator")
        self.geometry("450x550")
        self.resizable(False,False)

        display_frame = ctk.CTkFrame(self, fg_color="transparent")
        display_frame.pack(fill="x", padx=20, pady=20)

        self.second_label = ctk.CTkLabel(display_frame,text="",font=("Arial",18),anchor="e")
        self.second_label.pack(fill="x")

        self.result_label = ctk.CTkLabel(display_frame,text="0",font=("Arial",40,"bold"),anchor="e")
        self.result_label.pack(fill="x")

        btn_frame=ctk.CTkFrame(self)
        btn_frame.pack(expand=True, fill="both", padx=20, pady=10)

        btns=ctk.CTkFrame(btn_frame)
        btns.grid(row=0,column=0,columnspan=7)

        buttons=["7","8","9","-","%",
                 "4","5","6",'*',"/",
                 "1","2","3","(",")",
                 ".","0","+","^","AC"]
        
        for index in range(len(buttons)):

            if buttons[index] in "+-*/%^AC()":
                color = "#ff9500"
            else:
                color = None

            cmd=(lambda ind=index: self.press(buttons[ind])) if buttons[index]!="AC" else self.all_clear

            btn=ctk.CTkButton(btns,width=BUTTON_WIDTH,height=BUTTON_HEIGHT,
                              command=cmd,text=buttons[index],fg_color=color)
            btn.grid(row=index//5, column=index%5, padx=5, pady=5, sticky="nsew")
        
        eql_btn=ctk.CTkButton(btn_frame,text="=",command=self.evaluate,
                              height=BUTTON_HEIGHT,width=BUTTON_WIDTH,fg_color="#2ecc71",font=("Arial",20,"bold"))
        eql_btn.grid(row=1,column=0,columnspan=5,sticky="nswe")

        back = ctk.CTkButton(btn_frame,text="⌫",command=self.backspace,fg_color="red")
        back.grid(row=1,column=6,sticky="nsew")

        self.bind("<Return>", lambda e: self.evaluate())
        self.bind("<BackSpace>", lambda e: self.backspace())
        self.bind("<Escape>", lambda e: self.clear())

        for i in range(5):
            btns.grid_columnconfigure(i, weight=1)

        for i in range(4):
            btns.grid_rowconfigure(i, weight=1)

        for key in "0123456789+-*/().%":
            self.bind(key, lambda e, k=key: self.press(k))
    
    def press(self,value):

        self.expression_label=""
        self.update_second_label()

        if value==".":

            if not self.expression:
                self.expression="0."
                self.update()
                return
            
            if self.expression[-1]==".":
                return
            
            if not self.expression[-1].isdigit():
                self.expression+="0."
                self.update()
                return
            
        if not self.expression:
            self.expression+=value
            self.update()
            return

        if self.expression[-1].isdigit() or self.expression[-1]==".":
            self.expression+=value
            self.update()
        else:
            if value.isdigit() or value==".":
                self.expression+=value
                self.update()
                return 
            
            self.expression=self.expression[:-1]+value
            self.update()
    
    def update_second_label(self):
        self.second_label.configure(text=self.expression_label)
    
    def update(self):
        self.result_label.configure(text=self.expression)
    
    def backspace(self):

        self.expression_label=""
        self.update_second_label()

        if self.expression:
            self.expression=self.expression[:-1]
            self.update()
    
    def evaluate(self):
        self.expression=self.expression.replace("^","**")

        count_open_parathesis=0
        count_closed_parathesis=0
        index=0

        while index<len(self.expression):

            if self.expression[index]=="(":
                count_open_parathesis+=1
                add=0

                if index+1==len(self.expression) or not self.expression[index+1].isdigit():
                    self.expression+="1"
                    add+=1
                
                if index-1>=0 and self.expression[index-1].isdigit():
                    self.expression=self.expression[:index]+"*"+self.expression[index:]
                    add+=1
                
                index+=add
                
            
            if self.expression[index]==")":
                count_closed_parathesis+=1
                if index+1>=len(self.expression):
                    index+=1
                    continue
                
                if self.expression[index+1].isdigit():
                    self.expression=self.expression[:index]+"*"+self.expression[index:]
                    index+=1

            index+=1
        
        if count_open_parathesis>count_closed_parathesis:
            self.expression+=")"*(count_open_parathesis-count_closed_parathesis)
        
        try:
            self.expression_label=self.expression+"="
            self.update_second_label()
            self.expression=str(eval(self.expression))
            self.update()

        except Exception as e:
            messagebox.showerror("Error",str(e))
            self.all_clear()

    
    def all_clear(self):

        self.expression_label=""
        self.update_second_label()

        self.expression=""
        self.update()

    def run(self):
        self.mainloop()

if __name__=="__main__":
    calculator=Calculator()
    calculator.run()