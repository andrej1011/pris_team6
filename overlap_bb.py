from parse import parse_all_signals, parse_nodes
from visualizer import calc_all_bboxes
    
def overlap(report_file, route_filepath, filepath='b9/rrg.xml', prefix="overlap_reports/overlap_"):
    lista_svega = calc_all_bboxes(route_filepath, filepath)
    with open(report_file, 'a', encoding='utf-8') as log_file:
        log_file.write(f"PROVERA SVIH BOUNDING BOX PREKLAPANJA\n")
        log_file.write(f"ROUTE FILE: {route_filepath}\n")
        log_file.write(f"   Koordinate: (min_x, min_y, max_x,max_y)\n\n")
        for i in range(len(lista_svega)):
            signal_i = lista_svega[i]
            i_k = signal_i[1]
            for j in range(i + 1, len(lista_svega)):

                signal_j = lista_svega[j]
                j_k = signal_j[1]

                preklapanje_X = (i_k[0] <= j_k[2] and i_k[2] >= j_k[0])
                preklapanje_Y = (i_k[1] <= j_k[3] and i_k[3] >= j_k[1])
                if (preklapanje_X and preklapanje_Y):
                    
                        log_file.write(f"SIGNALI: {signal_i[0]} i {signal_j[0]}\n")
                        log_file.write(f"{i_k}\n")
                        log_file.write(f"{j_k}\n")
                        log_file.write("\n")

def build_conflict_graph(route_filepath, rrg_filepath='b9/rrg.xml'):
    """
    Gradi graf konflikata za dati .route fajl.
    Vraca:
      - conflicts: lista [(signal1_id, signal2_id, weight, [shared_node_objects])]
      - conflict_signals: set svih signala koji su u konfliktu
    """

    # Ucitavanje svih informacija o cvorovima (trebaju nam za detaljan ispis)
    nodes_dict = {} # {node_id: node_object}
    try:
        nodes_list = parse_nodes(rrg_filepath)
        for node in nodes_list:
            nodes_dict[node['id']] = node
    except Exception as e:
        print(f"Greska pri ucitavanju RRG cvorova: {e}")
        return [], set()

    # Ucitavanje svih signala
    signals_dict = parse_all_signals(route_filepath)
    if not signals_dict:
        print("Nema signala za analizu.")
        return [], set()

    # izbacujemo SINK cvorove
    clean_signals = {}
    for signal_id, node_list in signals_dict.items():
        clean_nodes = set()
        for node_id in node_list:
            # Provera da li cvor postoji i da NIJE SINK
            node_obj = nodes_dict.get(node_id)
            if node_obj and node_obj['type'] != 'SINK':
                clean_nodes.add(node_id)
        clean_signals[signal_id] = clean_nodes

    # Detekcija konflikata
    conflicts = []
    conflict_signals = set()
    signal_ids = sorted(list(clean_signals.keys()))

    for i in range(len(signal_ids)):
        signal_i_id = signal_ids[i]
        nodes_i = clean_signals[signal_i_id]

        for j in range(i + 1, len(signal_ids)):
            signal_j_id = signal_ids[j]
            nodes_j = clean_signals[signal_j_id]

            # Presek skupova ID-jeva cvorova
            intersection_ids = nodes_i.intersection(nodes_j)
            weight = len(intersection_ids)

            if weight > 0:
                # Imamo konflikt!
                conflict_signals.add(signal_i_id)
                conflict_signals.add(signal_j_id)
                
                # Nalazimo objekte za deljene cvorove radi detaljnog ispisa
                shared_node_objects = [nodes_dict[nid] for nid in intersection_ids]
                
                conflicts.append((signal_i_id, signal_j_id, weight, shared_node_objects))

    # Sortiramo konflikte po tezini opadajuce
    conflicts.sort(key=lambda x: x[2], reverse=True)

    return conflicts, conflict_signals

def conflict_report(report_filepath, route_filepath,rrg_filepath='b9/rrg.xml'):
    conflicts, conflict_signals = build_conflict_graph(route_filepath,rrg_filepath)
    # Generise detaljan tekstualni izvestaj o konfliktima
    try:
        with open(report_filepath, 'w', encoding='utf-8') as f:
            f.write("GRAF KONFLIKATA REPORT\n")
            f.write(f"ULAZNI FAJL: {route_filepath}\n\n")
            
            f.write(f"BROJ KONFLIKTNIH SIGNALA: {len(conflict_signals)}\n")
            # Sortira listu signala za lepsi ispis
            sorted_signals = sorted(list(conflict_signals))
            f.write(f"KONFLIKTNI SIGNALI: {sorted_signals}\n\n")
            
            f.write(f"BROJ KONFLIKTNIH PAROVA: {len(conflicts)}\n\n")

            if not conflicts:
                f.write("Nema detektovanih konflikata.\n")
                return

            f.write("== DETALJI KONFLIKATA ==\n\n")
            for sig1, sig2, weight, shared_nodes in conflicts:
                 f.write(f"SIGNALI: ({sig1}, {sig2}) \n")
                 f.write(f"TEŽINA KONFLIKTA: {weight}\n")
                 
                 for i, node in enumerate(shared_nodes, 1):
                     # Formatira string:
                     # 1. CHANX (3,2, ptc: 1) [nodeid: 134]
                     node_type = node['type']
                     x, y = node['x'], node['y']
                     ptc = node['ptc']
                     node_id = node['id']
                     
                     f.write(f" {i}. {node_type} ({x},{y}, ptc: {ptc}) [nodeid: {node_id}]\n")
                 
                 f.write("\n")

    except Exception as e:
        print(f"Greska pri generisanju reporta: {e}")


if __name__ == '__main__':
    print(f"Greska: (overlap_bb.py) se ne moze pokrenuti!\n        Pokrenite main.py fajl!")
    exit(1)