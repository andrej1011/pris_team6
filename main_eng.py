#TAČKA 17. MATPLOTLIB DEPENDENCY CHECK
#IAKO GA MAIN NE KORISTI, BOLJE DA ŠTO PRE BACI GREŠKU, PRE KORIŠĆENJA PROGRAMA
try:
    import matplotlib.pyplot as plt
except ImportError:
    print("Error - Missing a key library: matplotlib")
    print("-" * 50)
    print("This project cannot work without this library.")
    print("Please install it using the following command in terminal:\n")
    print("pip install matplotlib")
    print("-" * 50)
    print("\nExiting the program.")
    exit(1)

from visualizer import draw
from overlap_bb import overlap, conflict_report
from heatmap import heatmap_func
from folderopen import openfile, new_filename, uncountable_number
from times import TIME,TIMER
from log_eng import log_info,log_append

if __name__ == '__main__':
    # Pokretanje funkcije za iscrtavanje
    edges,signal,bb,bb_overlap,overlap_report,heatmap,filter,filter_report,graf_konflikata = False,False,False,False,False,False,False,False,False
    drawing_file,report_file,fajl, signal_id, option, signal_no = None, None, None, None, None, None

    print("\n===== MAIN MENU =====")
    print("1. Chip Architecture Visualization")
    print("2. Signal Path Visualization")
    print("3. Signal Visualization by Category (Filtering)")
    print("4. Bounding Box Visualization")
    print("5. Report of all Bounding Box Overlaps")
    print("6. Heatmap Visualization")
    print("7. Conflict Graph Report")
    print("\n8. Exit")
    choice = input("Choose an option: ")
    if choice == '1':
        edges = input("Do you want to draw the edges? (y/n) \n") == 'y'
    elif choice == '2':
        signal = True
        signal_id = input("Enter signal IDs separated by commas \n")
        signal_id = [int(x) for x in signal_id.split(',')]
        fajl = input("Enter the location of the .route file: \n")
    elif choice == '3':
        filter = True
        print("\nSignal filtering options:")
        print("  MINSINK - Signals with the fewest sink nodes")
        print("  MAXSINK - Signals with the most sink nodes")
        print("  MINBB - Signals with the smallest bounding boxes")
        print("  MAXBB - Signals with the largest bounding boxes")
        option = input("\nEnter signal filtering option:\n").upper()
        signal_no = int(input("How many signals do you want to display:\n"))
        filter_report= input("Do you want a report on filtered signals? (y/n) \n") == 'y'
        fajl = input("Enter the location of the .route file: \n")
    elif choice == '4':
        bb = True
        signal_id = input("Enter signal IDs separated by commas \n")
        signal_id = [int(x) for x in signal_id.split(',')]
        bb_overlap= input("Do you want a report of bounding-box overlaps? (y/n) \n") == 'y'
        fajl = input("Enter the location of the .route file: \n")
    elif choice == '5':
        overlap_report = True
        report__file = new_filename("reports/overlap_report_",".log")
        fajl = input("Enter the location of the .route file: \n")
    elif choice == '6':
        heatmap = True
        drawing_file = new_filename("slike/heatmap_")
        report_file = new_filename("reports/heatmap_report_",".log")
        fajl = input("Enter the location of the .route file: \n")
    elif choice == '7':
        graf_konflikata = True
        report_file = new_filename("reports/conflict_graph_report_",".log")
        fajl = input("Enter the location of the .route file: \n")
    elif choice == '8':
        print("Exiting the program.")
        exit(0)
    else:
        print("Invalid input, exiting the program.")
        exit(0)

    
    start_time = TIME()
    log_info(start_time,fajl,edges,signal,signal_id,bb,bb_overlap,overlap_report,heatmap)
    if(overlap_report):
        report_file = new_filename("reports/overlap_all_report_",".log")
        overlap(report_file,fajl)
    elif(heatmap):
        heatmap_func(drawing_file,report_file,fajl)
    elif(graf_konflikata):
        report_file = new_filename("reports/conflict_graph_report_",".log")
        conflict_report(report_file,fajl)
    else:
        drawing_file = new_filename()
        if(bb_overlap):
            report_file = new_filename("reports/overlap_report_",".log")
        if(filter_report):
            report_file = new_filename("reports/signal_filter_report_",".log")
        draw(drawing_file,fajl,edges,signal,signal_id,bb,bb_overlap,filter,filter_report,report_file,option,signal_no)
    end_time = TIME()
    total_time = TIMER(end_time-start_time)
    print("\nTotal time: " + total_time)
    log_append(total_time,drawing_file,report_file)
    if(drawing_file is not None):
        openfile(drawing_file)
    if(report_file is not None):
        openfile(report_file)
    logfile = f"logs/log_{uncountable_number()}.log"
    print(f"LOG REPORT GENERATED AT: {logfile}")