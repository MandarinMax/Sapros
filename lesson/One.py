import tkinter as tk
from tkinter import ttk

win = tk.Tk()
photo = tk.PhotoImage(file='submit-document.png')
win.iconphoto(False, photo)
# win.iconbitmap('logozapros.ico')
win.title('Zapros') #заголовок
win.geometry('800x600+400+200') #размер окна
win.minsize(300, 300) #минимальный размер окна
win.configure(bg='#a9f2ee') #цвет фона

label1_1 = tk.Label(win, text="""Приложение для отправки запросов
Первая итерация""", #форматируем лейбл
                    bg= 'red', #цвет фона
                    fg='white', #цвет текста
                    font=('Arial', 12, 'bold'), #настройки саого текста, шрифт, размер и  стиль
                    padx=10, #отступы по х
                    pady=1, # отступы по y
                    width=40,
                    height=2,
                    anchor='nw', #расположение текста
                    relief=tk.RAISED, #границы - по дефолту 2 пикселя
                    bd=10, #ширина границ
                    justify=tk.LEFT
                    )
label1_1.place(x=0, y=0)

def add_lebel():
    lable = tk.Label(win, text='Привет')
    lable.pack()

btn_send = tk.Button(win, text='Send',
                     command=add_lebel)
btn_send.place(x=50, y=100)

#наименование поля для ввода
tk.Label(win, text='Поле для ввода').place(x=100, y=150)

# Поле для ввода
rout = tk.Entry(win)
rout.place(x=200, y=150)

win.mainloop()