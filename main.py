from tkinter import *
from tkinter import messagebox
from random import randint, shuffle, choice
import pyperclip
import json


# ---------------------------- PASSWORD GENERATOR ------------------------------- #

def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v',
               'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q',
               'R',
               'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    pass_letters = [choice(letters) for letter in range(randint(8, 10))]
    pass_numbers = [choice(numbers) for number in range(randint(2, 4))]
    pass_symbols = [choice(symbols) for symbol in range(randint(2, 4))]

    password_list = pass_letters + pass_symbols + pass_numbers
    shuffle(password_list)
    password = ''.join(password_list)
    password_entry.insert(0, password)
    pyperclip.copy(password)
    messagebox.showinfo(title='Info', message='Password copied to clipboard!')


# ---------------------------- SAVE PASSWORD ------------------------------- #

def save():
    website = website_entry.get().lower()
    password = password_entry.get()
    email = username_entry.get()
    new_data = {
        website: {
            'email': email,
            'password': password,
        }
    }

    if len(website) == 0 or len(password) == 0 or len(email) == 0:
        messagebox.showinfo(title='Oops', message="Please don't leave empty fields")
    else:
        try:
            with open('data.json', 'r') as data_file:
                # reading old data
                data = json.load(data_file)
        except FileNotFoundError:
            with open('data.json', 'w') as data_file:
                json.dump(new_data, data_file, indent=4)
        else:
            with open('data.json', 'w') as data_file:
                data.update(new_data)
                json.dump(data, data_file, indent=4)
        finally:
            website_entry.delete(0, END)
            password_entry.delete(0, END)


# ---------------------------- FIND PASSWORD ------------------------------- #

def find_password():
    website = website_entry.get().lower()
    try:
        with open('data.json', 'r') as data_file:
            data = json.load(data_file)
            if website in data.keys():
                # print(type(data))
                messagebox.showinfo(title=f'{website}', message=f"Email: {data[website]['email']}\n"
                                                                f"Password: {data[website]['password']}")
            else:
                messagebox.showinfo(title=f'Oops', message=f"Credentials for {website} not created yet")
    except FileNotFoundError:
        messagebox.showinfo(title='Oops', message='No accounts/passwords created yet. Get started!')

# ---------------------------- UI SETUP ------------------------------- #
# Window
window = Tk()
window.config(padx=50, pady=50)
window.title('Password Manager')

# Canvas with logo
canvas = Canvas(width=200, height=200)
logo_image = PhotoImage(file='logo.png')
canvas.create_image(100, 100, image=logo_image)
canvas.grid(column=2, row=1)

# Labels
website_label = Label(text='Website:')
website_label.grid(column=1, row=2, sticky='e')
username_label = Label(text='Email/Username:')
username_label.grid(column=1, row=3, sticky='e')
password_label = Label(text='Password:')
password_label.grid(column=1, row=4, sticky='e')

# Entries
website_entry = Entry(width=24)
website_entry.grid(column=2, row=2, columnspan=2, sticky='w')
website_entry.focus()
username_entry = Entry(width=43)
username_entry.grid(column=2, row=3, columnspan=2, sticky='w')
username_entry.insert(0, 'janeta@email.com')
password_entry = Entry(width=24)
password_entry.grid(row=4, column=2, sticky='w')

# Buttons
generate_password_button = Button(text='Generate Password', width=14, command=generate_password)
generate_password_button.grid(column=2, row=4, columnspan=2, sticky='e')
add_button = Button(text='Add', width=36, command=save)
add_button.grid(column=2, row=5, columnspan=2, sticky='w')
search_button = Button(text='Search', width=14, command=find_password)
search_button.grid(column=2, row=2, columnspan=2, sticky='e')

window.mainloop()
