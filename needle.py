import tkinter as tk
from tkinter import Tk
import numpy as np
from PIL import Image, ImageTk
from tkinter import Tk, messagebox
import scratch
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
def main():
    main_window = Tk()
    app = NeedlemanWunschGUI(main_window)
    main_window.mainloop()
class NeedlemanWunschGUI:
    def __init__(self,root):

        self.root = root
        self.root.configure(bg="white")
        self.root.title("Needleman-Wunsch Alignment")
        def on_closing():
            if tk.messagebox.askokcancel("Quit", "Do you want to quit?"):
                self.root.destroy()

        self.root.protocol("WM_DELETE_WINDOW", on_closing)
        # setting window to the center
        width = self.root.winfo_screenwidth()
        height = self.root.winfo_screenheight()
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width / 2) - (width / 2)
        y = (screen_height / 2) - (height / 2)
        self.root.geometry(f'{width}x{height}+{int(x)}+{int(y)}')

        frame1 = tk.Frame(self.root, bg='light blue')
        frame1.pack(fill='x')

        START = tk.Label(frame1, text="NEEDLEMAN - WUNSCH ALGORITHM", font=("bold", 25), bg="light blue", fg="white", height=2)
        START.pack(padx=380, pady=10)

        frame2 = tk.Frame(self.root, bg='orange', height=10)
        frame2.pack(fill='x')

        main_frame = tk.Frame(self.root)
        main_frame.pack(expand=True, fill='both')

        my_canvas = tk.Canvas(main_frame,bg='white')
        my_canvas.pack(side='left', fill='both', expand=True)

        my_scroll = tk.Scrollbar(main_frame, orient=tk.VERTICAL, command=my_canvas.yview)
        my_scroll.pack(side='right', fill='y')

        my_canvas.configure(yscrollcommand=my_scroll.set)
        my_canvas.bind('<Configure>', lambda e: my_canvas.config(scrollregion=my_canvas.bbox(tk.ALL)))


        content_frame = tk.Frame(my_canvas,bg='white')
        my_canvas.create_window((0, 0), window=content_frame, anchor='nw')

        btn_back = tk.Button(my_canvas, text='Back', command=self.scratch,
                             font=("Times New Roman", 14, 'bold'), bd=3, relief= tk.RIDGE,
                             cursor='hand2', bg='#333637', fg='white', activeforeground='white', activebackground='#333637')
        # btn_back.grid(row=0, column=3,sticky="ne", columnspan=2)
        btn_back.place(x=screen_width-120, y=screen_height-765, width=90)

        self.seq1_label = tk.Label(content_frame, text="Sequence 1:", font=("bold", 15), bg="white", fg="black", width=10)
        self.seq1_label.grid(row=0, column=0, sticky="nsew", padx=20, pady=10)
        self.seq1_entry = tk.Entry(content_frame, width=30, bg="light blue", fg="black",font=("Arial", 14, "bold"))
        self.seq1_entry.grid(row=0, column=1, sticky="w", padx=20, pady=10)
        self.seq1_error_label = tk.Label(content_frame, text="", font=("bold", 7), bg="white", fg="red", width=6)


        self.seq2_label = tk.Label(content_frame, text="Sequence 2:", font=("bold", 15), bg="white", fg="black", width=10, height=1)
        self.seq2_label.grid(row=2, column=0, sticky="nsew", padx=20, pady=10)
        self.seq2_entry = tk.Entry(content_frame, width=30, bg="light blue", fg="black",font=("Arial", 14, "bold"))
        self.seq2_entry.grid(row=2, column=1, sticky="w", padx=20, pady=10)
        self.seq2_error_label = tk.Label(content_frame, text="", font=("bold", 7), bg="white", fg="red", width=6)
        self.seq_error_label = tk.Label(content_frame, text="", font=("bold", 7), bg="white", fg="red", width=6)

        self.match_reward_label = tk.Label(content_frame, text="Match Score:", font=("bold", 15), bg="white", fg="black", width=10, height=1)
        self.match_reward_label.grid(row=4, column=0, sticky="nsew", padx=20, pady=10)

        self.match_reward = tk.Entry(content_frame, width=30, bg="light blue", fg="black",font=("Arial", 14, "bold"))
        self.match_reward.grid(row=4, column=1, sticky="w", padx=20, pady=10)

        self.mismatch_penalty_label = tk.Label(content_frame, text="Mismatch Score:", bg="white", font=("bold", 15), fg="black", width=15, height=1)
        self.mismatch_penalty_label.grid(row=5, column=0, sticky="nsew", padx=20, pady=10)

        self.mismatch_penalty = tk.Entry(content_frame, width=30, bg="light blue", fg="black",font=("Arial", 14, "bold"))
        self.mismatch_penalty.grid(row=5, column=1, sticky="w", padx=20, pady=10)

        self.gap_penalty_label = tk.Label(content_frame, text="Gap Penalty:", font=("bold", 15), bg="white", fg="black", width=10, height=1)
        self.gap_penalty_label.grid(row=6, column=0, sticky="nsew", padx=20, pady=10)

        self.gap_penalty = tk.Entry(content_frame, width=30, bg="light blue", fg="black",font=("Arial", 14, "bold"))
        self.gap_penalty.grid(row=6, column=1, sticky="w", padx=20, pady=10)

        self.error_label = tk.Label(content_frame, text="", font=("bold", 7), bg="white", fg="red", width=6)
        self.align_button = tk.Button(content_frame, text="Align", command=self.align_sequences, bg="red", fg="white", bd=2, height=1, font=("bold", 14),width=30)
        self.align_button.grid(row=8, column=1, columnspan=1, sticky="w", padx=20, pady=10)

        self.alignment_label = tk.Label(content_frame, text="Aligned Sequences", font=("Helvetica", 20, "bold"), bg="white")
        self.alignment_label.grid(row=9, column=1, columnspan=1, sticky="nsew", padx=20, pady=10)

        self.alignment_text = tk.Text(content_frame, height=5, width=50,font=("Helvetica", 13))
        self.alignment_text.grid(row=10, column=1, columnspan=2, sticky="nsew", padx=10, pady=10)

        # self.intro_text = tk.Text(content_frame, height=5, width=50, bg="GREEN")
        # self.intro_text.grid(row=1, column=2, columnspan=1)

        self.matrix_canvas = tk.Canvas(content_frame,bg="WHITE")
        self.matrix_canvas.grid(row=11, column=1, sticky="nsew")


        content_frame.grid_rowconfigure(0, weight=1)  # Allow vertical expansion
        content_frame.grid_columnconfigure(0, weight=0)  # Disable horizontal expansion


        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=0)
        def update_scroll_region(event):
            self.matrix_canvas.configure(scrollregion=self.matrix_canvas.bbox(tk.ALL))
        self.matrix_canvas.bind('<Configure>', update_scroll_region)

        self.root.mainloop()



    def align_sequences(self):
        seq1 = self.seq1_entry.get().upper()
        seq2 = self.seq2_entry.get().upper()

        valid_seq1 = set(seq1).issubset('ACGT')
        valid_seq2 = set(seq2).issubset('ACGT')
        self.seq1_error_label.grid_forget()
        self.seq2_error_label.grid_forget()
        self.seq_error_label.grid_forget()
        self.alignment_text.grid(row=10, column=1, columnspan=2, sticky="nsew", padx=10, pady=10)
        if not valid_seq1:
            self.seq1_error_label.config(text="Invalid sequence(s). Please Enter Only Nucleotide Sequence - (ACGT)")
            self.seq1_error_label.grid(row=1, column=1, columnspan=1, sticky="nsew")
            self.matrix_canvas.grid_forget()
            self.alignment_text.grid_forget()

        if not valid_seq2:
            self.seq2_error_label.config(text="Invalid sequence(s). Please Enter Only Nucleotide Sequence - (ACGT)")
            self.seq2_error_label.grid(row=3, column=1, sticky="nsew")
            self.matrix_canvas.grid_forget()
            self.alignment_text.grid_forget()

        if not valid_seq1 or not valid_seq2:
            self.seq_error_label.config(text="Invalid sequence(s). Please enter only nucleotide Sequence-  (ACGT).")
            self.seq_error_label.grid(row=3, column=1, sticky="nsew")
            self.matrix_canvas.grid_forget()
            self.alignment_text.grid_forget()
            return


        try:
            match_reward = int(self.match_reward.get())
            mismatch_penalty = int(self.mismatch_penalty.get())
            gap_penalty = int(self.gap_penalty.get())
            alignment, alignment_score, main_matrix = self.needleman_wunsch(seq1, seq2,match_reward,mismatch_penalty,gap_penalty)
            self.alignment_text.delete('1.0', tk.END)
            self.alignment_text.insert(tk.END, f"Aligned Sequence 2: {alignment[1]}\nAligned Sequence 1: {alignment[0]}\nAlignment Score: {alignment_score}")
            self.draw_matrix(main_matrix,seq1, seq2)
            self.matrix_canvas.grid(row=11, column=1, sticky="nsew")
            self.error_label.grid_forget()
            self.alignment_text.grid(row=10, column=1, columnspan=2, sticky="nsew", padx=10, pady=10)
        except ValueError:
            # Display error message in label
            self.error_label.config(text="ERROR! PLEASE ENTER INTEGERS ONLY", fg="red")
            self.error_label.grid(row=7, column=1, sticky="nsew")
            self.matrix_canvas.grid_forget()
            self.alignment_text.grid_forget()



    def needleman_wunsch(self, seq1, seq2,match_reward,mismatch_penalty,gap_penalty):
        # Create matrices and perform the Needleman-Wunsch algorithm
        main_matrix = np.zeros((len(seq1) + 1, len(seq2) + 1),dtype='object')


        match_checker_matrix = np.zeros((len(seq1), len(seq2)))

        # Fill the match checker matrix according to match or mismatch
        for i in range(len(seq1)):
            for j in range(len(seq2)):
                if seq1[i] == seq2[j]:
                    match_checker_matrix[i][j] = match_reward
                else:
                    match_checker_matrix[i][j] = mismatch_penalty

        # Filling up the matrix using Needleman-Wunsch algorithm
        # Step 1: Initialization
        for i in range(len(seq1) + 1):
            main_matrix[i][0] = i * gap_penalty

        for j in range(len(seq2) + 1):
            main_matrix[0][j] = j * gap_penalty


        # Step 2: Matrix Filling
        for i in range(1, len(seq1) + 1):
            for j in range(1, len(seq2) + 1):
                main_matrix[i][j] = max(main_matrix[i - 1][j - 1] + match_checker_matrix[i - 1][j - 1],
                                        main_matrix[i - 1][j] + gap_penalty,
                                        main_matrix[i][j - 1] + gap_penalty)

        # Step 3: Traceback
        aligned_1 = ""
        aligned_2 = ""
        ti = len(seq1)
        tj = len(seq2)
        up_arrow = "\u2191"
        right_arrow = "\u2192"
        down_arrow = "\u2193"
        left_arrow = "\u2190"
        down_right_arrow = "\u2198"
        up_left_arrow = "\u2196"

        while ti > 0 or tj > 0:
            if ti > 0 and tj > 0 and main_matrix[ti][tj] == main_matrix[ti - 1][tj - 1] + match_checker_matrix[ti - 1][tj - 1]:
                main_matrix[ti][tj]=(up_left_arrow)+str(main_matrix[ti][tj])

                aligned_1 = seq1[ti - 1] + aligned_1
                aligned_2 = seq2[tj - 1] + aligned_2
                ti -= 1
                tj -= 1
            elif ti > 0 and main_matrix[ti][tj] == main_matrix[ti - 1][tj] + gap_penalty:
                main_matrix[ti][tj]=(up_arrow )+str(main_matrix[ti][tj])
                aligned_1 = seq1[ti - 1] + aligned_1
                aligned_2 = "-" + aligned_2
                ti -= 1
            else:
                main_matrix[ti][tj]=(left_arrow)+str(main_matrix[ti][tj])
                aligned_1 = "-" + aligned_1
                aligned_2 = seq2[tj - 1] + aligned_2
                tj -= 1
        self.create_alignment_pie_chart(aligned_1, aligned_2)

        return (aligned_1, aligned_2), main_matrix[-1][-1], main_matrix
    def draw_matrix(self,main_matrix, seq1, seq2):

        cell_width = 60
        cell_height = 60
        origin_x = 40
        origin_y = 40


        self.matrix_canvas.delete( 'all')
        canvas_width = (len(seq2) + 2) *cell_width  + origin_x * 2
        canvas_height = (len(seq1) + 2) *cell_height + origin_y * 2
        self.matrix_canvas.config(width=canvas_width, height=canvas_height)

        self.matrix_canvas.create_rectangle(origin_x, origin_y, origin_x + cell_width, origin_y + cell_height, fill='YELLOW',outline='WHITE', width=2)
        self.matrix_canvas.create_text((2 * origin_x + cell_width) / 2, (2 * origin_y + cell_height) / 2, text="")

        for i in range(len(seq1) + 2):
            for j in range(len(seq2) + 2):
                x1 = origin_x + j * cell_width
                y1 = origin_y + i * cell_height
                x2 = x1 + cell_width
                y2 = y1 + cell_height

                if i == 0 and j == 0:
                    self.matrix_canvas.create_rectangle(x1, y1, x2, y2, fill="GRAY",outline='WHITE', width=2)
                    self.matrix_canvas.create_text((x1 + x2) / 2, (y1 + y2) / 2, text="")
                elif i == 0 and j > 1:
                    self.matrix_canvas.create_rectangle(x1, y1, x2, y2, fill='#ffa500', outline='WHITE', width=2)
                    self.matrix_canvas.create_text((x1 + x2) / 2, (y1 + y2) / 2, text=seq2[j - 2],font="bold", fill="WHITE")
                elif j == 0 and i > 1:
                    self.matrix_canvas.create_rectangle(x1, y1, x2, y2, fill='#ffa500',outline='WHITE', width=2)
                    self.matrix_canvas.create_text((x1 + x2) / 2, (y1 + y2) / 2, text=seq1[i - 2],font="bold", fill="WHITE")
                else:
                    self.matrix_canvas.create_rectangle(x1, y1, x2, y2, fill='GRAY',outline='WHITE', width=2)
                    if (i, j) != (1, 0) and (i, j) != (0, 1):  # Add condition to skip (1, 0) and (0, 1)
                        # Checking if the cell contains an arrow and update its color
                        if isinstance(main_matrix[i - 1][j - 1], str) and main_matrix[i - 1][j - 1] != "":
                            self.matrix_canvas.create_rectangle(x1, y1, x2, y2, fill='RED',outline='WHITE', width=2)
                            self.matrix_canvas.create_text((x1 + x2) / 2, (y1 + y2) / 2, text=f"{(main_matrix[i - 1][j - 1])}",font="bold")
                        else:
                            self.matrix_canvas.create_rectangle(x1, y1, x2, y2, fill='WHITE',outline='WHITE', width=2)
                            self.matrix_canvas.create_text((x1 + x2) / 2, (y1 + y2) / 2, text=f"{(main_matrix[i - 1][j - 1])}")


        self.root.update()
    def create_alignment_pie_chart(self, aligned_1, aligned_2):
        print(aligned_1, aligned_2)
        print(zip(aligned_1, aligned_2))
        num_matches = sum(a == b for a, b in zip(aligned_1, aligned_2))
        num_mismatches = sum(a != b for a, b in zip(aligned_1, aligned_2))
        num_gaps = aligned_1.count('-') + aligned_2.count('-')
        # Calculating the percentages
        total_length = len(aligned_1)
        print(total_length)
        chart_window = tk.Toplevel(self.root)
        chart_window.title("Alignment Chart")
        chart_window.geometry("400x300")

        fig = Figure(figsize=(6, 4), dpi=100)
        ax = fig.add_subplot(111)
        canvas = FigureCanvasTkAgg(fig, master=chart_window)
        canvas_widget = canvas.get_tk_widget()
        if total_length==0:
            canvas_widget.pack_forget()

        else:
            ax.clear()
            match_percentage = (num_matches / total_length) * 100
            mismatch_percentage = (num_mismatches / total_length) * 100
            gap_percentage = (num_gaps / total_length) * 100


            # Create the pie chart
            labels = ['Matches', 'Mismatches', 'Gaps']
            sizes = [match_percentage, mismatch_percentage, gap_percentage]
            colors = ['green', 'red', 'blue']
            explode = (0.1, 0, 0)

            ax.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%',
                   shadow=True, startangle=90)
            ax.axis('equal')
            ax.set_title('Sequence Alignment')

            canvas_widget.pack()
            # self.root.update()

    def scratch(self):
        self.root.destroy()
        main_window = Tk()
        app = scratch.start(main_window)
        main_window.mainloop()


if __name__ == '__main__':
    main()