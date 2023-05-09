import os
import requests
import subprocess
from tkinter import Tk, Label, StringVar, Entry, Button, messagebox
from tkinter.filedialog import askdirectory
from threading import Thread

class Application:
    def __init__(self, root):
        self.root = root
        root.title("AutoGPT Installer")
        root_width = 300
        root_height = 125
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        x = (screen_width // 2) - (root_width // 2)
        y = (screen_height // 2) - (root_height // 2)
        root.geometry(f"{root_width}x{root_height}+{x}+{y}")
        self.message_var = StringVar()
        self.message_label = Label(self.root, textvariable=self.message_var)
        self.message_label.pack()

        self.setup_button = Button(self.root, text="Setup Application", command=self.setup_app)
        self.setup_button.pack()

    def setup_app(self):
        self.directory = askdirectory(title="Please select the directory where you want to clone the repository")
        
        if os.path.exists(os.path.join(self.directory, 'Auto-GPT')):
            messagebox.showerror("Error", "An installation already exists in the selected directory.")
            return

        self.entry = Entry(self.root)
        self.entry.pack()
        self.button = Button(self.root, text="Submit API Key and Start Installation", command=self.start_process)
        self.button.pack()
        
        self.root.bind('<Return>', lambda event: self.start_process())
        self.setup_button['state'] = 'disabled'

    def start_process(self):
        self.api_key = self.entry.get()
        self.button['state'] = 'disabled'
        self.entry['state'] = 'disabled'

        Thread(target=self.installation_process).start()

    def installation_process(self):
        repo_url = "https://github.com/Significant-Gravitas/Auto-GPT.git"

        if not os.path.exists(self.directory):
            os.makedirs(self.directory)

        os.chdir(self.directory)

        self.message_var.set("Cloning the repository...")
        self.root.update()

        response = requests.get("https://api.github.com/repos/Significant-Gravitas/Auto-GPT/releases/latest")
        release = response.json()
        tag_name = release['tag_name']

        subprocess.check_call(["git", "clone", f"{repo_url}", "--branch", tag_name, "--depth", "1"])

        os.chdir("Auto-GPT")

        os.rename('.env.template', '.env')

        with open('.env', 'r') as file:
            lines = file.readlines()

        with open('.env', 'w') as file:
            for line in lines:
                if line.startswith('OPENAI_API_KEY'):
                    file.write(f'OPENAI_API_KEY={self.api_key}\n')
                else:
                    file.write(line)

        self.message_var.set("Installation completed!")

        os.system('start cmd /k "cd ' + self.directory + '/Auto-GPT & pip install -r requirements.txt & python -m autogpt"')

root = Tk()
app = Application(root)
root.mainloop()
