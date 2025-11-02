from visualizer import draw
from overlap_bb import overlap
from folderopen import openfile, new_filename
from times import TIME,TIMER

if __name__ == '__main__':
    # Pokretanje funkcije za iscrtavanje
    edges,signal,bb,bb_overlap,overlap_report,heatmap = False,False,False,False,False,False
    fajl, signal_id = None, None

    print("\n===== GLAVNI MENI =====")
    print("1. Vizuelizacija arhitekture čipa")
    print("2. Vizuelizacija putanje signala")
    print("3. Vizuelizacija Bounding Box")
    print("4. Izveštaj bounding box preklapanja")
    print("5. Heatmap vizuelizacija")
    print("\n6. Izlaz")
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
        bb = True
        multi_bb= input("Da li želite da se crtaju boundingbox više signala? (y/n) \n") == 'y'
        signal_id = input("Unesite ID signala odvojene zarezima \n")
        signal_id = [int(x) for x in signal_id.split(',')]
        bb_overlap= input("Da li želite izveštaj o preklapanju boundingbox-ova? (y/n) \n") == 'y'
        fajl = input("Unesite lokaciju .route fajla: \n")
    elif choice == '4':
        overlap_report = True
        fajl = input("Unesite lokaciju .route fajla: \n")
    elif choice == '5':
        heatmap = True
        fajl = input("Unesite lokaciju .route fajla: \n")
    elif choice == '6':
        print("Izlazim iz programa.")
        exit(0)
    else:
        print("Pogrešan unos, pokušajte ponovo.")
        exit(0)

    
    start_time = TIME()
    if(overlap_report):
        overlap(fajl)
        openfile("overlap_reports/overlap.log")
    elif(heatmap):
        print("Opcija heatmap nije jos uvek implementirana.")
    else:
        drawing_file = new_filename()
        draw(drawing_file,fajl,edges,signal,signal_id,bb,bb_overlap)
        openfile(drawing_file)
    end_time = TIME()
    print("Ukupno vreme:" + TIMER(end_time-start_time))

    #openfile(drawing_file)