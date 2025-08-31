import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import requests
import json
import re
from tkinter import font


class APIViewerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced API Viewer")
        self.root.geometry("1100x750")
        self.setup_swagger_theme()
        self.create_widgets()

    def setup_swagger_theme(self):
        """Настраивает цветовую схему как в Swagger"""
        # Цветовая схема Swagger (темная тема)
        self.colors = {
            'background': '#1b1b1b',
            'foreground': '#ffffff',
            'key': '#61dafb',  # голубой - ключи
            'string': '#98c379',  # зеленый - строки
            'number': '#d19a66',  # оранжевый - числа
            'boolean': '#56b6c2',  # бирюзовый - булевы значения
            'null': '#c678dd',  # фиолетовый - null
            'brackets': '#abb2bf',  # серый - скобки
        }

        # Настраиваем шрифт
        self.custom_font = font.Font(family="Consolas", size=11)

    def create_widgets(self):
        # Панель управления слева
        control_frame = ttk.Frame(self.root, padding="10", width=200)
        control_frame.pack(side=tk.LEFT, fill=tk.Y)

        # Выбор метода HTTP
        ttk.Label(control_frame, text="HTTP Method:").pack(pady=(0, 5))
        self.method_var = tk.StringVar(value="GET")
        self.method_combobox = ttk.Combobox(
            control_frame,
            textvariable=self.method_var,
            values=["GET", "POST", "PUT", "PATCH", "DELETE"],
            state="readonly",
            width=10
        )
        self.method_combobox.pack(pady=(0, 15))

        # Поле для ввода URL
        ttk.Label(control_frame, text="URL:").pack(pady=(0, 5))
        self.url_entry = ttk.Entry(control_frame, width=30)
        self.url_entry.pack(pady=(0, 15))
        self.url_entry.insert(0, "https://potterapi-fedeperin.vercel.app/en/books")

        # Поле для тела запроса (для POST/PUT/PATCH)
        ttk.Label(control_frame, text="Request Body (JSON):").pack(pady=(0, 5))
        self.body_text = scrolledtext.ScrolledText(
            control_frame,
            wrap=tk.WORD,
            font=("Courier New", 10),
            height=10,
            width=30
        )
        self.body_text.pack(pady=(0, 15))
        self.apply_base_theme(self.body_text)

        # Кнопка отправки
        self.send_btn = ttk.Button(
            control_frame,
            text="Send Request",
            command=self.send_request
        )
        self.send_btn.pack(pady=10)

        # Правая часть с вкладками
        right_frame = ttk.Frame(self.root, padding="10")
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Вкладки для отображения результатов
        self.tab_control = ttk.Notebook(right_frame)

        # Вкладка с ответом
        self.tab_response = ttk.Frame(self.tab_control)
        self.response_text = scrolledtext.ScrolledText(
            self.tab_response,
            wrap=tk.WORD,
            font=("Courier New", 10)
        )
        self.response_text.pack(fill=tk.BOTH, expand=True)
        self.tab_control.add(self.tab_response, text="Response")
        self.apply_base_theme(self.response_text)

        # Вкладка с headers
        self.tab_headers = ttk.Frame(self.tab_control)
        self.headers_text = scrolledtext.ScrolledText(
            self.tab_headers,
            wrap=tk.WORD,
            font=("Courier New", 10)
        )
        self.headers_text.pack(fill=tk.BOTH, expand=True)
        self.tab_control.add(self.tab_headers, text="Headers")
        self.apply_base_theme(self.headers_text)

        # Вкладка с информацией о запросе
        self.tab_info = ttk.Frame(self.tab_control)
        self.info_text = scrolledtext.ScrolledText(
            self.tab_info,
            wrap=tk.WORD,
            font=("Courier New", 10)
        )
        self.info_text.pack(fill=tk.BOTH, expand=True)
        self.tab_control.add(self.tab_info, text="Request Info")
        self.apply_base_theme(self.info_text)

        self.tab_control.pack(fill=tk.BOTH, expand=True)

        # Статус бар
        self.status_var = tk.StringVar()
        self.status_bar = ttk.Label(
            right_frame,
            textvariable=self.status_var,
            relief=tk.SUNKEN
        )
        self.status_bar.pack(fill=tk.X)

        # Привязываем изменение метода к обновлению интерфейса
        self.method_combobox.bind("<<ComboboxSelected>>", self.update_ui_for_method)

    def apply_base_theme(self, text_widget):
        """Применяет базовую цветовую схему"""
        text_widget.configure(
            background=self.colors['background'],
            foreground=self.colors['foreground'],
            font=self.custom_font,
            insertbackground=self.colors['foreground']
        )

    def update_ui_for_method(self, event=None):
        """Обновляет интерфейс в зависимости от выбранного метода"""
        method = self.method_var.get()
        if method in ["POST", "PUT", "PATCH"]:
            self.body_text.configure(state='normal')
            self.apply_base_theme(self.body_text)
        else:
            self.body_text.configure(state='disabled')

    def display_formatted_response(self, response):
        """Отображает ответ с подсветкой синтаксиса как в Swagger"""
        try:
            json_data = response.json()
            formatted_json = json.dumps(json_data, indent=2, ensure_ascii=False)
            self.highlight_json(formatted_json, self.response_text)
        except ValueError:
            # Для не-JSON ответов используем обычный текст
            self.response_text.insert(tk.INSERT, response.text)
            self.response_text.configure(state='disabled')

    def display_formatted_headers(self, headers):
        """Отображает headers с подсветкой"""
        formatted_headers = json.dumps(headers, indent=2, ensure_ascii=False)
        self.highlight_json(formatted_headers, self.headers_text)

    def display_formatted_info(self, info):
        """Отображает информацию о запросе с подсветкой"""
        formatted_info = json.dumps(info, indent=2, ensure_ascii=False)
        self.highlight_json(formatted_info, self.info_text)

    def highlight_json(self, json_string, text_widget):
        """Подсвечивает JSON синтаксис как в Swagger"""
        text_widget.configure(state='normal')
        text_widget.delete(1.0, tk.END)

        # Регулярные выражения для разных типов токенов
        patterns = [
            (r'"(.*?)":', self.colors['key']),  # ключи
            (r':\s*"(.*?)"', self.colors['string']),  # строковые значения
            (r':\s*(\d+)', self.colors['number']),  # числа
            (r':\s*(true|false)', self.colors['boolean']),  # булевы значения
            (r':\s*(null)', self.colors['null']),  # null
            (r'[{}[\],]', self.colors['brackets']),  # скобки и запятые
        ]

        # Вставляем текст и применяем подсветку
        text_widget.insert(tk.INSERT, json_string)

        # Применяем подсветку для каждого pattern
        for pattern, color in patterns:
            self.apply_highlight(text_widget, pattern, color)

        text_widget.configure(state='disabled')

    def apply_highlight(self, text_widget, pattern, color):
        """Применяет подсветку для заданного pattern"""
        start_pos = "1.0"
        while True:
            pos = text_widget.search(pattern, start_pos, tk.END, regexp=True)
            if not pos:
                break

            # Определяем конец совпадения
            end_pos = f"{pos}+{len(text_widget.get(pos, f'{pos} lineend'))}c"

            # Применяем тег с цветом
            text_widget.tag_add(pattern, pos, end_pos)
            text_widget.tag_config(pattern, foreground=color)

            start_pos = end_pos

    def send_request(self):
        url = self.url_entry.get()
        method = self.method_var.get()

        if not url:
            messagebox.showerror("Error", "Please enter URL")
            return

        try:
            self.status_var.set(f"Sending {method} request...")
            self.root.update()

            headers = {'Content-Type': 'application/json'}
            body = None

            # Подготовка тела запроса для POST/PUT/PATCH
            if method in ["POST", "PUT", "PATCH"]:
                try:
                    body_text = self.body_text.get("1.0", tk.END).strip()
                    if body_text:
                        body = json.loads(body_text)
                except json.JSONDecodeError:
                    messagebox.showerror("Error", "Invalid JSON format in request body")
                    return

            # Отправка запроса
            response = requests.request(
                method=method,
                url=url,
                json=body,
                headers=headers
            )

            # Очищаем предыдущие данные
            self.clear_all_tabs()

            # Отображаем ответ с подсветкой
            self.display_formatted_response(response)

            # Отображаем headers с подсветкой
            self.display_formatted_headers(dict(response.headers))

            # Отображаем информацию о запросе с подсветкой
            request_info = {
                "URL": url,
                "Method": method,
                "Status Code": response.status_code,
                "Encoding": response.encoding,
                "Elapsed Time": str(response.elapsed),
                "Request Body": body if body else "None"
            }
            self.display_formatted_info(request_info)

            self.status_var.set(f"{method} request completed. Status: {response.status_code}")

        except Exception as e:
            messagebox.showerror("Error", f"Request failed: {str(e)}")
            self.status_var.set("Request failed")

    def clear_all_tabs(self):
        """Очищает все текстовые поля"""
        for text_widget in [self.response_text, self.headers_text, self.info_text]:
            text_widget.configure(state='normal')
            text_widget.delete(1.0, tk.END)


if __name__ == "__main__":
    root = tk.Tk()
    app = APIViewerApp(root)
    root.mainloop()