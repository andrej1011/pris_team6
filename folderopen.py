import subprocess
import os
from config_variables import file_prefix

def openfile(filename="slike/fpga.png"):
    try:
        # MacOS
        subprocess.run(["open", "-R", filename])
        
    except Exception as e:
        try:
            # Linux
            directory = os.path.dirname(filename)
            subprocess.run(["xdg-open", directory])
        except:
            # Windows
            directory = os.path.dirname(filename)
            os.startfile(filename)
            #print(f"An error occurred: {e}")

def new_filename(prefix="slike/fpga_",ext=".png"):
   new_number = uncountable_number()
   return f"{prefix}{new_number}{ext}"

def only_number():

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
        print(f"Info: {filepath} nije pronađen. Kreira se novi fajl i počinje se od broja 1.")
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
        print(f"Info: {filepath} nije pronađen. Kreira se novi fajl i počinje se od broja 1.")
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
        print(f"Info: {filepath} nije pronađen. Kreira se novi fajl i počinje se od broja 1.")
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