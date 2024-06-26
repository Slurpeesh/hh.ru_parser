import time
import threading
import tkinter as tk
from tkinter import ttk
import matplotlib
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
matplotlib.use("TkAgg")


# function that removes dictionary keys which values are less or equal to "n"
def remove_deviations(dictionary, n):
    keys_for_deleting = []
    for k, v in dictionary.items():
        if v <= n:
            keys_for_deleting.append(k)
    for k in keys_for_deleting:
        del dictionary[k]


# class of Parser app
class ParserApp:
    # creating window
    root = tk.Tk()
    LOGO = tk.PhotoImage(file="icon.png")
    root.iconphoto(False, LOGO)
    root.title("hh.ru parser")

    def __init__(self, command=None):
        # setting size
        width = 800
        height = 900
        self.root.geometry(f'{width}x{height}+600+100')
        self.command = command
        # creating elements in window
        header = tk.Label(self.root, text="hh.ru parser", font=("Arial", 20, "bold"))
        input_label = tk.Label(self.root, text="Введите текст запроса: ", font=("Arial", 14))
        self.string_entry = tk.StringVar()
        self.search_request = None
        self.query_entry = tk.Entry(self.root, width=25, borderwidth=1, relief="solid",
                                    textvariable=self.string_entry, highlightthickness=0.5)
        self.query_entry.bind("<Return>", self.enter_press)
        self.query_entry.bind("<FocusIn>", self.on_focus_in_entry)
        self.query_entry.bind("<FocusOut>", self.on_focus_out_entry)
        self.accept_button = tk.Button(self.root, text="Поиск", activebackground='#f59e9e',
                                       command=threading.Thread(target=self.command).start)
        # hover event on button
        self.accept_button.bind("<Enter>", self.on_enter_button)
        self.accept_button.bind("<Leave>", self.on_leave_button)
        self.waiting = tk.Label(self.root, text="Пожалуйста, подождите, это может занять несколько минут...", font=("Arial", 14))
        self.progress_bar = ttk.Progressbar(self.root, orient=tk.HORIZONTAL, length=400)
        self.output = tk.Frame(self.root, borderwidth=1, relief="solid")
        self.answer = tk.Text(self.output, height=4, wrap="word", state="disabled", width=45)
        self.result_label = None
        self.nothing_found_label = tk.Label(self.root, text="Вакансии не найдены", font=("Arial", 14))
        self.no_internet_label = tk.Label(self.root, text="Нет подключения к Интернету", font=("Arial", 14))

        # packing elements
        header.grid(row=0, column=0, columnspan=2, stick="we")
        input_label.grid(row=1, column=0, pady=5, stick="e")
        self.query_entry.grid(row=1, column=1, pady=5, stick="w")
        self.accept_button.grid(row=2, column=0, columnspan=2, pady=5)
        self.waiting.grid(row=3, column=0, columnspan=2, pady=5, sticky="we")
        self.waiting.grid_remove()
        self.progress_bar.grid(row=4, column=0, columnspan=2, pady=5)
        self.progress_bar.grid_remove()
        # setting minimum size for each column
        self.root.grid_columnconfigure(0, weight=1, minsize=400)
        self.root.grid_columnconfigure(1, weight=1, minsize=400)
        self.output.grid_columnconfigure(0, weight=777, minsize=777)
        self.output.grid_columnconfigure(1, weight=23, minsize=23)
        # focus entry element
        self.query_entry.focus_set()

    # method that shows root window
    def show(self):
        self.root.mainloop()

    # method that allows user to confirm query entry by pressing "Enter"
    def enter_press(self, event):
        threading.Thread(target=self.command).start()

    # methods that change background color of a button when hovering over it
    def on_enter_button(self, event):
        self.accept_button.config(background='#e9c5c5')

    def on_leave_button(self, event):
        self.accept_button.config(background='SystemButtonFace')

    # methods that highlight border of entry when focusing it
    def on_focus_in_entry(self, event):
        self.query_entry.config(highlightthickness=0.5, highlightbackground='#a00000', highlightcolor='#a00000')

    def on_focus_out_entry(self, event):
        self.query_entry.config(highlightthickness=0, highlightbackground='black', highlightcolor='black')

    def disable_input(self):
        self.accept_button.config(state=tk.DISABLED)
        self.query_entry.unbind("<Return>")

    def enable_input(self):
        self.accept_button.config(state=tk.NORMAL)
        self.query_entry.bind("<Return>", self.enter_press)

    # method that creates histogram
    def create_diagrams(self, data):
        # creating a clone of data dictionary and remove garbage data from histogram
        modified_data = data.copy()
        remove_deviations(modified_data, round(max(data.values())/10))
        print(modified_data)

        # checking length of data to be appropriately fitted into histogram
        decreasing_modified_data = {k: v for k, v in sorted(modified_data.items(), key=lambda item: item[1])}
        for k in decreasing_modified_data:
            if len(modified_data) <= 15:
                break
            del modified_data[k]

        # creating block for plot in tkinter
        figure = Figure(figsize=(6, 3), dpi=100, layout='constrained')
        plot = figure.add_subplot(1, 1, 1)
        canvas = FigureCanvasTkAgg(figure, self.output)
        canvas.get_tk_widget().grid(row=1, column=0)

        # preparing histogram to user
        plot.barh(list(modified_data.keys()), list(modified_data.values()), color='darkred')
        # remove axes splines
        for s in ['top', 'bottom', 'left', 'right']:
            plot.spines[s].set_visible(False)

        # remove x, y Ticks
        plot.xaxis.set_ticks_position('none')
        plot.yaxis.set_ticks_position('none')

        # add x, y gridlines
        plot.grid(color='grey', linestyle='-.', linewidth=0.5, alpha=0.3)
        # show top values
        plot.invert_yaxis()
        # add Plot Title
        plot.set_title("Число ключевых навыков в вакансиях", loc='left')

    # method that shows output text
    def show_results(self, results):
        output_max_height = int(len(results) / 3 + 2)
        # set restriction to max height of output window
        if output_max_height > 15:
            self.answer.config(height=15)
        else:
            self.answer.config(height=int(len(results) / 3 + 2))

        if not len(self.answer.get("1.0", 'end-1c')):
            self.answer.grid(row=0, column=0, pady=10, stick="nswe")
            y_scroll_output = ttk.Scrollbar(self.output, orient='vertical', command=self.answer.yview)
            self.answer['yscrollcommand'] = y_scroll_output.set
            y_scroll_output.grid(row=0, column=1, stick='ns')
        self.answer.config(state="normal")
        self.answer.delete("1.0", tk.END)
        self.answer.insert("1.0", results)
        self.answer.config(state="disabled")
        self.create_diagrams(results)
        self.output.grid(row=4, column=0, columnspan=2, sticky="wens")
        # creating a new Thread object to make multithreading working correctly
        self.accept_button.config(command=threading.Thread(target=self.command).start)
        # focus entry element
        self.query_entry.focus_force()

    # method that shows waiting message
    def create_waiting(self):
        self.waiting.grid()
        self.progress_bar.grid()
        self.root.update()

    # method that deletes waiting message
    def destroy_waiting(self):
        self.waiting.destroy()
        self.progress_bar.destroy()
        # recreate waiting label
        self.waiting = tk.Label(self.root, text="Пожалуйста, подождите, это может занять несколько минут...", font=("Arial", 14))
        self.waiting.grid(row=3, column=0, columnspan=2, pady=5, sticky="we")
        self.waiting.grid_remove()
        # recreate progress bar
        self.progress_bar = ttk.Progressbar(self.root, orient=tk.HORIZONTAL, length=400)
        self.progress_bar.grid(row=4, column=0, columnspan=2, pady=5)
        self.progress_bar.grid_remove()
        self.progress_bar.grid_remove()

    # method that shows that there are no vacancies
    def nothing_found_text(self):
        self.nothing_found_label.grid(row=4, column=0, columnspan=2, sticky="we")

    def no_internet_text(self):
        self.no_internet_label.grid(row=4, column=0, columnspan=2, sticky="we")

    # method that destroys nothing_found_text if exists
    def clear_nothing_found_text(self):
        if self.nothing_found_label.winfo_exists():
            self.nothing_found_label.destroy()
            self.nothing_found_label = tk.Label(self.root,
                                                text="Не найдено ни одной или слишком мало вакансий", font=("Arial", 14))
            # creating a new Thread object to make multithreading working correctly
            self.accept_button.config(command=threading.Thread(target=self.command).start)

    def clear_no_internet_text(self):
        if self.no_internet_label.winfo_exists():
            self.no_internet_label.destroy()
            self.no_internet_label = tk.Label(self.root,
                                                text="Нет подключения к Интернету", font=("Arial", 14))
            # creating a new Thread object to make multithreading working correctly
            self.accept_button.config(command=threading.Thread(target=self.command).start)

    # method that sets maximum value of progress bar (times 10 for smooth animation)
    def set_max_value_progress_bar(self, value):
        self.progress_bar.config(maximum=value*30)

    # method that updates progress bar
    def set_progress_bar(self, value):
        for step in range((value-1)*30, value*30+1):
            self.progress_bar.config(value=step)
            self.root.update()
            time.sleep(0.01)

    # method that deletes output text
    def clear_output(self):
        if self.output.winfo_exists():
            self.output.destroy()
            self.output = tk.Frame(self.root)
            self.answer = tk.Text(self.output, height=4, wrap="word", state="disabled", width=30)
            self.result_label = None
            self.output.grid_columnconfigure(0, weight=777, minsize=777)
            self.output.grid_columnconfigure(1, weight=23, minsize=23)


def test():
    app.disable_input()
    app.clear_output()
    app.create_waiting()
    time.sleep(2)
    app.destroy_waiting()
    text = {'Test1': 164, 'Test2': 80, 'Test3': 77, 'Test4': 61, 'Test5': 45, 'Test6': 34,
            'Test7': 29, 'Test8': 24, 'Test9': 18, 'Test10': 17, 'Test11': 15}
    app.show_results(text)
    app.enable_input()


# main code block
def main():
    app.show()


# entry point
if __name__ == "__main__":
    app = ParserApp(test)
    main()
