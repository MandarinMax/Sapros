import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import requests
import json


class APIViewerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced API Viewer")
        self.root.geometry("1100x750")

        self.create_widgets()

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

        # Вкладка с headers
        self.tab_headers = ttk.Frame(self.tab_control)
        self.headers_text = scrolledtext.ScrolledText(
            self.tab_headers,
            wrap=tk.WORD,
            font=("Courier New", 10)
        )
        self.headers_text.pack(fill=tk.BOTH, expand=True)
        self.tab_control.add(self.tab_headers, text="Headers")

        # Вкладка с информацией о запросе
        self.tab_info = ttk.Frame(self.tab_control)
        self.info_text = scrolledtext.ScrolledText(
            self.tab_info,
            wrap=tk.WORD,
            font=("Courier New", 10)
        )
        self.info_text.pack(fill=tk.BOTH, expand=True)
        self.tab_control.add(self.tab_info, text="Request Info")

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

    def update_ui_for_method(self, event=None):
        """Обновляет интерфейс в зависимости от выбранного метода"""
        method = self.method_var.get()
        if method in ["POST", "PUT", "PATCH"]:
            self.body_text.configure(state='normal')
        else:
            self.body_text.configure(state='disabled')

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

            # Отображаем ответ
            try:
                json_data = response.json()
                formatted_json = json.dumps(json_data, indent=2, ensure_ascii=False)
                self.response_text.insert(tk.INSERT, formatted_json)
            except ValueError:
                self.response_text.insert(tk.INSERT, response.text)

            # Отображаем headers
            formatted_headers = json.dumps(dict(response.headers), indent=2, ensure_ascii=False)
            self.headers_text.insert(tk.INSERT, formatted_headers)

            # Отображаем информацию о запросе
            request_info = {
                "URL": url,
                "Method": method,
                "Status Code": response.status_code,
                "Encoding": response.encoding,
                "Elapsed Time": str(response.elapsed),
                "Request Body": body if body else "None"
            }
            formatted_info = json.dumps(request_info, indent=2, ensure_ascii=False)
            self.info_text.insert(tk.INSERT, formatted_info)

            self.status_var.set(f"{method} request completed. Status: {response.status_code}")

        except Exception as e:
            messagebox.showerror("Error", f"Request failed: {str(e)}")
            self.status_var.set("Request failed")
        finally:
            # Делаем текстовые поля только для чтения
            self.response_text.configure(state='disabled')
            self.headers_text.configure(state='disabled')
            self.info_text.configure(state='disabled')

    def clear_all_tabs(self):
        """Очищает все текстовые поля"""
        for text_widget in [self.response_text, self.headers_text, self.info_text]:
            text_widget.configure(state='normal')
            text_widget.delete(1.0, tk.END)


if __name__ == "__main__":
    root = tk.Tk()
    app = APIViewerApp(root)
    root.mainloop()