import random
# GLOBAL VARIABLES

# ZA PROMENU VELICINA PROMENITE IH OVDE I SAMO OVDE
BLOCK_SIZE = 1
WINDOW_BORDER = BLOCK_SIZE * 0.3 
WIRE_LENGTH = BLOCK_SIZE * 1.0
WIRE_THICKNESS = BLOCK_SIZE * 0.5
PIN_WIRE_THICKNESS = BLOCK_SIZE * 0.15
PIN_WIRE_LENGHT = BLOCK_SIZE * 0.8
DRAWING_OFFSET = BLOCK_SIZE * 0.01

ERROR_RED = "\033[91m"

#COLORS
COLOROF_CHAN_WIRE = "#000000"
COLOROF_SINKSOURCE = "#000000"
COLOROF_EDGEWIRE = "#DFDDDD92"
COLOROF_EDGE_INDOT = "#000000BB"
COLOROF_EDGE_OUTDOT = "#9F9F9FFF"
SIGNAL_COLOR = "#34AAFF" 

def tamnija(hex_color):  #TODO: ZASTARELA FUNKCIJA, Deprecate this function
    hex = hex_color.lstrip('#')
    r, g, b = int(hex[0:2], 16), int(hex[2:4], 16), int(hex[4:6], 16)
    return f"#{int(r * 0.5):02x}{int(g * 0.5):02x}{int(b * 0.5):02x}"

def SIGNAL_COLOR(broj_boja):
    FIKSNE_BOJE = [
    "#34AAFF",  # 1. Plava
    "#B00101",  # 2. Crvena
    "#04B304",  # 3. Zelena
    "#3434FF",  # 4. Tamnoplava
    "#FFAA00",  # 5. Narandžasta
    "#53FDFD"   # 6. Cijan
    ]
    
    lista_boja = []
    for i in range(broj_boja):
        if i < len(FIKSNE_BOJE):
            # Uzmi fiksnu boju iz liste
            lista_boja.append(FIKSNE_BOJE[i])
        else:
            # Generiši nasumičnu boju
            color = f'#{random.randint(0, 0xFFFFFF):06x}'
            lista_boja.append(color)
            
    return lista_boja


#FILENAME OF IMAGES
file_prefix = 'slike/fpga_'