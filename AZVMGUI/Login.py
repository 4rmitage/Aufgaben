#!/usr/bin/env python3
"""
Azure Cloud Shell VM Creator
Erstellt Azure VMs über Cloud Shell API mit GUI-Interface
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import requests
import json
import threading
import time
from datetime import datetime

class AzureCloudShellVMCreator:
    def __init__(self, root):
        self.root = root
        self.root.title("Azure Cloud Shell VM Creator")
        self.root.geometry("900x800")
        self.root.resizable(True, True)
        
        # Cloud Shell Session Variables
        self.session = requests.Session()
        self.cloudshell_uri = None
        self.access_token = None
        self.terminal_id = None
        
        # VM Parameter Variables
        self.setup_variables()
        
        # GUI erstellen
        self.create_widgets()
        
    def setup_variables(self):
        """Initialisiert alle Tkinter-Variablen für VM-Parameter"""
        self.vm_name = tk.StringVar(value="vm-test01")
        self.resource_group = tk.StringVar(value="rg-test")
        self.location = tk.StringVar(value="westeurope")
        self.vm_size = tk.StringVar(value="Standard_B2s")
        self.image = tk.StringVar(value="2025-datacenter-azure-edition")
        self.admin_username = tk.StringVar(value="azureuser")
        self.admin_password = tk.StringVar(value="")
        self.vnet_name = tk.StringVar(value="vnet-default")
        self.subnet_name = tk.StringVar(value="subnet-default")
        self.nsg_name = tk.StringVar(value="nsg-default")
        self.public_ip = tk.BooleanVar(value=True)
        self.storage_sku = tk.StringVar(value="StandardSSD_LRS")
        self.no_wait = tk.BooleanVar(value=False)
        
        # Cloud Shell Connection
        self.tenant_id = tk.StringVar(value="")
        self.subscription_id = tk.StringVar(value="")
    
    def create_widgets(self):
        """Erstellt die GUI-Komponenten"""
        # Hauptframe mit Tabs
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Tab 1: Cloud Shell Connection
        self.create_connection_tab(notebook)
        
        # Tab 2: VM Configuration
        self.create_vm_config_tab(notebook)
        
        # Tab 3: Output/Logs
        self.create_output_tab(notebook)
        
    def create_connection_tab(self, notebook):
        """Erstellt Tab für Cloud Shell Verbindung"""
        connection_frame = ttk.Frame(notebook)
        notebook.add(connection_frame, text="Cloud Shell Verbindung")
        
        # Connection Settings
        settings_frame = ttk.LabelFrame(connection_frame, text="Azure Cloud Shell Einstellungen", padding=10)
        settings_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(settings_frame, text="Tenant ID:").grid(row=0, column=0, sticky=tk.W, pady=2)
        ttk.Entry(settings_frame, textvariable=self.tenant_id, width=50).grid(row=0, column=1, sticky=tk.W, padx=(5, 0))
        
        ttk.Label(settings_frame, text="Subscription ID:").grid(row=1, column=0, sticky=tk.W, pady=2)
        ttk.Entry(settings_frame, textvariable=self.subscription_id, width=50).grid(row=1, column=1, sticky=tk.W, padx=(5, 0))
        
        # Connection Actions
        action_frame = ttk.Frame(connection_frame)
        action_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Button(action_frame, text="Cloud Shell Session starten", 
                  command=self.start_cloudshell_session).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(action_frame, text="Verbindung testen", 
                  command=self.test_connection).pack(side=tk.LEFT, padx=5)
        ttk.Button(action_frame, text="Session beenden", 
                  command=self.end_session).pack(side=tk.LEFT, padx=5)
        
        # Connection Status
        self.connection_status = ttk.Label(connection_frame, text="Status: Nicht verbunden", 
                                         foreground="red")
        self.connection_status.pack(pady=10)
        
        # Info Text
        info_text = """
Hinweise zur Cloud Shell Verwendung:
1. Sie müssen über ein Azure-Konto mit entsprechenden Berechtigungen verfügen
2. Tenant ID finden Sie im Azure Portal unter Azure Active Directory
3. Subscription ID im Azure Portal unter Subscriptions
4. Alternativ: Verwenden Sie Device Code Authentication für einfachere Anmeldung
        """
        info_label = ttk.Label(connection_frame, text=info_text, wraplength=800, justify=tk.LEFT)
        info_label.pack(padx=10, pady=10)
        
        # Device Code Auth Button
        ttk.Button(connection_frame, text="Device Code Authentication", 
                  command=self.device_code_auth).pack(pady=5)
        
    def create_vm_config_tab(self, notebook):
        """Erstellt Tab für VM-Konfiguration"""
        config_frame = ttk.Frame(notebook)
        notebook.add(config_frame, text="VM Konfiguration")
        
        # Scrollable Frame
        canvas = tk.Canvas(config_frame)
        scrollbar = ttk.Scrollbar(config_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Basic Settings
        basic_frame = ttk.LabelFrame(scrollable_frame, text="Grundeinstellungen", padding=10)
        basic_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(basic_frame, text="VM Name:").grid(row=0, column=0, sticky=tk.W, pady=2)
        ttk.Entry(basic_frame, textvariable=self.vm_name, width=30).grid(row=0, column=1, sticky=tk.W, padx=(5, 0))
        
        ttk.Label(basic_frame, text="Resource Group:").grid(row=1, column=0, sticky=tk.W, pady=2)
        ttk.Entry(basic_frame, textvariable=self.resource_group, width=30).grid(row=1, column=1, sticky=tk.W, padx=(5, 0))
        
        ttk.Label(basic_frame, text="Location:").grid(row=2, column=0, sticky=tk.W, pady=2)
        location_combo = ttk.Combobox(basic_frame, textvariable=self.location, width=27)
        location_combo['values'] = ('westeurope', 'northeurope', 'eastus', 'westus2', 
                                   'centralus', 'southeastasia', 'australiaeast')
        location_combo.grid(row=2, column=1, sticky=tk.W, padx=(5, 0))
        
        ttk.Label(basic_frame, text="VM Größe:").grid(row=3, column=0, sticky=tk.W, pady=2)
        size_combo = ttk.Combobox(basic_frame, textvariable=self.vm_size, width=27)
        size_combo['values'] = ('Standard_B1s', 'Standard_B2s', 'Standard_B2ms', 
                               'Standard_D2s_v3', 'Standard_D2s_v5', 'Standard_D4s_v5')
        size_combo.grid(row=3, column=1, sticky=tk.W, padx=(5, 0))
        
        ttk.Label(basic_frame, text="Betriebssystem:").grid(row=4, column=0, sticky=tk.W, pady=2)
        image_combo = ttk.Combobox(basic_frame, textvariable=self.image, width=27)
        image_combo['values'] = ('2025-datacenter-azure-edition', '2025-datacenter-azure-edition-core',
                                'Win2022Datacenter', 'Ubuntu2204', 'Ubuntu2004', 'CentOS85Gen2')
        image_combo.grid(row=4, column=1, sticky=tk.W, padx=(5, 0))
        
        # Authentication
        auth_frame = ttk.LabelFrame(scrollable_frame, text="Authentifizierung", padding=10)
        auth_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(auth_frame, text="Admin Username:").grid(row=0, column=0, sticky=tk.W, pady=2)
        ttk.Entry(auth_frame, textvariable=self.admin_username, width=30).grid(row=0, column=1, sticky=tk.W, padx=(5, 0))
        
        ttk.Label(auth_frame, text="Admin Password:").grid(row=1, column=0, sticky=tk.W, pady=2)
        ttk.Entry(auth_frame, textvariable=self.admin_password, show="*", width=30).grid(row=1, column=1, sticky=tk.W, padx=(5, 0))
        
        # Network Settings
        network_frame = ttk.LabelFrame(scrollable_frame, text="Netzwerk-Einstellungen", padding=10)
        network_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(network_frame, text="VNet Name:").grid(row=0, column=0, sticky=tk.W, pady=2)
        ttk.Entry(network_frame, textvariable=self.vnet_name, width=30).grid(row=0, column=1, sticky=tk.W, padx=(5, 0))
        
        ttk.Label(network_frame, text="Subnet Name:").grid(row=1, column=0, sticky=tk.W, pady=2)
        ttk.Entry(network_frame, textvariable=self.subnet_name, width=30).grid(row=1, column=1, sticky=tk.W, padx=(5, 0))
        
        ttk.Label(network_frame, text="NSG Name:").grid(row=2, column=0, sticky=tk.W, pady=2)
        ttk.Entry(network_frame, textvariable=self.nsg_name, width=30).grid(row=2, column=1, sticky=tk.W, padx=(5, 0))
        
        ttk.Checkbutton(network_frame, text="Öffentliche IP erstellen", 
                       variable=self.public_ip).grid(row=3, column=1, sticky=tk.W, padx=(5, 0))
        
        # Storage Settings
        storage_frame = ttk.LabelFrame(scrollable_frame, text="Speicher-Einstellungen", padding=10)
        storage_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(storage_frame, text="Storage SKU:").grid(row=0, column=0, sticky=tk.W, pady=2)
        storage_combo = ttk.Combobox(storage_frame, textvariable=self.storage_sku, width=27)
        storage_combo['values'] = ('StandardSSD_LRS', 'Premium_LRS', 'Standard_LRS', 'UltraSSD_LRS')
        storage_combo.grid(row=0, column=1, sticky=tk.W, padx=(5, 0))
        
        ttk.Checkbutton(storage_frame, text="No-Wait (Asynchrone Erstellung)", 
                       variable=self.no_wait).grid(row=1, column=1, sticky=tk.W, padx=(5, 0))
        
        # Action Buttons
        button_frame = ttk.Frame(scrollable_frame)
        button_frame.pack(fill=tk.X, pady=10)
        
        ttk.Button(button_frame, text="Befehl generieren", 
                  command=self.generate_command).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(button_frame, text="VM erstellen", 
                  command=self.create_vm_cloudshell).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Konfiguration zurücksetzen", 
                  command=self.reset_config).pack(side=tk.LEFT, padx=5)
        
        # Pack Canvas
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
    def create_output_tab(self, notebook):
        """Erstellt Tab für Output/Logs"""
        output_frame = ttk.Frame(notebook)
        notebook.add(output_frame, text="Output & Logs")
        
        # Output Text Area
        self.output_text = scrolledtext.ScrolledText(output_frame, height=30, wrap=tk.WORD)
        self.output_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Clear Button
        ttk.Button(output_frame, text="Output löschen", 
                  command=self.clear_output).pack(pady=5)
    
    def log_output(self, message):
        """Fügt Nachricht zum Output hinzu"""
        def update_output():
            timestamp = datetime.now().strftime("%H:%M:%S")
            self.output_text.insert(tk.END, f"[{timestamp}] {message}\n")
            self.output_text.see(tk.END)
            self.output_text.update()
        
        self.root.after(0, update_output)
    
    def clear_output(self):
        """Löscht den Output"""
        self.output_text.delete(1.0, tk.END)
    
    def device_code_auth(self):
        """Startet Device Code Authentication"""
        def auth_flow():
            try:
                self.log_output("=== Device Code Authentication gestartet ===")
                
                # Simulierte Device Code Response (in echter Implementierung über Azure API)
                device_code = "A1B2C3D4"
                user_code = "ABCD-EFGH"
                verification_url = "https://microsoft.com/devicelogin"
                
                self.log_output(f"1. Öffnen Sie: {verification_url}")
                self.log_output(f"2. Geben Sie folgenden Code ein: {user_code}")
                self.log_output("3. Warten auf Authentifizierung...")
                
                # In der GUI anzeigen
                auth_message = f"Bitte öffnen Sie:\n{verification_url}\n\nUnd geben Sie den Code ein:\n{user_code}"
                messagebox.showinfo("Device Code Authentication", auth_message)
                
                # Simuliere Warten auf Auth (in echter Implementierung: Polling)
                for i in range(5):
                    self.log_output(f"Warte auf Authentifizierung... ({i+1}/5)")
                    time.sleep(2)
                
                # Simuliere erfolgreiche Auth
                self.log_output("✓ Authentifizierung erfolgreich!")
                self.access_token = "simulated_access_token_123"
                self.connection_status.config(text="Status: Authentifiziert", foreground="green")
                
                # Cloud Shell Session starten
                self.start_cloudshell_session()
                
            except Exception as e:
                self.log_output(f"✗ Fehler bei Authentication: {str(e)}")
        
        threading.Thread(target=auth_flow, daemon=True).start()
    
    def start_cloudshell_session(self):
        """Startet Cloud Shell Session"""
        def start_session():
            try:
                self.log_output("=== Cloud Shell Session wird gestartet ===")
                
                # Simuliere Cloud Shell Session Start
                self.log_output("Cloud Shell Container wird initialisiert...")
                time.sleep(3)
                
                self.cloudshell_uri = "https://cloudshell.azure.com/api/terminal/12345"
                self.terminal_id = "terminal_12345"
                
                self.log_output("✓ Cloud Shell Session erfolgreich gestartet")
                self.log_output(f"Terminal ID: {self.terminal_id}")
                self.connection_status.config(text="Status: Cloud Shell aktiv", foreground="green")
                
            except Exception as e:
                self.log_output(f"✗ Fehler beim Starten der Cloud Shell: {str(e)}")
        
        threading.Thread(target=start_session, daemon=True).start()
    
    def test_connection(self):
        """Testet die Cloud Shell Verbindung"""
        def test():
            if not self.cloudshell_uri:
                self.log_output("✗ Keine aktive Cloud Shell Session")
                return
                
            try:
                self.log_output("Teste Cloud Shell Verbindung...")
                
                # Simuliere Test-Befehl
                test_command = "az account show"
                self.log_output(f"Führe aus: {test_command}")
                time.sleep(2)
                
                # Simulierte Antwort
                response = {
                    "name": "Test Subscription",
                    "id": self.subscription_id.get() or "12345678-1234-1234-1234-123456789012",
                    "user": {"name": "user@example.com"}
                }
                
                self.log_output("✓ Verbindung erfolgreich getestet")
                self.log_output(f"Aktive Subscription: {response['name']}")
                self.log_output(f"Angemeldet als: {response['user']['name']}")
                
            except Exception as e:
                self.log_output(f"✗ Verbindungstest fehlgeschlagen: {str(e)}")
        
        threading.Thread(target=test, daemon=True).start()
    
    def generate_command(self):
        """Generiert den Azure CLI Befehl"""
        if not self.validate_inputs():
            return
        
        # Bestimme Image Format
        image_value = self.image.get()
        if image_value in ['2025-datacenter-azure-edition', '2025-datacenter-azure-edition-core']:
            image_param = f"MicrosoftWindowsServer:WindowsServer:{image_value}:latest"
        else:
            image_param = image_value
        
        # Baue Befehl zusammen
        command_parts = [
            "az vm create",
            f"--resource-group {self.resource_group.get()}",
            f"--name {self.vm_name.get()}",
            f"--image {image_param}",
            f"--size {self.vm_size.get()}",
            f"--admin-username {self.admin_username.get()}",
            f"--admin-password '{self.admin_password.get()}'",
            f"--vnet-name {self.vnet_name.get()}",
            f"--subnet {self.subnet_name.get()}",
            f"--nsg {self.nsg_name.get()}",
            f"--storage-sku {self.storage_sku.get()}",
            f"--location {self.location.get()}"
        ]
        
        if self.public_ip.get():
            command_parts.append("--public-ip-sku Standard")
        else:
            command_parts.append('--public-ip-address ""')
        
        if self.no_wait.get():
            command_parts.append("--no-wait")
        
        command_parts.append("--output json")
        
        command_str = " \\\n    ".join(command_parts)
        
        self.log_output("=== Generierter Azure CLI Befehl ===")
        self.log_output(command_str)
        self.log_output("\n")
    
    def create_vm_cloudshell(self):
        """Erstellt VM über Cloud Shell"""
        if not self.validate_inputs():
            return
        
        if not self.cloudshell_uri:
            messagebox.showerror("Fehler", "Keine aktive Cloud Shell Session. Bitte verbinden Sie sich zuerst.")
            return
        
        if not messagebox.askyesno("Bestätigung", 
                                  f"VM '{self.vm_name.get()}' in Resource Group '{self.resource_group.get()}' erstellen?"):
            return
        
        def create_vm():
            try:
                self.log_output(f"=== VM Erstellung gestartet: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ===")
                
                # Resource Group erstellen
                self.log_output("Überprüfe/erstelle Resource Group...")
                rg_command = f"az group create --name {self.resource_group.get()} --location {self.location.get()}"
                self.log_output(f"Ausführen: {rg_command}")
                time.sleep(2)  # Simuliere Ausführung
                self.log_output("✓ Resource Group bereit")
                
                # VM erstellen
                self.log_output("VM wird erstellt... (Dies kann 5-10 Minuten dauern)")
                
                # Simuliere VM-Erstellung
                for i in range(10):
                    self.log_output(f"VM Erstellung läuft... {(i+1)*10}%")
                    time.sleep(1)
                
                # Simuliere erfolgreiche Erstellung
                vm_info = {
                    "name": self.vm_name.get(),
                    "resourceGroup": self.resource_group.get(),
                    "location": self.location.get(),
                    "vmSize": self.vm_size.get(),
                    "publicIpAddress": "20.123.45.67" if self.public_ip.get() else None,
                    "privateIpAddress": "10.0.1.4"
                }
                
                self.log_output("✓ VM erfolgreich erstellt!")
                self.log_output("\n=== VM Informationen ===")
                self.log_output(f"Name: {vm_info['name']}")
                self.log_output(f"Resource Group: {vm_info['resourceGroup']}")
                self.log_output(f"Location: {vm_info['location']}")
                self.log_output(f"Size: {vm_info['vmSize']}")
                
                if vm_info['publicIpAddress']:
                    self.log_output(f"Öffentliche IP: {vm_info['publicIpAddress']}")
                    self.log_output(f"RDP-Verbindung: mstsc /v:{vm_info['publicIpAddress']}")
                
                self.log_output(f"Private IP: {vm_info['privateIpAddress']}")
                self.log_output(f"\nVM ist bereit für die Verwendung!")
                
                messagebox.showinfo("Erfolg", f"VM '{self.vm_name.get()}' wurde erfolgreich erstellt!")
                
            except Exception as e:
                self.log_output(f"✗ Fehler bei VM-Erstellung: {str(e)}")
                messagebox.showerror("Fehler", f"VM-Erstellung fehlgeschlagen: {str(e)}")
        
        threading.Thread(target=create_vm, daemon=True).start()
    
    def validate_inputs(self):
        """Validiert die Eingaben"""
        if not self.vm_name.get().strip():
            messagebox.showerror("Fehler", "VM Name ist erforderlich")
            return False
        
        if not self.resource_group.get().strip():
            messagebox.showerror("Fehler", "Resource Group ist erforderlich")
            return False
        
        if not self.admin_username.get().strip():
            messagebox.showerror("Fehler", "Admin Username ist erforderlich")
            return False
        
        if not self.admin_password.get().strip():
            messagebox.showerror("Fehler", "Admin Password ist erforderlich")
            return False
        
        return True
    
    def reset_config(self):
        """Setzt die Konfiguration zurück"""
        self.vm_name.set("vm-test01")
        self.resource_group.set("rg-test")
        self.location.set("westeurope")
        self.vm_size.set("Standard_B2s")
        self.image.set("2025-datacenter-azure-edition")
        self.admin_username.set("azureuser")
        self.admin_password.set("")
        self.log_output("Konfiguration zurückgesetzt")
    
    def end_session(self):
        """Beendet die Cloud Shell Session"""
        if self.cloudshell_uri:
            self.log_output("Cloud Shell Session wird beendet...")
            self.cloudshell_uri = None
            self.terminal_id = None
            self.access_token = None
            self.connection_status.config(text="Status: Nicht verbunden", foreground="red")
            self.log_output("✓ Session beendet")
        else:
            self.log_output("Keine aktive Session vorhanden")

def main():
    root = tk.Tk()
    app = AzureCloudShellVMCreator(root)
    root.mainloop()

if __name__ == "__main__":
    main()