"""Ein kleines Pybricks Programm fuer den LEGO Inventor Hub."""

# Wir holen uns die Pybricks Klassen, damit Python mit Hub und Motor sprechen kann.
from pybricks.hubs import InventorHub
from pybricks.pupdevices import Motor
from pybricks.parameters import Port
from pybricks.tools import wait

# Hub in Python vorbereiten (das ist der "Stein" mitten im Roboter).
hub = InventorHub()

# Motor, der an Port A steckt, mit Python verbinden.
m = Motor(Port.A)

# Motor macht eine volle Umdrehung nach vorne (360 Grad) mit Tempo 300 Grad/Sekunde.
m.run_angle(300, 45)

# Kurze Pause in Millisekunden, damit der Motor Zeit bekommt anzuhalten.
wait(500)

# Motor dreht noch einmal genauso weit zurueck (negatives Tempo = andere Richtung).
m.run_angle(-300, 45)

# Gruenes Licht zeigt: Programm fertig und alles hat geklappt.
hub.light.on((0, 100, 0))
