#!/usr/bin/env python3
"""
Tastatur-Controller für Lego Mindstorms Roboter.

Steuere den Roboter mit deiner Mac-Tastatur über Bluetooth.

Steuerung:
  W/A/S/D: Fahrzeug (vorwärts/links/rückwärts/rechts)
  I/K: Greifarm hoch/runter
  J/L: Greifarm links/rechts drehen
  0: Lenkung zentrieren
  X: Alles stoppen
  M: Abstand messen
  H: Hilfe anzeigen
  Q: Beenden
"""

import sys
import tty
import termios
from pybricks.messaging import BluetoothMailboxServer, TextMailbox


class KeyboardController:
    """Tastatur-Controller für den Roboter."""
    
    def __init__(self):
        self.running = True
        self.server = None
        self.mbox = None
        
    def get_key(self):
        """Liest eine Taste ohne Enter-Taste."""
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            key = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return key
    
    def print_help(self):
        """Zeigt die Hilfe an."""
        print("\n" + "="*60)
        print("🤖 LEGO MINDSTORMS ROBOTER-STEUERUNG")
        print("="*60)
        print("\n🚗 Fahrzeug-Steuerung:")
        print("  W = ⬆️  Vorwärts fahren")
        print("  S = ⬇️  Rückwärts fahren")
        print("  A = ⬅️  Links lenken")
        print("  D = ➡️  Rechts lenken")
        print("\n🦾 Greifarm-Steuerung:")
        print("  I = ⬆️  Arm hochschwenken")
        print("  K = ⬇️  Arm runterschwenken")
        print("  J = ↪️   Arm nach links drehen")
        print("  L = ↩️   Arm nach rechts drehen")
        print("\n⚙️  Weitere Befehle:")
        print("  0 = 🎯 Lenkung zentrieren")
        print("  X = 🛑 Alles stoppen")
        print("  M = 📏 Abstand messen")
        print("  H = ❓ Diese Hilfe anzeigen")
        print("  Q = 👋 Programm beenden")
        print("="*60)
        print()
    
    def connect(self):
        """Verbindet mit dem Roboter."""
        print("🔍 Suche nach Roboter...")
        print("   (Stelle sicher, dass main.py auf dem Roboter läuft)")
        
        try:
            self.server = BluetoothMailboxServer()
            self.mbox = TextMailbox('commands', self.server)
            
            print("⏳ Warte auf Verbindung...")
            self.server.wait_for_connection()
            
            print("✅ Verbunden mit Roboter!")
            return True
            
        except Exception as e:
            print(f"❌ Verbindung fehlgeschlagen: {e}")
            return False
    
    def send_command(self, cmd):
        """Sendet einen Befehl an den Roboter."""
        try:
            self.mbox.send(cmd)
            return True
        except Exception as e:
            print(f"\n❌ Fehler beim Senden: {e}")
            return False
    
    def run(self):
        """Hauptschleife der Steuerung."""
        self.print_help()
        
        # Mit Roboter verbinden
        if not self.connect():
            print("\n⚠️  Konnte keine Verbindung zum Roboter herstellen.")
            print("   Stelle sicher, dass:")
            print("   1. Der Roboter eingeschaltet ist")
            print("   2. main.py auf dem Roboter läuft")
            print("   3. Bluetooth auf dem Mac aktiviert ist")
            return
        
        print("\n🎮 Bereit für Steuerung!\n")
        
        # Befehlszuordnung für Ausgabe
        command_map = {
            'w': '⬆️  Vorwärts',
            's': '⬇️  Rückwärts',
            'a': '⬅️  Links',
            'd': '➡️  Rechts',
            'i': '⬆️  Arm hoch',
            'k': '⬇️  Arm runter',
            'j': '↪️   Arm links',
            'l': '↩️   Arm rechts',
            '0': '🎯 Zentrum',
            'x': '🛑 Stop',
            'm': '📏 Abstand'
        }
        
        try:
            while self.running:
                # Taste einlesen
                key = self.get_key().lower()
                
                # Befehle verarbeiten
                if key == 'q':
                    print("\n\n👋 Beende Steuerung...")
                    self.send_command('q')
                    self.running = False
                    
                elif key == '\x03':  # Ctrl+C
                    raise KeyboardInterrupt
                    
                elif key == 'h':
                    self.print_help()
                    
                elif key in 'wasdijkl0xm':
                    # Gültige Befehle
                    label = command_map.get(key, key)
                    print(f"[{label}]", end='', flush=True)
                    
                    if not self.send_command(key):
                        print("\n⚠️  Verbindung verloren!")
                        break
                    
                elif key in ['\r', '\n']:
                    # Enter - neue Zeile
                    print()
                    
                else:
                    # Ungültige Taste
                    if ord(key) >= 32:  # Druckbares Zeichen
                        print(f"\n⚠️  Ungültige Taste: '{key}' (Drücke 'H' für Hilfe)")
                    
        except KeyboardInterrupt:
            print("\n\n⚠️  Unterbrochen durch Benutzer")
        except Exception as e:
            print(f"\n\n❌ Fehler: {e}")
        finally:
            print("\n👋 Controller beendet.\n")


if __name__ == "__main__":
    print("🤖 Roboter-Controller wird gestartet...\n")
    
    try:
        controller = KeyboardController()
        controller.run()
    except KeyboardInterrupt:
        print("\n\n👋 Abgebrochen\n")
    except Exception as e:
        print(f"\n❌ Fehler: {e}\n")
        import traceback
        traceback.print_exc()
