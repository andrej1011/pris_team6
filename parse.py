import xml.etree.ElementTree as ET
import re
from config_variables import ERROR_RED, BLOCK_SIZE, WIRE_LENGTH, PIN_WIRE_LENGHT,DRAWING_OFFSET



def parse_size(filepath):
    tree = ET.parse(filepath)
    root = tree.getroot()

    channel_info = root.find('channels/channel')
    x_max = int(channel_info.get('x_max'))
    y_max = int(channel_info.get('y_max'))

    return x_max, y_max

def parse_grid(filepath):

    tree = ET.parse(filepath)
    root = tree.getroot()

    block_types = {}
    for block_type in root.findall('block_types/block_type'):
        block_id = block_type.get('id')
        block_name = block_type.get('name')
        block_types[block_id] = block_name

    grid_locations = []
    for grid_loc in root.findall('grid/grid_loc'):
        loc_info = {
            'x': int(grid_loc.get('x')),
            'y': int(grid_loc.get('y')),
            'id': grid_loc.get('block_type_id')
        }
        grid_locations.append(loc_info)

    return grid_locations, block_types

def parse_nodes(filepath):
    tree = ET.parse(filepath)
    root = tree.getroot()

    nodes_list = []
    for node in root.findall('rr_nodes/node'):
        loc = node.find('loc')
        
        type = node.get('type')
        ptc = int(loc.get('ptc'))
        x = int(loc.get('xhigh'))
        y = int(loc.get('yhigh'))
        side = None
        
        #IF BLOKOVI I RACUNANJE ABSOLUTE_X_Y
        # MESTO BLOKA KOME PRIPADA + POMERAJ U ODNOSU NA BLOK
        absolute_x1 = 0
        absolute_y1 = 0
        absolute_x2 = 0
        absolute_y2 = 0
        if(type=='CHANX'):
            absolute_x1 = 2*x*BLOCK_SIZE
            absolute_y1 = (2*y+1+0.1+0.1*ptc)*BLOCK_SIZE
            absolute_x2 = absolute_x1 + WIRE_LENGTH
            absolute_y2 = absolute_y1 
        elif(type=='CHANY'):
            absolute_x1 = (2*x+1+0.1+0.1*ptc)*BLOCK_SIZE
            absolute_y1 = 2*y*BLOCK_SIZE
            absolute_x2 = absolute_x1 
            absolute_y2 = absolute_y1 + WIRE_LENGTH
        elif(type in ('IPIN','OPIN')):
            side = loc.get('side')

            if(side=='TOP'):
                absolute_x1 = 2*x*BLOCK_SIZE + BLOCK_SIZE/9*(ptc+0.5)
                absolute_y1 = (2*y+1)*BLOCK_SIZE 
                absolute_x2 = absolute_x1
                absolute_y2 = absolute_y1 + PIN_WIRE_LENGHT
            if(side=='BOTTOM'):
                absolute_x1 = 2*x*BLOCK_SIZE + BLOCK_SIZE/9*(ptc+0.5)
                absolute_y1 = 2*y*BLOCK_SIZE 
                absolute_x2 = absolute_x1
                absolute_y2 = absolute_y1 - PIN_WIRE_LENGHT
            if(side=='LEFT'):
                absolute_x1 = 2*x*BLOCK_SIZE
                absolute_y1 = 2*y*BLOCK_SIZE + BLOCK_SIZE/9*(ptc+0.5)
                absolute_x2 = absolute_x1 - PIN_WIRE_LENGHT
                absolute_y2 = absolute_y1
            if(side=='RIGHT'):
                absolute_x1 = (2*x+1)*BLOCK_SIZE 
                absolute_y1 = 2*y*BLOCK_SIZE + BLOCK_SIZE/9*(ptc+0.5)
                absolute_x2 = absolute_x1 + PIN_WIRE_LENGHT
                absolute_y2 = absolute_y1
            if(side=='TOP_RIGHT'):
                absolute_x1 = 2*x*BLOCK_SIZE + BLOCK_SIZE/15*ptc+0.035
                absolute_y1 = (2*y+1)*BLOCK_SIZE 
                absolute_x2 = (2*x+1)*BLOCK_SIZE
                absolute_y2 = 2*y*BLOCK_SIZE + BLOCK_SIZE/15*ptc+0.035
            # CLB IMA ISTE PINOVE I SA GORNJE (TOP) I SA DESNE (RIGHT) STRANE
            # X1,Y1 JE TOP POZICIJA PINA, X2,Y2 JE RIGHT POZICIJA PINA
            # KORISTIMO IH PO POTREBI (AKO JE RIGHT BLIZE, POVEZI SA RIGHT STRANOM)

        elif(type in ('SINK','SOURCE')):
            absolute_x1 = 2*x*BLOCK_SIZE + BLOCK_SIZE/2.0
            absolute_y1 = 2*y*BLOCK_SIZE + BLOCK_SIZE/2.0
            absolute_x2 = absolute_x1
            absolute_y2 = absolute_y1

        node_info = {
            'id': int(node.get('id')),
            'type':type, 
            'ptc': ptc,
            'x': x,
            'y': y,
            'a_x1':absolute_x1,
            'a_y1':absolute_y1,
            'a_x2':absolute_x2,
            'a_y2':absolute_y2,
        }
        if (side!='None'):
            node_info['side'] = side
        
        nodes_list.append(node_info)
        
    return nodes_list

def parse_edges(filepath):
    
    tree = ET.parse(filepath)
    root = tree.getroot()
    
    edges_list = []
    for edge in root.findall('rr_edges/edge'):
        edge_info = {
            'source': int(edge.get('src_node')),
            'sink': int(edge.get('sink_node'))
        }
        edges_list.append(edge_info)
        
    return edges_list

def parse_1signal(filepath, signal_id):

    signal_nodes_list = []
    capturing = False # Flag koji oznacava da li smo na trazenom signalu
    
    net_pattern = re.compile(r"Net\s+(\d+)\s+")
    node_id_pattern = re.compile(r"Node:\s*(\d+)\s*")

    try:
        with open(filepath, 'r') as f:
            for line in f:
                line = line.strip()
                net_match = net_pattern.match(line)
                if net_match:
                    current_net = int(net_match.group(1))
                    if current_net == signal_id:
                        capturing = True
                    elif capturing:
                        break
                    continue
                if capturing:
                    node_match = node_id_pattern.search(line)
                    if node_match:
                        node_id = int(node_match.group(1))
                        signal_nodes_list.append(node_id)
            return signal_nodes_list
            
    except FileNotFoundError:
        print(f"Greška: Fajl '{filepath}' nije pronađen.")
        return []
    except Exception as e:
        print(f"Došlo je do greške prilikom čitanja fajla: {e}")
        return []

if __name__ == '__main__':
    print(f"{ERROR_RED}Greska: Ovaj fajl se ne moze pokrenuti!\n        Pokrenite main.py fajl!")
    exit(1)