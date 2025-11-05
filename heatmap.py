#HEATMAP.py je u izradi

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.lines import Line2D

from parse import parse_size,parse_grid,parse_nodes, parse_all_signals
from config_variables import rrg_filepath, BLOCK_SIZE,DRAWING_OFFSET,WIRE_THICKNESS, heavily_used_node,very_used_node,\
heat_colorsgrid,heat_background_purple,heatmap_colors



def provera_node(route_filepath):

    all_nodes_list = parse_nodes(rrg_filepath)
    all_signals_dict = parse_all_signals(route_filepath)

    temp_report = {}
    for node in all_nodes_list:
        node_id = node['id']
        temp_report[node_id] = [0, []] # [puta_iskoriscen, [lista_signala]]

    for signal_id, node_id_list in all_signals_dict.items():
        for node_id in node_id_list:
            if node_id in temp_report:
                temp_report[node_id][0] += 1
                temp_report[node_id][1].append(signal_id)

    final_report = {}
    for node_id, data in temp_report.items():
        final_report[node_id] = (data[0], data[1])

    sorted_items = sorted(final_report.items(), key=lambda item: item[1][0], reverse=True)
    sorted_report = dict(sorted_items)

    return sorted_report

def draw_heatmap_grid(ax):

    grid_data, block_types = parse_grid(rrg_filepath)

    for block_info in grid_data:
        block_name = block_types.get(block_info['id'])
        x, y = block_info['x'], block_info['y']

        if block_name != 'EMPTY':

            # Iscrtavanje kvadrata za blok
            rect = patches.Rectangle(
                (x*2*BLOCK_SIZE, y*2*BLOCK_SIZE), BLOCK_SIZE, BLOCK_SIZE,
                facecolor=heat_colorsgrid.get(block_name)
            )
            ax.add_patch(rect)
            
            # TEKST BLOK TYPE
            ax.text(
                x*2*BLOCK_SIZE + 0.05*BLOCK_SIZE, y*2*BLOCK_SIZE + 0.05*BLOCK_SIZE, block_name.upper(),
                ha='left', va='bottom', 
                fontsize=12*BLOCK_SIZE,
                fontweight='medium',     
                fontfamily='sans-serif'
            )

def draw_heated_nodes(ax,nodelist,nodes_lookup):
    for node_id, data_tuple in nodelist.items():
        count = data_tuple[0]
        node = nodes_lookup.get(node_id)
        draw_heated_singlenode(node,ax,heatmap_colors[count])

def draw_heated_singlenode(node,ax,SIGNAL_COLOR):
    type,a_x1,a_y1,a_x2,a_y2 = node['type'],node['a_x1'],node['a_y1'],node['a_x2'],node['a_y2']
    #if(type =='SINK'):
        #ax.add_patch(patches.Circle((a_x1, a_y1), radius=0.1, color=SIGNAL_COLOR))
    if(type=='CHANY'):
        ax.add_line(Line2D([a_x1, a_x2], [a_y1+DRAWING_OFFSET, a_y2-DRAWING_OFFSET], color=SIGNAL_COLOR, linewidth=WIRE_THICKNESS*3))
    elif(type=='CHANX'):
        ax.add_line(Line2D([a_x1+DRAWING_OFFSET, a_x2-DRAWING_OFFSET], [a_y1, a_y2], color=SIGNAL_COLOR, linewidth=WIRE_THICKNESS*3))

def draw_heated_edges(ax,route_filepath,nodes_lookup,nodelist):
    edgeslist = compile_all_edges(route_filepath,nodes_lookup)
    for edge in edgeslist:
        node1_id, node2_id = edge
        node1 = nodes_lookup.get(node1_id)
        node2 = nodes_lookup.get(node2_id)
        #ODREDJUJEMO BOJU VEZE - BOJA UPOTREBLJENIJEG
        count1 = nodelist[node1_id][0]
        count2 = nodelist[node2_id][0]
        EDGE_COLOR = heatmap_colors[max(count1,count2)]
        draw_heated_edge_connection(node1,node2,EDGE_COLOR,ax)

def draw_heated_edge_connection(node1, node2,EDGE_COLOR,ax):
   x1,y1,x2,y2 = 0,0,0,0
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
   elif(node1['type'] in ('SOURCE','CHANX','CHANY') and node2['type'] in ('CHANX','CHANY','SINK')):
        wire_node = node1 if node1['type'] in ('CHANX', 'CHANY') else node2
        s_node = node2 if node2['type'] in ('SINK', 'SOURCE') else node1
        if(wire_node['type']=='CHANX'):
            x1,x2,y1,y2 = s_node['a_x1'],s_node['a_x1'],s_node['a_y1'],wire_node['a_y1']
        else:
            x1,x2,y1,y2 = s_node['a_x1'],wire_node['a_x1'],s_node['a_y1'],s_node['a_y1']
   if not(set([x1,x2,y1,y2]) == {0}):
        ax.add_line(Line2D([x1,x2], [y1,y2], color=EDGE_COLOR, linewidth=WIRE_THICKNESS))  

def compile_all_edges(route_filepath,nodes_lookup):

    all_nodes_list = parse_nodes(rrg_filepath)
    net_to_nodes_ids_map = parse_all_signals(route_filepath)
    
    all_edges = set()

    for net_id, node_id_list in net_to_nodes_ids_map.items():
        
        if len(node_id_list) < 2:
            continue # Nema ivica ako ima manje od 2 čvora

        signal_nodes = []
        for node_id in node_id_list:
            if node_id in nodes_lookup:
                signal_nodes.append(nodes_lookup[node_id])

        if len(signal_nodes) < 2:
            continue

        for i in range(len(signal_nodes) - 1):
            try:
                node1 = signal_nodes[i]
                if node1['type'] == 'SINK':
                    continue

                node2 = signal_nodes[i+1]
                sink_node = None

                if node2['type'] in ('IPIN', 'OPIN'):
                    if i + 2 < len(signal_nodes):
                        sink_node = signal_nodes[i+2]
                    else:
                        continue
                else:
                    sink_node = node2
                
                if sink_node is None:
                    continue
                    
                source_id = int(node1['id'])
                sink_id = int(sink_node['id'])
                
                all_edges.add((sink_id, source_id))
            
            except IndexError:
                # Desiće se ako je 'i+2' van opsega
                continue

    return all_edges

def draw_legend(fig, ax):
    
    # Naslov legende
    fig.text(0.015, 0.95, 'HEATMAP legenda\n(prema korišćenju čvora)', color='white', ha='left', weight='bold', fontsize=10, transform=fig.transFigure)
    
    for i, color in enumerate(heatmap_colors):
        y_pos = 0.9 - (i * 0.025) 
        
        rect = patches.Rectangle(
            (0.04, y_pos - 0.005), 0.015, 0.01, # x, y, širina, visina
            facecolor=color,
            transform=fig.transFigure, # Koordinate u odnosu na celu sliku
            clip_on=False
        )
        ax.add_patch(rect)
        # Labela
        label = f"{i}" # 0,1,2...
        # Tekst labela
        fig.text(0.015, y_pos, label, color='white', ha='left', va='center', fontsize=7, transform=fig.transFigure)

def heatmap_func(drawing_file,report_file,route_filepath):
    nodelist = provera_node(route_filepath)
    all_nodes_list = parse_nodes(rrg_filepath)
    nodes_lookup = {node['id']: node for node in all_nodes_list}
    draw_heatmap(drawing_file,route_filepath,nodelist,nodes_lookup)
    heatmap_report(nodelist,report_file,route_filepath,nodes_lookup)

def draw_heatmap(drawing_file, route_filepath, nodelist, nodes_lookup):

    max_x, max_y = parse_size(rrg_filepath)
    fig, ax = plt.subplots(figsize=(max_x, max_y))

    fig.patch.set_facecolor(heat_background_purple)
    ax.set_facecolor(heat_background_purple)

    draw_heatmap_grid(ax)

    draw_heated_nodes(ax, nodelist, nodes_lookup)
    draw_heated_edges(ax,route_filepath,nodes_lookup,nodelist)

    draw_legend(fig, ax)

    ax.set_xlim(0, max_x*2-BLOCK_SIZE)
    ax.set_ylim(0, max_y*2-BLOCK_SIZE)
    ax.set_aspect('equal', adjustable='box')
    ax.axis('off')
    fig.tight_layout()
    plt.rcParams['savefig.dpi'] = 600
    plt.savefig(drawing_file)
    plt.close(fig)
    
def heatmap_report(nodelist, report_file, route_filepath,nodes_lookup):
    heavy_nodes = []
    very_nodes = []
    one_nodes = []
    zero_nodes = []

    for node_id, data_tuple in nodelist.items():
        count = data_tuple[0]

        if count >= heavily_used_node:
            heavy_nodes.append((node_id, data_tuple))
        elif count >= very_used_node:
            very_nodes.append((node_id, data_tuple))
        elif count == 1:
            one_nodes.append((node_id, data_tuple))
        elif count == 0:
            zero_nodes.append((node_id, data_tuple))

    with open(report_file, 'a', encoding='utf-8') as log_file:
        log_file.write("HEATMAP REPORT\n")
        log_file.write(f"   .ROUTE FILE: {route_filepath}\n\n")
        
        def write_log_line(node_id, count, signal_list):
            node_details = nodes_lookup.get(node_id) # Pronalazi detalje čvora

            node_type = node_details.get('type', 'N/A')
            x = node_details.get('x', '?')
            y = node_details.get('y', '?')
            ptc = node_details.get('ptc', 'N/A')
            
            log_line = (
                f"Node id:{node_id} {node_type} ({x},{y} ptc:{ptc})\n"
                f"      Count:{count} Signals: {signal_list}\n"
            )
            
            log_file.write(log_line)

        log_file.write(f"====VEOMA ISKORIŠĆENI ČVOROVI (>={heavily_used_node}) - Ukupno: {len(heavy_nodes)}====\n")
        for node_id, (count, signal_list) in heavy_nodes:
            write_log_line(node_id, count, signal_list)

        log_file.write(f"\n\n====ČVOROVI ISKORIŠĆENI VIŠE PUTA (između {very_used_node} i {heavily_used_node - 1}) - Ukupno: {len(very_nodes)}====\n")
        for node_id, (count, signal_list) in very_nodes:
            write_log_line(node_id, count, signal_list)

        log_file.write(f"\n\n====ČVOROVI ISKORIŠĆENI SAMO JEDNOM - Ukupno: {len(one_nodes)}====\n")
        for node_id, (count, signal_list) in one_nodes:
            write_log_line(node_id, count, signal_list)

        log_file.write(f"\n\n====NEISKORIŠĆENI ČVOROVI - Ukupno: {len(zero_nodes)}====\n")
        for node_id, (count, signal_list) in zero_nodes:
            write_log_line(node_id, count, signal_list)
        

if __name__ == '__main__':
    pp = compile_all_edges("b9/b9.route")
    print(pp)