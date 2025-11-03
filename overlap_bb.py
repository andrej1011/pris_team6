from visualizer import calc_all_bboxes
from folderopen import only_number

def overlap_report_file(prefix):
    return f"{prefix}{only_number()}.log"

    
def overlap(route_filepath, filepath='b9/rrg.xml', prefix="overlap_reports/overlap_"):
    report_file = overlap_report_file(prefix)
    lista_svega = calc_all_bboxes(route_filepath, filepath)
    with open(report_file, 'a', encoding='utf-8') as log_file:
        log_file.write(f"PROVERA BOUNDING BOX PREKLAPANJA ZA {route_filepath}\n")
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


if __name__ == '__main__':
    print(f"Greska: Ovaj fajl se ne moze pokrenuti!\n        Pokrenite main.py fajl!")
    exit(1)