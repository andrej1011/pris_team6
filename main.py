import visualizer


if __name__ == '__main__':
    # Pokretanje funkcije za iscrtavanje
    # Potrebno je da se 'rrg.xml' nalazi u istom direktorijumu
    fajl = input("Unesite lokaciju route fajla: \n")
    answer = input("Da li želite da se crtaju ivice? (y/n) \n")
    edges = (answer == 'y')
    answer = input("Da li želite da se crtaju signali? (y/n) \n")
    signal = False
    signal_id = None
    bb = False
    if (answer == 'y') :
        signal= True
        signal_id = int(input("Unesite ID signala \n"))
        answer = input("Da li želite da se crta boudning box? (y/n) \n")
        bb = (answer == 'y')
        
    visualizer.draw(fajl,edges,signal,signal_id,bb)