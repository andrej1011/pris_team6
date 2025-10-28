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

if __name__ == '__main__':
    openfile()