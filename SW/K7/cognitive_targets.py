# Programm berechnet die gültigen "cognitive targets" bei RoboCupJunior Rescue Maze

# Datei öffnen
datei = open("cognitive_targets.txt", mode = "w")

# gültige "cognitive targets" berechnen
for i in range(-2,3):
    for j in range(-2,3):
        for k in range(-2,3):
            for l in range(-2,3):
                for m in range(-2,3):
                    summe = i + j + k + l + m
                    if (summe == 0) or (summe == 1) or (summe == 2):
                        string = "rings: {} {} {} {} {} summe: {} \n".format(i, j, k, l, m, summe)
                        datei.write(string)

# Datei schließen
datei.close()
                        
