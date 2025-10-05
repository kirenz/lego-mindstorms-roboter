"""
Roboter-Steuerung die Befehle über print() empfängt.

Dieser Ansatz nutzt die Tatsache, dass wir Text über die
Verbindung senden können, den das Programm dann liest.
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

print("Initialisiere...")

# Geräte initialisieren
steering_motor = None
drive_motor = None
arm_rotate_motor = None
arm_lift_motor = None
distance_sensor = None

try:
    steering_motor = Motor(Port.A)
    print("OK:A")
except:
    print("FAIL:A")

try:
    drive_motor = Motor(Port.B)
    print("OK:B")
except:
    print("FAIL:B")

try:
    arm_rotate_motor = Motor(Port.C)
    print("OK:C")
except:
    print("FAIL:C")

try:
    arm_lift_motor = Motor(Port.D)
    print("OK:D")
except:
    print("FAIL:D")

try:
    distance_sensor = UltrasonicSensor(Port.F)
    print("OK:F")
except:
    print("FAIL:F")

# Lenkung zentrieren
if steering_motor:
    steering_motor.run_target(300, 0, wait=True)

print("READY")
hub.light.on(Color.GREEN)


def execute_cmd(cmd):
    """Führt Befehl aus."""
    if cmd == 'w' and drive_motor:
        print("CMD:forward")
        drive_motor.run_time(DRIVE_SPEED, 1000, wait=False)
        hub.light.on(Color.BLUE)
        
    elif cmd == 's' and drive_motor:
        print("CMD:backward")
        drive_motor.run_time(-DRIVE_SPEED, 1000, wait=False)
        hub.light.on(Color.YELLOW)
        
    elif cmd == 'a' and steering_motor:
        print("CMD:left")
        steering_motor.run_target(500, -STEERING_ANGLE, wait=False)
        
    elif cmd == 'd' and steering_motor:
        print("CMD:right")
        steering_motor.run_target(500, STEERING_ANGLE, wait=False)
        
    elif cmd == 'i' and arm_lift_motor:
        print("CMD:arm_up")
        arm_lift_motor.run_time(ARM_LIFT_SPEED, 1000, wait=False)
        
    elif cmd == 'k' and arm_lift_motor:
        print("CMD:arm_down")
        arm_lift_motor.run_time(-ARM_LIFT_SPEED, 1000, wait=False)
        
    elif cmd == 'j' and arm_rotate_motor:
        print("CMD:arm_left")
        arm_rotate_motor.run_time(-ARM_ROTATE_SPEED, 1000, wait=False)
        
    elif cmd == 'l' and arm_rotate_motor:
        print("CMD:arm_right")
        arm_rotate_motor.run_time(ARM_ROTATE_SPEED, 1000, wait=False)
        
    elif cmd == 'x':
        print("CMD:stop")
        if drive_motor:
            drive_motor.stop()
        if steering_motor:
            steering_motor.hold()
        if arm_rotate_motor:
            arm_rotate_motor.stop()
        if arm_lift_motor:
            arm_lift_motor.stop()
        hub.light.on(Color.GREEN)
        
    elif cmd == '0' and steering_motor:
        print("CMD:center")
        steering_motor.run_target(500, 0, wait=True)
        
    elif cmd == 'm' and distance_sensor:
        try:
            dist = distance_sensor.distance()
            print(f"DIST:{dist}")
        except:
            print("DIST:ERROR")


# Hauptschleife - prüft Hub-Tasten als Fallback
print("LOOP:START")
try:
    while True:
        # Hub-Tasten als Fallback
        pressed = hub.buttons.pressed()
        
        if Button.BLUETOOTH in pressed:
            print("EXIT:USER")
            break
        elif Button.LEFT in pressed:
            execute_cmd('a')
            wait(100)
        elif Button.RIGHT in pressed:
            execute_cmd('d')
            wait(100)
        
        wait(50)

except KeyboardInterrupt:
    print("EXIT:INTERRUPT")

finally:
    print("CLEANUP")
    if drive_motor:
        drive_motor.stop()
    if steering_motor:
        steering_motor.run_target(300, 0)
    if arm_rotate_motor:
        arm_rotate_motor.stop()
    if arm_lift_motor:
        arm_lift_motor.stop()
    hub.light.on(Color.RED)
    print("DONE")
