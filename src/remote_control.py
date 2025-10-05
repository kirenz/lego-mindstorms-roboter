#!/usr/bin/env python3
"""
Tastatur-Controller für Lego Mindstorms Roboter.

Starte dieses Script auf deinem Mac, nachdem der Roboter läuft.
Verbinde dich dann mit: uv run python src/remote_control.py

Steuerung:
  W/A/S/D: Fahren (vorwärts/links/rückwärts/rechts)
  I/K: Greifarm hoch/runter
  J/L: Greifarm links/rechts drehen
  0: Lenkung zentrieren
  X: Alles stoppen
  M: Abstand messen
  Q: Beenden
"""

import sys
import tty
import termios
import subprocess
import time


class RobotRemoteControl:
    """Fernsteuerung für den Roboter über Tastatur."""
    
    def __init__(self):
        self.running = True
        self.last_command = ""
        
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
    
    def send_command_to_robot(self, command):
        """
        Sendet einen Befehl zum Roboter.
        
        Hinweis: Dies ist ein vereinfachter Ansatz.
        Für die volle Funktionalität müsste man einen REPL-Server
        auf dem Roboter laufen lassen.
        """
        print(f"\nSende Befehl: '{command}'")
        # Hier würde der Befehl über pybricksdev gesendet
        # In einer vollständigen Implementation würde man hier
        # eine BLE-Verbindung aufbauen und Befehle senden
        
    def print_help(self):
        """Zeigt die Hilfe an."""
        print("\n" + "="*50)
        print("ROBOTER-FERNSTEUERUNG")
        print("="*50)
        print("\nFahrzeug-Steuerung:")
        print("  W = Vorwärts fahren")
        print("  S = Rückwärts fahren")
        print("  A = Links lenken")
        print("  D = Rechts lenken")
        print("\nGreifarm-Steuerung:")
        print("  I = Arm hochschwenken")
        print("  K = Arm runterschwenken")
        print("  J = Arm nach links drehen")
        print("  L = Arm nach rechts drehen")
        print("\nWeitere Befehle:")
        print("  0 = Lenkung zentrieren")
        print("  X = Alles stoppen")
        print("  M = Abstand messen")
        print("  H = Diese Hilfe anzeigen")
        print("  Q = Programm beenden")
        print("="*50)
        print("\nBereit für Eingaben...\n")
    
    def run(self):
        """Hauptschleife der Fernsteuerung."""
        self.print_help()
        
        print("HINWEIS: Diese Version zeigt nur die Befehle an.")
        print("Für echte Steuerung muss der Roboter in einem REPL-Modus laufen.\n")
        print("Starte mit: uv run pybricksdev run ble --wait src/main.py")
        print("Dann kannst du Befehle an den Roboter senden.\n")
        
        try:
            while self.running:
                # Taste einlesen
                key = self.get_key().lower()
                
                # Befehle verarbeiten
                if key == 'q':
                    print("\n\nBeende Fernsteuerung...")
                    self.running = False
                    
                elif key == '\x03':  # Ctrl+C
                    raise KeyboardInterrupt
                    
                elif key == 'h':
                    self.print_help()
                    
                elif key in 'wasdijkl0xm':
                    # Gültige Befehle
                    command_map = {
                        'w': '⬆️  Vorwärts',
                        's': '⬇️  Rückwärts',
                        'a': '⬅️  Links',
                        'd': '➡️  Rechts',
                        'i': '⬆️  Arm hoch',
                        'k': '⬇️  Arm runter',
                        'j': '↪️  Arm links',
                        'l': '↩️  Arm rechts',
                        '0': '🎯 Zentrum',
                        'x': '🛑 Stop',
                        'm': '📏 Abstand'
                    }
                    
                    print(f"[{command_map.get(key, key)}]", end='', flush=True)
                    self.last_command = key
                    self.send_command_to_robot(key)
                    
                else:
                    # Ungültige Taste
                    print(f"\n⚠️  Ungültige Taste: '{key}' (Drücke 'H' für Hilfe)")
                    
        except KeyboardInterrupt:
            print("\n\nUnterbrochen durch Benutzer")
        except Exception as e:
            print(f"\n\n❌ Fehler: {e}")
        finally:
            print("\n👋 Fernsteuerung beendet.\n")


if __name__ == "__main__":
    print("🤖 Roboter-Fernsteuerung wird gestartet...")
    time.sleep(0.5)
    
    controller = RobotRemoteControl()
    controller.run()
