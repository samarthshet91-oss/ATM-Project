import tkinter as tk
from tkinter import *
import subprocess
from PIL import Image, ImageTk

def run_backend(operation,acc_no,pin="",amount="0"):
    result = subprocess.run(["atm_backend.exe",operation,acc_no,pin,amount], capture_output=True, text=True)
    return result.stdout.strip()

def login():
    acc = acc_entry.get()
    pin = pin_entry.get()
    result = run_backend("login", acc, pin )

    if "success" in result.lower():
        global current_acc,current_pin
        current_acc = acc   
        current_pin = pin
        output_label.config(text="Login successful!.✅", fg="green")

        root.after(1000,show_atm_options,acc,pin)
    else:
        output_label.config(text="Invalid account number or PIN.❌", fg="red")



def show_atm_options(acc,pin):
    login_frame.pack_forget()
    atm_frame.pack(pady=10)
    global current_acc,current_pin
    current_acc = acc
    current_pin = pin

def show_result(message, color="white"):
    atm_frame.pack_forget()
    result_frame.pack(pady=50)
    result_label.config(text=message, fg=color)
    root.after(3000,back_to_menu_screen)

def back_to_menu_screen():
    result_frame.pack_forget()
    atm_frame.pack(pady=20)    

def logout():
    atm_frame.pack_forget()
    login_frame.pack(pady=20)
    output_label.config(text="Logged out",fg="yellow")

def disable_button():
    for widget in atm_frame.winfo_children():
        if isinstance(widget, Button):
            widget.config(state="disabled")

def enable_button():
    for widget in atm_frame.winfo_children():
        if isinstance(widget, Button):
            widget.config(state="normal")

def back_to_menu():
    output_label.config(text="Select an option", fg="cyan")
    enable_button()                           

def check_balance():
    result = run_backend("balance", current_acc, current_pin)
    show_result(f"Your current balance is: ${result}", "lightblue")

def deposit():
    amount = amount_entry.get()
    if amount=="":
        output_label.config(text="Enter amount first!", fg="red")
        return
    result = run_backend("deposit", current_acc, current_pin, amount)
    amount_entry.delete(0, END)
    show_result("Amount Deposited Successfully", "green")

def withdraw():
    amount = amount_entry.get()
    result = run_backend("withdraw", current_acc, current_pin, amount)
    if "Insufficient" in result:
        show_result(result, "red")
    else:
        show_result("Amount Withdrawn Successfully", "green")

def history():
    result = run_backend("history", current_acc, current_pin)
    if result =="":
        show_result("No transactions yet!", "yellow")
    else:
        show_result(f"Transaction History:\n{result}", "lightblue")

root = Tk()
root.title("ATM System")
root.geometry("800x600")
root.config(bg="#1e1e2f")
root.state("zoomed")

bg_img=Image.open("atm_bg.png.png")
bg_img = bg_img.resize((root.winfo_screenwidth(), root.winfo_screenheight()))
bg_photo = ImageTk.PhotoImage(bg_img)
bg_label = Label(root, image=bg_photo)
bg_label.place(x=0, y=0, relwidth=1, relheight=1)
bg_label.image = bg_photo


main_card = Frame(root, bg="#2c2f4a")
main_card.place(relx=0.5, rely=0.5, anchor="center", width=350, height=450)
main_card.lift()

Label(main_card, text="🏧ATM MACHINE", font=("Arial", 18,"bold"), bg="#2c2f4a", fg="white").pack(pady=20)
              
login_frame = Frame(main_card, bg="#2c2f4a")
login_frame.pack(pady=20)

Label(login_frame, text="Account Number:", font=("Arial", 12), bg="#2c2f4a", fg="white").grid(row=0, column=0, pady=10)
acc_entry=Entry(login_frame, font=("Arial", 12),justify="center")
acc_entry.grid(row=1, column=0, pady=5)

Label(login_frame, text="PIN:", font=("Arial", 12), bg="#2c2f4a", fg="white").grid(row=2, column=0, pady=10)
pin_entry=Entry(login_frame, font=("Arial", 12), show="*",justify="center")
pin_entry.grid(row=3, column=0, pady=5)

Button(login_frame, text="Login", font=("Arial", 12,"bold"),bg="#0be881",fg="black",width=15, command=login).grid(row=4, column=0, pady=20)  

output_label=Label(login_frame, text="", font=("Arial", 12), bg="#2c2f4a", fg="white")
output_label.grid(row=5, column=0, pady=10)
login_frame.pack(pady=20)

atm_frame = Frame(main_card, bg="#1e1e2f")
result_frame = Frame(main_card, bg="#1e1e2f")
result_label=Label(result_frame, text="Result will  appear here", font=("Arial", 14,"bold"), bg="#1e1e2f", fg="white")
result_label.pack(pady=50)

Label(atm_frame, text="Amount", font=("Arial", 16,"bold"), bg="#1e1e2f", fg="white").pack(pady=10)
amount_entry = Entry(atm_frame, font=("Arial", 12),justify="center")
amount_entry.pack(pady=5)

Button(atm_frame, text="📊Check Balance", font=("Arial", 12,"bold"), bg="#0be881", fg="black", width=20, command=check_balance).pack(pady=5)
Button(atm_frame, text="💰Deposit", font=("Arial", 12,"bold"), bg="#0be881", fg="black", width=20, command=deposit).pack(pady=5)
Button(atm_frame, text="💸Withdraw", font=("Arial", 12,"bold"), bg="#0be881", fg="black", width=20, command=withdraw).pack(pady=5)
Button(atm_frame, text="📜Transaction History", font=("Arial", 12,"bold"), bg="#0be881", fg="black", width=20, command=history).pack(pady=5)
Button(atm_frame, text="🔙Logout", font=("Arial", 12,"bold"), bg="orange", fg="white", width=20, command=lambda:(atm_frame.pack_forget(), login_frame.pack(pady=20))).pack(pady=5)

result_frame = Frame(main_card, bg="#1e1e2f")
result_label=Label(
result_frame, text="Result will  appear here", font=("Arial", 14,"bold"), bg="#1e1e2f", fg="white",wraplength=300, justify="center"
)
result_label.pack(pady=50)

root.mainloop()