from tkinter import *
from tkinter import messagebox
from random import randint, choice, shuffle
import pyperclip
import json


# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def password_generator():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
               'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_letters = [choice(letters) for _ in range(randint(8, 10))]
    password_symbols = [choice(symbols) for _ in range(randint(2, 4))]
    password_numbers = [choice(numbers) for _ in range(randint(2, 4))]

    password_list = password_letters + password_symbols + password_numbers
    shuffle(password_list)

    password = "".join(password_list)
    password_text_box.insert(0, f"{password}")
    pyperclip.copy(password)


# ---------------------------- SAVE PASSWORD ------------------------------- #
def save():
    website = website_text_box.get()
    email = email_text_box.get()
    password = password_text_box.get()
    new_data = {
        website: {
            "email": email,
            "password": password
        }
    }
    # text = f"{website} | {email} | {password}\n"

    if len(website) == 0 or len(password) == 0:
        messagebox.showinfo(title="Oops", message="Please don't leave any fields empty!")
    else:
        is_ok = messagebox.askokcancel(title=website, message=f"These are the details entered: \nEmail: {email} "
                                                              f"\nPassword: {password}\n Is it ok to save?")
        if is_ok:
            try:
                with open("data_entry.json", "r") as file:
                    # Reading old data
                    data = json.load(file)
            except FileNotFoundError:
                with open("data_entry.json", "w") as file:
                    json.dump(new_data, file, indent=4)
            else:
                # Updating old data
                data.update(new_data)

                with open("data_entry.json", "w") as file:
                    json.dump(data, file, indent=4)
            finally:
                website_text_box.delete(0, END)
                password_text_box.delete(0, END)


# ---------------------------- Search website password ------------------------------- #
def find_password():
    website = website_text_box.get()
    try:
        with open("data_entry.json", "r") as file:
            data_search = json.load(file)
    except FileNotFoundError:
        messagebox.showinfo(title="Oops", message="No Data File Found.")
    else:
        if website in data_search:
            email = data_search[website]["email"]
            password = data_search[website]["password"]
            messagebox.showinfo(title=f"{website}", message=f"Email/Username: {email}\n Password: {password}")
        else:
            messagebox.showinfo(title="Error", message=f"No details for {website} exists.")


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Password Manager")
window.config(padx=20, pady=20)

canvas = Canvas(width=200, height=200)
lock_img = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=lock_img)
canvas.grid(row=0, column=1)

# Labels
website_label = Label(text="Website :")
website_label.grid(row=1, column=0)

email_label = Label(text="Email/Username :")
email_label.grid(row=2, column=0)

password_label = Label(text="Password :")
password_label.grid(row=3, column=0)

# Entry
website_text_box = Entry(width=32)
website_text_box.grid(row=1, column=1)
website_text_box.focus()

email_text_box = Entry(width=51)
email_text_box.grid(row=2, column=1, columnspan=2)
email_text_box.insert(0, "tharish3547@gmail.com")

password_text_box = Entry(width=32)
password_text_box.grid(row=3, column=1)

# Buttons
search_button = Button(text="Search", command=find_password, width=14)
search_button.grid(row=1, column=2)

password_generator_button = Button(text="Generate Password", command=password_generator)
password_generator_button.grid(row=3, column=2)

add_button = Button(text="Add", width=44, command=save)
add_button.grid(row=4, column=1, columnspan=2)

window.mainloop()
