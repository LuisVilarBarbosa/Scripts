$file1 = Read-Host -Prompt "File 1"
$file2 = Read-Host -Prompt "File 2"

$f1 = Get-Content $file1
$f2 = Get-Content $file2

if(($f1 -eq $null) -or ($f2 -eq $null)) {
    Write-Host "Error."
}
elseif($f1 -eq $f2) {
    Write-Host "The files are equal."
}
else {
    Write-Host "The files are not equal."
}

pause
