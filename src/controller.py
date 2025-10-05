"""Controller-Script für Mac - Sendet Tastatureingaben an den Roboter."""

import sys
import tty
import termios
from pybricksdev.connections.pybricks import PybricksHub
import asyncio


class RobotController:
    """Controller für die Robotersteuerung über Tastatur."""
    
    def __init__(self):
        self.hub = None
        self.running = True
        
    def get_key(self):
        """Liest eine Taste ohne Enter zu benötigen."""
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch
    
    async def connect(self):
        """Verbindet mit dem Roboter über BLE."""
        print("Suche nach Roboter...")
        # Hier würde die BLE-Verbindung aufgebaut
        # Dies ist ein Platzhalter für die tatsächliche Implementierung
        pass
    
    async def send_command(self, command):
        """Sendet einen Befehl an den Roboter."""
        if self.hub:
            # Befehl an Roboter senden
            pass
    
    async def run(self):
        """Hauptschleife für die Steuerung."""
        print("\n=== Roboter-Steuerung ===")
        print("WASD: Fahren | IJKL: Greifarm | Space: Stop | Q: Beenden\n")
        
        while self.running:
            key = self.get_key().lower()
            
            if key == 'q':
                print("\nBeende...")
                self.running = False
                break
            elif key in 'wasdijkl ':
                print(f"Taste: {key}")
                await self.send_command(key)
            elif key == '\x03':  # Ctrl+C
                break


if __name__ == "__main__":
    try:
        controller = RobotController()
        asyncio.run(controller.run())
    except KeyboardInterrupt:
        print("\nUnterbrochen")
    except Exception as e:
        print(f"Fehler: {e}")
