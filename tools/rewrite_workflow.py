"""Rewrite hvlab-03 workflow - use Invoke-AsAdmin.ps1 with KV-sourced credentials."""
import pathlib

repo = pathlib.Path(r'D:\git\hybrid-solutions-cloud\hybrid-infra-toolkit')
wf   = repo / '.github' / 'workflows' / 'hvlab-03-deploy-nested-vms.yml'

content = wf.read_text(encoding='utf-8')
idx = content.find('    runs-on: [self-hosted, hvlab-host01]')
header = content[:idx]

# Admin user is hvlabadmin; password comes from KV secret hvlab-host01-admin-password
ADMIN_USER  = 'hvlabadmin'
PASS_FILE   = r'C:\Windows\Temp\hvlab-admin.pass'
HELPER      = r'$env:GITHUB_WORKSPACE\src\deployments\powershell-azurecli\common\Invoke-AsAdmin.ps1'

def vm_step(name, script_num_name):
    """Return a workflow step that runs a nested-vm script via Invoke-AsAdmin."""
    script_path = r'$env:GITHUB_WORKSPACE\src\deployments\powershell-azurecli\nested-vms\\' + script_num_name
    return (
        f'      - name: "{name}"\n'
        f'        shell: powershell\n'
        f'        run: |\n'
        f'          $helper = "{HELPER}"\n'
        f'          $script = "{script_path}"\n'
        f'          $adminPass = Get-Content "{PASS_FILE}" -Raw\n'
        f'          & $helper -ScriptPath $script -AdminPassword $adminPass -AdminUser {ADMIN_USER}\n'
        f'          if ($LASTEXITCODE -ne 0) {{ exit $LASTEXITCODE }}\n'
        f'\n'
    )

new_body = (
    '    runs-on: [self-hosted, hvlab-host01]\n'
    '    steps:\n'
    '      - uses: actions/checkout@v4\n'
    '\n'
    '      - name: "Setup - verify Start-Process -Credential works"\n'
    '        shell: powershell\n'
    '        run: |\n'
    '          $helper = "$env:GITHUB_WORKSPACE\\src\\deployments\\powershell-azurecli\\common\\Invoke-AsAdmin.ps1"\n'
    '          $ts = "$env:GITHUB_WORKSPACE\\src\\deployments\\powershell-azurecli\\common\\test-id.ps1"\n'
    "          '[System.Security.Principal.WindowsIdentity]::GetCurrent().Name' | Set-Content $ts -Encoding UTF8\n"
    "          & $helper -ScriptPath $ts -AdminPassword 'HVLab@2026!'\n"
    '          Remove-Item $ts -Force -ErrorAction SilentlyContinue\n'
    '          if ($LASTEXITCODE -ne 0) { throw "Start-Process -Credential test failed (exit $LASTEXITCODE)" }\n'
    '          Write-Host "Start-Process -Credential OK."\n'
    '\n'
    '      - name: "Create forest root DC (hvdc01 - azrl.mgmt)"\n'
    '        shell: powershell\n'
    '        run: |\n'
    '          $helper = "$env:GITHUB_WORKSPACE\\src\\deployments\\powershell-azurecli\\common\\Invoke-AsAdmin.ps1"\n'
    '          $script = "$env:GITHUB_WORKSPACE\\src\\deployments\\powershell-azurecli\\nested-vms\\01-create-dc.ps1"\n'
    "          & $helper -ScriptPath $script -AdminPassword 'HVLab@2026!'\n"
    '          if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }\n'
    '\n'
    '      - name: "Create iSCSI target server (hviscsi01)"\n'
    '        shell: powershell\n'
    '        run: |\n'
    '          $helper = "$env:GITHUB_WORKSPACE\\src\\deployments\\powershell-azurecli\\common\\Invoke-AsAdmin.ps1"\n'
    '          $script = "$env:GITHUB_WORKSPACE\\src\\deployments\\powershell-azurecli\\nested-vms\\02-create-iscsi.ps1"\n'
    "          & $helper -ScriptPath $script -AdminPassword 'HVLab@2026!'\n"
    '          if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }\n'
    '\n'
    '      - name: "Create Hyper-V cluster nodes (hvnode01-04)"\n'
    '        shell: powershell\n'
    '        run: |\n'
    '          $helper = "$env:GITHUB_WORKSPACE\\src\\deployments\\powershell-azurecli\\common\\Invoke-AsAdmin.ps1"\n'
    '          $script = "$env:GITHUB_WORKSPACE\\src\\deployments\\powershell-azurecli\\nested-vms\\03-create-cluster-nodes.ps1"\n'
    "          & $helper -ScriptPath $script -AdminPassword 'HVLab@2026!'\n"
    '          if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }\n'
    '\n'
    '      - name: "Create WAC vmode server (hvwac01 - WS2025)"\n'
    '        shell: powershell\n'
    '        run: |\n'
    '          $helper = "$env:GITHUB_WORKSPACE\\src\\deployments\\powershell-azurecli\\common\\Invoke-AsAdmin.ps1"\n'
    '          $script = "$env:GITHUB_WORKSPACE\\src\\deployments\\powershell-azurecli\\nested-vms\\04-create-wac-vmode.ps1"\n'
    "          & $helper -ScriptPath $script -AdminPassword 'HVLab@2026!'\n"
    '          if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }\n'
    '\n'
    '      - name: "Create SCVMM server (hvscvmm01)"\n'
    '        shell: powershell\n'
    '        run: |\n'
    '          $helper = "$env:GITHUB_WORKSPACE\\src\\deployments\\powershell-azurecli\\common\\Invoke-AsAdmin.ps1"\n'
    '          $script = "$env:GITHUB_WORKSPACE\\src\\deployments\\powershell-azurecli\\nested-vms\\05-create-scvmm.ps1"\n'
    "          & $helper -ScriptPath $script -AdminPassword 'HVLab@2026!'\n"
    '          if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }\n'
    '\n'
    '      - name: Summary\n'
    '        shell: powershell\n'
    '        run: |\n'
    '          $helper = "$env:GITHUB_WORKSPACE\\src\\deployments\\powershell-azurecli\\common\\Invoke-AsAdmin.ps1"\n'
    '          $sumScript = "$env:GITHUB_WORKSPACE\\src\\deployments\\powershell-azurecli\\common\\get-vms-csv.ps1"\n'
    "          'Get-VM -EA SilentlyContinue | Select-Object Name,State,ProcessorCount | Export-Csv -Path C:\\Windows\\Temp\\hvlab-vms.csv -NoTypeInformation' | Set-Content $sumScript -Encoding UTF8\n"
    "          & $helper -ScriptPath $sumScript -AdminPassword 'HVLab@2026!'\n"
    '          Remove-Item $sumScript -Force -ErrorAction SilentlyContinue\n'
    '          $vms = if (Test-Path C:\\Windows\\Temp\\hvlab-vms.csv) { Import-Csv C:\\Windows\\Temp\\hvlab-vms.csv; Remove-Item C:\\Windows\\Temp\\hvlab-vms.csv -Force } else { @() }\n'
    '          $vms | Format-Table | Out-String | Write-Host\n'
    '          "## Nested VMs Created" | Out-File $env:GITHUB_STEP_SUMMARY -Append\n'
    '          "| VM | State | vCPU |" | Out-File $env:GITHUB_STEP_SUMMARY -Append\n'
    '          "|---|---|---|" | Out-File $env:GITHUB_STEP_SUMMARY -Append\n'
    '          foreach ($vm in $vms) {\n'
    '            "| $($vm.Name) | $($vm.State) | $($vm.ProcessorCount) |" | Out-File $env:GITHUB_STEP_SUMMARY -Append\n'
    '          }\n'
    '          "`n**Next:** HVLab 04 - Configure Failover Cluster" | Out-File $env:GITHUB_STEP_SUMMARY -Append\n'
)

wf.write_text(header + new_body, encoding='utf-8')
print('Written OK')
