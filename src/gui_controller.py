#!/usr/bin/env python3
"""
Grafisches Interface für Lego Mindstorms Roboter-Steuerung.

Klicke auf Buttons oder nutze die Tastatur (WASD/IJKL).
"""

import tkinter as tk
from tkinter import ttk
import subprocess
import threading
import time


class RobotGUI:
    """Grafisches Interface für Roboter-Steuerung."""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("🤖 Lego Mindstorms Steuerung")
        self.root.geometry("800x600")
        self.root.configure(bg='#2c3e50')
        
        self.process = None
        self.connected = False
        
        self.create_widgets()
        self.bind_keys()
        
    def create_widgets(self):
        """Erstellt alle UI-Elemente."""
        # Titel
        title = tk.Label(
            self.root,
            text="🤖 LEGO MINDSTORMS STEUERUNG",
            font=("Arial", 24, "bold"),
            bg='#2c3e50',
            fg='white'
        )
        title.pack(pady=20)
        
        # Status
        self.status_label = tk.Label(
            self.root,
            text="⚠️  Nicht verbunden",
            font=("Arial", 14),
            bg='#e74c3c',
            fg='white',
            padx=20,
            pady=10
        )
        self.status_label.pack(pady=10)
        
        # Verbindungs-Button
        self.connect_btn = tk.Button(
            self.root,
            text="🔗 Mit Roboter verbinden",
            font=("Arial", 14, "bold"),
            bg='#27ae60',
            fg='white',
            padx=30,
            pady=15,
            command=self.connect_robot
        )
        self.connect_btn.pack(pady=20)
        
        # Hauptframe für Steuerung
        main_frame = tk.Frame(self.root, bg='#2c3e50')
        main_frame.pack(pady=20)
        
        # Linke Seite: Fahrzeug
        vehicle_frame = tk.LabelFrame(
            main_frame,
            text="🚗 FAHRZEUG",
            font=("Arial", 16, "bold"),
            bg='#34495e',
            fg='white',
            padx=20,
            pady=20
        )
        vehicle_frame.grid(row=0, column=0, padx=20)
        
        # Vorwärts
        tk.Button(
            vehicle_frame,
            text="⬆️\nW\nVorwärts",
            font=("Arial", 12, "bold"),
            bg='#3498db',
            fg='white',
            width=10,
            height=3,
            command=lambda: self.send_command('w')
        ).grid(row=0, column=1, padx=5, pady=5)
        
        # Links
        tk.Button(
            vehicle_frame,
            text="⬅️\nA\nLinks",
            font=("Arial", 12, "bold"),
            bg='#3498db',
            fg='white',
            width=10,
            height=3,
            command=lambda: self.send_command('a')
        ).grid(row=1, column=0, padx=5, pady=5)
        
        # Rückwärts
        tk.Button(
            vehicle_frame,
            text="⬇️\nS\nRückwärts",
            font=("Arial", 12, "bold"),
            bg='#3498db',
            fg='white',
            width=10,
            height=3,
            command=lambda: self.send_command('s')
        ).grid(row=1, column=1, padx=5, pady=5)
        
        # Rechts
        tk.Button(
            vehicle_frame,
            text="➡️\nD\nRechts",
            font=("Arial", 12, "bold"),
            bg='#3498db',
            fg='white',
            width=10,
            height=3,
            command=lambda: self.send_command('d')
        ).grid(row=1, column=2, padx=5, pady=5)
        
        # Rechte Seite: Greifarm
        arm_frame = tk.LabelFrame(
            main_frame,
            text="🦾 GREIFARM",
            font=("Arial", 16, "bold"),
            bg='#34495e',
            fg='white',
            padx=20,
            pady=20
        )
        arm_frame.grid(row=0, column=1, padx=20)
        
        # Arm hoch
        tk.Button(
            arm_frame,
            text="⬆️\nI\nHoch",
            font=("Arial", 12, "bold"),
            bg='#9b59b6',
            fg='white',
            width=10,
            height=3,
            command=lambda: self.send_command('i')
        ).grid(row=0, column=1, padx=5, pady=5)
        
        # Arm links
        tk.Button(
            arm_frame,
            text="↪️\nJ\nLinks",
            font=("Arial", 12, "bold"),
            bg='#9b59b6',
            fg='white',
            width=10,
            height=3,
            command=lambda: self.send_command('j')
        ).grid(row=1, column=0, padx=5, pady=5)
        
        # Arm runter
        tk.Button(
            arm_frame,
            text="⬇️\nK\nRunter",
            font=("Arial", 12, "bold"),
            bg='#9b59b6',
            fg='white',
            width=10,
            height=3,
            command=lambda: self.send_command('k')
        ).grid(row=1, column=1, padx=5, pady=5)
        
        # Arm rechts
        tk.Button(
            arm_frame,
            text="↩️\nL\nRechts",
            font=("Arial", 12, "bold"),
            bg='#9b59b6',
            fg='white',
            width=10,
            height=3,
            command=lambda: self.send_command('l')
        ).grid(row=1, column=2, padx=5, pady=5)
        
        # Zusätzliche Buttons unten
        extra_frame = tk.Frame(self.root, bg='#2c3e50')
        extra_frame.pack(pady=20)
        
        tk.Button(
            extra_frame,
            text="🛑 STOP (X)",
            font=("Arial", 12, "bold"),
            bg='#e74c3c',
            fg='white',
            width=12,
            command=lambda: self.send_command('x')
        ).grid(row=0, column=0, padx=10)
        
        tk.Button(
            extra_frame,
            text="🎯 Zentrum (0)",
            font=("Arial", 12, "bold"),
            bg='#f39c12',
            fg='white',
            width=12,
            command=lambda: self.send_command('0')
        ).grid(row=0, column=1, padx=10)
        
        tk.Button(
            extra_frame,
            text="📏 Abstand (M)",
            font=("Arial", 12, "bold"),
            bg='#16a085',
            fg='white',
            width=12,
            command=lambda: self.send_command('m')
        ).grid(row=0, column=2, padx=10)
        
        # Log
        self.log_text = tk.Text(
            self.root,
            height=5,
            width=80,
            bg='#1a1a1a',
            fg='#00ff00',
            font=("Courier", 10)
        )
        self.log_text.pack(pady=10)
        
    def bind_keys(self):
        """Bindet Tastatur-Shortcuts."""
        keys = 'wasdijkl0xm'
        for key in keys:
            self.root.bind(key, lambda e, k=key: self.send_command(k))
            self.root.bind(key.upper(), lambda e, k=key: self.send_command(k))
    
    def log(self, message):
        """Fügt Nachricht zum Log hinzu."""
        self.log_text.insert('end', message + '\n')
        self.log_text.see('end')
    
    def connect_robot(self):
        """Verbindet mit dem Roboter."""
        self.status_label.config(text="⏳ Verbinde...", bg='#f39c12')
        self.connect_btn.config(state='disabled')
        self.log("🔍 Suche nach Roboter...")
        
        def connect_thread():
            try:
                self.process = subprocess.Popen(
                    ['uv', 'run', 'pybricksdev', 'run', 'ble', 'src/main.py', '--wait'],
                    stdin=subprocess.PIPE,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                    bufsize=1
                )
                
                time.sleep(3)
                
                if self.process.poll() is None:
                    self.connected = True
                    self.status_label.config(text="✅ Verbunden", bg='#27ae60')
                    self.log("✅ Roboter verbunden!")
                else:
                    self.status_label.config(text="❌ Verbindung fehlgeschlagen", bg='#e74c3c')
                    self.log("❌ Verbindung fehlgeschlagen")
                    self.connect_btn.config(state='normal')
            except Exception as e:
                self.log(f"❌ Fehler: {e}")
                self.status_label.config(text="❌ Fehler", bg='#e74c3c')
                self.connect_btn.config(state='normal')
        
        threading.Thread(target=connect_thread, daemon=True).start()
    
    def send_command(self, cmd):
        """Sendet Befehl zum Roboter."""
        if not self.connected:
            self.log("⚠️  Nicht verbunden!")
            return
        
        command_names = {
            'w': '⬆️ Vorwärts', 's': '⬇️ Rückwärts',
            'a': '⬅️ Links', 'd': '➡️ Rechts',
            'i': '⬆️ Arm hoch', 'k': '⬇️ Arm runter',
            'j': '↪️ Arm links', 'l': '↩️ Arm rechts',
            '0': '🎯 Zentrum', 'x': '🛑 Stop', 'm': '📏 Abstand'
        }
        
        try:
            command = f"execute_command('{cmd}')\n"
            self.process.stdin.write(command)
            self.process.stdin.flush()
            self.log(f"📤 {command_names.get(cmd, cmd)}")
        except:
            self.log("❌ Fehler beim Senden")
            self.connected = False
            self.status_label.config(text="❌ Verbindung verloren", bg='#e74c3c')
    
    def run(self):
        """Startet die GUI."""
        self.root.mainloop()


if __name__ == "__main__":
    app = RobotGUI()
    app.run()
