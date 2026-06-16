# PNG-Bild in PPM - Format umwandeln
# Bildformat 189 x 189

# Bibliothek importieren
from PIL import Image

# Bild-Datei öffnen
im = Image.open("cognitive_target.png")
# Liste mit RGB-Werten erstelllen
pixels = list(im.getdata())

# In Datei schreiben
with open("cognitive_target.ppm", mode = "w") as datei:
    # Dateikopf schreiben
    datei.write("P3\n")
    datei.write("# Farbbild der Groesse 189 x 189 Pixels\n")
    datei.write("189 189\n")
    datei.write("255\n")
    for i in range(len(pixels)):
        # hier Zeilenumbruch (nicht notwendig, verbessert die Übersicht)
        if i%189 == 0:
            datei.write("\n{} {} {} ".format(pixels[i][0], pixels[i][1], pixels[i][2]))
        # kein Zeilenumbruch
        else:
            datei.write("{} {} {} ".format(pixels[i][0], pixels[i][1], pixels[i][2]))
   
