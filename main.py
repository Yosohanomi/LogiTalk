from customtkinter import *
import base64
import io
from socket import socket, AF_INET, SOCK_STREAM
import threading
from PIL import Image

class MainWindow(CTk):
    def __init__(self):
        super().__init__()
        self.geometry("800x500")

        self.frame = CTkFrame(self, width=30, height=300)
        self.frame.pack_propagate(False)
        self.frame.place(x=0, y=0)
        self.is_show_menu = False
        self.frame_width = 0
        self.username = 'Sophia'



        self.theme = None
        self.btn = CTkButton(self, text='>>',  width=30, command = self.toggle_show_menu)
        self.btn.place(x=0, y=0)
        self.menu_show_speed=20
        self.speed_animate_menu = -20

        self.chat_field = CTkScrollableFrame(self)
        self.chat_field.place(x=0, y=0)
        self.btn_show_image = CTkButton(self, text='Open', height=40, width=50, command=self.open_image)
        self.btn_show_image.place(x=0, y=0)

        self.message_input = CTkEntry(self, placeholder_text='Введіть повідомлення: ', height=40)
        self.message_input.place(x=0, y=250)
        self.button_send = CTkButton(self, text=">>", width=50, height=40, command= self.send_message)
        self.button_send.place(x=200, y=250)
        self.arrow = CTkImage(Image.open('arrow.png'), size=(20, 20))

        self.adaptive_ui()
        self.add_message("Демонстрація відображення зображення:", CTkImage(Image.open('cat.jpg'), size=(300, 300)))
        try:
            self.sock = socket(AF_INET, SOCK_STREAM)
            self.sock.connect(('4.tcp.eu.ngrok.io', 18569))
            hello = f'TEXT@{self.username}@[SYSTEM] {self.username} приєднався(лась) до чату! \n'
            self.sock.send(hello.encode('utf-8'))
            threading.Thread(target=self.recv_message, daemon=True).start()
        except Exception as e:
            self.add_message(f'Не вдалося підключитися до сервера: {e}')

    def change_theme(self, choice):
        if choice == "Світла":
            self.configure(fg_color="#f0f0f0")
            self.frame.configure(fg_color="#ffffff")
            self.chat_field.configure(fg_color="#fafafa")
            self.message_input.configure(fg_color="#ffffff", text_color="#000000", placeholder_text_color="#666666")

            try:
                self.label.configure(text_color="#000000")
                self.entry.configure(fg_color="#ffffff", text_color="#000000")
            except:
                pass

            for message_frame in self.chat_field.winfo_children():
                message_frame.configure(fg_color="#e0e0e0")
                for label in message_frame.winfo_children():
                    label.configure(text_color="#000000")
        else:
            self.configure(fg_color="#2b2b2b")
            self.frame.configure(fg_color="#1f1f1f")
            self.chat_field.configure(fg_color="#333333")
            self.message_input.configure(fg_color="#343638", text_color="#ffffff", placeholder_text_color="#a0a0a0")

            try:
                self.label.configure(text_color="#ffffff")
                self.entry.configure(fg_color="#343638", text_color="#ffffff")
            except:
                pass

            for message_frame in self.chat_field.winfo_children():
                message_frame.configure(fg_color="#404040")
                for label in message_frame.winfo_children():
                    label.configure(text_color="#ffffff")
    def save_name(self):
        new_name = self.entry.get().strip()
        if new_name:
            self.username = new_name
            self.add_message(f"Ваш новий нік: {self.username}")

    def toggle_show_menu(self):
        if self.is_show_menu:
            self.speed_animate_menu *= -1
            self.btn.configure(text=">>")
            self.is_show_menu = False
            self.show_menu()
        else:
            self.speed_animate_menu *= -1
            self.btn.configure(text="<<")
            self.is_show_menu = True
            self.show_menu()
            self.label = CTkLabel(self.frame, text='Ваше ім`я: ')
            self.label.pack(pady=30)
            self.entry = CTkEntry(self.frame)
            self.entry.pack(pady=30)
            self.label_theme = CTkOptionMenu(self.frame, values=['Темна', 'Світла'], command=self.change_theme)
            self.theme = "Темна"
            self.label_theme.pack(side='bottom', pady=20)
            self.btn_add_name = CTkButton(self.frame, text='Зберегти', command=self.save_name)
            self.btn_add_name.pack()
    def show_menu(self):
        self.frame.configure(width=self.frame.winfo_width() + self.speed_animate_menu)
        if not self.frame.winfo_width() >= 200 and self.is_show_menu:
            self.after(10, self.show_menu)
        elif self.frame.winfo_width() >= 40 and not self.is_show_menu:
            self.after(10, self.show_menu)
            if self.label and self.entry:
                self.label.destroy()
                self.entry.destroy()
                self.label_theme.destroy()
                self.btn_add_name.destroy()
    def close_menu(self):
        if self.frame_width >= 0:
            self.frame_width -= self.menu_show_speed
            self.frame.configure(width=self.frame_width)
            if self.frame_width >= 30:
                self.btn.configure(width=self.frame_width, text='>>')
        if not self.is_show_menu:
            self.after(20, self.close_menu)
    def adaptive_ui(self):
        self.frame.configure(height=self.winfo_height())
        self.chat_field.place(x=self.frame.winfo_width())
        self.chat_field.configure(width = self.winfo_width()-self.frame.winfo_width()-20,
                                  height=self.winfo_height()-40)
        self.btn_show_image.place(x=self.winfo_width()-105,  y=self.button_send.winfo_y())
        self.button_send.place(x=self.winfo_width()-50, y=self.winfo_height()-40)
        self.message_input.place(x=self.frame.winfo_width(), y=self.button_send.winfo_y())
        self.message_input.configure(width=self.winfo_width()-self.frame.winfo_width()- self.button_send.winfo_width() - self.btn_show_image.winfo_width() - 10)

        self.after(50, self.adaptive_ui)
    def add_message(self, message, img=None):
        message_frame = CTkFrame(self.chat_field, fg_color='grey')
        message_frame.pack(pady=5, anchor='w')
        wrapleng_size = self.winfo_width() - self.frame.winfo_width() - 40
        if not img:
            CTkLabel(message_frame, text=message, wraplength=wrapleng_size,
                     text_color='white', justify='left').pack(pady=5, padx=10)

        else:
            CTkLabel(message_frame, text=message, wraplength=wrapleng_size,
                     text_color='white', image=img, compound='top', justify='left').pack(pady=5, padx=10)

    def send_message(self):
        message = self.message_input.get()
        if message:
            self.add_message(f"{self.username}: {message}")
            data = f"TEXT@{self.username}@{message}\n"
            try:
                self.sock.sendall(data.encode())
            except:
                pass
            self.message_input.delete(0, END)

    def recv_message(self):
        buffer = ""
        while True:
            try:
                chunk = self.sock.recv(4096)
                if not chunk:
                    break
                buffer += chunk.decode('utf-8', errors='ignore')

                while "\n" in buffer:
                    line, buffer = buffer.split('\n', 1)
                    self.handle_line(line.strip())
            except:
                break
            self.sock.close()
    def handle_line(self, line):
        if not line:
            return
        parts = line.split("@", 3)
        msg_type = parts[0]
        if len(parts) >= 3:
            author = parts[1]
            message = parts[2]
            self.add_message(f"{author}: {message}")
        elif msg_type == 'IMAGE':
            if len(parts) >= 4:
                author = parts[1]
                message = parts[2]
                b64_image = parts[3]
                try:
                    img_data = base64.b64decode(b64_image)
                    pil_img = Image.open(io.BytesIO(img_data))
                    ctk_img = CTkImage(pil_img, size=(300, 300))
                    self.add_message(f"{author} надіслав(ла) зображення: {filename}", img=ctk_img)
                except Exception as e:
                    self.add_message(f"Помилка відображення зображення: {e}")
            else:
                self.add_message(line)
    def open_image(self):
        file_name = filedialog.askopenfilename()
        if not file_name:
            return
        try:
            with open(file_name, "rb") as f:
                raw = f.read()
            b64_data = base64.b64encode(raw).decode()
            short_name = os.path.basename(file_name)
            data = f"IMAGE@{self.username}@{short_name}@{b64_data}\n"
            self.sock.sendall(data.encode())
            self.add_message( '', CTkImage(light_image=Image.open(file_name), size=(300, 300)))
        except Exception as e:
            self.add_message(f"Не вдалося завантажити зображення: {e}")



win = MainWindow()
win.mainloop()
