import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
import subprocess

class HyperVVMCreator:
    def __init__(self, root):
        self.root = root
        self.root.title("Hyper-V VM Ersteller")
        self.root.geometry("400x450")
        
        # Name der VM
        self.vm_name_label = tk.Label(root, text="VM Name:")
        self.vm_name_label.pack(pady=5)
        self.vm_name_entry = tk.Entry(root)
        self.vm_name_entry.pack(pady=5)

        # CPU Anzahl
        self.cpu_label = tk.Label(root, text="Anzahl CPUs:")
        self.cpu_label.pack(pady=5)
        self.cpu_entry = tk.Entry(root)
        self.cpu_entry.pack(pady=5)

        # RAM Größe
        self.ram_label = tk.Label(root, text="RAM (MB):")
        self.ram_label.pack(pady=5)
        self.ram_entry = tk.Entry(root)
        self.ram_entry.pack(pady=5)

        # Festplatte Pfad Auswahl
        self.disk_label = tk.Label(root, text="Festplatte (Pfad zur VHD):")
        self.disk_label.pack(pady=5)
        self.disk_button = tk.Button(root, text="VHD auswählen", command=self.select_disk_path)
        self.disk_button.pack(pady=5)
        self.disk_path_label = tk.Label(root, text="Kein Pfad ausgewählt")
        self.disk_path_label.pack(pady=5)

        # Betriebssystem ISO Auswahl
        self.iso_label = tk.Label(root, text="Betriebssystem ISO (Pfad):")
        self.iso_label.pack(pady=5)
        self.iso_button = tk.Button(root, text="ISO auswählen", command=self.select_iso_path)
        self.iso_button.pack(pady=5)
        self.iso_path_label = tk.Label(root, text="Kein Pfad ausgewählt")
        self.iso_path_label.pack(pady=5)

        # VM erstellen Button
        self.create_button = tk.Button(root, text="VM Erstellen", command=self.create_vm)
        self.create_button.pack(pady=20)

        # Pfade speichern
        self.disk_path = ""
        self.iso_path = ""

    def select_disk_path(self):
        # Datei-Dialog für Festplatten-Pfad (VHD)
        self.disk_path = filedialog.asksaveasfilename(defaultextension=".vhd", filetypes=[("VHD Dateien", "*.vhd")])
        if self.disk_path:
            self.disk_path_label.config(text=self.disk_path)

    def select_iso_path(self):
        # Datei-Dialog für ISO-Dateipfad
        self.iso_path = filedialog.askopenfilename(filetypes=[("ISO Dateien", "*.iso")])
        if self.iso_path:
            self.iso_path_label.config(text=self.iso_path)

    def create_vm(self):
        vm_name = self.vm_name_entry.get()
        cpu_count = self.cpu_entry.get()
        ram_size = self.ram_entry.get()

        # Überprüfen, ob alle Felder ausgefüllt sind
        if not vm_name or not cpu_count or not ram_size or not self.disk_path or not self.iso_path:
            messagebox.showerror("Fehler", "Bitte fülle alle Felder aus und wähle alle Pfade aus!")
            return

        # PowerShell Befehl zum Erstellen der VM
        ps_script = f"""
        New-VM -Name '{vm_name}' -MemoryStartupBytes {int(ram_size) * 1024 * 1024} -Generation 2 -Path 'C:\\VMs\\'
        Set-VMProcessor -VMName '{vm_name}' -Count {cpu_count}
        New-VHD -Path '{self.disk_path}' -SizeBytes 40GB -Dynamic
        Add-VMHardDiskDrive -VMName '{vm_name}' -Path '{self.disk_path}'
        Set-VMDVDDrive -VMName '{vm_name}' -Path '{self.iso_path}'
        Start-VM -Name '{vm_name}'
        """

        try:
            # Ausführen des PowerShell-Skripts
            result = subprocess.run(["powershell", "-Command", ps_script], capture_output=True, text=True)

            # Überprüfen, ob der Befehl erfolgreich war
            if result.returncode == 0:
                messagebox.showinfo("Erfolg", f"VM '{vm_name}' wurde erfolgreich erstellt!")
            else:
                messagebox.showerror("Fehler", f"Fehler beim Erstellen der VM: {result.stderr}")
        except Exception as e:
            messagebox.showerror("Fehler", f"Es gab ein Problem bei der Ausführung: {str(e)}")

# Tkinter Fenster erstellen und starten
if __name__ == "__main__":
    root = tk.Tk()
    app = HyperVVMCreator(root)
    root.mainloop()