#!/usr/bin/env python3
"""
Azure VM Creator GUI
Erstellt Azure VMs über die Azure CLI mit einer benutzerfreundlichen GUI
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
import subprocess
import threading
import json
import os
from datetime import datetime

class AzureVMCreator:
    def __init__(self, root):
        self.root = root
        self.root.title("Azure VM Creator")
        self.root.geometry("800x900")
        self.root.resizable(True, True)
        
        # Azure CLI Befehl für Windows/Linux-Kompatibilität
        self.az_command = "az"
        self.shell_flag = False
        if os.name == 'nt':  # Windows
            self.az_command = "az.cmd"
            self.shell_flag = True
        
        # Variablen für die VM-Parameter
        self.setup_variables()
        
        # GUI erstellen
        self.create_widgets()
        
        # Azure CLI Status prüfen
        self.check_azure_cli()
        
        # Resource Groups laden
        self.load_resource_groups()
    
    def setup_variables(self):
        """Initialisiert alle Tkinter-Variablen"""
        self.vm_name = tk.StringVar(value="myVM")
        self.resource_group = tk.StringVar(value="")
        self.location = tk.StringVar(value="West Europe")
        self.vm_size = tk.StringVar(value="Standard_B1s")
        # Korrigiertes Image für Windows Server 2022 Datacenter
        self.image = tk.StringVar(value="MicrosoftWindowsServer:WindowsServer:2022-datacenter:latest")
        self.admin_username = tk.StringVar(value="Adminuser")
        self.authentication_type = tk.StringVar(value="ssh")
        self.ssh_key_path = tk.StringVar()
        self.admin_password = tk.StringVar()
        self.subnet_name = tk.StringVar(value="default")
        self.vnet_name = tk.StringVar(value="myVNet")
        self.nsg_name = tk.StringVar(value="myNSG")
        self.public_ip = tk.BooleanVar(value=True)

        # Liste verfügbarer Resource Groups
        self.available_resource_groups = []

    def create_widgets(self):
        """Erstellt alle GUI-Widgets"""
        # Hauptframe mit Scrollbar
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Canvas für Scrolling
        canvas = tk.Canvas(main_frame)
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Title
        title_label = ttk.Label(scrollable_frame, text="Azure VM Creator", 
                               font=("Arial", 16, "bold"))
        title_label.pack(pady=(0, 20))
        
        # VM Grundeinstellungen
        self.create_basic_settings_frame(scrollable_frame)
        
        # Authentifizierung
        self.create_auth_frame(scrollable_frame)
        
        # Netzwerk-Einstellungen
        self.create_network_frame(scrollable_frame)
        
        # Zusätzliche Optionen
        self.create_additional_options_frame(scrollable_frame)
        
        # Aktions-Buttons
        self.create_action_buttons_frame(scrollable_frame)
        
        # Output-Bereich
        self.create_output_frame(scrollable_frame)
        
        # Pack canvas und scrollbar
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Mouse wheel binding für Scrolling
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
    
    def create_basic_settings_frame(self, parent):
        """Erstellt die Grundeinstellungen"""
        frame = ttk.LabelFrame(parent, text="VM Grundeinstellungen", padding=10)
        frame.pack(fill=tk.X, pady=(0, 10))
        
        # VM Name
        ttk.Label(frame, text="VM Name:").grid(row=0, column=0, sticky=tk.W, pady=2)
        ttk.Entry(frame, textvariable=self.vm_name, width=40).grid(row=0, column=1, sticky=tk.W, padx=(5, 0))
        
        # Resource Group mit Dropdown
        ttk.Label(frame, text="Resource Group:").grid(row=1, column=0, sticky=tk.W, pady=2)
        rg_frame = ttk.Frame(frame)
        rg_frame.grid(row=1, column=1, sticky=tk.W, padx=(5, 0))
        
        self.rg_combo = ttk.Combobox(rg_frame, textvariable=self.resource_group, width=30)
        self.rg_combo.pack(side=tk.LEFT)
        
        refresh_button = ttk.Button(rg_frame, text="↻", width=3, command=self.refresh_resource_groups)
        refresh_button.pack(side=tk.LEFT, padx=(5, 0))
        
        # Hinweis für Resource Groups
        info_label = ttk.Label(frame, text="Wählen Sie eine vorhandene Resource Group aus", 
                              foreground="gray", font=("Arial", 8))
        info_label.grid(row=2, column=1, sticky=tk.W, padx=(5, 0))
        
        # Location
        ttk.Label(frame, text="Location:").grid(row=3, column=0, sticky=tk.W, pady=2)
        location_combo = ttk.Combobox(frame, textvariable=self.location, width=37)
        location_combo['values'] = ('West Europe', 'East US', 'West US 2', 'Central US', 
                                   'North Europe', 'Southeast Asia', 'Australia East')
        location_combo.grid(row=3, column=1, sticky=tk.W, padx=(5, 0))
        
        # VM Size
        ttk.Label(frame, text="VM Größe:").grid(row=4, column=0, sticky=tk.W, pady=2)
        size_combo = ttk.Combobox(frame, textvariable=self.vm_size, width=37)
        size_combo['values'] = ('Standard_B1s', 'Standard_B1ms', 'Standard_B2s', 
                               'Standard_B2ms', 'Standard_D2s_v3', 'Standard_D4s_v3')
        size_combo.grid(row=4, column=1, sticky=tk.W, padx=(5, 0))
        
        # Image
        ttk.Label(frame, text="Betriebssystem:").grid(row=5, column=0, sticky=tk.W, pady=2)
        image_combo = ttk.Combobox(frame, textvariable=self.image, width=37)
        # Korrigierte Images für Azure
        image_combo['values'] = (
            'MicrosoftWindowsServer:WindowsServer:2022-datacenter:latest',
            'MicrosoftWindowsServer:WindowsServer:2019-datacenter:latest',
            'Canonical:UbuntuServer:22_04-lts:latest',
            'OpenLogic:CentOS:8_5-gen2:latest',
            'Debian:debian-11:11:latest'
        )
        image_combo.grid(row=5, column=1, sticky=tk.W, padx=(5, 0))
    
    def create_auth_frame(self, parent):
        """Erstellt die Authentifizierungs-Einstellungen"""
        frame = ttk.LabelFrame(parent, text="Authentifizierung", padding=10)
        frame.pack(fill=tk.X, pady=(0, 10))
        
        # Admin Username
        ttk.Label(frame, text="Admin Benutzername:").grid(row=0, column=0, sticky=tk.W, pady=2)
        ttk.Entry(frame, textvariable=self.admin_username, width=40).grid(row=0, column=1, sticky=tk.W, padx=(5, 0))
        
        # Authentication Type
        ttk.Label(frame, text="Authentifizierung:").grid(row=1, column=0, sticky=tk.W, pady=2)
        auth_frame = ttk.Frame(frame)
        auth_frame.grid(row=1, column=1, sticky=tk.W, padx=(5, 0))
        
        ttk.Radiobutton(auth_frame, text="SSH Key", variable=self.authentication_type, 
                       value="ssh", command=self.toggle_auth_fields).pack(side=tk.LEFT)
        ttk.Radiobutton(auth_frame, text="Passwort", variable=self.authentication_type, 
                       value="password", command=self.toggle_auth_fields).pack(side=tk.LEFT, padx=(10, 0))
        
        # SSH Key Path
        self.ssh_label = ttk.Label(frame, text="SSH Key Pfad:")
        self.ssh_label.grid(row=2, column=0, sticky=tk.W, pady=2)
        ssh_frame = ttk.Frame(frame)
        ssh_frame.grid(row=2, column=1, sticky=tk.W, padx=(5, 0))
        self.ssh_entry = ttk.Entry(ssh_frame, textvariable=self.ssh_key_path, width=30)
        self.ssh_entry.pack(side=tk.LEFT)
        self.ssh_button = ttk.Button(ssh_frame, text="Durchsuchen", command=self.browse_ssh_key)
        self.ssh_button.pack(side=tk.LEFT, padx=(5, 0))
        
        # Password
        self.password_label = ttk.Label(frame, text="Passwort:")
        self.password_label.grid(row=3, column=0, sticky=tk.W, pady=2)
        self.password_entry = ttk.Entry(frame, textvariable=self.admin_password, show="*", width=40)
        self.password_entry.grid(row=3, column=1, sticky=tk.W, padx=(5, 0))
        
        # Initial state
        self.toggle_auth_fields()
    
    def create_network_frame(self, parent):
        """Erstellt die Netzwerk-Einstellungen"""
        frame = ttk.LabelFrame(parent, text="Netzwerk-Einstellungen", padding=10)
        frame.pack(fill=tk.X, pady=(0, 10))
        
        # VNet Name
        ttk.Label(frame, text="Virtual Network:").grid(row=0, column=0, sticky=tk.W, pady=2)
        ttk.Entry(frame, textvariable=self.vnet_name, width=40).grid(row=0, column=1, sticky=tk.W, padx=(5, 0))
        
        # Subnet Name
        ttk.Label(frame, text="Subnet:").grid(row=1, column=0, sticky=tk.W, pady=2)
        ttk.Entry(frame, textvariable=self.subnet_name, width=40).grid(row=1, column=1, sticky=tk.W, padx=(5, 0))
        
        # NSG Name
        ttk.Label(frame, text="Network Security Group:").grid(row=2, column=0, sticky=tk.W, pady=2)
        ttk.Entry(frame, textvariable=self.nsg_name, width=40).grid(row=2, column=1, sticky=tk.W, padx=(5, 0))
        
        # Public IP
        ttk.Checkbutton(frame, text="Öffentliche IP-Adresse erstellen", 
                       variable=self.public_ip).grid(row=3, column=1, sticky=tk.W, padx=(5, 0), pady=5)
    
    def create_additional_options_frame(self, parent):
        """Erstellt zusätzliche Optionen"""
        frame = ttk.LabelFrame(parent, text="Zusätzliche Optionen", padding=10)
        frame.pack(fill=tk.X, pady=(0, 10))
        
        info_text = ("Weitere Azure CLI Parameter können im Output-Bereich nach der "
                    "Generierung des Befehls hinzugefügt werden.")
        ttk.Label(frame, text=info_text, wraplength=600).pack(anchor=tk.W)
    
    def create_action_buttons_frame(self, parent):
        """Erstellt die Aktions-Buttons"""
        frame = ttk.Frame(parent)
        frame.pack(fill=tk.X, pady=10)
        
        ttk.Button(frame, text="Azure CLI Status prüfen", 
                  command=self.check_azure_cli).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(frame, text="Resource Groups aktualisieren", 
                  command=self.refresh_resource_groups).pack(side=tk.LEFT, padx=5)
        ttk.Button(frame, text="Befehl generieren", 
                  command=self.generate_command).pack(side=tk.LEFT, padx=5)
        ttk.Button(frame, text="VM erstellen", 
                  command=self.create_vm).pack(side=tk.LEFT, padx=5)
        ttk.Button(frame, text="Output löschen", 
                  command=self.clear_output).pack(side=tk.LEFT, padx=5)
    
    def create_output_frame(self, parent):
        """Erstellt den Output-Bereich"""
        frame = ttk.LabelFrame(parent, text="Output / Befehl", padding=10)
        frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        self.output_text = scrolledtext.ScrolledText(frame, height=15, wrap=tk.WORD)
        self.output_text.pack(fill=tk.BOTH, expand=True)
    
    def load_resource_groups(self):
        """Lädt verfügbare Resource Groups von Azure"""
        def load_rg():
            try:
                self.log_output("Resource Groups werden geladen...")
                result = subprocess.run(
                    [self.az_command, "group", "list", "--query", "[].name", "--output", "json"], 
                    capture_output=True, text=True, timeout=30, shell=self.shell_flag
                )
                
                if result.returncode == 0:
                    resource_groups = json.loads(result.stdout)
                    self.available_resource_groups = resource_groups
                    
                    # GUI auf dem Main Thread aktualisieren
                    self.root.after(0, self.update_resource_group_combo)
                    self.log_output(f"✓ {len(resource_groups)} Resource Groups gefunden")
                else:
                    self.log_output("✗ Fehler beim Laden der Resource Groups")
                    self.log_output(result.stderr if result.stderr else "Unbekannter Fehler")
                    
            except subprocess.TimeoutExpired:
                self.log_output("✗ Timeout beim Laden der Resource Groups")
            except json.JSONDecodeError:
                self.log_output("✗ Fehler beim Parsen der Resource Groups")
            except Exception as e:
                self.log_output(f"✗ Unerwarteter Fehler beim Laden der Resource Groups: {str(e)}")
        
        # Nur laden wenn Azure CLI verfügbar ist
        threading.Thread(target=load_rg, daemon=True).start()
    
    def update_resource_group_combo(self):
        """Aktualisiert die Resource Group Combobox"""
        if hasattr(self, 'rg_combo'):
            self.rg_combo['values'] = self.available_resource_groups
            if self.available_resource_groups and not self.resource_group.get():
                self.resource_group.set(self.available_resource_groups[0])
    
    def refresh_resource_groups(self):
        """Aktualisiert die Resource Groups Liste"""
        self.load_resource_groups()
    
    def toggle_auth_fields(self):
        """Schaltet zwischen SSH und Passwort-Authentifizierung um"""
        if self.authentication_type.get() == "ssh":
            self.ssh_label.grid()
            self.ssh_entry.master.grid()
            self.password_label.grid_remove()
            self.password_entry.grid_remove()
        else:
            self.ssh_label.grid_remove()
            self.ssh_entry.master.grid_remove()
            self.password_label.grid()
            self.password_entry.grid()
    
    def browse_ssh_key(self):
        """Öffnet Datei-Dialog für SSH Key"""
        filename = filedialog.askopenfilename(
            title="SSH Key auswählen",
            filetypes=[("All files", "*.*"), ("PUB files", "*.pub")]
        )
        if filename:
            self.ssh_key_path.set(filename)
    
    def check_azure_cli(self):
        """Prüft ob Azure CLI installiert und angemeldet ist"""
        def run_check():
            self.log_output("=== Azure CLI Status wird geprüft ===")
            
            # Azure CLI Version prüfen
            try:
                result = subprocess.run([self.az_command, "--version"], 
                                      capture_output=True, text=True, timeout=10, 
                                      shell=self.shell_flag)
                if result.returncode == 0:
                    version_line = result.stdout.split('\n')[0]
                    self.log_output(f"✓ Azure CLI gefunden: {version_line}")
                else:
                    self.log_output("✗ Azure CLI nicht gefunden oder nicht installiert")
                    self.log_output("Installieren Sie Azure CLI: winget install Microsoft.AzureCLI")
                    return
            except Exception as e:
                self.log_output(f"✗ Fehler beim Prüfen der Azure CLI: {str(e)}")
                self.log_output("Möglicherweise ist Azure CLI nicht installiert oder nicht im PATH")
                return
            
            # Login Status prüfen
            try:
                result = subprocess.run([self.az_command, "account", "show"], 
                                      capture_output=True, text=True, timeout=15,
                                      shell=self.shell_flag)
                if result.returncode == 0:
                    account_info = json.loads(result.stdout)
                    self.log_output(f"✓ Angemeldet als: {account_info.get('user', {}).get('name', 'Unknown')}")
                    self.log_output(f"✓ Aktuelle Subscription: {account_info.get('name', 'Unknown')}")
                else:
                    self.log_output("✗ Nicht bei Azure angemeldet")
                    self.log_output("Bitte führen Sie 'az login' in der Eingabeaufforderung aus")
            except Exception as e:
                self.log_output(f"✗ Fehler beim Prüfen des Login-Status: {str(e)}")
        
        threading.Thread(target=run_check, daemon=True).start()
    
    def generate_command(self):
        """Generiert den Azure CLI Befehl"""
        if not self.validate_inputs():
            return
        
        command_parts = [self.az_command, "vm", "create"]
        command_parts.extend(["--name", self.vm_name.get()])
        command_parts.extend(["--resource-group", self.resource_group.get()])
        command_parts.extend(["--location", self.location.get()])
        command_parts.extend(["--size", self.vm_size.get()])
        command_parts.extend(["--image", self.image.get()])
        command_parts.extend(["--admin-username", self.admin_username.get()])
        
        # Authentifizierung
        if self.authentication_type.get() == "ssh":
            if self.ssh_key_path.get():
                command_parts.extend(["--ssh-key-values", self.ssh_key_path.get()])
            else:
                command_parts.extend(["--generate-ssh-keys"])
        else:
            command_parts.extend(["--admin-password", self.admin_password.get()])
        
        # Netzwerk
        command_parts.extend(["--vnet-name", self.vnet_name.get()])
        command_parts.extend(["--subnet", self.subnet_name.get()])
        command_parts.extend(["--nsg", self.nsg_name.get()])
        
        if self.public_ip.get():
            command_parts.append("--public-ip-sku")
            command_parts.append("Standard")
        else:
            command_parts.append("--public-ip-address")
            command_parts.append('""')
        
        # Output format
        command_parts.extend(["--output", "json"])
        
        command_str = " ".join(f'"{part}"' if " " in part else part for part in command_parts)
        
        self.log_output("=== Generierter Azure CLI Befehl ===")
        self.log_output(command_str)
        self.log_output("\nSie können diesen Befehl anpassen, bevor Sie die VM erstellen.")
    
    def validate_inputs(self):
        """Validiert die Eingaben"""
        if not self.vm_name.get().strip():
            messagebox.showerror("Fehler", "VM Name ist erforderlich")
            return False
        
        if not self.resource_group.get().strip():
            messagebox.showerror("Fehler", "Resource Group ist erforderlich")
            return False
        
        if not self.admin_username.get().strip():
            messagebox.showerror("Fehler", "Admin Benutzername ist erforderlich")
            return False
        
        if self.authentication_type.get() == "password" and not self.admin_password.get():
            messagebox.showerror("Fehler", "Passwort ist erforderlich")
            return False
        
        # Prüfen ob Resource Group ausgewählt wurde
        if self.resource_group.get() not in self.available_resource_groups:
            messagebox.showerror("Fehler", "Bitte wählen Sie eine gültige Resource Group aus der Liste aus")
            return False
        
        return True
    
    def create_vm(self):
        """Erstellt die VM"""
        if not self.validate_inputs():
            return
        
        if not messagebox.askyesno("Bestätigung", 
                                  f"Möchten Sie die VM '{self.vm_name.get()}' in der Resource Group '{self.resource_group.get()}' erstellen?"):
            return
        
        def run_creation():
            self.log_output(f"=== VM Erstellung gestartet: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ===")
            
            try:
                # VM erstellen
                self.log_output("VM wird erstellt... (Dies kann einige Minuten dauern)")
                
                command_parts = [self.az_command, "vm", "create"]
                command_parts.extend(["--name", self.vm_name.get()])
                command_parts.extend(["--resource-group", self.resource_group.get()])
                command_parts.extend(["--location", self.location.get()])
                command_parts.extend(["--size", self.vm_size.get()])
                command_parts.extend(["--image", self.image.get()])
                command_parts.extend(["--admin-username", self.admin_username.get()])
                
                if self.authentication_type.get() == "ssh":
                    if self.ssh_key_path.get():
                        command_parts.extend(["--ssh-key-values", self.ssh_key_path.get()])
                    else:
                        command_parts.extend(["--generate-ssh-keys"])
                else:
                    command_parts.extend(["--admin-password", self.admin_password.get()])
                
                command_parts.extend(["--vnet-name", self.vnet_name.get()])
                command_parts.extend(["--subnet", self.subnet_name.get()])
                command_parts.extend(["--nsg", self.nsg_name.get()])
                
                if self.public_ip.get():
                    command_parts.extend(["--public-ip-sku", "Standard"])
                else:
                    command_parts.extend(["--public-ip-address", ""])
                
                command_parts.extend(["--output", "json"])
                
                # Befehl ausführen
                result = subprocess.run(command_parts, capture_output=True, text=True, 
                                      timeout=600, shell=self.shell_flag)
                
                if result.returncode == 0:
                    self.log_output("✓ VM erfolgreich erstellt!")
                    try:
                        vm_info = json.loads(result.stdout)
                        self.log_output("\n=== VM Informationen ===")
                        self.log_output(f"VM Name: {vm_info.get('name', 'N/A')}")
                        self.log_output(f"Resource Group: {vm_info.get('resourceGroup', 'N/A')}")
                        self.log_output(f"Location: {vm_info.get('location', 'N/A')}")
                        if 'publicIpAddress' in vm_info and vm_info['publicIpAddress']:
                            self.log_output(f"Öffentliche IP: {vm_info['publicIpAddress']}")
                        if 'privateIpAddress' in vm_info:
                            self.log_output(f"Private IP: {vm_info['privateIpAddress']}")
                    except json.JSONDecodeError:
                        self.log_output("VM erstellt, aber Informationen konnten nicht geparst werden")
                        self.log_output(result.stdout)
                else:
                    self.log_output(f"✗ Fehler beim Erstellen der VM:")
                    self.log_output(result.stderr)
                    if result.stdout:
                        self.log_output("Zusätzliche Ausgabe:")
                        self.log_output(result.stdout)
                        
            except subprocess.TimeoutExpired:
                self.log_output("✗ Timeout: VM Erstellung dauerte zu lange")
            except Exception as e:
                self.log_output(f"✗ Unerwarteter Fehler: {str(e)}")
            
            self.log_output(f"\n=== VM Erstellung abgeschlossen: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ===")
        
        threading.Thread(target=run_creation, daemon=True).start()
    
    def log_output(self, message):
        """Fügt eine Nachricht zum Output hinzu"""
        def update_gui():
            self.output_text.insert(tk.END, message + "\n")
            self.output_text.see(tk.END)
            self.output_text.update()
        
        # GUI-Updates müssen im Main Thread erfolgen
        self.root.after(0, update_gui)
    
    def clear_output(self):
        """Löscht den Output"""
        self.output_text.delete(1.0, tk.END)