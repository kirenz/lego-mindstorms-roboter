"""Erweiterte Roboter-Steuerung mit Hub-Tasten.

Hub-Tasten Steuerung:
- Linke Taste: Links + Vorwärts
- Rechte Taste: Rechts + Vorwärts  
- Beide Tasten: Vorwärts geradeaus
- Bluetooth-Taste kurz: Modus wechseln
- Bluetooth-Taste lang (2s): Beenden

Modi:
1. Fahr-Modus (Blau): Lenken + Fahren
2. Arm-Modus (Lila): Greifarm steuern
"""

from pybricks.hubs import InventorHub
from pybricks.pupdevices import Motor, UltrasonicSensor
from pybricks.parameters import Port, Button, Color
from pybricks.tools import wait, StopWatch

# Hub initialisieren
hub = InventorHub()

# Geschwindigkeiten
DRIVE_SPEED = 500
STEERING_ANGLE = 45
ARM_ROTATE_SPEED = 300
ARM_LIFT_SPEED = 300

# Geräte initialisieren
print("Initialisiere...")

steering_motor = None
drive_motor = None
arm_rotate_motor = None
arm_lift_motor = None
distance_sensor = None

try:
    steering_motor = Motor(Port.A)
    print("✓ Lenkung (A)")
except:
    print("✗ Lenkung (A)")

try:
    drive_motor = Motor(Port.B)
    print("✓ Antrieb (B)")
except:
    print("✗ Antrieb (B)")

try:
    arm_rotate_motor = Motor(Port.C)
    print("✓ Arm-Drehung (C)")
except:
    print("✗ Arm-Drehung (C)")

try:
    arm_lift_motor = Motor(Port.D)
    print("✓ Arm-Heben (D)")
except:
    print("✗ Arm-Heben (D)")

try:
    distance_sensor = UltrasonicSensor(Port.F)
    print("✓ Sensor (F)")
except:
    print("✗ Sensor (F)")

# Lenkung zentrieren
if steering_motor:
    steering_motor.run_target(300, 0, wait=True)

print("\n=== BEREIT ===")

# Modi
MODE_DRIVE = 0
MODE_ARM = 1
current_mode = MODE_DRIVE

mode_names = {
    MODE_DRIVE: "🚗 FAHR-MODUS",
    MODE_ARM: "🦾 ARM-MODUS"
}

mode_colors = {
    MODE_DRIVE: Color.BLUE,
    MODE_ARM: Color.MAGENTA
}

print(f"\n{mode_names[current_mode]}")
print("Links/Rechts: Steuern")
print("Bluetooth kurz: Modus")
print("Bluetooth lang: Ende")
hub.light.on(mode_colors[current_mode])

# Hauptschleife
try:
    is_active = False
    bluetooth_timer = StopWatch()
    bluetooth_pressed = False
    
    while True:
        pressed = hub.buttons.pressed()
        
        # Bluetooth-Taste für Modus-Wechsel oder Beenden
        if Button.BLUETOOTH in pressed:
            if not bluetooth_pressed:
                bluetooth_timer.reset()
                bluetooth_pressed = True
        else:
            if bluetooth_pressed:
                # Taste wurde losgelassen
                press_time = bluetooth_timer.time()
                
                if press_time > 2000:
                    # Lang gedrückt (>2s) = Beenden
                    print("\nBeende...")
                    break
                else:
                    # Kurz gedrückt = Modus wechseln
                    current_mode = (current_mode + 1) % 2
                    print(f"\n{mode_names[current_mode]}")
                    hub.light.on(mode_colors[current_mode])
                    
                    # Stop alle Motoren beim Wechsel
                    if drive_motor:
                        drive_motor.stop()
                    if steering_motor:
                        steering_motor.hold()
                    if arm_rotate_motor:
                        arm_rotate_motor.stop()
                    if arm_lift_motor:
                        arm_lift_motor.stop()
                    
                    wait(500)  # Kurze Pause
                
                bluetooth_pressed = False
        
        # Steuerung je nach Modus
        if current_mode == MODE_DRIVE:
            # FAHR-MODUS
            if Button.LEFT in pressed and Button.RIGHT in pressed:
                # Beide Tasten = Geradeaus
                if not is_active:
                    print("Vorwärts")
                    hub.light.on(Color.CYAN)
                if drive_motor:
                    drive_motor.run(DRIVE_SPEED)
                if steering_motor:
                    steering_motor.run_target(500, 0, wait=False)
                is_active = True
                
            elif Button.LEFT in pressed:
                # Links + Vorwärts
                if not is_active:
                    print("Links + Vor")
                    hub.light.on(Color.GREEN)
                if drive_motor:
                    drive_motor.run(DRIVE_SPEED)
                if steering_motor:
                    steering_motor.run_target(500, -STEERING_ANGLE, wait=False)
                is_active = True
                
            elif Button.RIGHT in pressed:
                # Rechts + Vorwärts
                if not is_active:
                    print("Rechts + Vor")
                    hub.light.on(Color.YELLOW)
                if drive_motor:
                    drive_motor.run(DRIVE_SPEED)
                if steering_motor:
                    steering_motor.run_target(500, STEERING_ANGLE, wait=False)
                is_active = True
                
            else:
                # Keine Taste = Stop
                if is_active:
                    print("Stop")
                    hub.light.on(Color.BLUE)
                    if drive_motor:
                        drive_motor.stop()
                    if steering_motor:
                        steering_motor.hold()
                    is_active = False
        
        elif current_mode == MODE_ARM:
            # ARM-MODUS
            if Button.LEFT in pressed and Button.RIGHT in pressed:
                # Beide Tasten = Arm hoch
                if not is_active:
                    print("Arm HOCH")
                    hub.light.on(Color.WHITE)
                if arm_lift_motor:
                    arm_lift_motor.run(ARM_LIFT_SPEED)
                is_active = True
                
            elif Button.LEFT in pressed:
                # Links = Arm links drehen
                if not is_active:
                    print("Arm LINKS")
                    hub.light.on(Color.ORANGE)
                if arm_rotate_motor:
                    arm_rotate_motor.run(-ARM_ROTATE_SPEED)
                is_active = True
                
            elif Button.RIGHT in pressed:
                # Rechts = Arm rechts drehen
                if not is_active:
                    print("Arm RECHTS")
                    hub.light.on(Color.VIOLET)
                if arm_rotate_motor:
                    arm_rotate_motor.run(ARM_ROTATE_SPEED)
                is_active = True
                
            else:
                # Keine Taste = Stop
                if is_active:
                    print("Stop")
                    hub.light.on(Color.MAGENTA)
                    if arm_rotate_motor:
                        arm_rotate_motor.stop()
                    if arm_lift_motor:
                        arm_lift_motor.stop()
                    is_active = False
        
        wait(50)

except KeyboardInterrupt:
    print("\nUnterbrochen")

finally:
    print("\nStoppe...")
    if drive_motor:
        drive_motor.stop()
    if steering_motor:
        steering_motor.run_target(300, 0)
    if arm_rotate_motor:
        arm_rotate_motor.stop()
    if arm_lift_motor:
        arm_lift_motor.stop()
    hub.light.on(Color.RED)
    print("Gestoppt")
