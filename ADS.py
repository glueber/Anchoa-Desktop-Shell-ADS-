import tkinter as tk
from tkinter import messagebox
import subprocess
import time

def execute_command(command):
    try:
        resultado = subprocess.run(command, shell=True, capture_output=True, text=True)
        if resultado.returncode == 0:
            return resultado.stdout.strip()
        else:
            return f"Error: {resultado.stderr.strip()}"
    except Exception as e:
        return f"Error: {str(e)}"

def update_system_stats():
    kernel = execute_command("uname -r")
    uptime = execute_command("uptime -p 2>/dev/null || echo 'Uptime utility missing'")
    memory = execute_command("free -h | awk '/^Mem:/ {print $3 \" / \" $2}'")
    
    stats_text = f"OS: Anchoa Linux v1.1\nKernel: {kernel}\n{uptime}\nRAM Usage: {memory}"
    lbl_info.config(text=stats_text)
    root.after(5000, update_system_stats)

def open_terminal():
    subprocess.Popen(["xterm"])

def install_package():
    package = entry_package.get().strip()
    if not package:
        messagebox.showwarning("Warning", "Please enter a package name.")
        return
    
    lbl_status.config(text=f"Enpacking {package}... Please wait...", fg="yellow")
    root.update_idletasks()
    
    command = f"/usr/local/bin/latilla install {package}"
    result = execute_command(command)
    
    lbl_status.config(text="Operation completed", fg="white")
    messagebox.showinfo("Latilla Package Manager", result)
    entry_package.delete(0, tk.END)

def poweroff_system():
    if messagebox.askyesno("Power Off", "Shut down Anchoa OS?"):
        execute_command("poweroff")

def reboot_system():
    if messagebox.askyesno("Reboot", "Restart Anchoa OS?"):
        execute_command("reboot")

root = tk.Tk()
root.title("Anchoa Desktop Shell")

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
root.geometry(f"{screen_width}x{screen_height}+0+0")
root.configure(bg="#008080")

root.overrideredirect(True)

lbl_banner = tk.Label(
    root, 
    text="🐟 ANCHOA OPERATING SYSTEM 🐟", 
    fg="#00FFFF", 
    bg="#008080", 
    font=("Courier", 26, "bold")
)
lbl_banner.pack(pady=40)

frame_main = tk.Frame(root, bg="#008080")
frame_main.pack(expand=True)

frame_info = tk.LabelFrame(frame_main, text=" System Status ", fg="white", bg="#008080", font=("Arial", 11, "bold"), bd=3)
frame_info.pack(padx=20, pady=15, fill="x")

lbl_info = tk.Label(frame_info, text="Loading hardware metrics...", fg="#00FFFF", bg="#008080", font=("Courier", 12), justify="left")
lbl_info.pack(padx=20, pady=20)

frame_software = tk.LabelFrame(frame_main, text=" Latilla Package Manager (GUI) ", fg="white", bg="#008080", font=("Arial", 11, "bold"), bd=3)
frame_software.pack(padx=20, pady=15, fill="x")

lbl_instalar = tk.Label(frame_software, text="Enter the package name to build:", fg="white", bg="#008080", font=("Arial", 10))
lbl_instalar.pack(pady=10)

entry_package = tk.Entry(frame_software, font=("Arial", 12), width=30, bd=3)
entry_package.pack(pady=5)

btn_install = tk.Button(frame_software, text="📦 Enpack Application", command=install_package, bg="#4CAF50", fg="white", font=("Arial", 11, "bold"), padx=10, pady=5)
btn_install.pack(pady=10)

lbl_status = tk.Label(frame_software, text="", fg="white", bg="#008080", font=("Arial", 10, "italic"))
lbl_status.pack()

frame_shortcuts = tk.LabelFrame(frame_main, text=" System Tools ", fg="white", bg="#008080", font=("Arial", 11, "bold"), bd=3)
frame_shortcuts.pack(padx=20, pady=15, fill="x")

btn_term = tk.Button(frame_shortcuts, text="💻 Open Terminal (Xterm)", command=open_terminal, bg="#333333", fg="white", font=("Arial", 10, "bold"), padx=10, pady=5)
btn_term.pack(pady=15)

frame_bar = tk.Frame(root, bg="#333333", height=40)
frame_bar.pack(side="bottom", fill="x")

btn_reboot = tk.Button(frame_bar, text="🔄 Reboot", command=reboot_system, bg="#ff9800", fg="black", font=("Arial", 10, "bold"), bd=0, padx=15)
btn_reboot.pack(side="left", fill="y")

btn_poweroff = tk.Button(frame_bar, text="🛑 Power Off", command=poweroff_system, bg="#f44336", fg="white", font=("Arial", 10, "bold"), bd=0, padx=15)
btn_poweroff.pack(side="left", fill="y")

def update_clock():
    current_time = time.strftime("%H:%M:%S")
    lbl_clock.config(text=current_time)
    lbl_clock.after(1000, update_clock)

lbl_clock = tk.Label(frame_bar, text="", fg="white", bg="#333333", font=("Courier", 12, "bold"), padx=20)
lbl_clock.pack(side="right", fill="y")

update_system_stats()
update_clock()

root.mainloop()