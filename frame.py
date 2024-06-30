from ttkthemes import ThemedTk
import tkinter as tk
from tkinter import ttk,Checkbutton, messagebox,Misc
from tkintermapview import TkinterMapView
import data
from os import system
system('cls')


class Window(tk.Tk):
    def __init__(self):
        super().__init__()

        # try:
        #     self.__data = data.load_data()
        # except Exception as e:
        #     messagebox.showwarning(title='警告',message=str(e))
        
        #先做主視窗    
        mainframe=ttk.Frame(self)
        mainframe.pack(expand=True,fill='both',padx=10,pady=10)
        
        #左上條件欄位，使用labelframe賦予邊框與標題
        self.left_top_frame=ttk.Labelframe(mainframe,border=5,labelanchor='n',text="查詢條件",height=600)
        self.left_top_frame.grid(column=0,row=0,sticky=tk.NW)
        
        #設定日期
        date_frame=ttk.Labelframe(self.left_top_frame,labelanchor='nw',text="日期",width=500,height=80)
        date_frame.grid(column=0,row=0,sticky=tk.W)
        date_frame.grid_propagate(False)
        years=list(range(2018,2025))
        months=list(range(1,13))
        days=list(range(1,32))
        start_label=ttk.Label(date_frame,text="從：")
        start_label.grid(column=0,row=0)
        self.start_year=ttk.Combobox(date_frame,values=years,width=4,state="readonly")    #state讓使用者只能下拉選取，無法自行輸入
        self.start_year.set(years[0]) #設定預設值，避免回傳空值發生錯誤
        self.start_year.grid(column=1,row=0)
        start_year_label=ttk.Label(date_frame,text="年")
        start_year_label.grid(column=2,row=0)
        self.start_month=ttk.Combobox(date_frame,values=months,width=3,state="readonly")
        self.start_month.set(months[0])
        self.start_month.grid(column=3,row=0)
        start_month_label=ttk.Label(date_frame,text="月")
        start_month_label.grid(column=4,row=0)
        self.start_day=ttk.Combobox(date_frame,values=days,width=3,state="readonly")
        self.start_day.set(days[0])
        self.start_day.grid(column=5,row=0)
        start_day_label=ttk.Label(date_frame,text="日")
        start_day_label.grid(column=6,row=0)    
        end_label=ttk.Label(date_frame,text="到：")
        end_label.grid(column=0,row=1)
        self.end_year=ttk.Combobox(date_frame,values=years,width=4,state="readonly")
        self.end_year.set(years[-1])
        self.end_year.grid(column=1,row=1)
        end_year_label=ttk.Label(date_frame,text="年")
        end_year_label.grid(column=2,row=1)
        self.end_month=ttk.Combobox(date_frame,values=months,width=3,state="readonly")
        self.end_month.set(months[-1])
        self.end_month.grid(column=3,row=1)
        end_month_label=ttk.Label(date_frame,text="月")
        end_month_label.grid(column=4,row=1)
        self.end_day=ttk.Combobox(date_frame,values=days,width=3,state="readonly")
        self.end_day.set(days[-1])
        self.end_day.grid(column=5,row=1)
        end_day_label=ttk.Label(date_frame,text="日")
        end_day_label.grid(column=6,row=1)
        self.start_year.bind("<<ComboboxSelected>>",self.Update_end_dates)
        self.start_month.bind("<<ComboboxSelected>>",self.Update_end_dates)
        self.start_day.bind("<<ComboboxSelected>>",self.Update_end_dates)
        self.end_year.bind("<<ComboboxSelected>>",self.Update_end_dates)
        self.end_month.bind("<<ComboboxSelected>>",self.Update_end_dates)
        
        #設定縣市
        city_frame=ttk.Labelframe(self.left_top_frame,labelanchor='nw',text="縣市：",width=500,height=120)
        city_frame.grid(column=0,row=1,sticky=tk.W)
        city_frame.grid_propagate(False)

        cities=["臺北市","新北市","基隆市","桃園市","新竹市","新竹縣","苗栗縣","臺中市","臺中縣","彰化縣","南投縣","雲林縣","嘉義市","嘉義縣","臺南市","高雄市","宜蘭縣","花蓮縣","臺東縣","澎湖縣","金門縣","連江縣"]
        self.city_vars={city:tk.BooleanVar(value=False) for city in cities} #儲存按鈕的布林值
        self.select_all_button=ttk.Button(city_frame,text="全選",command=self.select_all)
        self.select_all_button.grid(column=0,row=1)
        for i, city in enumerate(cities):
            city_check = ttk.Checkbutton(city_frame, text=city, variable=self.city_vars[city])
            city_check.grid(column=i%6+1,row=i//6)
        # show_button = ttk.Button(mainframe, text="顯示選擇", command=self.show_selection)
        # show_button.grid(column=0,row=3)
        
        #設定進階選項   
        extra_frame=ttk.Labelframe(self.left_top_frame,labelanchor='nw',text="進階選項：",width=500,height=110)
        extra_frame.grid(column=0,row=2,sticky=tk.W)
        extra_frame.grid_propagate(False)
                
        #設定天氣
        weather_label=ttk.Label(extra_frame,text="天候：")
        weather_label.grid(column=0,row=1,sticky=tk.W)
        weathers=["晴天","陰天","雨天"]
        self.weather_vars={weather:tk.BooleanVar(value=True) for weather in weathers} #儲存按鈕的布林值
        for i , weather in enumerate(weathers):
            weather_check = ttk.Checkbutton(extra_frame, text=weather, variable=self.weather_vars[weather])
            weather_check.grid(column=i+1,row=1,sticky=tk.W)
        check_values_button = ttk.Button(extra_frame, text="取得值", command=self.get_weather_values)   #這兩行用於確認資料取得形式的範例，再刪除
        check_values_button.grid(column=4, row=1,sticky=tk.W)
        #設定光線狀態
        light_label=ttk.Label(extra_frame,text="光線：")
        light_label.grid(column=0,row=2,sticky=tk.W)
        lights=["日間自然光線","夜間(或隧道)有照明","有照明且開啟","無照明","晨或暮光","夜間(或隧道)無照明","有照明未開啟或故障"]
        self.light_vars={light:tk.BooleanVar(value=True) for light in lights} #儲存按鈕的布林值
        for i , light in enumerate(lights):
            light_check = ttk.Checkbutton(extra_frame, text=light, variable=self.light_vars[light])
            light_check.grid(column=i%4+1,row=i//4+2,sticky=tk.W)
        #設定是否為肇逃
        run_label=ttk.Label(extra_frame,text="肇逃：")
        run_label.grid(column=0,row=4,sticky=tk.W)
        runs=["是","否"]
        self.run_vars={run:tk.BooleanVar(value=True) for run in runs}
        for i , run in enumerate(runs):
            run_check = ttk.Checkbutton(extra_frame, text=run, variable=self.run_vars[run])
            run_check.grid(column=i%4+1,row=i//4+4,sticky=tk.W)
        
        #設定小計案件類別   
        count_frame=ttk.Labelframe(self.left_top_frame,labelanchor='nw',text="類別小計：",width=500,height=80)
        count_frame.grid(column=0,row=3,sticky=tk.W)
        count_frame.grid_propagate(False)
        A1_label=ttk.Label(count_frame,text=f"A1案件：XX 件")
        A1_label.grid(column=0,row=0)
        A2_label=ttk.Label(count_frame,text=f"A2案件：XX 件")
        A2_label.grid(column=0,row=1)

        #右上地圖欄位
        self.right_top_frame=ttk.Labelframe(mainframe,border=5,labelanchor='n',text="事故地圖")
        self.right_top_frame.grid(column=1,row=0)
        map=TkinterMapView(self.right_top_frame,width=800,height=400)
        map.grid(column=0,row=0)
        mapdefault=map.set_position(25.115035182309448, 121.53834876780614,marker=True)
        
        #下方資料欄位
        self.bottom_frame=ttk.Labelframe(mainframe,border=5,labelanchor='nw',text="詳細資料",width=800)
        self.bottom_frame.grid(column=0,row=1,columnspan=2,sticky=tk.NW)
        
        #設定column
        columns=('#1','#2','#3','#4','#5','#6','#7','#8')
        tree=ttk.Treeview(self.bottom_frame,columns=columns,show='tree headings')
        #設定heading
        tree.heading('#0',text='日期')
        tree.column('#0', minwidth=60,width=150)
        tree.heading('#1',text='時間')
        tree.column('#1', minwidth=60,width=150)
        tree.heading('#2',text='事故類別')
        tree.column('#2', minwidth=60,width=150)
        tree.heading('#3',text='地區')
        tree.column('#3', minwidth=60,width=150)
        tree.heading('#4',text='事故類別')
        tree.column('#4', minwidth=60,width=150)
        tree.heading('#5',text='天氣')
        tree.column('#5', minwidth=60,width=150)
        tree.heading('#6',text='光線狀態')
        tree.column('#6', minwidth=60,width=150)
        tree.heading('#7',text='肇因研判')
        tree.column('#7', minwidth=60,width=150)
        tree.heading('#8',text='肇事逃逸')
        tree.column('#8', minwidth=60,width=150)
        tree.grid(column=0,row=0)
   
    
    def Update_end_dates(self,event):   #自動調整日期
        start_year=int(self.start_year.get())
        start_month=int(self.start_month.get())
        start_day=int(self.start_day.get())
        end_year=int(self.end_year.get())
        end_month=int(self.end_month.get())
        end_day=int(self.end_day.get())
        valid_end_year=list(range(start_year,2025))
        self.end_year['values']=valid_end_year
        if end_year < start_year:
            self.end_year.set(start_year)
            
        if start_year == end_year:
            valid_end_month=list(range(start_month,13))
            self.end_month['values']=valid_end_month
            if end_month < start_month:
                self.end_month.set(start_month)
                
        if start_month == 2:
            self.start_day['values']=list(range(1,29))
            if start_day > 28:
                self.start_day.set(28)
        elif start_month in [4,6,9,11]:
            self.start_day['values']=list(range(1,31))
            if start_day > 30:
                    self.start_day.set(30)
        else:
            self.start_day['values']=list(range(1,32))
            
        if end_month == 2:
            self.end_day['values']=list(range(1,29))
            if end_day > 28:
                self.end_day.set(28)
        elif end_month in [4,6,9,11]:
            self.end_day['values']=list(range(1,31))
            if end_day > 30:
                self.end_day.set(30)
        else:
            self.end_day['values']=list(range(1,32))
            
        if start_year == end_year and start_month == end_month:
            if start_month == 2:
                valid_end_day=list(range(start_day,29))
                self.end_day['values']=valid_end_day
                if end_day > 28:
                    self.end_day.set(28)
            elif start_month in [4,6,9,11]:
                valid_end_day=list(range(start_day,31))
                self.end_day['values']=valid_end_day
                if end_day > 30:
                    self.end_day.set(30)
            else:
                valid_end_day=list(range(start_day,32))
                self.end_day['values']=valid_end_day
            if end_day < start_day:
                self.end_day.set(start_day)
    def show_selection(self):           #匯出城市選擇結果
        selected_cities = [city for city, var in self.city_vars.items() if var.get()]
    def select_all(self):               #全選按鈕
        all_selected= all(var.get() for var in self.city_vars.values())
        if all_selected:
            for var in self.city_vars.values():
                var.set(False)
        else:
            for var in self.city_vars.values():
                var.set(True)
    def get_weather_values(self):       #取得天氣結果的方法，參考用
        values = {weather: var.get() for weather, var in self.weather_vars.items()}
        print(values)
    

def main():

    window = Window()
    window.title('全台近年交通事故資料表')
    window.geometry("1400x800")
    window.mainloop()

if __name__ == '__main__':
    main()

