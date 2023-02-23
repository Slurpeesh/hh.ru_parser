import tkinter as tk
from tkinter import ttk
import time


# class of Parser app
class ParserApp:
    # creating window
    root = tk.Tk()
    LOGO = tk.PhotoImage(file="icon.png")
    root.iconphoto(False, LOGO)
    root.title("hh.ru parser")

    def __init__(self, command=None):
        # setting size
        width = 600
        height = 700
        self.root.geometry(f'{width}x{height}+600+250')
        self.command = command
        # creating elements in window
        header = tk.Label(self.root, text="hh.ru parser", font=("Arial", 20, "bold"))
        input_label = tk.Label(self.root, text="Input query text: ", font=("Arial", 14))
        self.string_entry = tk.StringVar()
        self.search_request = None
        self.query_entry = tk.Entry(self.root, width=25, borderwidth=1, relief="solid", textvariable=self.string_entry)
        accept_button = tk.Button(self.root, text="Search", command=self.command)
        self.waiting = tk.Label(self.root, text="Please, wait, it may take up to a few minutes ...", font=("Arial", 14))
        self.output = tk.Frame(self.root)
        self.answer = tk.Text(self.output, height=4, wrap="word", state="disabled", width=30)
        self.result_label = None

        # packing elements
        header.grid(row=0, column=0, columnspan=2, stick="we")
        input_label.grid(row=1, column=0, pady=5, stick="e")
        self.query_entry.grid(row=1, column=1, pady=5, stick="w")
        accept_button.grid(row=2, column=0, columnspan=2, pady=5)
        self.waiting.grid(row=3, column=0, columnspan=2, pady=5, sticky="we")
        self.waiting.grid_remove()
        # setting minimum size for each column
        self.root.grid_columnconfigure(0, minsize=300)
        self.root.grid_columnconfigure(1, minsize=300)
        self.output.grid_columnconfigure(0, minsize=577)
        self.output.grid_columnconfigure(1, minsize=23)

    # method that shows root window
    def show(self):
        self.root.mainloop()

    # method that shows output text
    def show_results(self, results):
        self.answer.config(height=int(len(results) / 3 + 2))
        if not len(self.answer.get("1.0", 'end-1c')):
            self.answer.grid(row=0, column=0, stick="nswe")
            y_scroll_output = ttk.Scrollbar(self.output, orient='vertical', command=self.answer.yview)
            self.answer['yscrollcommand'] = y_scroll_output.set
            y_scroll_output.grid(row=0, column=1, stick='ns')
        self.answer.config(state="normal")
        self.answer.delete("1.0", tk.END)
        self.answer.insert("1.0", results)
        self.answer.config(state="disabled")
        self.output.grid(row=4, column=0, columnspan=2, sticky="wens")

    # method that shows waiting message
    def create_waiting(self):
        self.waiting.grid()
        self.root.update()

    # method that deletes waiting message
    def destroy_waiting(self):
        self.waiting.destroy()
        self.waiting = tk.Label(self.root, text="Please, wait, it may take up to a few minutes ...", font=("Arial", 14))
        self.waiting.grid(row=3, column=0, columnspan=2, pady=5, sticky="we")
        self.waiting.grid_remove()

    # method that deletes output text
    def clear_output(self):
        if self.output.winfo_exists():
            self.output.destroy()
            self.output = tk.Frame(self.root)
            self.answer = tk.Text(self.output, height=4, wrap="word", state="disabled", width=30)
            self.result_label = None
            self.output.grid_columnconfigure(0, minsize=577)
            self.output.grid_columnconfigure(1, minsize=23)


def test():
    app.clear_output()
    app.create_waiting()
    time.sleep(2)
    app.destroy_waiting()
    text = {5: "dsggggggggggggggggggggggggggggggggggggggg",
            6: "dsgsdgdsgdsggggggdgdgsdssgddddddddddddddd",
            7: "sgddddddddddddddddddddddddddddddddddddddd",
            8: "dsggggggggggggggggggggggggggggggggggggggg",
            9: "dsgsdgdsgdsggggggdgdgsdssgddddddddddddddd",
            10: "sgddddddddddddddddddddddddddddddddddddddd",
            11: "dsggggggggggggggggggggggggggggggggggggggg",
            12: "dsgsdgdsgdsggggggdgdgsdssgddddddddddddddd",
            13: "sgddddddddddddddddddddddddddddddddddddddd",
            14: "dsggggggggggggggggggggggggggggggggggggggg",
            15: "dsgsdgdsgdsggggggdgdgsdssgddddddddddddddd",
            16: "sgddddddddddddddddddddddddddddddddddddddd",
            17: "dsggggggggggggggggggggggggggggggggggggggg",
            18: "dsgsdgdsgdsggggggdgdgsdssgddddddddddddddd",
            19: "sgddddddddddddddddddddddddddddddddddddddd",
            20: "dsggggggggggggggggggggggggggggggggggggggg",
            21: "dsgsdgdsgdsggggggdgdgsdssgddddddddddddddd",
            22: "sgddddddddddddddddddddddddddddddddddddddd",
            23: "dsggggggggggggggggggggggggggggggggggggggg",
            24: "dsgsdgdsgdsggggggdgdgsdssgddddddddddddddd",
            25: "sgddddddddddddddddddddddddddddddddddddddd",
            26: "dsggggggggggggggggggggggggggggggggggggggg",
            27: "dsgsdgdsgdsggggggdgdgsdssgddddddddddddddd",
            28: "sgddddddddddddddddddddddddddddddddddddddd",
            29: 1, 30: 30, 31: 31, 32: 32, 33: 33, 34: 34, 35: 35,
            36: 36, 37: 37, 38: 38, 39: 39, 40: 40, 41: 41, 42: 42,
            43: 43, 44: 44, 45: 45, 46: 46, 47: 47, 48: 48, 49: 49,
            50: 50, 51: 51, 52: 52, 53: 53, 54: 54, 55: 55, 56: 56,
            57: 57, 58: 58, 59: 59, 60: 60, 61: 61, 62: 62, 63: 63,
            64: 64, 65: 65, 66: 66, 67: 67, 68: 68, 69: 69, 70: 70}
    app.show_results(text)


# main code block
def main():
    app.show()


# entry point
if __name__ == "__main__":
    app = ParserApp(test)
    main()
