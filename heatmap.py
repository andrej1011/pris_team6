#HEATMAP.py je u izradi




















import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.lines import Line2D

from parse import parse_size,parse_nodes, parse_all_signals
from visualizer import draw_grid,draw_nodes
from config_variables import rrg_filepath, BLOCK_SIZE, heavily_used_node,very_used_node


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

def heatmap_func(drawing_file,report_file,route_filepath):
    nodelist = provera_node(route_filepath)
    #draw_heatmap(drawing_file,route_filepath)
    heatmap_report(nodelist,report_file,route_filepath)

def draw_heatmap(drawing_file,route_filepath):
    #TODO ZAPOCETO HEATMAP CRTANJE
    max_x, max_y = parse_size(rrg_filepath)
    fig, ax = plt.subplots(figsize=(max_x, max_y))

    #Ova dva se crtaju po default-u
    draw_grid(rrg_filepath,ax)
    draw_nodes(rrg_filepath,ax)

    ax.set_xlim(0, max_x*2-BLOCK_SIZE)
    ax.set_ylim(0, max_y*2-BLOCK_SIZE)
    ax.set_aspect('equal', adjustable='box')
    ax.axis('off')
    fig.tight_layout()
    plt.rcParams['savefig.dpi'] = 40
    plt.savefig(drawing_file)

def heatmap_report(nodelist, report_file, route_filepath):

    all_nodes_list = parse_nodes(rrg_filepath)
    nodes_lookup = {node['id']: node for node in all_nodes_list}

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
            node_details = nodes_lookup.get(node_id) # Pronađi detalje čvora

            node_type = node_details.get('type', 'N/A')
            x = node_details.get('x', '?')
            y = node_details.get('y', '?')
            ptc = node_details.get('ptc', 'N/A')
            
            # Formatiraj liniju tačno kako si tražio
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
    print(f"Greska: Ovaj fajl se ne moze pokrenuti!\n        Pokrenite main.py fajl!")
    exit(1)