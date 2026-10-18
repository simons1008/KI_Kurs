# Supervised learning: Erkenne Sportarten anhand von Features
# - Perzeptron-Funktion definieren
# - Perzeptron-Lernregel anwenden
# - test_feature definieren
# - gelernte Gewichte auf test_feature anwenden und Voraussage prüfen
# Quelle:  https://www.youtube.com/@STARTUPTEENS/playlists 
#          Programmiere mit Python - Baue deine eigene KI! #19
# Änderungen: Features angepasst, Visualisierung entfernt,
#             3-mal perzeptron aufrufen

# Bibliothek importieren
import numpy as np
import matplotlib.pyplot as plt

# Daten in numpy-Array speichern
# [gruen_50, weiss_50, kreisform, gelb, ist_tennis, ist_ski, ist_fussball]
train_feature = np.array([[1, 0, 1, 1, 1, 0, 0],
			  [1, 0, 1, 1, 1, 0, 0],
			  [0, 0, 1, 1, 1, 0, 0],
			  [1, 0, 1, 1, 1, 0, 0],
			  [0, 1, 0, 0, 0, 1, 0],
			  [0, 1, 0, 0, 0, 1, 0],
			  [0, 1, 0, 0, 0, 1, 0],
			  [0, 1, 0, 0, 0, 1, 0],
			  [1, 0, 1, 0, 0, 0, 1],
			  [1, 0, 1, 0, 0, 0, 1],
			  [1, 0, 0, 0, 0, 0, 1],
			  [1, 0, 1, 0, 0, 0, 1],
			  [1, 0, 1, 0, 0, 0, 1]])

test_feature = np.array([[0, 0, 1, 0, 0, 0, 0],
                         [1, 0, 1, 0, 0, 0, 1],
                         [1, 0, 1, 0, 0, 0, 1],
                         [0, 0, 1, 1, 1, 0, 0],
                         [0, 0, 1, 1, 1, 0, 0],
                         [0, 1, 0, 0, 0, 1, 0],
                         [0, 1, 0, 0, 0, 1, 0]])
                         
# Array-Dimensionen ausgeben
print("Array-Dimensionen")
print("train_feature", train_feature.shape)
print("test_feature", test_feature.shape)
   
# Gewichte initialisieren
tennis_w = np.zeros(4)
ski_w = np.zeros(4)
fussball_w = np.zeros(4)
print("Gewichte zu Beginn")
print("tennis_w", tennis_w)
print("ski_w", ski_w)
print("fussball_w", fussball_w)
print("\n")

# Perzeptron-Funktion
def perzeptron(w, x):
    if np.dot(w, x) > 2:
        return 1
    else:
        return 0

# Perzeptron Lernregel
# +/- gruen_50  zu w[0]
# +/- weiss_50  zu w[1]
# +/- kreisform zu w[2]
# +/- gelb      zu w[3]
print("Training")
cnt = 0
max_epochs = 4
fehler = np.zeros(max_epochs)
while cnt < max_epochs:
    print("Durchlauf", cnt)
    for index in range(len(train_feature)):
        x = train_feature[index, 0:4]
        # 3-mal perzeptron aufrufen
        # auf Tennis prüfen
        label = train_feature[index, 4] # Tennis-Label
        delta = label - perzeptron(tennis_w, x) # Tennis-Gewichte
        if delta != 0: # falsch klassifiziert
            print("Tennis Perzeptron: index", index, "falsch klassifiert")
            fehler[cnt] += 1
            tennis_w += delta * x
            print("Neu: tennis_w", tennis_w)
        # auf Ski prüfen
        label = train_feature[index, 5] # Ski-Label
        delta = label - perzeptron(ski_w, x) # Ski-Gewichte
        if delta != 0: # falsch klassifiziert
            print("Ski Perzeptron: index", index, "falsch klassifiert")
            fehler[cnt] += 1
            ski_w += delta * x
            print("Neu: ski_w", ski_w)
        # auf Fussball prüfen
        label = train_feature[index, 6] # Fussball-Label
        delta = label - perzeptron(fussball_w, x) # Fussball-Gewichte
        if delta != 0: # falsch klassifiziert
            print("Fussball Perzeptron: index", index, "falsch klassifiert")
            fehler[cnt] += 1
            fussball_w += delta * x
            print("Neu: fussball_w", fussball_w)         
    # wenn trainiert
    if fehler[cnt] == 0:
        break
    cnt += 1
else:
    print("Es wurde keine Lösung gefunden.")

# Fehler in den Epochen zeigen
plt.plot(range(max_epochs), fehler)
plt.xlabel('Epochen')
plt.ylabel('Falsche Klassifikationen')
plt.show()

# gelernte Gewichte ausgeben
print("\n")
print("gelernte Gewichte")
print("tennis_w", tennis_w)
print("ski_w", ski_w)
print("fussball_w", fussball_w)
print("\n")

# gelernte Gewichte auf test_feature anwenden
print("Test")
correct = 0
for index in range(len(test_feature)):
    x = test_feature[index, 0:4]
    # 3-mal perzeptron aufrufen
    # auf Tennis prüfen
    label = test_feature[index, 4] # Tennis-Label
    delta = label - perzeptron(tennis_w, x) # gelernte Tennis-Gewichte
    if delta != 0: # falsch klassifiziert
        print("Tennis Perzeptron: index", index, "falsch klassifiert")
    else:
        correct += 1
    # auf Ski prüfen
    label = test_feature[index, 5] # Ski-Label
    delta = label - perzeptron(ski_w, x) # gelernte Ski-Gewichte
    if delta != 0: # falsch klassifiziert
        print("Ski Perzeptron: index", index, "falsch klassifiert")      
    else:
        correct += 1
    # auf Fussball prüfen
    label = test_feature[index, 6] # Fussball-Label
    delta = label - perzeptron(fussball_w, x) # gelernte Fussball-Gewichte
    if delta != 0: # falsch klassifiziert
        print("Fussball Perzeptron: index", index, "falsch klassifiert")
    else: 
        correct += 1

# Verhältnis berechnen
ratio = correct/ (3 * len(test_feature))
print("Es wurden {:5.1f} Prozent richtig klassifiziert".format(100*ratio))

# Ende
input("Fertig? ")
