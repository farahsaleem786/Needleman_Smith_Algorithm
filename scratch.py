from tkinter import *
import needle,smith
from PIL import Image, ImageTk
def main():
    main_window = Tk()
    app = start(main_window)
    main_window.mainloop()
class start:
    def __init__(self, root):
        self.root = root
        self.root.title('ALGORITHMS')
        # setting window to the center
        width = self.root.winfo_screenwidth()
        height = self.root.winfo_screenheight()
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width / 2) - (width / 2)
        y = (screen_height / 2) - (height / 2)
        self.root.geometry(f'{width}x{height}+{int(x)}+{int(y)}')


        # **** BG image *********
        self.bg = ImageTk.PhotoImage(
            file='loginback3.jpg')  # self.bg = class object by default
        lbl_bg = Label(self.root, image=self.bg)  # bg  = root window object
        lbl_bg.place(x=0, y=0, relwidth=1, relheight=1)
        frame2 = Frame(self.root, bg='WHITE',highlightbackground="#012832" , highlightthickness=4)
        frame2.place(x=450, y=130, width=505, height=380)
        title = Label(frame2, text="WELCOME TO\nBIOINFORMATICS ALGORITHMS", font=("Lucida Calligraphy", 23, "bold","italic"), bg='WHITE', fg='#333637')
        title.place(x=7, y=50)


        btn_1 = Button(frame2, command=self.needle, text='NEEDLEMAN WUNSCH ALGORITHM',
                       font=("Times New Roman", 15, 'bold'), bd=3,
                       relief=RIDGE,
                       cursor='hand2', bg='#b87e1d', fg='white', activeforeground='white', activebackground='#012832')
        btn_1.place(x=65, y=170, width=370, height=45)

        btn_1 = Button(frame2, command=self.smith, text='SMITH WATERMAN ALGORITHM',
                       font=("Times New Roman", 15, 'bold'), bd=3,
                       relief=RIDGE,
                       cursor='hand2', bg='#b87e1d', fg='white', activeforeground='white', activebackground='#012832')
        btn_1.place(x=65, y=230, width=370, height=45)


    def needle(self):
            self.root.destroy()
            main_window = Tk()
            app = needle.NeedlemanWunschGUI(main_window)
            main_window.mainloop()
    def smith(self):
        self.root.destroy()
        main_window = Tk()
        app = smith.smith_watermanGUI(main_window)
        main_window.mainloop()

if __name__ == '__main__':
    main()