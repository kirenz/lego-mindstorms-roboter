"""
Web-Interface für Lego Mindstorms Roboter-Steuerung.

Startet einen Webserver auf http://localhost:5000
Steuere den Roboter über Browser mit Maus oder Tastatur!
"""

from flask import Flask, render_template, jsonify, request
import subprocess
import threading
import time
from pathlib import Path

app = Flask(__name__)

# Globale Variablen
robot_process = None
robot_connected = False
command_history = []


class RobotController:
    """Verwaltet die Verbindung zum Roboter."""
    
    def __init__(self):
        self.process = None
        self.connected = False
        
    def connect(self):
        """Startet die Verbindung zum Roboter."""
        try:
            self.process = subprocess.Popen(
                ['uv', 'run', 'pybricksdev', 'run', 'ble', 'src/main.py', '--wait'],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=1,
                cwd=Path(__file__).parent.parent
            )
            
            # Warte auf Verbindung
            time.sleep(3)
            
            if self.process.poll() is None:
                self.connected = True
                return True
            return False
            
        except Exception as e:
            print(f"Verbindungsfehler: {e}")
            return False
    
    def send_command(self, cmd):
        """Sendet einen Befehl an den Roboter."""
        if self.connected and self.process:
            try:
                command = f"execute_command('{cmd}')\n"
                self.process.stdin.write(command)
                self.process.stdin.flush()
                return True
            except:
                self.connected = False
                return False
        return False
    
    def disconnect(self):
        """Trennt die Verbindung."""
        if self.process:
            self.process.terminate()
            self.connected = False


# Globaler Controller
controller = RobotController()


@app.route('/')
def index():
    """Hauptseite."""
    return render_template('index.html')


@app.route('/api/connect', methods=['POST'])
def connect():
    """Verbindet mit dem Roboter."""
    global robot_connected
    
    if controller.connect():
        robot_connected = True
        return jsonify({'success': True, 'message': 'Roboter verbunden!'})
    else:
        return jsonify({'success': False, 'message': 'Verbindung fehlgeschlagen'}), 500


@app.route('/api/disconnect', methods=['POST'])
def disconnect():
    """Trennt die Verbindung."""
    global robot_connected
    
    controller.disconnect()
    robot_connected = False
    return jsonify({'success': True, 'message': 'Verbindung getrennt'})


@app.route('/api/status')
def status():
    """Status der Verbindung."""
    return jsonify({
        'connected': controller.connected,
        'history': command_history[-10:]  # Letzte 10 Befehle
    })


@app.route('/api/command', methods=['POST'])
def command():
    """Sendet einen Befehl an den Roboter."""
    data = request.json
    cmd = data.get('command', '')
    
    if not controller.connected:
        return jsonify({'success': False, 'message': 'Nicht verbunden'}), 400
    
    if controller.send_command(cmd):
        # Füge zu Historie hinzu
        command_history.append({
            'command': cmd,
            'time': time.strftime('%H:%M:%S')
        })
        
        return jsonify({'success': True, 'message': f'Befehl "{cmd}" gesendet'})
    else:
        return jsonify({'success': False, 'message': 'Fehler beim Senden'}), 500


if __name__ == '__main__':
    print("\n" + "="*70)
    print("🤖 LEGO MINDSTORMS WEB-INTERFACE".center(70))
    print("="*70)
    print("\n📱 Öffne in deinem Browser:")
    print("   → http://localhost:8080")
    print("\n💡 Du kannst den Roboter dann mit:")
    print("   - Maus-Klicks auf die Buttons")
    print("   - Tastatur (WASD + IJKL)")
    print("   steuern!")
    print("\n⚠️  Drücke Ctrl+C zum Beenden")
    print("="*70 + "\n")
    
    app.run(debug=True, host='0.0.0.0', port=8080)
