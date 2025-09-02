import tkinter as tk
from tkinter import ttk, messagebox, filedialog

# Fest definierte Parameter
RESOURCE_GROUP = "tn_ivan_riabik"
OS_IMAGE = "MicrosoftWindowsServer:WindowsServer:2025-datacenter-azure-edition:latest"
STORAGE_SKU = "StandardSSD_LRS"

def get_regions():
    """Gibt fest definierte Regionen zurück."""
    return [
        "North Europe (northeurope)",
        "Central India (centralindia)",
        "Central Mexico (centralmexico)"
    ]

def generate_commands():
    """Erstellt die Azure CLI Befehle als Liste."""
    region = region_var.get().split("(")[-1].rstrip(")")
    vnet_name = vnet_var.get()
    subnet_name = subnet_var.get()
    vnet_range = vnet_range_var.get()
    subnet_range = subnet_range_var.get()
    public_ip = publicip_var.get()
    nsg_name = nsg_var.get()
    nic_name = nic_var.get()
    vm_name = vm_var.get()
    vm_size = sku_var.get()
    admin_user = user_var.get()
    admin_pass = pass_var.get()

    if not all([region, vnet_name, subnet_name, vnet_range, subnet_range,
                public_ip, nsg_name, nic_name, vm_name, vm_size, admin_user, admin_pass]):
        return None

    lines = [
        f'az network vnet create --resource-group {RESOURCE_GROUP} -n {vnet_name} --address-prefixes {vnet_range} --subnet-name {subnet_name} --subnet-prefixes {subnet_range} -l {region}',
        f'az network public-ip create --name {public_ip} --resource-group {RESOURCE_GROUP} --location {region} --allocation-method Static',
        f'az network nsg create --name {nsg_name} --resource-group {RESOURCE_GROUP} --location {region}',
        f'az network nsg rule create --resource-group {RESOURCE_GROUP} --nsg-name {nsg_name} --name RDP-Rule --protocol Tcp --direction Inbound --priority 1000 --source-address-prefixes * --source-port-ranges * --destination-address-prefixes * --destination-port-ranges 3389 --access Allow',
        f'az network nic create --resource-group {RESOURCE_GROUP} --name {nic_name} --vnet-name {vnet_name} --subnet {subnet_name} --network-security-group {nsg_name} --public-ip-address {public_ip} --location {region}',
        f'az vm create --resource-group {RESOURCE_GROUP} --name {vm_name} --image {OS_IMAGE} --size {vm_size} --admin-username {admin_user} --admin-password {admin_pass} --nics {nic_name} --storage-sku {STORAGE_SKU} --location {region} --no-wait'
    ]
    return lines

def show_commands_window():
    """Zeigt die Befehle in einem neuen Fenster an."""
    commands = generate_commands()
    if commands is None:
        messagebox.showwarning("Fehler", "Bitte alle Felder ausfüllen!")
        return

    cmd_window = tk.Toplevel(root)
    cmd_window.title("Azure CLI Befehle")

    text = tk.Text(cmd_window, width=120, height=15)
    text.pack(padx=10, pady=10)
    text.insert(tk.END, "\n".join(commands))
    text.config(state=tk.NORMAL)

    def save_file():
        filepath = filedialog.asksaveasfilename(
            defaultextension=".ps1",
            filetypes=[("PowerShell Script", "*.ps1"), ("Textdatei", "*.txt"), ("Alle Dateien", "*.*")]
        )
        if filepath:
            try:
                with open(filepath, "w", encoding="utf-8") as f:
                    f.write(text.get("1.0", tk.END))
                messagebox.showinfo("Fertig", f"Die Datei wurde gespeichert:\n{filepath}")
            except Exception as e:
                messagebox.showerror("Fehler", f"Fehler beim Speichern:\n{e}")

    save_btn = ttk.Button(cmd_window, text="Speichern...", command=save_file)
    save_btn.pack(pady=(0,10))

# --- GUI Aufbau ---
root = tk.Tk()
root.title("Azure VM PS1 Generator")

frame = ttk.Frame(root, padding=10)
frame.grid(row=0, column=0, sticky="nsew")

ttk.Label(frame, text="Region:").grid(row=0, column=0, sticky="w")
region_var = tk.StringVar()
region_combo = ttk.Combobox(frame, textvariable=region_var, width=40, state="readonly")
region_combo['values'] = get_regions()
region_combo.grid(row=0, column=1)
region_combo.current(0)

ttk.Label(frame, text="VM-Name:").grid(row=1, column=0, sticky="w")
vm_var = tk.Entry(frame)
vm_var.grid(row=1, column=1)

ttk.Label(frame, text="VM-SKU:").grid(row=2, column=0, sticky="w")
sku_var = tk.StringVar()
sku_combo = ttk.Combobox(frame, textvariable=sku_var, width=40, state="readonly")
sku_combo['values'] = ["Standard_B2ms", "Standard_B1s", "Standard_DS1_v2", "Standard_D2s_v3"]
sku_combo.grid(row=2, column=1)
sku_combo.current(0)

ttk.Label(frame, text="VNet-Name:").grid(row=3, column=0, sticky="w")
vnet_var = tk.Entry(frame)
vnet_var.insert(0, "BerlinVMNET")
vnet_var.grid(row=3, column=1)

ttk.Label(frame, text="VNet-Range:").grid(row=4, column=0, sticky="w")
vnet_range_var = tk.Entry(frame)
vnet_range_var.insert(0, "10.0.0.0/16")
vnet_range_var.grid(row=4, column=1)

ttk.Label(frame, text="Subnetz-Name:").grid(row=5, column=0, sticky="w")
subnet_var = tk.Entry(frame)
subnet_var.insert(0, "MeinSubnet")
subnet_var.grid(row=5, column=1)

ttk.Label(frame, text="Subnetz-Range:").grid(row=6, column=0, sticky="w")
subnet_range_var = tk.Entry(frame)
subnet_range_var.insert(0, "10.0.1.0/24")
subnet_range_var.grid(row=6, column=1)

ttk.Label(frame, text="Public IP:").grid(row=7, column=0, sticky="w")
publicip_var = tk.Entry(frame)
publicip_var.insert(0, "BerlinPublicIp")
publicip_var.grid(row=7, column=1)

ttk.Label(frame, text="NSG-Name:").grid(row=8, column=0, sticky="w")
nsg_var = tk.Entry(frame)
nsg_var.insert(0, "NSG_Berlin")
nsg_var.grid(row=8, column=1)

ttk.Label(frame, text="NIC-Name:").grid(row=9, column=0, sticky="w")
nic_var = tk.Entry(frame)
nic_var.insert(0, "NIC_Server01")
nic_var.grid(row=9, column=1)

ttk.Label(frame, text="Admin-User:").grid(row=10, column=0, sticky="w")
user_var = tk.Entry(frame)
user_var.insert(0, "adminuser")
user_var.grid(row=10, column=1)

ttk.Label(frame, text="Admin-Passwort:").grid(row=11, column=0, sticky="w")
pass_var = tk.Entry(frame, show="*")
pass_var.grid(row=11, column=1)

ttk.Button(frame, text="Befehle anzeigen", command=show_commands_window).grid(row=12, column=0, columnspan=2, pady=10)

root.mainloop()
