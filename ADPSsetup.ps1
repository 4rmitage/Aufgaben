Set-Location -Path "C:\Python\Aufgaben-1"
# Nach dem Namen der VM fragen
$vmName = Read-Host "Bitte gib den Namen der VM ein"

# Verbindung zur VM herstellen (ersetze ggf. durch deinen Hypervisor/Remote-Mechanismus)
# Beispiel für Hyper-V:
Invoke-Command -VMName $vmName -ScriptBlock {
    Write-Host "Installiere Active Directory Domain Services..."
    Install-WindowsFeature -Name AD-Domain-Services -IncludeManagementTools
    Write-Host "Installation abgeschlossen."
}