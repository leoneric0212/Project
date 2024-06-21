import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image, ImageTk
import os
from tkintermapview import TkinterMapView

class AccidentApp:
    def __init__(self, root):
        self.root = root
        self.root.title("交通事故查詢地圖")

        self.label = tk.Label(root, text="選擇事故ID:")
        self.label.pack()

        self.accident_id_combobox = ttk.Combobox(root)
        self.accident_id_combobox.pack()

        self.fetch_button = tk.Button(root, text="查詢事故", command=self.fetch_accident)
        self.fetch_button.pack()

        self.analysis_button = tk.Button(root, text="分析事故數據", command=self.analyze_data)
        self.analysis_button.pack()

        self.display_frame = tk.Frame(root)
        self.display_frame.pack(fill=tk.BOTH, expand=True)

        self.accident_data = {
            "accident001": {
                "date": "2024-06-20",
                "time": "15:30",
                "location": {"latitude": 40.712776, "longitude": -74.005974},
                "vehicles": ["car", "truck"],
                "injuries": 2,
                "description": "A car collided with a truck at the intersection."
            },
            "accident002": {
                "date": "2024-06-21",
                "time": "10:45",
                "location": {"latitude": 34.052235, "longitude": -118.243683},
                "vehicles": ["motorcycle", "car"],
                "injuries": 1,
                "description": "A motorcycle hit by a car on the highway."
            },
            "accident003": {
                "date": "2024-06-22",
                "time": "08:20",
                "location": {"latitude": 41.878113, "longitude": -87.629799},
                "vehicles": ["bus", "car"],
                "injuries": 5,
                "description": "A bus and a car collision in downtown."
            }
        }

        self.accident_id_combobox['values'] = list(self.accident_data.keys())

    def fetch_accident(self):
        accident_id = self.accident_id_combobox.get().strip()
        if not accident_id:
            messagebox.showwarning("警告", "請選擇事故ID")
            return

        data = self.accident_data.get(accident_id)
        
        if data:
            self.display_accident(data)
        else:
            messagebox.showerror("錯誤", "未找到事故")

    def display_accident(self, data):
        location = data['location']
        
        for widget in self.display_frame.winfo_children():
            widget.destroy()

        map_widget = TkinterMapView(self.display_frame, width=800, height=600)
        map_widget.set_position(location['latitude'], location['longitude'])
        map_widget.set_zoom(12)
        map_widget.pack(fill=tk.BOTH, expand=True)

        map_widget.set_marker(location['latitude'], location['longitude'], text=data['description'])

        details_label = tk.Label(self.display_frame, text=f"事故描述:\n{data['description']}", padx=10, pady=10)
        details_label.pack(side=tk.RIGHT, padx=10, pady=10, fill=tk.BOTH, expand=True)

    def analyze_data(self):
        data = {
            'date': ["2024-06-20", "2024-06-21", "2024-06-22", "2024-06-20"],
            'location': ["New York", "Los Angeles", "Chicago", "New York"],
            'injuries': [2, 1, 5, 3]
        }
        df = pd.DataFrame(data)

        for widget in self.display_frame.winfo_children():
            widget.destroy()

        plt.figure(figsize=(4, 3), dpi=80)
        accident_counts = df['location'].value_counts()
        accident_counts.plot(kind='bar', ax=plt.gca())
        plt.title('不同城市的交通事故比例')
        plt.xlabel('城市')
        plt.ylabel('事故數量')
        plt.tight_layout()
        bar_chart_path = os.path.join(os.getcwd(), "bar_chart.png")
        plt.savefig(bar_chart_path, dpi=80)
        plt.close()

        bar_chart_image = Image.open(bar_chart_path)
        bar_chart_image = ImageTk.PhotoImage(bar_chart_image)
        bar_chart_label = tk.Label(self.display_frame, image=bar_chart_image)
        bar_chart_label.image = bar_chart_image
        bar_chart_label.pack(side=tk.LEFT, padx=10, pady=10)

        plt.figure(figsize=(4, 3), dpi=80)
        plt.pie(accident_counts, labels=accident_counts.index, autopct='%1.1f%%', startangle=140)
        plt.title('不同城市的交通事故比例')
        plt.axis('equal')
        plt.tight_layout()
        pie_chart_path = os.path.join(os.getcwd(), "pie_chart.png")
        plt.savefig(pie_chart_path, dpi=80)
        plt.close()

        pie_chart_image = Image.open(pie_chart_path)
        pie_chart_image = ImageTk.PhotoImage(pie_chart_image)
        pie_chart_label = tk.Label(self.display_frame, image=pie_chart_image)
        pie_chart_label.image = pie_chart_image
        pie_chart_label.pack(side=tk.LEFT, padx=10, pady=10)

if __name__ == "__main__":
    root = tk.Tk()
    app = AccidentApp(root)
    root.mainloop()
