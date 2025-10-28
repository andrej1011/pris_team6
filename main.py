from visualizer import draw
from folderopen import openfile, new_filename


if __name__ == '__main__':
    # Pokretanje funkcije za iscrtavanje
    
    edges = input("Da li želite da se crtaju ivice? (y/n) \n") == 'y'
    signal = False
    signal_id = None
    bb = False
    if (input("Da li želite da se crtaju signali? (y/n) \n") == 'y') :
        signal= True
        fajl = input("Unesite lokaciju .route fajla: \n")
        signal_id = int(input("Unesite ID signala \n"))
        bb = input("Da li želite da se crta bounding box oko signala? (y/n) \n") == 'y'
    drawing_file = new_filename()
    draw(drawing_file,fajl,edges,signal,signal_id,bb)

    openfile(drawing_file)