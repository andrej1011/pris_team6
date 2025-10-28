import subprocess
import os
from config_variables import filename

def openfile():
    try:
        # MacOS
        subprocess.run(["open", "-R", filename])
        # Linux
        directory = os.path.dirname(filename)
        subprocess.run(["xdg-open", directory])
        # Windows
        os.startfile(filename)

    except Exception as e:
        print(f"An error occurred: {e}")


def file_number():
    #ZAPOČETO
    try:
        with open('file_counter.txt', 'r') as f:
            for line in f:
                line = line.strip()

    except FileNotFoundError:
        return "0"

if __name__ == '__main__':
    openfile()