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

def SIGNAL_COLOR(broj_boja,alpha_hex='80'):
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
            rgb_boja = FIKSNE_BOJE[i]
            # 2. Dodaj joj alpha (npr. "#34AAFF" + "CC" -> "#34AAFFCC")
            lista_boja.append(f"{rgb_boja}{alpha_hex}")
        else:
            # 1. Generiši nasumičnu osnovnu boju
            rgb_boja = f'#{random.randint(0, 0xFFFFFF):06x}'
            # 2. Dodaj joj alpha
            lista_boja.append(f"{rgb_boja}{alpha_hex}")
            
    return lista_boja

#DEFINICIJE ISKORISCENIH NODEOVA ZA HEATMAP.PY
heavily_used_node = 4 # 4 i vise
very_used_node = 2 # 2 i vise


#FILENAMES OF IMAGES
rrg_filepath = 'b9/rrg.xml'
file_prefix = 'slike/fpga_'
