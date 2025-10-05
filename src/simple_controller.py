#!/usr/bin/env python3
"""
Einfaches Terminal-Interface für Lego Mindstorms Roboter-Steuerung.

Drücke einfach die Tasten (kein Enter nötig!):
  W/A/S/D: Fahrzeug steuern
  I/K/J/L: Greifarm steuern
  Q: Beenden
"""

import sys
import tty
import termios
import subprocess
import threading
import time
from queue import Queue


class SimpleRobotController:
    """Einfacher Terminal-Controller mit direkter Tasteneingabe."""
    
    def __init__(self):
        self.running = True
        self.command_queue = Queue()
        self.process = None
        
    def get_key(self):
        """Liest eine Taste ohne Enter."""
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            key = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return key
    
    def print_interface(self):
        """Zeigt das Interface an."""
        print("\033[2J\033[H")  # Clear screen
        print("=" * 70)
        print("🤖 LEGO MINDSTORMS ROBOTER-STEUERUNG".center(70))
        print("=" * 70)
        print()
        print("  🚗 FAHRZEUG-STEUERUNG:        🦾 GREIFARM-STEUERUNG:")
        print("                                ")
        print("        [W]                           [I]")
        print("         ⬆️                             ⬆️")
        print("    Vorwärts                      Arm hoch")
        print()
        print("  [A] ⬅️  [D] ➡️                  [J] ↪️  [L] ↩️")
        print("   Links  Rechts                Arm links  Arm rechts")
        print()
        print("        [S]                           [K]")
        print("         ⬇️                             ⬇️")
        print("    Rückwärts                     Arm runter")
        print()
        print("-" * 70)
        print("  [X] = 🛑 Stop    [M] = 📏 Abstand    [0] = 🎯 Zentrum    [Q] = Beenden")
        print("=" * 70)
        print()
        print("📊 Status:")
        print("  ✅ Roboter verbunden")
        print("  🎮 Bereit für Eingaben")
        print()
        print("💡 Tipp: Einfach Tasten drücken - kein Enter nötig!")
        print()
        print("-" * 70)
        print("Letzte Befehle: ", end="", flush=True)
    
    def send_to_robot(self, command):
        """Sendet Befehl zum Roboter über pybricksdev."""
        if self.process and self.process.poll() is None:
            try:
                # Sende Python-Befehl zum laufenden Programm
                cmd = f"execute_command('{command}')\n"
                self.process.stdin.write(cmd)
                self.process.stdin.flush()
            except:
                pass
    
    def start_robot_connection(self):
        """Startet die Verbindung zum Roboter."""
        print("\n🔍 Starte Roboter-Verbindung...")
        print("   (Das kann einen Moment dauern...)")
        
        try:
            # Starte pybricksdev im interaktiven Modus
            self.process = subprocess.Popen(
                ['uv', 'run', 'pybricksdev', 'run', 'ble', 'src/main.py', '--wait'],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=1
            )
            
            # Warte kurz
            time.sleep(3)
            
            if self.process.poll() is None:
                print("✅ Roboter verbunden!\n")
                time.sleep(1)
                return True
            else:
                print("❌ Verbindung fehlgeschlagen")
                return False
                
        except Exception as e:
            print(f"❌ Fehler: {e}")
            return False
    
    def run(self):
        """Hauptschleife."""
        # Zeige Interface
        self.print_interface()
        
        # Befehlszuordnung
        command_labels = {
            'w': '⬆️ Vorwärts',
            's': '⬇️ Rückwärts', 
            'a': '⬅️ Links',
            'd': '➡️ Rechts',
            'i': '⬆️ Arm↑',
            'k': '⬇️ Arm↓',
            'j': '↪️ Arm←',
            'l': '↩️ Arm→',
            '0': '🎯 Mitte',
            'x': '🛑 Stop',
            'm': '📏 Dist'
        }
        
        command_history = []
        
        try:
            while self.running:
                # Taste einlesen
                key = self.get_key().lower()
                
                if key == 'q' or key == '\x03':  # Q oder Ctrl+C
                    print("\n\n👋 Beende...")
                    self.running = False
                    break
                
                elif key in 'wasdijkl0xm':
                    # Gültiger Befehl
                    label = command_labels.get(key, key)
                    
                    # Füge zu Historie hinzu
                    command_history.append(label)
                    if len(command_history) > 15:
                        command_history.pop(0)
                    
                    # Zeige in der letzten Zeile
                    print(f"[{label}] ", end="", flush=True)
                    
                    # Sende zum Roboter
                    self.send_to_robot(key)
        
        except KeyboardInterrupt:
            print("\n\n⚠️ Unterbrochen")
        finally:
            if self.process:
                self.process.terminate()
            print("\n\n👋 Controller beendet\n")


def main():
    """Hauptfunktion."""
    print("\n🚀 Starte Roboter-Controller...")
    print("\n⚠️  WICHTIG:")
    print("   Stelle sicher, dass der Roboter EINGESCHALTET ist")
    print("   und in Reichweite (< 10m) steht!\n")
    
    input("Drücke ENTER zum Starten...")
    
    controller = SimpleRobotController()
    
    # Starte Roboter-Verbindung
    if not controller.start_robot_connection():
        print("\n❌ Konnte keine Verbindung zum Roboter herstellen.")
        print("\nPrüfe:")
        print("  1. Ist der Roboter eingeschaltet?")
        print("  2. Ist Bluetooth am Mac aktiviert?")
        print("  3. Läuft main.py auf dem Roboter?")
        return
    
    # Starte Controller
    controller.run()


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n❌ Fehler: {e}")
        import traceback
        traceback.print_exc()
