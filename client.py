import pickle
from base64 import b64encode
import json
import xml.etree.ElementTree as ET
from cryptography.fernet import Fernet
import tkinter as tk
import requests


class ClientGUI:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Client")
        self.format_var = tk.StringVar()
        self.encrypt_var = tk.BooleanVar()
        self.dict_var = tk.StringVar()

        tk.Label(self.window, text="Pickling format:").pack()
        tk.OptionMenu(self.window, self.format_var, "binary", "json", "xml").pack()
        tk.Checkbutton(self.window, text="Encrypt file", variable=self.encrypt_var).pack()
        tk.Label(self.window, text="Dictionary:").pack()
        tk.Entry(self.window, textvariable=self.dict_var).pack()
        tk.Button(self.window, text="Send file", command=self.send_file).pack()

        self.window.mainloop()

    def serialize_dict(self, format, my_dict):
        if format == "binary":
            serialized_data = pickle.dumps(my_dict)
        elif format == "json":
            serialized_data = json.dumps(my_dict).encode()
        elif format == "xml":
            root = ET.Element("root")
            for key, value in my_dict.items():
                child = ET.Element(key)
                child.text = str(value)
                root.append(child)
            serialized_data = ET.tostring(root)
        return serialized_data

    def create_encrypted_file(self, data):
        key = Fernet.generate_key()
        f = Fernet(key)
        encrypted_data = f.encrypt(data)
        return encrypted_data, key

    def send_file_data(self, host, port, format, serialized_data, key=None):
        url = f'http://{host}:{port}/upload'
        payload = {'format': format, 'file_content': b64encode(serialized_data).decode()}
        if key:
            payload['key'] = key.decode()
        print(f"Sending POST request to {url}: {payload}")
        response = requests.post(url, json=payload)
        return response.status_code

    def send_file(self):
        format = self.format_var.get()
        encrypt = self.encrypt_var.get()
        my_dict = eval(self.dict_var.get())
        serialized_data = self.serialize_dict(format, my_dict)
        if encrypt:
            encrypted_data, key = self.create_encrypted_file(serialized_data)
            self.send_file_data("localhost", 1234, format, encrypted_data, key)
        else:
            self.send_file_data("localhost", 1234, format, serialized_data)


if __name__ == "__main__":
    ClientGUI()