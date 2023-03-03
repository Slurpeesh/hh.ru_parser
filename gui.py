import time
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
        accept_button = tk.Button(self.root, text="Search", command=self.command)
        self.waiting = tk.Label(self.root, text="Please, wait, it may take up to a few minutes ...", font=("Arial", 14))
        self.progress_bar = ttk.Progressbar(self.root, orient=tk.HORIZONTAL, length=400)
        self.output = tk.Frame(self.root, borderwidth=1, relief="solid")
        self.answer = tk.Text(self.output, height=4, wrap="word", state="disabled", width=45)
        self.result_label = None

        # packing elements
        header.grid(row=0, column=0, columnspan=2, stick="we")
        input_label.grid(row=1, column=0, pady=5, stick="e")
        self.query_entry.grid(row=1, column=1, pady=5, stick="w")
        accept_button.grid(row=2, column=0, columnspan=2, pady=5)
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
        self.progress_bar = ttk.Progressbar(self.root, orient=tk.HORIZONTAL)
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
    text = {'Python': 164,
            'Linux': 80,
            'SQL': 77,
            'Git': 61,
            'Docker': 45,
            'PostgreSQL': 34,
            'Bash': 29,
            'C++': 24,
            'CI/CD': 18,
            'Java': 17,
            'RabbitMQ': 15,
            'MySQL': 15,
            'Ansible': 15,
            'Django Framework': 14,
            'Английский\xa0— B1 — Средний': 14,
            'Jenkins': 14,
            'Kubernetes': 14,
            'TCP/IP': 14,
            'Английский язык': 13,
            'ООП': 12,
            'Базы данных': 11,
            'Тестирование': 11,
            'Flask': 9,
            'Nginx': 9,
            'СУБД': 9,
            'Hadoop': 9,
            'Английский\xa0— B2 — Средне-продвинутый': 9,
            'QA': 9,
            'ClickHouse': 8,
            'Redis': 8,
            'Анализ данных': 8,
            'Spark': 8,
            'ETL': 8,
            'MongoDB': 7,
            'Django': 7,
            'Информационные технологии': 7,
            'Управление проектами': 7,
            'PyTorch': 7,
            'SCALA': 7,
            'Gitlab': 7,
            'MS SQL': 7,
            'Qt': 7,
            'ELK': 7,
            'Elasticsearch': 6,
            'JavaScript': 6,
            'Английский\xa0— A1 — Начальный': 6,
            'REST API': 6,
            'DWH': 6,
            'C#': 6,
            'Kafka': 6,
            'ML': 6,
            'C/C++': 6,
            'Администрирование серверов Linux': 6,
            'Математическое моделирование': 6,
            'Английский\xa0— A2 — Элементарный': 5,
            'Tableau': 5,
            'Pandas': 5,
            'Airflow': 5,
            'Функциональное тестирование': 5,
            'Golang': 5,
            'Grafana': 5,
            'Информационная безопасность': 5,
            'Администрирование': 5,
            'SQLAlchemy': 4,
            'Работа в команде': 4,
            'Docker-compose': 4,
            'API': 4,
            'Machine Learning': 4,
            'Computer Vision': 4,
            'DevOps': 4,
            'MS Excel': 4,
            'Gitlab CI': 4,
            'Автоматизация тестирования': 4,
            'Go': 4,
            'Clickhouse': 4,
            'A/B тесты': 4,
            'Atlassian Jira': 4,
            'Groovy': 4,
            'Prometheus': 4,
            'Регрессионное тестирование': 4,
            'aiohttp': 3,
            'R': 3,
            'asyncio': 3,
            'Машинное обучение': 3,
            'HTTP': 3,
            'Руководство коллективом': 3,
            'Асинхронное программирование': 3,
            'PyCharm': 3,
            'Data Science': 3,
            'Разработка ПО': 3,
            'Имитационное моделирование': 3,
            'Ручное тестирование': 3,
            'XML': 3,
            'K8S': 3,
            'Аналитическое мышление': 3,
            'NLP': 3,
            'HTML': 3,
            'CSS': 3,
            'SVN': 3,
            'Нейронные сети': 3,
            'Ruby': 3,
            'CentOS': 3,
            'Zabbix': 3,
            'Cisco': 3,
            'OpenShift': 3,
            'Деловая переписка': 3,
            'REST': 3, 'Английский\xa0— C1 — Продвинутый': 3,
            'Power BI': 3,
            'Технические средства информационной защиты': 3}
    app.show_results(text)


# main code block
def main():
    app.show()


# entry point
if __name__ == "__main__":
    app = ParserApp(test)
    main()
