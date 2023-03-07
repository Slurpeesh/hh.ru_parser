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
        input_label = tk.Label(self.root, text="Input query text: ", font=("Arial", 14))
        self.string_entry = tk.StringVar()
        self.search_request = None
        self.query_entry = tk.Entry(self.root, width=25, borderwidth=1, relief="solid", textvariable=self.string_entry)
        self.accept_button = tk.Button(self.root, text="Search", command=threading.Thread(target=self.command).start)
        self.waiting = tk.Label(self.root, text="Please, wait, it may take up to a few minutes ...", font=("Arial", 14))
        self.progress_bar = ttk.Progressbar(self.root, orient=tk.HORIZONTAL, length=400)
        self.output = tk.Frame(self.root, borderwidth=1, relief="solid")
        self.answer = tk.Text(self.output, height=4, wrap="word", state="disabled", width=45)
        self.result_label = None

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
        self.root.grid_columnconfigure(0, minsize=400)
        self.root.grid_columnconfigure(1, minsize=400)
        self.output.grid_columnconfigure(0, minsize=777)
        self.output.grid_columnconfigure(1, minsize=23)

    # method that shows root window
    def show(self):
        self.root.mainloop()

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
        # Remove axes splines
        for s in ['top', 'bottom', 'left', 'right']:
            plot.spines[s].set_visible(False)

        # Remove x, y Ticks
        plot.xaxis.set_ticks_position('none')
        plot.yaxis.set_ticks_position('none')

        # Add x, y gridlines
        plot.grid(color='grey', linestyle='-.', linewidth=0.5, alpha=0.3)
        # Show top values
        plot.invert_yaxis()
        # Add Plot Title
        plot.set_title("Occurrences of key skills in vacancies", loc='left')

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
        self.waiting = tk.Label(self.root, text="Please, wait, it may take up to a few minutes ...", font=("Arial", 14))
        self.waiting.grid(row=3, column=0, columnspan=2, pady=5, sticky="we")
        self.waiting.grid_remove()
        # recreate progress bar
        self.progress_bar = ttk.Progressbar(self.root, orient=tk.HORIZONTAL, length=400)
        self.progress_bar.grid(row=4, column=0, columnspan=2, pady=5)
        self.progress_bar.grid_remove()

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
            self.output.grid_columnconfigure(0, minsize=777)
            self.output.grid_columnconfigure(1, minsize=23)


def test():
    app.clear_output()
    app.create_waiting()
    time.sleep(2)
    app.destroy_waiting()
    text = {'Test1': 164, 'Test2': 80, 'Test3': 77, 'Test4': 61, 'Test5': 45, 'Test6': 34,
            'Test7': 29, 'Test8': 24, 'Test9': 18, 'Test10': 17, 'Test11': 15}
    app.show_results(text)


# main code block
def main():
    app.show()


# entry point
if __name__ == "__main__":
    app = ParserApp(test)
    main()
