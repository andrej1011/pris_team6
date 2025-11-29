#IMPLEMENTACIJA LOGIKE ZA LOG FAJLOVE
from folderopen import countable_number,uncountable_number

def log_info(start_time,route_file,edges,signal,signal_id,bb,bb_overlap,overlap_report,heatmap):
    #Establish new log name
    log_filename = f"logs/log_{countable_number()}.log"
    with open(log_filename, 'a', encoding='utf-8') as log_file:
        log_file.write(f"LOG INFO\n\n")
        log_file.write(f"START TIME: {start_time}\n")
        log_file.write(f".ROUTE FILE: {route_file}\n")
        log_file.write(f"SELECTED OPTION: ")
        #proveravamo sta se crta
        if(heatmap):
            log_file.write(f"HEATMAP\n")
        elif(overlap_report):
            log_file.write(f"OVERLAP REPORT\n")
        else:
            #onda je neko od crtanja
                if(bb_overlap):
                    log_file.write(f"Bounding Box Visualization + Bounding Box overlap report\n")
                    log_file.write(f"SIGNALS: {signal_id}\n")
                elif(bb):
                    log_file.write(f"Bounding Box Visualization\n")
                    log_file.write(f"SIGNALS: {signal_id}\n")
                elif(signal):
                    log_file.write(f"Signal path visualization\n")
                    log_file.write(f"SIGNALS: {signal_id}\n")
                else:
                    log_file.write(f"Chip architecture visualization\n")
                    log_file.write(f"EDGES: {edges}\n")
        log_file.write("\n\n")

def log_the_error(e):
    #TODO Implementirati logovanje gresaka
    return

def log_append(total_time, drawing_file, report_file = None):
    log_filename = f"logs/log_{uncountable_number()}.log"
    with open(log_filename, 'a', encoding='utf-8') as log_file:
        log_file.write(f"TIME ELAPSED: {total_time}\n\n")
        log_file.write(f"FILES GENERATED:\n")
        if(drawing_file is not None):
            log_file.write(f"   {drawing_file}\n")
        if(report_file is not None):
            log_file.write(f"   {report_file}\n")
        log_file.write("---------------------------------------------\n")

if __name__ == '__main__':

    print(f"Error: This file is not executable!\n        Please run the main.py file!")
    exit(1)