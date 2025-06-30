import tkinter as tk
from tkinter import filedialog, messagebox
import subprocess

class HyperVVMCreator:
    def __init__(self, root):
        self.root = root
        self.root.title("Hyper-V VM Creator")
        self.root.geometry("400x400")

        # UI Elemente
        self.create_widgets()

    def create_widgets(self):
        # PC Name
        self.label_pcname = tk.Label(self.root, text="PC Name:")
        self.label_pcname.pack(pady=5)
        self.entry_pcname = tk.Entry(self.root)
        self.entry_pcname.pack(pady=5)

        # IP Address
        self.label_ip = tk.Label(self.root, text="Static IP Address:")
        self.label_ip.pack(pady=5)
        self.entry_ip = tk.Entry(self.root)
        self.entry_ip.pack(pady=5)

        # Remote Control
        self.label_remote = tk.Label(self.root, text="Enable Remote Control:")
        self.label_remote.pack(pady=5)
        self.var_remote = tk.BooleanVar()
        self.checkbox_remote = tk.Checkbutton(self.root, variable=self.var_remote)
        self.checkbox_remote.pack(pady=5)

        # Image File Selection
        self.label_image = tk.Label(self.root, text="Select Windows Image File:")
        self.label_image.pack(pady=5)
        self.button_browse = tk.Button(self.root, text="Browse", command=self.browse_image)
        self.button_browse.pack(pady=5)

        # Start VM Creation Button
        self.button_create = tk.Button(self.root, text="Create VM", command=self.create_vm)
        self.button_create.pack(pady=20)

        # Initialize variables
        self.image_path = None

    def browse_image(self):
        # Image-Datei auswählen
        self.image_path = filedialog.askopenfilename(filetypes=[("ISO Files", "*.iso")])
        if self.image_path:
            messagebox.showinfo("Image Selected", f"Selected Image: {self.image_path}")

    def create_vm(self):
        # Hier sammeln wir alle Eingaben
        pcname = self.entry_pcname.get()
        ip_address = self.entry_ip.get()
        remote_enabled = self.var_remote.get()

        if not pcname or not ip_address or not self.image_path:
            messagebox.showerror("Input Error", "Please fill all fields and select an image file.")
            return

        # VM-Erstellungs-Befehl in PowerShell
        powershell_script = f'''
        New-VM -Name "{pcname}" -MemoryStartupBytes 2GB -NewVHDPath "C:\\VMs\\{pcname}.vhdx" -NewVHDSizeBytes 60GB
        Set-VM -Name "{pcname}" -ProcessorCount 2
        Set-VMNetworkAdapter -VMName "{pcname}" -StaticMacAddress "00-15-5D-12-34-56"
        Set-VM -Name "{pcname}" -BootDevice CD
        Set-VMDvdDrive -VMName "{pcname}" -Path "{self.image_path}"
        '''

        # Remote Control Aktivieren
        if remote_enabled:
            powershell_script += f'''
            Enable-PSRemoting -Force
            '''

        # PowerShell-Skript ausführen
        try:
            subprocess.run(["powershell", "-Command", powershell_script], check=True)
            messagebox.showinfo("VM Created", f"VM '{pcname}' created successfully!")
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Error", f"Error creating VM: {e}")

# Main Function
if __name__ == "__main__":
    root = tk.Tk()
    app = HyperVVMCreator(root)
    root.mainloop()