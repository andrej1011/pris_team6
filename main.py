from visualizer import draw
from folderopen import openfile, new_filename
from times import TIME,TIMER

if __name__ == '__main__':
    # Pokretanje funkcije za iscrtavanje
    
    edges = input("Da li želite da se crtaju ivice? (y/n) \n") == 'y'
    signal,bb = False,False
    fajl, signal_id = None, None
    if (input("Da li želite da se crtaju signali? (y/n) \n") == 'y') :
        signal= True
        signal_id = int(input("Unesite ID signala \n"))
        fajl = input("Unesite lokaciju .route fajla: \n")
        bb = input("Da li želite da se crta bounding box oko signala? (y/n) \n") == 'y'
    drawing_file = new_filename()
    start_time = TIME()
    draw(drawing_file,fajl,edges,signal,None or signal_id,bb)
    end_time = TIME()
    print("Ukupno vreme:" + TIMER(end_time-start_time))

    openfile(drawing_file)