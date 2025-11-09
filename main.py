from visualizer import draw
from overlap_bb import overlap
from heatmap import heatmap_func
from folderopen import openfile, new_filename
from times import TIME,TIMER
from log_report import log_info,log_append

if __name__ == '__main__':
    # Pokretanje funkcije za iscrtavanje
    edges,signal,bb,bb_overlap,overlap_report,heatmap,filter,filter_report = False,False,False,False,False,False,False,False
    drawing_file,report_file,fajl, signal_id, option, signal_no = None, None, None, None, None, None

    print("\n===== GLAVNI MENI =====")
    print("1. Vizuelizacija arhitekture čipa")
    print("2. Vizuelizacija putanje signala")
    print("3. Vizuelizacija signala po kategoriji (Filtriranje)")
    print("4. Vizuelizacija Bounding Box")
    print("5. Izveštaj bounding box preklapanja")
    print("6. Heatmap vizuelizacija")
    print("\n7. Izlaz")
    choice = input("Izaberite opciju: ")
    if choice == '1':
        edges = input("Da li želite da se crtaju ivice? (y/n) \n") == 'y'
    elif choice == '2':
        signal = True
        multi_signal = input("Da li želite da se crtaju putanje više signala? (y/n) \n") == 'y'
        signal_id = input("Unesite ID signala odvojene zarezima \n")
        signal_id = [int(x) for x in signal_id.split(',')]
        fajl = input("Unesite lokaciju .route fajla: \n")
    elif choice == '3':
        filter = True
        print("\nOpcije za filtriranje signala:")
        print("  MINSINK - Signali sa najmanje uvorišnih čvorova")
        print("  MAXSINK - Signali sa najviše uvorišnih čvorova")
        print("  MINBB - Signali sa najmanjim opisanim pravougaonicima")
        print("  MAXBB - Signali sa najvećim opisanim pravougaonicima")
        option = input("\nUnesite opciju za filtriranje signala:\n").upper()
        signal_no = int(input("Koliko signala želite da prikažete:\n"))
        filter_report= input("Da li želite izveštaj o filtriranim signalima? (y/n) \n") == 'y'
        fajl = input("Unesite lokaciju .route fajla: \n")
    elif choice == '4':
        bb = True
        multi_bb= input("Da li želite da se crtaju boundingbox više signala? (y/n) \n") == 'y'
        signal_id = input("Unesite ID signala odvojene zarezima \n")
        signal_id = [int(x) for x in signal_id.split(',')]
        bb_overlap= input("Da li želite izveštaj o preklapanju boundingbox-ova? (y/n) \n") == 'y'
        fajl = input("Unesite lokaciju .route fajla: \n")
    elif choice == '5':
        overlap_report = True
        drawing_file = new_filename("reports/overlap_",".log")
        fajl = input("Unesite lokaciju .route fajla: \n")
    elif choice == '6':
        heatmap = True
        drawing_file = new_filename("slike/heatmap_")
        report_file = new_filename("reports/heatmap_",".log")
        fajl = input("Unesite lokaciju .route fajla: \n")


    elif choice == '7':
        print("Izlazim iz programa.")
        exit(0)
    else:
        print("Pogrešan unos, izlazim iz programa.")
        exit(0)

    
    start_time = TIME()
    log_info(start_time,fajl,edges,signal,signal_id,bb,bb_overlap,overlap_report,heatmap)
    if(overlap_report):
        overlap(drawing_file,fajl)
    elif(heatmap):
        heatmap_func(drawing_file,report_file,fajl)
    else:
        drawing_file = new_filename()
        if(bb_overlap):
            report_file = new_filename("reports/overlap_",".log")
        if(filter_report):
            report_file = new_filename("reports/signal_filter_",".log")
        draw(drawing_file,fajl,edges,signal,signal_id,bb,bb_overlap,filter,filter_report,report_file,option,signal_no)
    end_time = TIME()
    total_time = TIMER(end_time-start_time)
    print("Ukupno vreme:" + total_time)
    log_append(total_time,drawing_file,report_file)

    openfile(drawing_file)
    if(report_file is not None):
        openfile(drawing_file)