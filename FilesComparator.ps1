$file1 = Read-Host -Prompt "File 1"
$file2 = Read-Host -Prompt "File 2"

$bytes1 = [System.IO.File]::ReadAllBytes($file1)
$bytes2 = [System.IO.File]::ReadAllBytes($file2)

if($bytes1.length -ne $bytes2.length) {
	Write-Host "The files are not equal."
}
else {
	$equal = $true;
	for($i=0; $i -lt $bytes1.length; $i++) {
		if($bytes1[$i] -ne $bytes2[$i]) {
			$equal = $false;
		}
	}
	
	if($equal -eq $true) {
		Write-Host "The files are equal."
	}
	else {
		Write-Host "The files are not equal."
	}
}

pause
