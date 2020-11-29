from tkinter import *
from tkinter import filedialog
from tkinter import font
from tkinter import colorchooser
from tkinter import ttk
import os, sys
import win32print
import win32api
import time

root = Tk()
root.title('Daily Post')
root.iconbitmap('c:/Users/haugl/PycharmProjects/TutorialPlayground/Images/icon.ico')
root.geometry('1200x650')

# style = ttk.Style()
# style.theme_use('clam')

# TODO:
# f'#100DaysOfCode -- Day {day}:{text}'
# post to twitter

# f'{date} -- {day} -- {text}'
# Github -- Project Log -- 100 Days of Code

# f'{date} -- {hours} -- {text}'
# 2020 Coding Hours

# f'''
# {day} : {date}
# Today's Progress: {text}
# Thoughts: {thoughts}
# Links:{github links}
# '''

# Ideas
# Scrape trending keywords on twitter and display on side of screen
# List followers on side of screen
# Save each post to a PDF / Text File / Database
# Look through Code Snippets for additional features


# Style
# SystemButtonFace

textbox_bg_style = '#0084B4'
text_bg_color = '#E8F5FD'
textbox_select_style = 'yellow'
label_style = 'black'
bg_style = '#08a0e9'


# Set Variable for Open File Name
global open_status_name
open_status_name = False

global selected
selected = False

global day, date, hours
day = 59
date = time.strftime('%x')
hours = 8


def new_file():
    my_text.delete('1.0', END)
    root.title('New File - Text Editor')
    status_bar.config(text='New File        ')

    global open_status_name
    open_status_name = False


def open_file():
    my_text.delete('1.0', END)
    text_file = filedialog.askopenfilename(initialdir='c:/Users/haugl/PycharmProjects/TutorialPlayground/', title='Open File', filetypes=(('Text Files', '*.txt'), ('HTML Files', '*.html'), ('Python Files', '*.py'), ('All Files', '*.*')))

    if text_file:
        global open_status_name
        open_status_name = text_file

    # Update Status Bars
    name = text_file
    status_bar.config(text=f'{name}        ')
    name = name.replace('C:/Users/haugl/PycharmProjects/TutorialPlayground/', '')
    name = name.replace('.txt', '')
    root.title(f'{name} - Text Editor')

    # Open File
    text_file = open(text_file, 'r')
    text = text_file
    my_text.insert(END, text)
    text_file.close


def save_as_file():
    text_file = filedialog.asksaveasfilename(defaultextension='.*', initialdir='C:/Users/haugl/PycharmProjects/TutorialPlayground/', title='Save File As', filetypes=(('Text Files', '*.txt'), ('HTML Files', '*.html'), ('Python Files', '*.py'), ('All Files', '*.*')))
    if text_file:
        # Update Status Bars
        name = text_file
        status_bar.config(text=f'Saved:  {name}        ')
        name = name.replace('C:/Users/haugl/PycharmProjects/TutorialPlayground/', '')
        root.title(f'{name} - Text Editor')

        # Save The File
        text_file = open(text_file, 'w')
        text_file.write(my_text.get(1.0, END))
        text_file.close()


def save_file():
    global open_status_name

    if open_status_name:
        # Save The File
        text_file = open(open_status_name, 'w')
        text_file.write(my_text.get(1.0, END))
        text_file.close()

        status_bar.config(text=f'Saved:  {open_status_name}        ')
    else:
        save_as_file()


def cut_text(e):
    global selected
    # Check if Keyboard Shortcut Used
    if e:
        selected = root.clipboard_get()
    else:
        if my_text.selection_get():
            # Grab Selected Text  From Text Box
            selected = my_text.selection_get()
            # Delete Selected Text
            my_text.delete('sel.first', 'sel.last')
            # Clear Clipboard then Append
            root.clipboard_clear()
            root.clipboard_append(selected)


def copy_text(e):
    global selected
    # Check to See if  Used Keyboard Shortcut
    if e:
        selected = root.clipboard_get()
    if my_text.selection_get():
        # Grab Selected Text  From Text Box
        selected = my_text.selection_get()
        # Clear Clipboard then Append
        root.clipboard_clear()
        root.clipboard_append(selected)


def paste_text(e):
    global selected
    # Check if Keyboard Shortcut Used
    if e:
        selected = root.clipboard_get()
    else:
        if selected:
            position = my_text.index(INSERT)
            my_text.insert(position, selected)


def bold_text():
    # Create Font
    bold_font = font.Font(my_text, my_text.cget('font'))
    bold_font.configure(weight='bold')

    # Configure Tag
    my_text.tag_configure('bold', font=bold_font)

    # Define Current Tags
    current_tags = my_text.tag_names('sel.first')

    if 'bold' in current_tags:
        my_text.tag_remove('bold', 'sel.first', 'sel.last')
    else:
        my_text.tag_add('bold', 'sel.first', 'sel.last')


def italics_text():
    # Create Font
    italics_font = font.Font(my_text, my_text.cget('font'))
    italics_font.configure(slant='italic')

    # Configure Tag
    my_text.tag_configure('italic', font=italics_font)

    # Define Current Tags
    current_tags = my_text.tag_names('sel.first')

    if 'italic' in current_tags:
        my_text.tag_remove('italic', 'sel.first', 'sel.last')
    else:
        my_text.tag_add('italic', 'sel.first', 'sel.last')


def text_color():
    # Pick a Color
    my_color = colorchooser.askcolor()[1]
    if my_color:
        status_bar.config(text=my_color)

        # Create Font
        color_font = font.Font(my_text, my_text.cget('font'))

        # Configure Tag
        my_text.tag_configure('colored', font=color_font, foreground=my_color)

        # Define Current Tags
        current_tags = my_text.tag_names('sel.first')

        if 'colored' in current_tags:
            my_text.tag_remove('colored', 'sel.first', 'sel.last')
        else:
            my_text.tag_add('colored', 'sel.first', 'sel.last')


def bg_color():
    my_color = colorchooser.askcolor()[1]
    if my_color:
        my_text.config(bg=my_color)


def all_text_color():
    my_color = colorchooser.askcolor()[1]
    if my_color:
        my_text.config(fg=my_color)


def print_file():
    # printer_name = win32print.GetDefaultPrinter()
    # status_bar.config(text=printer_name)
    file_to_print = filedialog.askopenfilename(initialdir='c:/Users/haugl/PycharmProjects/TutorialPlayground/', title='Open File', filetypes=(('Text Files', '*.txt'), ('HTML Files', '*.html'), ('Python Files', '*.py'), ('All Files', '*.*')))

    if file_to_print:
        win32api.ShellExecute(0, 'print', file_to_print, None, '.', 0)


def select_all(e):
    # Add sel tag to select all text
    my_text.tag_add('sel', '1.0', 'end')


def clear_all():
    my_text.delete(1.0, END)


def night_on():
    main_color = '#000000'
    second_color = '#373737'
    text_color = 'green'

    root.config(bg=main_color)
    status_bar.config(bg=main_color, fg=text_color)
    my_text.config(bg=second_color)
    toolbar_frame.config(bg=main_color)

    # Toolbar Buttons
    bold_button.config(bg=second_color)
    italics_button.config(bg=second_color)
    redo_button.config(bg=second_color)
    undo_button.config(bg=second_color)
    color_text_button.config(bg=second_color)

    # File Menu Colors
    file_menu.config(bg=main_color, fg=text_color)
    edit_menu.config(bg=main_color, fg=text_color)
    color_menu.config(bg=main_color, fg=text_color)
    options_menu.config(bg=main_color, fg=text_color)


def night_off():
    # SystemButtonFace
    main_color = bg_style
    second_color = 'SystemButtonFace'
    text_color = 'black'

    root.config(bg=main_color)
    status_bar.config(bg=main_color, fg=text_color)
    my_text.config(bg='white')
    toolbar_frame.config(bg=main_color)

    # Toolbar Buttons
    bold_button.config(bg=second_color)
    italics_button.config(bg=second_color)
    redo_button.config(bg=second_color)
    undo_button.config(bg=second_color)
    color_text_button.config(bg=second_color)

    # File Menu Colors
    file_menu.config(bg=main_color, fg=text_color)
    edit_menu.config(bg=main_color, fg=text_color)
    color_menu.config(bg=main_color, fg=text_color)
    options_menu.config(bg=main_color, fg=text_color)


night_toggle_on = True


def night_toggle():
    global night_toggle_on
    if night_toggle_on is True:
        night_on()
        night_toggle_on = False
    elif night_toggle_on is False:
        night_off()
        night_toggle_on = True


twitter_keywords = [
    'python', 'tkinter', 'app', 'zerotomastery', 'programmer', 'programmers',
    'programming', 'code', 'coding', 'udemy', 'computerscience', 'computer',
    'chess', 'django', 'pygame', 'git', 'github', 'website', 'algorithm',
    'algorithms', 'sublimetext', 'pycharm', 'career', 'norwegian', 'norway',
    'web', 'design', 'fordummies', 'duolingo', 'twitter', 'kivy', 'api'
]


def text_to_tweet():
    original_tweet = main_textbox.get('1.0', END)
    original_tweet = re.split(r'(\s|\,)', original_tweet)
    new_tweet = ''

    days_programming = day_textbox.get('1.0', END).strip()
    start_of_tweet = f'#100DaysOfCode Day {days_programming}: '

    # Check if any words need a # added to it then add to tweet
    for word in original_tweet:
        if word in twitter_keywords or word.lower() in twitter_keywords:
            new_tweet += (f'#{word}')
        else:
            new_tweet += word

    to_post_tweet = start_of_tweet + new_tweet

    twitter_textbox.delete('1.0', END)
    twitter_textbox.insert(END, to_post_tweet)
    

def text_to_2020():
    original_text = main_textbox.get('1.0', END)
    hours_programming = hours_textbox.get('1.0', END).strip()

    new_text = f'{date} -- {hours_programming} hours --  {original_text}'

    github_2020hours_textbox.delete('1.0', END)
    github_2020hours_textbox.insert(END, new_text)

    # TODO: If date/hours is 2 digit then 1 less space
    # 11/28/20 --  8 hours  --  


def text_to_100():
    original_text = main_textbox.get('1.0', END)
    days_programming = day_textbox.get('1.0', END).strip()

    new_text = f'{date} -- Day {days_programming} --  {original_text}'

    github_100days_textbox.delete('1.0', END)
    github_100days_textbox.insert(END, new_text)
    # 11/28/20 --  Day 58  --  
    pass



# Create a Toolbar Frame
toolbar_frame = Frame(root)
toolbar_frame.grid(row=0, column=1, sticky=W,)
# Removed fill=X

# Create  Main Frame
# my_frame = Frame(root)
# my_frame.grid(pady=5)

# Create Vertical Scrollbar for Text Box
# text_scroll = Scrollbar(my_frame)
# text_scroll.pack(side=RIGHT, fill=Y)

# Create Horizontal Scrollbar for Text Box
# hor_scroll = Scrollbar(my_frame, orient='horizontal')
# hor_scroll.pack(side=BOTTOM, fill=X)

# Removed From Scrollbars
# yscrollcommand=text_scroll.set
# xscrollcommand=hor_scroll.set
# wrap='none'



# Create Text Box Labels

# Day
day_label = Label(root, text='Day:', fg=text_bg_color, bg=bg_style)
day_label.grid(row=1, column=0, sticky=W)

# Date
day_label = Label(root, text='Date:', fg=text_bg_color, bg=bg_style)
day_label.grid(row=2, column=0, sticky=W)

# Hours
day_label = Label(root, text='Hours:', fg=text_bg_color, bg=bg_style)
day_label.grid(row=3, column=0, sticky=W)

# Text
day_label = Label(root, text='Text:', fg=text_bg_color, bg=bg_style)
day_label.grid(row=4, column=0, sticky=W)

# Tweet
day_label = Label(root, text='Twitter:', fg=text_bg_color, bg=bg_style)
day_label.grid(row=5, column=0, sticky=W)

# 2020 Hours
day_label = Label(root, text='2020 Hours:', fg=text_bg_color, bg=bg_style)
day_label.grid(row=6, column=0, sticky=W)

# 100 Days
day_label = Label(root, text='100 Days:', fg=text_bg_color, bg=bg_style)
day_label.grid(row=7, column=0, sticky=W)




# Create Text Box -- Day
day_textbox = Text(root, width=10, height=1, font=('Helvetica', 16), selectbackground=textbox_select_style,
               selectforeground='black', undo=True, bg=textbox_bg_style, fg=text_bg_color)
day_textbox.grid(row=1, column=1, sticky=W, padx=5)
day_textbox.insert(END, day)


# Create Text Box -- Date
date_textbox = Text(root, width=10, height=1, font=('Helvetica', 16), selectbackground=textbox_select_style,
               selectforeground='black', undo=True, bg=textbox_bg_style, fg=text_bg_color)
date_textbox.grid(row=2, column=1, sticky=W, padx=5)
date_textbox.insert(END, date)


# Create Text Box -- Hours
hours_textbox = Text(root, width=10, height=1, font=('Helvetica', 16), selectbackground=textbox_select_style,
               selectforeground='black', undo=True, bg=textbox_bg_style, fg=text_bg_color)
hours_textbox.grid(row=3, column=1, sticky=W, padx=5)
hours_textbox.insert(END, hours)


# Create Text Box -- Text
main_textbox = Text(root, width=70, height=4, font=('Helvetica', 16), selectbackground=textbox_select_style,
               selectforeground='black', undo=True, bg=textbox_bg_style, fg=text_bg_color)
main_textbox.grid(row=4, column=1, sticky=W, padx=5)
main_textbox.insert(END, "Python tkinter, chess, pygame, daily post app")


# Create Text Box -- Twitter
# TODO: countdown tweet_length = 280
twitter_textbox = Text(root, width=70, height=4, font=('Helvetica', 16), selectbackground=textbox_select_style,
               selectforeground='black', undo=True, bg=textbox_bg_style, fg=text_bg_color)
twitter_textbox.grid(row=5, column=1, sticky=W, padx=5)
twitter_textbox.insert(END, "")


# Create Text Box -- Github 2020 Hours
github_2020hours_textbox = Text(root, width=70, height=4, font=('Helvetica', 16), selectbackground=textbox_select_style,
               selectforeground='black', undo=True, bg=textbox_bg_style, fg=text_bg_color)
github_2020hours_textbox.grid(row=6, column=1, sticky=W, padx=5)
github_2020hours_textbox.insert(END, "")

# Create Text Box -- Github 100 Days
github_100days_textbox = Text(root, width=70, height=4, font=('Helvetica', 16), selectbackground=textbox_select_style,
               selectforeground='black', undo=True, bg=textbox_bg_style, fg=text_bg_color)
github_100days_textbox.grid(row=7, column=1, sticky=W, padx=5)
github_100days_textbox.insert(END, "")

# THIS NEEDS TO BE DELETED, THIS FIXES THE COLOR BUG ON ABOVE TEXTBOX
# Create Text Box -- REMOVE
my_text = Text(root, width=1, height=1, font=('Helvetica', 16), selectbackground=textbox_select_style,
               selectforeground='black', undo=True, bg=textbox_bg_style, fg=text_bg_color)
my_text.grid(row=8, column=1, sticky=W, padx=5)






# Configure Scrollbar
# text_scroll.config(command=my_text.yview)
# hor_scroll.config(command=my_text.xview)

# Create Menu
my_menu = Menu(root)
root.config(menu=my_menu)

# Add File Menu
file_menu = Menu(my_menu, tearoff=False)
my_menu.add_cascade(label='File', menu=file_menu)
file_menu.add_command(label='New', command=new_file)
file_menu.add_command(label='Open', command=open_file)
file_menu.add_command(label='Save', command=save_file)
file_menu.add_command(label='Save As', command=save_as_file)
file_menu.add_separator()
file_menu.add_command(label='Print File', command=print_file)

file_menu.add_separator()
file_menu.add_command(label='Exit', command=root.quit)

# Add Edit Menu
edit_menu = Menu(my_menu, tearoff=False)
my_menu.add_cascade(label='Edit', menu=edit_menu)
edit_menu.add_command(label='Cut', command=lambda: cut_text(False), accelerator='(Ctrl+x)')
edit_menu.add_command(label='Copy', command=lambda: copy_text(False), accelerator='(Ctrl+c)')
edit_menu.add_command(label='Paste', command=lambda: paste_text(False), accelerator='(Ctrl+v)')
edit_menu.add_separator()
edit_menu.add_command(label='Undo', command=my_text.edit_undo, accelerator='(Ctrl+z)')
edit_menu.add_command(label='Redo', command=my_text.edit_redo, accelerator='(Ctrl+y)')
edit_menu.add_separator()
edit_menu.add_command(label='Select All', command=lambda: select_all(True), accelerator='(Ctrl+a)')
edit_menu.add_command(label='Clear', command=clear_all)

# Add Color Menu
color_menu = Menu(my_menu, tearoff=False)
my_menu.add_cascade(label='Colors', menu=color_menu)
color_menu.add_command(label='Selected Text', command=text_color)
color_menu.add_command(label='All Text', command=all_text_color)
color_menu.add_command(label='Background', command=bg_color)

# Add Options Menu
options_menu = Menu(my_menu, tearoff=False)
my_menu.add_cascade(label='Options', menu=options_menu)
options_menu.add_command(label='Night Mode On', command=night_on)
options_menu.add_command(label='Night Mode Off', command=night_off)

# Add Status Bar to Bottom of App
status_bar = Label(root, text='Ready')
status_bar.grid(row=8, column=1, ipady=5)
# Removed fill=X, side=BOTTOM,

# Edit Bindings
root.bind('<Control-Key-x>', cut_text)
root.bind('<Control-Key-c>', copy_text)
root.bind('<Control-Key-v>', paste_text)
root.bind('<Control-a>', select_all)





# Create Toolbar Buttons
# Bold Button
bold_button = Button(toolbar_frame, text='Bold', command=bold_text)
bold_button.grid(row=0, column=0, sticky=W, padx=5)
# Italics Button
italics_button = Button(toolbar_frame, text='Italics', command=italics_text)
italics_button.grid(row=0, column=1, sticky=W, padx=5)
# Undo Button
undo_button = Button(toolbar_frame, text='Undo', command=my_text.edit_undo)
undo_button.grid(row=0, column=2, sticky=W, padx=5)
# Redo Button
redo_button = Button(toolbar_frame, text='Redo', command=my_text.edit_redo)
redo_button.grid(row=0, column=3, sticky=W, padx=5)
# Toggle Night Mode Button
night = 'Night'
night_toggle_button = Button(toolbar_frame, text='night', command=night_toggle)
night_toggle_button.grid(row=0, column=4, sticky=W, padx=5)
# Text Color Button
color_text_button = Button(toolbar_frame, text='Text Color', command=text_color)
color_text_button.grid(row=0, column=5, sticky=W, padx=5)

# Submit Button
submit_button = Button(root, text='Submit')
submit_button.grid(row=9, column=1, ipady=5)

# Text to Tweet Button
text_to_tweet_button = Button(root, text='Text to Tweet', command=text_to_tweet)
text_to_tweet_button.grid(row=5, column=2, ipady=5)

# Text to 2020 Coding Hours Button
text_to_tweet_button = Button(root, text='Text to 2020', command=text_to_2020)
text_to_tweet_button.grid(row=6, column=2, ipady=5)

# Text to 100 Days of Code Button
text_to_tweet_button = Button(root, text='Text to 100', command=text_to_100)
text_to_tweet_button.grid(row=7, column=2, ipady=5)




def clock():
    clock_date = time.strftime('%x')
    clock_hour = time.strftime('%H')
    clock_minute = time.strftime('%M')
    # second = time.strftime('%S')
    clock_day = time.strftime('%A')

    my_label.config(text=clock_hour + ':' + clock_minute)
    my_label.after(1000, clock)

    my_label2.config(text=clock_day)

    my_label3.config(text=clock_date)


def update():
    my_label.config(text='New Text')

my_label3 = Label(toolbar_frame, text='', font=('Helvetica', 16), fg='white', bg='black')
my_label3.grid(row=0, column=7)

my_label2 = Label(toolbar_frame, text='', font=('Helvetica', 16), fg='white', bg='black')
my_label2.grid(row=0, column=8)

my_label = Label(toolbar_frame, text='', font=('Helvetica', 16), fg='white', bg='black')
my_label.grid(row=0, column=6)

clock()

night_off()





root.mainloop()