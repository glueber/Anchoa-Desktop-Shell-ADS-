#!/usr/bin/env python3
import tkinter as tk
from tkinter import messagebox
import subprocess
import time
import os

class AnchoaDE:
    def __init__(self, root):
        self.root = root
        self.root.title("Anchoa Desktop Shell")
        
        self.root.attributes('-topmost', True)
        self.root.configure(bg="#1e1e2e")
        self.root.overrideredirect(True)
        
        width = self.root.winfo_screenwidth()
        height = self.root.winfo_screenheight()
        
        if width <= 1024:
            width = 1280
            height = 720
            
        self.root.geometry(f"{width}x{height}+0+0")

        self.bg_panel = "#11111b"
        self.accent_color = "#00f5d4"
        self.text_color = "#cdd6f4"
        self.alert_color = "#ff6b6b"

        self.create_top_panel()
        self.create_main_content()
        self.create_bottom_dock()
        
        self.update_clock()
        self.update_stats()

    def create_top_panel(self):
        self.top_panel = tk.Frame(self.root, bg=self.bg_panel, height=40, bd=0)
        self.top_panel.pack(fill="x", side="top")
        self.top_panel.pack_propagate(False)

        self.logo_label = tk.Label(self.top_panel, text=" 🐟 ANCHOA DE v1.0", font=("Courier", 12, "bold"), bg=self.bg_panel, fg=self.accent_color)
        self.logo_label.pack(side="left", padx=15)

        self.ram_label = tk.Label(self.top_panel, text="RAM: Oculto MB", font=("Courier", 11), bg=self.bg_panel, fg=self.text_color)
        self.ram_label.pack(side="left", padx=20)

        self.clock_label = tk.Label(self.top_panel, text="", font=("Courier", 12, "bold"), bg=self.bg_panel, fg=self.accent_color)
        self.clock_label.pack(side="right", padx=15)

    def create_main_content(self):
        self.center_frame = tk.Frame(self.root, bg="#1e1e2e")
        self.center_frame.place(relx=0.5, rely=0.45, anchor="center")

        title_box = tk.Label(self.center_frame, text="─── LATILLA PACKAGE MANAGER ───", font=("Courier", 14, "bold"), bg="#1e1e2e", fg=self.accent_color)
        title_box.pack(pady=10)

        subtitle = tk.Label(self.center_frame, text="Enter a package name to enpack from Debian mirrors:", font=("Courier", 10), bg="#1e1e2e", fg=self.text_color)
        subtitle.pack(pady=5)

        self.package_entry = tk.Entry(self.center_frame, font=("Courier", 14), bg=self.bg_panel, fg=self.accent_color, insertbackground=self.accent_color, bd=2, relief="flat", width=30, justify="center")
        self.package_entry.pack(pady=10, ipady=5)
        self.package_entry.focus_set()

        btn_install = tk.Button(self.center_frame, text="[ ENPACK APPLICATION ]", font=("Courier", 11, "bold"), bg=self.bg_panel, fg=self.accent_color, activebackground=self.accent_color, activeforeground=self.bg_panel, bd=1, relief="solid", command=self.run_latilla)
        btn_install.pack(pady=10, ipadx=10, ipady=5)

    def create_bottom_dock(self):
        self.dock = tk.Frame(self.root, bg=self.bg_panel, height=50, bd=1, relief="solid", highlightbackground=self.accent_color)
        self.dock.pack(side="bottom", pady=20, ipadx=10)

        def quick_btn(text, cmd, color):
            return tk.Button(self.dock, text=text, font=("Courier", 10, "bold"), bg=self.bg_panel, fg=color, activebackground=color, activeforeground=self.bg_panel, bd=0, cursor="hand2", command=cmd)

        quick_btn(" >_ Terminal ", self.open_terminal, self.accent_color).pack(side="left", padx=10, pady=5)
        quick_btn(" 󰍉 Top ", lambda: self.open_app_in_terminal("htop"), self.text_color).pack(side="left", padx=10, pady=5)
        
        tk.Label(self.dock, text="|", bg=self.bg_panel, fg="#45475a").pack(side="left", padx=5)

        quick_btn(" 󰐥 Reboot ", self.sys_reboot, self.text_color).pack(side="left", padx=10, pady=5)
        quick_btn(" 󰐥 Poweroff ", self.sys_poweroff, self.alert_color).pack(side="left", padx=10, pady=5)

    def run_latilla(self):
        package = self.package_entry.get().strip()
        if not package:
            messagebox.showwarning("Warning", "Please type a package name first.")
            return

        xterm_command = [
            "xterm", 
            "-title", f"Latilla Installer: {package}",
            "-bg", self.bg_panel, "-fg", self.accent_color,
            "-fa", "Monospace", "-fs", "11",
            "-e", "bash", "-c", f"/usr/local/bin/latilla install {package}; echo -e '\\n─── Process finished. Press ENTER to close ───'; read"
        ]

        try:
            subprocess.Popen(xterm_command)
            self.package_entry.delete(0, tk.END)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to launch installer:\n{e}")

    def open_terminal(self):
        subprocess.Popen(["xterm", "-bg", self.bg_panel, "-fg", self.accent_color, "-fa", "Monospace", "-fs", "11"])

    def open_app_in_terminal(self, app_name):
        subprocess.Popen(["xterm", "-bg", self.bg_panel, "-fg", self.text_color, "-fa", "Monospace", "-fs", "11", "-e", app_name])

    def update_clock(self):
        current_time = time.strftime(" %Y-%m-%d  %H:%M:%S ")
        self.clock_label.config(text=current_time)
        self.root.after(1000, self.update_clock)

    def update_stats(self):
        try:
            with open('/proc/meminfo', 'r') as f:
                lines = f.readlines()
            mem_total = int(lines[0].split()[1])
            mem_free = int(lines[1].split()[1])
            mem_cached = int(lines[4].split()[1])
            mem_used = (mem_total - mem_free - mem_cached) // 1024
            self.ram_label.config(text=f"RAM: {mem_used} MB")
        except:
            self.ram_label.config(text="RAM: Error")
        self.root.after(5000, self.update_stats)

    def sys_reboot(self):
        if messagebox.askyesno("Reboot", "Are you sure you want to reboot the system?"):
            os.system("sudo reboot")

    def sys_poweroff(self):
        if messagebox.askyesno("Poweroff", "Are you sure you want to power off?"):
            os.system("sudo poweroff")

if __name__ == "__main__":
    root = tk.Tk()
    app = AnchoaDE(root)
    root.mainloop()
