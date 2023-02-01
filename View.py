from datetime import datetime, timedelta
from tkinter import *
import tkinter.font as tkfont
from tkinter import ttk

from PIL import Image, ImageTk


class View(Tk):

    def __init__(self, controller, model):
        super().__init__()
        self.controller = controller
        self.model = model
        self.userinput = StringVar()

        self.big_font_style = tkfont.Font(family='Courier', size=18, weight='bold')
        self.default_style_bold = tkfont.Font(family='Verdana', size=10, weight='bold')
        self.default_style = tkfont.Font(family='Verdana', size=10)

        # Window properties
        self.geometry('512x200')
        self.title('Hangman')
        self.center(self)

        # Create two frames
        self.frame_top, self.frame_bottom, self.frame_img = self.create_three_frames()

        self.image = ImageTk.PhotoImage(Image.open(self.model.image_files[len(self.model.image_files)-1]))
        self.label_image = None

        # Create all buttons, labels and entry
        self.btn_new, self.btn_cancel, self.btn_send = self.create_all_buttons()
        self.lbl_error, self.lbl_result, self.lbl_time = self.create_all_labels()
        self.char_input = self.create_input_entry()

        # Bind enter key
        self.bind('<Return>', lambda event: self.controller.click_btn_send())
        # Enter klahv ei toimi õigesti, kui mäng on lõppenud.
    def main(self):
        self.mainloop()

    @staticmethod
    def center(win):
        """
        https://stackoverflow.com/questions/3352918/how-to-center-a-window-on-the-screen-in-tkinter
        centers a tkinter window
        :param win: the main window or Toplevel window to center
        """
        win.update_idletasks()
        width = win.winfo_width()
        frm_width = win.winfo_rootx() - win.winfo_x()
        win_width = width + 2 * frm_width
        height = win.winfo_height()
        titlebar_height = win.winfo_rooty() - win.winfo_y()
        win_height = height + titlebar_height + frm_width
        x = win.winfo_screenwidth() // 2 - win_width // 2
        y = win.winfo_screenheight() // 2 - win_height // 2
        win.geometry('{}x{}+{}+{}'.format(width, height, x, y))
        win.deiconify()
    def create_three_frames(self):
        frame_top = Frame(self, bg='#0096FF', height=50)  # Blue
        frame_bottom = Frame(self, bg='#EBEB00')  # Yellow

        frame_top.pack(fill='both')
        frame_bottom.pack(expand=True, fill='both')

        # hangman image frame
        frame_img = Frame(frame_top, bg='white', width=130, height=130)
        frame_img.grid(row=0, column=3, rowspan=4, padx=5,pady=5)

        return frame_top, frame_bottom, frame_img  # method returns two variables

    def create_all_buttons(self):
        # New game
        btn_new = Button(self.frame_top, text='New Game', font=self.default_style, command=self.controller.click_btn_new)
        Button(self.frame_top, text='Leaderboard',
               font=self.default_style, command=self.controller.click_btn_leaderboard).grid(row=0,
                                                                                            column=1,
                                                                                            padx=5, pady=2, sticky=EW)
        btn_cancel = Button(self.frame_top, text='Cancel', font=self.default_style,
                            state='disabled', command=self.controller.click_btn_cancel)
        btn_send = Button(self.frame_top, text='Send', font=self.default_style, state='disabled',
                          command=self.controller.click_btn_send)

        btn_new.grid(row=0, column=0, padx=5, pady=2, sticky=EW)
        btn_cancel.grid(row=0, column=2, padx=5, pady=2, sticky=EW)
        btn_send.grid(row=1, column=2, padx=5, pady=2, sticky=EW)

        return btn_new, btn_cancel, btn_send

    def create_all_labels(self):
        Label(self.frame_top, text='Input letter', font=self.default_style_bold).grid(row=1, column=0, padx=5, pady=2)
        lbl_error = Label(self.frame_top, text='Wrong 0 letters', anchor='w', font=self.default_style_bold)
        lbl_time = Label(self.frame_top, text='0:00:00', font=self.default_style)
        lbl_result = Label(self.frame_bottom, text='Let\'s play'.upper(), font=self.big_font_style)
        self.label_image = Label(self.frame_img, image=self.image)
        self.label_image.pack()

        lbl_error.grid(row=2, column=0, columnspan=3, sticky=EW, padx=5, pady=2)
        lbl_time.grid(row=3, column=0, columnspan=3, sticky=EW, padx=5, pady=2)
        lbl_result.pack(padx=5, pady=2)

        return lbl_error, lbl_result, lbl_time

    def create_input_entry(self):
        char_input = Entry(self.frame_top, textvariable=self.userinput, justify='center', font=self.default_style)
        char_input['state'] = 'disabled'
        char_input.grid(row=1, column=1, padx=5, pady=2)

        return char_input

    def change_image(self, image_id):
        self.image = ImageTk.PhotoImage(Image.open(self.model.image_files[image_id]))
        self.label_image.configure(image=self.image)
        self.label_image.image = self.image

    def create_popup_window(self):
        top = Toplevel(self)
        top.geometry('500x180')
        top.resizable(False, False)
        top.grab_set()
        top.focus()

        frame = Frame(top)
        frame.pack(expand=True, fill='both')
        self.center(top)
        return frame

    def generate_leaderbord(self, frame, data):
        # Table view
        my_table = ttk.Treeview(frame)

        # Vertical scrollbar
        vsb = ttk.Scrollbar(frame, orient='vertical', command=my_table.yview)
        vsb.pack(side='right', fill='y')
        my_table.configure(yscrollcommand=vsb.set)

        # Column id
        my_table['columns'] = ('date_time', 'name', 'word', 'misses', 'game_time')

        # Columns characteristics
        my_table.column('#0', width=0, stretch=NO)
        my_table.column('date_time', anchor=CENTER, width=90)
        my_table.column('name', anchor=CENTER, width=80)
        my_table.column('word', anchor=CENTER, width=80)
        my_table.column('misses', anchor=CENTER, width=80)
        my_table.column('game_time', anchor=CENTER, width=40)

        # Table column heading
        my_table.heading('#0', text='', anchor=CENTER)
        my_table.heading('date_time', text='Date', anchor=CENTER)
        my_table.heading('name', text='Player', anchor=CENTER)
        my_table.heading('word', text='Word', anchor=CENTER)
        my_table.heading('misses', text='Wrong letters', anchor=CENTER)
        my_table.heading('game_time', text='Time', anchor=CENTER)

        # Add data into table
        x = 0
        for p in data:
            dt = datetime.strptime(p.date, '%Y-%m-%d %H:%M:%S').strftime('%d.%m.%Y %H:%M:%S')
            my_table.insert(parent='', index='end', iid=str(x), text='',
                            values=(dt, p.name, p.word, p.misses, str(timedelta(seconds=p.time))))
            x += 1

        my_table.pack(expand=True, fill=BOTH)
