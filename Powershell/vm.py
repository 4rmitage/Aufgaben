import tkinter as tk
from tkinter import messagebox
import subprocess

class VMCreator:
    def __init__(self, root):
        self.root = root
        self.root.title("Hyper-V VM Creator")
        self.root.geometry("400x400")

        # UI Elemente für VM-Einstellungen
        self.create_widgets()

    def create_widgets(self):
        # VM Name
        self.label_name = tk.Label(self.root, text="VM Name:")
        self.label_name.pack(pady=5)
        self.entry_name = tk.Entry(self.root)
        self.entry_name.pack(pady=5)

        # Arbeitsspeicher (in GB)
        self.label_memory = tk.Label(self.root, text="Memory Size (in GB):")
        self.label_memory.pack(pady=5)
        self.entry_memory = tk.Entry(self.root)
        self.entry_memory.pack(pady=5)

        # Anzahl der CPUs
        self.label_cpu = tk.Label(self.root, text="Number of CPUs:")
        self.label_cpu.pack(pady=5)
        self.entry_cpu = tk.Entry(self.root)
        self.entry_cpu.pack(pady=5)

        # Button für VM-Erstellung
        self.button_create = tk.Button(self.root, text="Create VM", command=self.create_vm)
        self.button_create.pack(pady=20)

    def create_vm(self):
        # Eingabewerte abfragen
        vm_name = self.entry_name.get()
        memory_size = self.entry_memory.get()
        cpu_count = self.entry_cpu.get()

        # Überprüfen, ob alle Eingabefelder ausgefüllt sind und gültig sind
        if not vm_name or not memory_size or not cpu_count:
            messagebox.showerror("Input Error", "Please fill in all fields.")
            return

        try:
            memory_size = int(memory_size)  # Speicher in Integer umwandeln
            cpu_count = int(cpu_count)  # CPU Anzahl in Integer umwandeln
        except ValueError:
            messagebox.showerror("Input Error", "Memory and CPU count must be integers.")
            return

        # PowerShell-Skript zur VM-Erstellung
        powershell_script = f'''
        New-VM -Name "{vm_name}" -MemoryStartupBytes {memory_size}GB -NewVHDPath "C:\\VMs\\{vm_name}.vhdx" -NewVHDSizeBytes 60GB
        Set-VM -Name "{vm_name}" -ProcessorCount {cpu_count}
        Set-VM -Name "{vm_name}" -BootDevice CD
        '''

        # PowerShell-Befehl ausführen
        try:
            subprocess.run(["powershell", "-Command", powershell_script], check=True)
            messagebox.showinfo("VM Created", f"VM '{vm_name}' created successfully!")
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Error", f"Error creating VM: {e}")
        
# Main Function
if __name__ == "__main__":
    root = tk.Tk()
    app = VMCreator(root)
    root.mainloop()