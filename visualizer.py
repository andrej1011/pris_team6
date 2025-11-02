
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.lines import Line2D
from math import sqrt

from parse import parse_edges, parse_grid, parse_size, parse_nodes, parse_1signal

#VARIJABLE
from  config_variables import BLOCK_SIZE,WIRE_THICKNESS, PIN_WIRE_LENGHT, PIN_WIRE_THICKNESS, DRAWING_OFFSET,\
ERROR_RED,COLOROF_CHAN_WIRE, COLOROF_SINKSOURCE,COLOROF_EDGEWIRE,COLOROF_EDGE_INDOT,COLOROF_EDGE_OUTDOT, SIGNAL_COLOR



def draw(drawing_file,r_filepath,want_edges,want_signal,signal_id,want_bb):

    filepath = 'b9/rrg.xml'
    max_x, max_y = parse_size(filepath)
    fig, ax = plt.subplots(figsize=(max_x, max_y))

    #Ova dva se crtaju po default-u
    draw_grid(filepath,ax)
    draw_nodes(filepath,ax)

    if(want_edges):
        draw_edges(filepath,ax)
    if(want_signal):
        draw_signal(signal_id,SIGNAL_COLOR,r_filepath,filepath,ax)

    if(want_bb):
        draw_bounding_box(signal_id,SIGNAL_COLOR,r_filepath,filepath,ax)

    # Podešavanje izgleda grafika
    ax.set_xlim(0, max_x*2-BLOCK_SIZE)
    ax.set_ylim(0, max_y*2-BLOCK_SIZE)
    ax.set_aspect('equal', adjustable='box')
    ax.axis('off')
    fig.canvas.manager.set_window_title("FPGA Chip Layout")
    fig.tight_layout()
    plt.rcParams['savefig.dpi'] = 600 #POVECAN DPI SLIKE
    plt.savefig(drawing_file)

def draw_grid(filepath,ax):

    try:
        grid_data, block_types = parse_grid(filepath)
    except FileNotFoundError:
        print(f"Greška: fajl '{filepath}' nije pronađen.")
        return
    except Exception as e:
        print(f"Došlo je do greške prilikom parsiranja fajla: {e}")
        return

    colorsgrid = {
        'io': "#808080",  # IO boja sa slike 12
        'clb': '#E2DBDB', # CLB boja sa slike 12
    }


    for block_info in grid_data:
        block_name = block_types.get(block_info['id'])
        x, y = block_info['x'], block_info['y']

        if block_name != 'EMPTY':

            # Iscrtavanje kvadrata za blok
            rect = patches.Rectangle(
                (x*2*BLOCK_SIZE, y*2*BLOCK_SIZE), BLOCK_SIZE, BLOCK_SIZE,
                facecolor=colorsgrid.get(block_name)
            )
            ax.add_patch(rect)
            
            # TEKST koordinate (x,y)
            ax.text(
                x*2*BLOCK_SIZE + 0.075*BLOCK_SIZE, y*2*BLOCK_SIZE + 0.70*BLOCK_SIZE, f"({x},{y})",
                ha='left', va='top',
                fontsize=7*BLOCK_SIZE,
                fontfamily='sans-serif'
            )
            # TEKST BLOK TYPE
            ax.text(
                x*2*BLOCK_SIZE + 0.05*BLOCK_SIZE, y*2*BLOCK_SIZE + 0.05*BLOCK_SIZE, block_name.upper(),
                ha='left', va='bottom', 
                fontsize=12*BLOCK_SIZE,
                fontweight='medium',     
                fontfamily='sans-serif'
            )

def draw_nodes(filepath,ax):
    try:
        nodes_list = parse_nodes(filepath)
    except FileNotFoundError:
        print(f"Greška: fajl '{filepath}' nije pronađen.")
        return
    except Exception as e:
        print(f"Došlo je do greške prilikom parsiranja fajla: {e}")
        return
    
    for node in nodes_list:
        if(node['type']=='CHANY'):
            ax.add_line(Line2D([node['a_x1'],node['a_x2']], [node['a_y1']+DRAWING_OFFSET, node['a_y2']-DRAWING_OFFSET], color= COLOROF_CHAN_WIRE, linewidth=WIRE_THICKNESS))
        elif(node['type']=='CHANX'):
            ax.add_line(Line2D([node['a_x1']+DRAWING_OFFSET, node['a_x2']-DRAWING_OFFSET], [node['a_y1'], node['a_y2']], color= COLOROF_CHAN_WIRE, linewidth=WIRE_THICKNESS))

def draw_edges(filepath,ax):
    try:
        edges_list = parse_edges(filepath)
        nodes_list = parse_nodes(filepath)
        nodes_dict = {node['id']: node for node in nodes_list}

    except FileNotFoundError:
        print(f"Greška: fajl '{filepath}' nije pronađen.")
        return
    except Exception as e:
        print(f"Došlo je do greške prilikom parsiranja fajla: {e}")
        return
    for pin_node in nodes_list:
        if(pin_node['type'] in ('IPIN','OPIN')):
            if(pin_node['side']=='TOP_RIGHT'):
                # CRTANJE TOP STRANE
                ax.add_patch(patches.Circle((pin_node['a_x1'], pin_node['a_y1']), radius=0.005, color=COLOROF_SINKSOURCE, zorder=1))
                ax.add_line(Line2D([pin_node['a_x1'], pin_node['a_x1']], [pin_node['a_y1'], pin_node['a_y1']+PIN_WIRE_LENGHT], color=COLOROF_EDGEWIRE, linewidth=PIN_WIRE_THICKNESS))
                # CRTANJE RIGHT STRANE
                ax.add_patch(patches.Circle((pin_node['a_x2'],pin_node['a_y2']), radius=0.01, color= COLOROF_SINKSOURCE, zorder=1))
                ax.add_line(Line2D([pin_node['a_x2'], pin_node['a_x2']+PIN_WIRE_LENGHT], [pin_node['a_y2'], pin_node['a_y2']], color=COLOROF_EDGEWIRE, linewidth=PIN_WIRE_THICKNESS))
            else:
                ax.add_patch(patches.Circle((pin_node['a_x1'], pin_node['a_y1']), radius=0.005, color=COLOROF_SINKSOURCE, zorder=1))
                ax.add_line(Line2D([pin_node['a_x1'], pin_node['a_x2']], [pin_node['a_y1'], pin_node['a_y2']], color=COLOROF_EDGEWIRE, linewidth=PIN_WIRE_THICKNESS))

    for edge in edges_list:
        source_id, sink_id = edge['source'],edge['sink']
        source_node = nodes_dict.get(source_id)
        sink_node = nodes_dict.get(sink_id)
        draw_edge_connection(source_node,sink_node,ax)

def draw_edge_connection(node1, node2, ax):
    if(node1['type']=='CHANX' and node2['type']=='CHANX'):
        if(node1['x'] < node2['x']):
            ax.add_line(Line2D([node1['a_x2'], node2['a_x1']], [node1['a_y2'], node2['a_y1']], color=COLOROF_EDGEWIRE, linewidth=WIRE_THICKNESS))
        else:
            ax.add_line(Line2D([node2['a_x2'], node1['a_x1']], [node2['a_y2'], node1['a_y1']], color=COLOROF_EDGEWIRE, linewidth=WIRE_THICKNESS))
    elif(node1['type']=='CHANY' and node2['type']=='CHANY'):
        if(node1['y'] < node2['y']):
            ax.add_line(Line2D([node1['a_x2'], node2['a_x1']], [node1['a_y2'], node2['a_y1']], color=COLOROF_EDGEWIRE, linewidth=WIRE_THICKNESS))
        else:
            ax.add_line(Line2D([node2['a_x2'], node1['a_x1']], [node2['a_y2'], node1['a_y1']], color=COLOROF_EDGEWIRE, linewidth=WIRE_THICKNESS))
    #PIN NA ZICU (IPIN/OPIN -> CHANX/CHANX)
    elif (node1['type'] in ('CHANX', 'CHANY') and node2['type'] in ('IPIN', 'OPIN')) or \
    (node2['type'] in ('CHANX', 'CHANY') and node1['type'] in ('IPIN', 'OPIN')):
        pin_node = node1 if node1['type'] in ('IPIN', 'OPIN') else node2
        wire_node = node2 if node2['type'] in ('CHANX', 'CHANY') else node1

        b_x, b_y = 0,0
        if(pin_node['side']=='TOP_RIGHT'):
                if(wire_node['type']=='CHANX'):
                    b_x, b_y = pin_node['a_x1'], wire_node['a_y1']
                else:
                    b_x, b_y = wire_node['a_x1'], pin_node['a_y2']
        else:
            if(pin_node['side'] in ('TOP','BOTTOM')):
               b_x, b_y = pin_node['a_x1'], wire_node['a_y1']
            else:
                b_x, b_y = wire_node['a_x1'], pin_node['a_y2']
        ax.add_patch(patches.Circle((b_x, b_y), radius=0.005, color=COLOROF_EDGE_INDOT if pin_node['type'] == 'IPIN' else COLOROF_EDGE_OUTDOT, zorder=1))

def triangle(x_center, y_center, height):
    s = (2 * height) / sqrt(3)
    r_outer = height * 2/3
    r_inner = height * 1/3

    v1 = (x_center, y_center + r_outer)         # Gornji vrh
    v2 = (x_center - s/2, y_center - r_inner)   # Donji levi vrh
    v3 = (x_center + s/2, y_center - r_inner)   # Donji desni vrh

    return [v1, v2, v3]

def draw_singlenode(node,ax,SIGNAL_COLOR):
    type,a_x1,a_y1,a_x2,a_y2 = node['type'],node['a_x1'],node['a_y1'],node['a_x2'],node['a_y2']
    if(type =='SINK'):
        ax.add_patch(patches.Circle((a_x1, a_y1), radius=0.1, color=SIGNAL_COLOR))
    elif(type=='SOURCE'):
        ax.add_patch(patches.Polygon(triangle(a_x1, a_y1, 0.3), color=SIGNAL_COLOR))
    elif(type=='CHANY'):
        ax.add_line(Line2D([a_x1, a_x2], [a_y1+DRAWING_OFFSET, a_y2-DRAWING_OFFSET], color=SIGNAL_COLOR, linewidth=WIRE_THICKNESS*3))
    elif(type=='CHANX'):
        ax.add_line(Line2D([a_x1+DRAWING_OFFSET, a_x2-DRAWING_OFFSET], [a_y1, a_y2], color=SIGNAL_COLOR, linewidth=WIRE_THICKNESS*3))

def calc_si_nodes(node_id_list,filepath):
    nodes_dict = {node['id']: node for node in parse_nodes(filepath)}
    signal_nodes_objects = []
    for node_id in node_id_list:
        node_object = nodes_dict.get(node_id)
        if node_object:
            signal_nodes_objects.append(node_object)
        else:
            print(f"Upozorenje: Čvor ID {node_id} iz signala nije pronađen u nodes_dict.")
    return signal_nodes_objects

def calc_si_edges(signal_nodes):
    list_conns = []
    for i in range(len(signal_nodes)-1):
        node1 = signal_nodes[i]
        if(node1['type']=='SINK'):
            continue
        node2 = signal_nodes[i+1]
        if(node2['type'] in ('IPIN','OPIN')):
            node2 = signal_nodes[i+2]
        #sad smo sigurni da pravilno vezujemo, sad mozemo vezivati, tj return koordinate
        x1,y1,x2,y2 = 0,0,0,0
        #ZICA NA ZICU
        if(node1['type'] in ('CHANX','CHANY') and node2['type'] in ('CHANX','CHANY')):
            if(node1['type']==node2['type']):
                if(node1['x'] < node2['x'] or node1['y']<node2['y']):
                    x1,x2,y1,y2 = node1['a_x2'],node2['a_x1'],node1['a_y2'], node2['a_y1']
                else:
                    x1,x2,y1,y2 = node2['a_x2'],node1['a_x1'],node2['a_y2'],node1['a_y1']
            else:
                median=(node1['a_x1']+node1['a_x2'])/2
                if(abs(median-node2['a_x1'])< abs(median-node2['a_x2'])):
                    x2 = node2['a_x1']
                else:
                    x2 = node2['a_x2']
                median=(node1['a_y1']+node1['a_y2'])/2
                if(abs(median-node2['a_y1'])< abs(median-node2['a_y2'])):
                    y2 = node2['a_y1']
                else:
                    y2 = node2['a_y2']
                #ONDA NALAZIMO GDE NODE1 TREBA DA SE VEZUJE
                median=(node2['a_x1']+node2['a_x2'])/2
                if(abs(median-node1['a_x1'])< abs(median-node1['a_x2'])):
                    x1 = node1['a_x1']
                else:
                    x1 = node1['a_x2']
                median= (node2['a_y1']+node2['a_y2'])/2
                if(abs(median-node1['a_y1'])< abs(median-node1['a_y2'])):
                    y1 = node1['a_y1']
                else:
                    y1 = node1['a_y2']
        #SOURCE/SINK NA ZICU
        elif(node1['type'] in ('SOURCE','CHANX','CHANY') and node2['type'] in ('CHANX','CHANY','SINK')):
            wire_node = node1 if node1['type'] in ('CHANX', 'CHANY') else node2
            s_node = node2 if node2['type'] in ('SINK', 'SOURCE') else node1
            if(wire_node['type']=='CHANX'):
                x1,x2,y1,y2 = s_node['a_x1'],s_node['a_x1'],s_node['a_y1'],wire_node['a_y1']
            else:
                x1,x2,y1,y2 = s_node['a_x1'],wire_node['a_x1'],s_node['a_y1'],s_node['a_y1']
        if not(set([x1,x2,y1,y2]) == {0}):
            list_conns.append([x1,x2,y1,y2])
    return list_conns

def calc_signal(signal_id,route_filepath,filepath):
    signal_nodes, signal_edges = [],[]
    signal_info = parse_1signal(route_filepath,signal_id)
    signal_nodes = calc_si_nodes(signal_info,filepath)
    signal_edges = calc_si_edges(signal_nodes)

    return signal_nodes,signal_edges

def draw_signal(signal_id,SIGNAL_COLOR,route_filepath,filepath,ax):
    signal_nodes,signal_edges = calc_signal(signal_id,route_filepath,filepath)
    for node in signal_nodes:
        draw_singlenode(node,ax,SIGNAL_COLOR)
    for edge in signal_edges:
        print(f'{edge}')
        ax.add_line(Line2D([edge[0],edge[1]], [edge[2],edge[3]], color=SIGNAL_COLOR, linewidth=WIRE_THICKNESS))

def calc_bounding_box(signal_id,route_filepath,filepath):
    max_x,max_y = 0,0
    min_x, min_y = 7*2+BLOCK_SIZE,7*2+BLOCK_SIZE
    signal_list, _ = calc_signal(signal_id,route_filepath,filepath)
    for node in signal_list:
        if node['type'] in ('SINK, SOURCE'):
            #DA SELEKTUJE CEO BLOK A NE SAMO POLA BLOKA
            node['a_x1'],node['a_x2'],node['a_y1'],node['a_y2'] = 2*node['x']*BLOCK_SIZE,(2*node['x']+1)*BLOCK_SIZE,2*node['y']*BLOCK_SIZE,(2*node['y']+1)*BLOCK_SIZE
        if (min(node['a_x1'],node['a_x2'])<min_x):
            min_x = min(node['a_x1'],node['a_x2'])
        if (max(node['a_x1'],node['a_x2'])>max_x):
            max_x = max(node['a_x1'],node['a_x2'])
        if (min(node['a_y1'],node['a_y2'])<min_y):
            min_y = min(node['a_y1'],node['a_y2'])
        if (max(node['a_y1'],node['a_y2'])>max_y):
            max_y = max(node['a_y1'],node['a_y2'])

    return min_x, min_y, max_x,max_y

def draw_bounding_box(signal_id,SIGNAL_COLOR,route_filepath,filepath,ax):
    min_x, min_y, max_x, max_y  = calc_bounding_box(signal_id,route_filepath,filepath)
    ax.add_patch(patches.Rectangle((min_x, min_y),(max_x-min_x),(max_y-min_y),facecolor=SIGNAL_COLOR,edgecolor='none',alpha=0.2,linewidth=4*BLOCK_SIZE))

if __name__ == '__main__':
    print(f"{ERROR_RED}Greska: Ovaj fajl se ne moze pokrenuti!\n        Pokrenite main.py fajl!")
    exit(1)
    