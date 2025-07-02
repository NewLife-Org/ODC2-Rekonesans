import time
import sys
import os
import random
import subprocess

# === KOLORY TERMINALA ===
GREEN = '\033[92m'
WHITE = '\033[97m'
YELLOW = '\033[93m'
RED = '\033[91m'
RESET = '\033[0m'

# === INTRO LOGO ===
Intro = '''
                                             :       ====:.-:..........                                 
                             .==:     =--+-+-:+ .. :=-+=--=.-          .                                 
                      :+=-  +-  .+=+--+   -====#-   +##= :+=+==+====++ +-                               
                -   :+:  .=-   ++ ===-==+=- +#=++++*- -*#===:          *.                               
              -= --+-   =- :+=  --+ -=*+####+*****- ++==-*#:=======+=-=======                            
            -+   =:   ++   +=.++:-==+:###-+##--=-------:--=##-      -=      =:::::::::::-+.             
          ++   +=            +==:+-**##+     *#*====------=:*##=+.+--+ ++    ==+++-.  -:               
 ==                            --++##+        *#*#========++=                                           
-+-#****************************-###=          +##+-=-+=====:+:=.=:==.+=:+=:+=-+=                       
 -===+==+================+-==- --###=        =##+*:=-=+: ==-=                                           
       *  =  ------------== -= -::- +###-  =##+*-+-=:=-=-=-                                            
       + =+                =----=-==:==##*##**:===-=--                      =                          
    ==:=-=--=:=-==.=-:=-==:=-==:=+=+=-==*#**-========:-=:  -+   :=   -+  -*:=-                       
                   =+=+===+-     =-  =-+- -=-+-==-=-    =.=-  :=: ==*: :+:+-                          
                           .====-    +- =-  =:  =:+-=-  +-+  +-      .+:=.                           
                                      :+   -=:-=      +=   --                                           
                                             -  =+                                                    
             _  _               _     _   __                                   _ 
            | \| | ___ __ __ __| |   (_) / _| ___     ___  _ _  __ _     _ __ | |
            | .` |/ -_)\ V  V /| |__ | ||  _|/ -_) _ / _ \| '_|/ _` | _ | '_ \| |
            |_|\_|\___| \_/\_/ |____||_||_|  \___|(_)\___/|_|  \__, |(_)| .__/|_|
                                                               |___/    |_|      
'''

def matrix_logo_effect(logo, duration=4):
    charset = "newlife"
    lines = logo.splitlines()
    width = max(len(line) for line in lines) if lines else 0
    start_time = time.time()

    while True:
        elapsed = time.time() - start_time
        if elapsed > duration:
            break

        progress = elapsed / duration
        os.system('cls' if os.name == 'nt' else 'clear')
        for line in lines:
            rendered_line = ""
            for char in line:
                if char != " ":
                    if random.random() < progress:
                        rendered_line += WHITE + char + RESET
                    else:
                        if random.random() < 0.85:
                            rendered_line += GREEN + char + RESET
                        else:
                            rendered_line += GREEN + random.choice(charset) + RESET
                else:
                    rendered_line += " " if random.random() > 0.02 else GREEN + random.choice(charset) + RESET
            print(rendered_line)
        time.sleep(0.06)

    os.system('cls' if os.name == 'nt' else 'clear')
    for line in lines:
        print(WHITE + line + RESET)

def blinking_cursor(seconds=2):
    end_time = time.time() + seconds
    visible = True
    while time.time() < end_time:
        sys.stdout.write('\r' + (WHITE + '█' + RESET if visible else ' '))
        sys.stdout.flush()
        time.sleep(0.5)
        visible = not visible
    sys.stdout.write('\r \r')
    sys.stdout.flush()

def intro():
    os.system('cls' if os.name == 'nt' else 'clear')
    matrix_logo_effect(Intro, duration=4)
    blinking_cursor(1.5)

# === SKANER NMAP ===
scan_modes = {
    "1": {
        "name": "STEALTH SCAN | Fast & Smooth",
        "command": lambda ip: ["nmap", "-sS", "-T3", ip]
    },
    "2": {
        "name": "VULNERS SCAN | Slow but satisfying",
        "command": lambda ip: ["nmap", "-sV", "--script", "vulners", ip]
    },
    "3": {
        "name": "WEIRD SCANS | Null & FIN & Xmas",
        "command": lambda ip: [
            ["nmap", "-sN", ip],
            ["nmap", "-sF", ip],
            ["nmap", "-sX", ip]
        ]
    },
    "4": {
        "name": "AGGRESSIVE SCAN | Unkind but you need this",
        "command": lambda ip: ["nmap", "-A", "-T4", ip]
    },
    "5": {
        "name": "Full UDP & TCP SCAN | You got time, and motivation",
        "command": lambda ip: ["nmap", "-sS", "sU", "-pT:-,U:-", "sV", ip]
    }
}

def ask_input():
    target_ip = input(YELLOW + "Podaj IP celu (np. 192.168.56.101): " + RESET)
    output_file = input(YELLOW + "Podaj nazwę pliku do zapisu raportu (np. raport.txt): " + RESET)

    print("\nDostępne tryby skanowania:")
    for k, v in scan_modes.items():
        print(f" {k}. {v['name']}")

    scan_choice = input(YELLOW + "\nWybierz tryb skanowania (1-5): " + RESET)
    return target_ip.strip(), output_file.strip(), scan_choice.strip()

def execute_scan(cmd_list, output_file, label):
    if isinstance(cmd_list[0], list):
        for i, cmd in enumerate(cmd_list):
            print(f"{WHITE}⏳ Trwa skan {label} #{i+1}: {GREEN}{' '.join(cmd)}{RESET}")
            result = subprocess.run(cmd, capture_output=True, text=True)
            with open(output_file, 'a') as f:
                f.write(f"\n\n====== {label} #{i+1} ======\n")
                f.write(result.stdout)
            print(GREEN + f"[✔] Skan {label} #{i+1} zakończony sukcesem." + RESET)
    else:
        print(f"{WHITE}⏳ Trwa skan {label}: {GREEN}{' '.join(cmd_list)}{RESET}")
        result = subprocess.run(cmd_list, capture_output=True, text=True)
        with open(output_file, 'a') as f:
            f.write(f"\n\n====== {label} ======\n")
            f.write(result.stdout)
        print(GREEN + f"[✔] Skan {label} zakończony sukcesem." + RESET)

def main():
    intro()
    ip, output, mode = ask_input()

    if mode not in scan_modes:
        print(RED + "❌ Nieprawidłowy wybór trybu skanowania." + RESET)
        return

    label = scan_modes[mode]['name']
    command = scan_modes[mode]['command'](ip)

    print(YELLOW + f"\n📦 Zbieranie danych o {ip} w trybie: {label}" + RESET)
    time.sleep(1)

    execute_scan(command, output, label)

    print(GREEN + f"\n✅ Raport zapisany do pliku: {output}" + RESET)

if __name__ == "__main__":
    main()
