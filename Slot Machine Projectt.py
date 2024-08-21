from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
import mysql.connector as sql
import random

# Database connection setup
conn = sql.connect(host='localhost', user='root', passwd='charansingh', database='python')
c1 = conn.cursor()

# Initialize main window
ws = Tk()
ws.geometry('400x300')
ws.title('PythonGuides')

# Image background for the main page
image = Image.open(r"C:\Users\Charan singh\Desktop\DAILY\PERSONAL PROJECT\image1.png")
bg = ImageTk.PhotoImage(image)
background_label = Label(ws, image=bg)
background_label.place(relwidth=1, relheight=1)

f = ("Times bold", 14)

def show_how_to_play_page():
    ws_how_to_play = Tk()
    ws_how_to_play.geometry('600x400')
    ws_how_to_play.title('PythonGuides')
    ws_how_to_play['bg'] = '#ffbf00'

    f = ("Times bold", 18)
    g = ("Times bold", 14)

    def show_registration_from_how_to_play():
        ws_how_to_play.destroy()
        show_registration_page()

    Label(
        ws_how_to_play,
        text="RULES!!",
        padx=10,
        pady=10,
        font=f
    ).pack(expand=True, anchor="center", pady=(10, 10))

    Label(
        ws_how_to_play,
        text="""You will deposit some money into it and then click on spin button.
        If two symbols match, your amount is doubled. If all three match,
        your bet is ten times. If none match, you lose everything.""",
        padx=20,
        pady=20,
        bg='#ffbf00',
        font=g
    ).pack(expand=True, fill=BOTH)

    Button(
        ws_how_to_play,
        text="CONTINUE TO REGISTRATION",
        font=f,
        command=show_registration_from_how_to_play
    ).pack(fill=X, expand=True, side=LEFT)

    ws_how_to_play.mainloop()

def show_registration_page():
    ws_registration = Tk()
    ws_registration.geometry('400x300')
    ws_registration.title('Registration Form')
    ws_registration['bg'] = '#CCCCCC'

    f = ("Times bold", 14)
    global total_amount
    total_amount = 0

    def deposit():
        name = name_entry.get()
        contact = contact_entry.get()
        amount = amount_entry.get()

        if amount.isdigit():
            amount = int(amount)
        else:
            messagebox.showerror("Error", "Enter a valid amount!")
            return

        if amount <= 0:
            messagebox.showerror("Error", "Entered amount should be greater than zero!")
            return

        input_data(name, contact, amount)
        messagebox.showinfo("Deposit Successful", "You can now continue to the game.")

    def next_page():
        global total_amount
        amount=amount_entry.get()
        if not amount.isdigit() or int(amount)<=0:
            messagebox.showerror("Error","Please Enter A Valid Amount")
            return
        ws_registration.withdraw()
        total_amount += int(amount_entry.get())
        show_game_page(name_entry.get())

    def input_data(name, contact, amount):
        insert_query_user = "INSERT INTO user (name, contact, deposited) VALUES (%s, %s, %s)"
        user_data = (name, contact, amount)
        c1.execute(insert_query_user, user_data)
        conn.commit()

    deposit_frame = Frame(ws_registration)
    deposit_frame.pack(pady=10)

    name_label = Label(deposit_frame, text="Name:")
    name_label.grid(row=1, column=0, pady=10)

    name_entry = Entry(deposit_frame)
    name_entry.grid(row=1, column=1, padx=10)

    contact_label = Label(deposit_frame, text="Contact:")
    contact_label.grid(row=3, column=0, pady=20)

    contact_entry = Entry(deposit_frame)
    contact_entry.grid(row=3, column=1, pady=20)

    amount_label = Label(deposit_frame, text="Amount:")
    amount_label.grid(row=7, column=0, pady=20)

    amount_entry = Entry(deposit_frame)
    amount_entry.grid(row=7, column=1, pady=20)

    deposit_button = Button(deposit_frame, text="Deposit", command=deposit)
    deposit_button.grid(row=9, columnspan=2, pady=10)

    continue_button = Button(ws_registration, text="CONTINUE TO GAME", font=f, command=next_page)
    continue_button.pack(fill=X, expand=True, side=BOTTOM)

    ws_registration.mainloop()

def show_game_page(player_name):
    global total_amount

    def reveal_text(button, label):
        ab = ["❤️", "♠️", "♦️"]
        x = random.choice(ab)
        if label.cget("text") == "":
            label.config(text=x)
            button.config(text=x)
        else:
            label.config(text="")
            button.config(text="Reveal Text")

    def spin():
        global total_amount

        emoji_symbols = ["❤️", "♠️", "♦️"]
        chosen_symbols = [random.choice(emoji_symbols) for _ in range(3)]

        button1.config(text=chosen_symbols[0])
        button2.config(text=chosen_symbols[1])
        button3.config(text=chosen_symbols[2])

        if chosen_symbols[0] == chosen_symbols[1] == chosen_symbols[2]:
            total_amount *= 10
            messagebox.showinfo("Congratulations!", f"All three symbols match! Your new total amount is {total_amount}.")
        elif chosen_symbols[0] == chosen_symbols[1] or chosen_symbols[1] == chosen_symbols[2] or chosen_symbols[0] == chosen_symbols[2]:
            total_amount *= 2
            messagebox.showinfo("Congratulations!", f"Two symbols match! Your new total amount is {total_amount}.")
        else:
            total_amount = 0
            messagebox.showinfo("You Lost Everything", "You lost all your amount.")

        update_query = "UPDATE user SET deposited = %s WHERE name = %s"
        c1.execute(update_query, (total_amount, player_name))
        conn.commit()

        messagebox.showinfo("Total Amount", f"Total amount left: {total_amount}")

        spin_again = messagebox.askyesno("Spin Again", "Do you want to spin again?")
        if not spin_again:
            root.destroy()

    root = Tk()
    root.title("Slot Machine")
    root.geometry("700x400")
    root.configure(background="seagreen")

    intro = """Welcome to the game...
    Click on the buttons to reveal the symbols. If all three symbols are the same, your bet will be doubled."""

    nameLabel = Label(root, text="SLOT MACHINE", font=('Cambria', 60))
    nameLabel.pack()
    lbl = Label(root, text=intro, background='seagreen', font=('Cambria', 12))
    lbl.pack()

    button_frame = Frame(root)
    button_frame.pack(pady=30)

    label = Label(root, text="", font=("Arial", 20), bg="red")
    label.pack()

    button1 = Button(button_frame, text="Reveal Text", command=lambda: reveal_text(button1, label), width=17, height=5, bg="red")
    button1.pack(side="left", padx=15)

    button2 = Button(button_frame, text="Reveal Text", command=lambda: reveal_text(button2, label), width=17, height=5, bg="red")
    button2.pack(side="left", padx=15)

    button3 = Button(button_frame, text="Reveal Text", command=lambda: reveal_text(button3, label), width=17, height=5, bg="red")
    button3.pack(side="left", padx=15)

    spin_button = Button(root, text="SPIN", command=spin, width=20, height=2, bg="green")
    spin_button.pack(pady=20)

    root.mainloop()

def show_how_to_play():
    ws.destroy()
    show_how_to_play_page()

def show_registration():
    ws.destroy()
    show_registration_page()

Label(
    ws,
    text="SLOT MACHINE!!!!",
    padx=10,
    pady=10,
    font=f
).place(relx=0.5, rely=0.05, anchor="center")

Button(
    ws,
    text=" HOW TO PLAY",
    font=f,
    command=show_how_to_play
).place(relx=0.1, rely=0.99, anchor="sw")

Button(
    ws,
    text="REGISTRATION",
    font=f,
    command=show_registration
).place(relx=0.9, rely=0.99, anchor="se")

ws.mainloop()
