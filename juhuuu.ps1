az network vnet create --resource-group tn_ivan_riabik -n BerlinVMNET --address-prefixes 10.0.0.0/16 --subnet-name MeinSubnet --subnet-prefixes 10.0.1.0/24 -l northeurope
az network public-ip create --name BerlinPublicIp --resource-group tn_ivan_riabik --location northeurope --allocation-method Static
az network nsg create --name NSG_Berlin --resource-group tn_ivan_riabik --location northeurope
az network nsg rule create --resource-group tn_ivan_riabik --nsg-name NSG_Berlin --name RDP-Rule --protocol Tcp --direction Inbound --priority 1000 --source-address-prefixes * --source-port-ranges * --destination-address-prefixes * --destination-port-ranges 3389 --access Allow
az network nic create --resource-group tn_ivan_riabik --name NIC_Server01 --vnet-name BerlinVMNET --subnet MeinSubnet --network-security-group NSG_Berlin --public-ip-address BerlinPublicIp --location northeurope
az vm create --resource-group tn_ivan_riabik --name ekfguwe --image MicrosoftWindowsServer:WindowsServer:2025-datacenter-azure-edition:latest --size Standard_D2s_v3 --admin-username adminuser --admin-password eqzmrrtpeo --nics NIC_Server01 --storage-sku StandardSSD_LRS --location northeurope --no-wait
