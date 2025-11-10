import subprocess
import os
import sys
from config_variables import file_prefix

def openfile(filename="slike/fpga.png"):
    directory = os.path.dirname(filename)

    if directory == "":
        directory = "."

    directory = os.path.abspath(directory)

    try:
        if sys.platform == "win32":
            # Windows
            os.startfile(directory)
        elif sys.platform == "darwin":
            # MacOS
            subprocess.run(["open", directory])
        elif sys.platform.startswith("linux"):
            # Linux
            subprocess.run(["xdg-open", directory])
        else:
            print(f"Unsupported operating system: {sys.platform}")
    except Exception as e:
        print(f"An error occurred trying to open the directory: {e}")

        
def new_filename(prefix="slike/fpga_",ext=".png"):
   new_number = uncountable_number()
   return f"{prefix}{new_number}{ext}"

def uncountable_number():

    current_number = 0
    filepath = 'file_counter.txt'
    
    try:
        with open(filepath, 'r') as f:
            line = f.readline().strip()

            if line:
                try:
                    current_number = int(line)
                except ValueError:
                    print(f"Upozorenje: Vrednost '{line}' u {filepath} nije integer. Resetuje se na 0.")
                    current_number = 0

            
    except FileNotFoundError:
        current_number = 0
    except Exception as e:
        print(f"Neočekivana greška pri čitanju {filepath}: {e}")
        current_number = 0

    return current_number

def countable_number():

    current_number = 0
    filepath = 'file_counter.txt'
    
    try:
        with open(filepath, 'r') as f:
            line = f.readline().strip()

            if line:
                try:
                    current_number = int(line)
                except ValueError:
                    print(f"Upozorenje: Vrednost '{line}' u {filepath} nije integer. Resetuje se na 0.")
                    current_number = 0

            
    except FileNotFoundError:
        current_number = 0
    except Exception as e:
        print(f"Neočekivana greška pri čitanju {filepath}: {e}")
        current_number = 0

    new_number = current_number + 1
    
    try:
        with open(filepath, 'w') as f:
            f.write(str(new_number))
    except IOError as e:
        print(f"GREŠKA: Nije moguće upisati u {filepath}: {e}")
    
    return new_number

if __name__ == '__main__':
    openfile()