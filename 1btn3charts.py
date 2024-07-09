import tkinter as tk
from tkinter import ttk, messagebox
import csv
import matplotlib.pyplot as plt  # Import Matplotlib
from tkintermapview import TkinterMapView
import pandas as pd

class Window(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("交通事故資料查詢系統")
        self.geometry("1600x1000")  

        self.init_vars()

        self.setup_gui()

        self.populate_treeview()

    def init_vars(self):
        self.years = list(range(2018, 2025))
        self.months = list(range(1, 13))
        self.days = list(range(1, 32))

        # Initialize variables for city selection
        self.cities = ["臺北市", "新北市", "基隆市", "桃園市", "新竹市", "新竹縣", "苗栗縣", "臺中市", "臺中縣", "彰化縣", "南投縣", "雲林縣",
                       "嘉義市", "嘉義縣", "臺南市", "高雄市", "宜蘭縣", "花蓮縣", "臺東縣", "澎湖縣", "金門縣", "連江縣"]

        # Initialize variables for weather and light conditions
        self.weathers = ["晴天", "陰天", "雨天"]
        self.lights = ["日間自然光線", "夜間(或隧道)有照明", "有照明且開啟", "無照明", "晨或暮光", "夜間(或隧道)無照明", "有照明未開啟或故障"]

        # Initialize variables for checkboxes
        self.city_vars = {city: tk.BooleanVar() for city in self.cities}
        self.weather_vars = {weather: tk.BooleanVar(value=True) for weather in self.weathers}
        self.light_vars = {light: tk.BooleanVar(value=True) for light in self.lights}
        self.run_vars = {"是": tk.BooleanVar(value=True), "否": tk.BooleanVar(value=True)}

    def setup_gui(self):

        mainframe = ttk.Frame(self)
        mainframe.pack(expand=True, fill='both', padx=10, pady=10)

        left_top_frame = ttk.Labelframe(mainframe, text="查詢條件")
        left_top_frame.grid(column=0, row=0, padx=10, pady=10, sticky=tk.NW)

        date_frame = ttk.Labelframe(left_top_frame, text="日期")
        date_frame.grid(column=0, row=0, padx=10, pady=10, sticky=tk.W)
        self.setup_date_widgets(date_frame)

        city_frame = ttk.Labelframe(left_top_frame, text="縣市：")
        city_frame.grid(column=0, row=1, padx=10, pady=10, sticky=tk.W)
        self.setup_city_widgets(city_frame)

        extra_frame = ttk.Labelframe(left_top_frame, text="進階選項：")
        extra_frame.grid(column=0, row=2, padx=10, pady=10, sticky=tk.W)
        self.setup_extra_widgets(extra_frame)

        right_top_frame = ttk.Labelframe(mainframe, text="事故地圖")
        right_top_frame.grid(column=1, row=0, padx=10, pady=10)
        self.setup_map(right_top_frame)

        bottom_frame = ttk.Labelframe(mainframe, text="事故資料")
        bottom_frame.grid(column=0, row=1, columnspan=2, padx=10, pady=10, sticky=tk.NSEW)
        self.setup_treeview(bottom_frame)

    def setup_date_widgets(self, parent):
        ttk.Label(parent, text="從：").grid(column=0, row=0, padx=5, pady=5, sticky=tk.E)
        self.start_year = ttk.Combobox(parent, values=self.years, width=5, state="readonly")
        self.start_year.grid(column=1, row=0, padx=5, pady=5)
        self.start_month = ttk.Combobox(parent, values=self.months, width=5, state="readonly")
        self.start_month.grid(column=2, row=0, padx=5, pady=5)
        self.start_day = ttk.Combobox(parent, values=self.days, width=5, state="readonly")
        self.start_day.grid(column=3, row=0, padx=5, pady=5)

        ttk.Label(parent, text="到：").grid(column=0, row=1, padx=5, pady=5, sticky=tk.E)
        self.end_year = ttk.Combobox(parent, values=self.years, width=5, state="readonly")
        self.end_year.grid(column=1, row=1, padx=5, pady=5)
        self.end_month = ttk.Combobox(parent, values=self.months, width=5, state="readonly")
        self.end_month.grid(column=2, row=1, padx=5, pady=5)
        self.end_day = ttk.Combobox(parent, values=self.days, width=5, state="readonly")
        self.end_day.grid(column=3, row=1, padx=5, pady=5)

        self.start_year.bind("<<ComboboxSelected>>", self.update_end_dates)
        self.start_month.bind("<<ComboboxSelected>>", self.update_end_dates)
        self.start_day.bind("<<ComboboxSelected>>", self.update_end_dates)

    def setup_city_widgets(self, parent):
        self.select_all_button = ttk.Button(parent, text="全選", command=self.select_all)
        self.select_all_button.grid(column=0, row=0, padx=5, pady=5, sticky=tk.W)
        for i, city in enumerate(self.cities):
            cb = ttk.Checkbutton(parent, text=city, variable=self.city_vars[city])
            cb.grid(column=i % 6 + 1, row=i // 6, padx=5, pady=5, sticky=tk.W)

    def setup_extra_widgets(self, parent):
        # 天气
        ttk.Label(parent, text="天候：").grid(column=0, row=0, padx=5, pady=5, sticky=tk.E)
        for i, weather in enumerate(self.weathers):
            ttk.Checkbutton(parent, text=weather, variable=self.weather_vars[weather]).grid(column=i + 1, row=0, padx=5, pady=5, sticky=tk.W)
        
        # 灯光
        ttk.Label(parent, text="光線：").grid(column=0, row=1, padx=5, pady=5, sticky=tk.E)
        for i, light in enumerate(self.lights):
            column = i % 3 + 1
            row = i // 3 + 1  # Start from row 2 to leave row 1 empty
            ttk.Checkbutton(parent, text=light, variable=self.light_vars[light]).grid(column=column, row=row, padx=5, pady=5, sticky=tk.W)

        # 肇逃
        ttk.Label(parent, text="肇逃：").grid(column=0, row=5, padx=5, pady=5, sticky=tk.E)
        for i, (run, var) in enumerate(self.run_vars.items()):
            ttk.Checkbutton(parent, text=run, variable=var).grid(column=i + 1, row=5, padx=5, pady=5, sticky=tk.W)


    def setup_map(self, parent):
        self.map = TkinterMapView(parent, width=800, height=400)
        self.map.grid(column=0, row=0, padx=10, pady=10)

        self.pie_chart_button = ttk.Button(parent, text="顯示对应的线图", command=self.show_pie_chart)
        self.pie_chart_button.grid(column=0, row=1, padx=10, pady=10)

    def setup_treeview(self, parent):
        self.treeview = ttk.Treeview(parent, columns=('#0', '#1', '#2', '#3', '#4', '#5', '#6', '#7', '#8'), show='headings')
        self.treeview.grid(column=0, row=0, sticky='nsew')

        headings = ['日期', '時間', '事故類別', '地區', '事故類別', '天氣', '光線狀態', '肇因研判', '肇事逃逸']
        for i, col in enumerate(headings):
            self.treeview.heading('#' + str(i), text=col, anchor='e')
            self.treeview.column('#' + str(i), minwidth=60, width=150, anchor='e')

        scrollbar = ttk.Scrollbar(parent, orient="vertical", command=self.treeview.yview)
        scrollbar.grid(column=1, row=0, sticky='ns')
        self.treeview.configure(yscrollcommand=scrollbar.set)

    def populate_treeview(self):
        for row in self.treeview.get_children():
            self.treeview.delete(row)

        # Read CSV and populate Treeview
        with open('112年度A2交通事故資料_1.csv', newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            next(reader) 
            for row in reader:
                self.treeview.insert('', 'end', values=row)

    def update_end_dates(self, event=None):
        start_year = int(self.start_year.get())
        start_month = int(self.start_month.get())

        self.end_year['values'] = list(range(start_year, 2025))
        self.end_month['values'] = list(range(start_month, 13))

        self.end_year.set(self.start_year.get())
        self.end_month.set(self.start_month.get())

    def select_all(self):
        for var in self.city_vars.values():
            var.set(True)

    def show_pie_chart(self):
        selected_cities = [city for city, var in self.city_vars.items() if var.get()]
        selected_weather = [weather for weather, var in self.weather_vars.items() if var.get()]
        selected_light = [light for light, var in self.light_vars.items() if var.get()]
        selected_run = [run for run, var in self.run_vars.items() if var.get()]

        # 假资料
        data = [
            {'事故類別': '碰撞', '肇事逃逸': '否'},
            {'事故類別': '碰撞', '肇事逃逸': '是'},
            {'事故類別': '倒車', '肇事逃逸': '否'},
            {'事故類別': '碰撞', '肇事逃逸': '否'},
            {'事故類別': '碰撞', '肇事逃逸': '是'},
            {'事故類別': '倒車', '肇事逃逸': '否'},
            {'事故類別': '倒車', '肇事逃逸': '是'},
        ]

        accident_types = {}
        for row in data:
            if row['肇事逃逸'] in selected_run:
                if row['事故類別'] in accident_types:
                    accident_types[row['事故類別']] += 1
                else:
                    accident_types[row['事故類別']] = 1

        #  dictionary ---> pandas DataFrame for plotting
        df = pd.DataFrame(list(accident_types.items()), columns=['事故類別', 'Count'])
        fig, axes = plt.subplots(nrows=2, ncols=2, figsize=(12, 10))

        # Pie chart
        axes[0, 0].pie(df['Count'], labels=df['事故類別'], autopct='%1.1f%%', startangle=140)
        axes[0, 0].set_title('事故類別分佈')

        # Bar chart
        axes[0, 1].bar(df['事故類別'], df['Count'], color='skyblue')
        axes[0, 1].set_title('事故類別分佈 - 柱狀圖')

        # Line chart
        axes[1, 0].plot(df['事故類別'], df['Count'], marker='o', color='orange', linestyle='-')
        axes[1, 0].set_title('事故類別分佈 - 折線圖')
        axes[1, 0].set_xlabel('事故類別')
        axes[1, 0].set_ylabel('Count')

        
        axes[1, 1].axis('off')
        plt.tight_layout()
        plt.show()

if __name__ == "__main__":
    app = Window()
    app.mainloop()
