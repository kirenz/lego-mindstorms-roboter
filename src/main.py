"""Roboter-Steuerung für LEGO Mindstorms MVP-Buggy-Fahrzeug.

Dieses Programm läuft auf dem Roboter und wartet auf Tasten-Befehle.
Nutze die Hub-Tasten für Links/Rechts-Lenkung.
"""

from pybricks.hubs import InventorHub
from pybricks.pupdevices import Motor, UltrasonicSensor
from pybricks.parameters import Port, Button, Color
from pybricks.tools import wait

# Hub initialisieren
hub = InventorHub()

# Geschwindigkeiten und Winkel
DRIVE_SPEED = 500        # Fahrgeschwindigkeit in Grad/Sekunde
STEERING_ANGLE = 45      # Maximaler Lenkwinkel
ARM_ROTATE_SPEED = 300   # Greifarm Drehgeschwindigkeit
ARM_LIFT_SPEED = 300     # Greifarm Hebe-Geschwindigkeit

# Motoren und Sensoren mit Fehlerbehandlung initialisieren
print("Initialisiere Geräte...")
#hub.light.on((100, 100, 0))  # Gelb = wird initialisiert

steering_motor = None
drive_motor = None
arm_rotate_motor = None
arm_lift_motor = None
distance_sensor = None

try:
    steering_motor = Motor(Port.A)
    print("✓ Motor A (Lenkung) gefunden")
except OSError:
    print("✗ Motor A (Lenkung) nicht gefunden")

try:
    drive_motor = Motor(Port.B)
    print("✓ Motor B (Antrieb) gefunden")
except OSError:
    print("✗ Motor B (Antrieb) nicht gefunden")

try:
    arm_rotate_motor = Motor(Port.C)
    print("✓ Motor C (Greifarm Drehung) gefunden")
except OSError:
    print("✗ Motor C (Greifarm Drehung) nicht gefunden")

try:
    arm_lift_motor = Motor(Port.D)
    print("✓ Motor D (Greifarm Hoch/Runter) gefunden")
except OSError:
    print("✗ Motor D (Greifarm Hoch/Runter) nicht gefunden")

try:
    distance_sensor = UltrasonicSensor(Port.F)
    print("✓ Sensor F (Ultraschall-Abstandssensor) gefunden")
except OSError:
    distance_sensor = None
    print("✗ Sensor F (Ultraschall-Abstandssensor) nicht gefunden")

# Lenkung in Mittelposition bringen, falls vorhanden
if steering_motor:
    print("Zentriere Lenkung...")
    steering_motor.run_target(300, 0, wait=True)

print("\n=== Roboter bereit! ===")
print("Hub-Tasten-Steuerung:")
print("  Links = Links lenken + Vorwärts")
print("  Rechts = Rechts lenken + Vorwärts")
print("  Beide gleichzeitig = Vorwärts geradeaus")
print("  Bluetooth-Taste = Beenden")
hub.light.on(Color.GREEN)  # Grün = bereit


def execute_command(cmd):
    """Führt einen Steuerbefehl aus."""
    cmd = cmd.lower().strip()
    
    if cmd == 'w':
        # Vorwärts fahren
        if drive_motor:
            print("Vorwärts")
            drive_motor.run_time(DRIVE_SPEED, 1000, wait=False)
            hub.light.on(Color.BLUE)  # Blau
        else:
            print("Motor B nicht verfügbar")
        
    elif cmd == 's':
        # Rückwärts fahren
        if drive_motor:
            print("Rückwärts")
            drive_motor.run_time(-DRIVE_SPEED, 1000, wait=False)
            hub.light.on(Color.YELLOW)  # Gelb
        else:
            print("Motor B nicht verfügbar")
        
    elif cmd == 'a':
        # Links lenken
        if steering_motor:
            print("Links")
            steering_motor.run_target(500, -STEERING_ANGLE, wait=False)
        else:
            print("Motor A nicht verfügbar")
        
    elif cmd == 'd':
        # Rechts lenken
        if steering_motor:
            print("Rechts")
            steering_motor.run_target(500, STEERING_ANGLE, wait=False)
        else:
            print("Motor A nicht verfügbar")
        
    elif cmd == 'i':
        # Greifarm hoch
        if arm_lift_motor:
            print("Arm hoch")
            arm_lift_motor.run_time(ARM_LIFT_SPEED, 1000, wait=False)
        else:
            print("Motor D nicht verfügbar")
        
    elif cmd == 'k':
        # Greifarm runter
        if arm_lift_motor:
            print("Arm runter")
            arm_lift_motor.run_time(-ARM_LIFT_SPEED, 1000, wait=False)
        else:
            print("Motor D nicht verfügbar")
        
    elif cmd == 'j':
        # Greifarm links drehen
        if arm_rotate_motor:
            print("Arm links")
            arm_rotate_motor.run_time(-ARM_ROTATE_SPEED, 1000, wait=False)
        else:
            print("Motor C nicht verfügbar")
        
    elif cmd == 'l':
        # Greifarm rechts drehen
        if arm_rotate_motor:
            print("Arm rechts")
            arm_rotate_motor.run_time(ARM_ROTATE_SPEED, 1000, wait=False)
        else:
            print("Motor C nicht verfügbar")
        
    elif cmd == 'x' or cmd == ' ':
        # Alles stoppen
        print("Stop")
        if drive_motor:
            drive_motor.stop()
        if steering_motor:
            steering_motor.hold()
        if arm_rotate_motor:
            arm_rotate_motor.stop()
        if arm_lift_motor:
            arm_lift_motor.stop()
        hub.light.on(Color.GREEN)  # Grün
        
    elif cmd == 'm':
        # Abstand messen
        if distance_sensor:
            try:
                distance = distance_sensor.distance()
                print(f"Abstand: {distance} mm")
            except Exception as e:
                print(f"Sensor-Fehler: {e}")
        else:
            print("Sensor F nicht verfügbar")
    
    elif cmd == '0':
        # Lenkung zentrieren
        if steering_motor:
            print("Zentriere Lenkung")
            steering_motor.run_target(500, 0, wait=True)
        else:
            print("Motor A nicht verfügbar")
    
    else:
        print(f"Unbekannter Befehl: {cmd}")


# Hauptsteuerungsschleife mit Hub-Tasten
try:
    print("\n🎮 Steuerung aktiv!")
    
    # Fahrmodus-Variable
    is_driving = False
    
    while True:
        # Prüfe Hub-Tasten
        pressed = hub.buttons.pressed()
        
        if Button.BLUETOOTH in pressed:
            # Bluetooth-Taste beendet Programm
            print("Beende...")
            break
        
        # Beide Tasten = Vorwärts geradeaus
        elif Button.LEFT in pressed and Button.RIGHT in pressed:
            if not is_driving:
                print("Vorwärts geradeaus")
                hub.light.on(Color.BLUE)
            if drive_motor:
                drive_motor.run(DRIVE_SPEED)
            if steering_motor:
                steering_motor.run_target(500, 0, wait=False)
            is_driving = True
            
        # Nur linke Taste = Links lenken + vorwärts
        elif Button.LEFT in pressed:
            if not is_driving:
                print("Links + Vorwärts")
                hub.light.on(Color.CYAN)
            if drive_motor:
                drive_motor.run(DRIVE_SPEED)
            if steering_motor:
                steering_motor.run_target(500, -STEERING_ANGLE, wait=False)
            is_driving = True
            
        # Nur rechte Taste = Rechts lenken + vorwärts
        elif Button.RIGHT in pressed:
            if not is_driving:
                print("Rechts + Vorwärts")
                hub.light.on(Color.MAGENTA)
            if drive_motor:
                drive_motor.run(DRIVE_SPEED)
            if steering_motor:
                steering_motor.run_target(500, STEERING_ANGLE, wait=False)
            is_driving = True
            
        # Keine Taste = Stop
        else:
            if is_driving:
                print("Stop")
                hub.light.on(Color.GREEN)
                if drive_motor:
                    drive_motor.stop()
                if steering_motor:
                    steering_motor.hold()
                is_driving = False
        
        # Alternativ: Einfache Demo-Sequenz
        # Auskommentieren, um automatische Demo zu aktivieren
        """
        print("\nDemo-Sequenz:")
        execute_command('w')
        wait(2000)
        execute_command('x')
        
        execute_command('a')
        wait(1000)
        execute_command('0')
        
        execute_command('w')
        wait(2000)
        execute_command('x')
        
        execute_command('d')
        wait(1000)
        execute_command('0')
        
        execute_command('s')
        wait(2000)
        execute_command('x')
        
        print("Demo beendet.")
        break
        """
        
        wait(50)

except KeyboardInterrupt:
    print("\nUnterbrochen")

finally:
    # Aufräumen - Alle Motoren stoppen
    print("\nStoppe alle Motoren...")
    if drive_motor:
        drive_motor.stop()
    if steering_motor:
        steering_motor.run_target(300, 0)
    if arm_rotate_motor:
        arm_rotate_motor.stop()
    if arm_lift_motor:
        arm_lift_motor.stop()
    hub.light.on(Color.RED)
    print("Roboter gestoppt.")
