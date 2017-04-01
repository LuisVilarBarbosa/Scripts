$file = [System.IO.File]::OpenText("data.txt")
for($i = 1; $null -ne ($line = $file.ReadLine()) -and $i -lt 1000; $i++) {
    "UPDATE " + '"Table"' + " SET column = '" + $line + "' WHERE " + '"TableID"' + " = " + $i + ";" | Out-File update.sql -Append
}