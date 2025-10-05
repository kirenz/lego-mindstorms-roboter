"""
Vereinfachte Lösung: Web-Interface das die Hub-Tasten verwendet.

Da direkte stdin-Steuerung mit pybricksdev nicht funktioniert,
nutzen wir das bereits funktionierende Hub-Tasten-System.

Anleitung:
1. Starte main_advanced.py auf dem Roboter
2. Nutze die Hub-Tasten zur Steuerung
3. Das Web-Interface dient als visuelle Referenz
"""

from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('manual.html')

if __name__ == '__main__':
    print("\n" + "="*70)
    print("🤖 LEGO MINDSTORMS REFERENZ-INTERFACE".center(70))
    print("="*70)
    print("\n📱 Öffne in deinem Browser:")
    print("   → http://localhost:8080")
    print("\n💡 Dieses Interface zeigt dir:")
    print("   - Welche Tasten am Hub was machen")
    print("   - Tastatur-Shortcuts als Referenz")
    print("\n🎮 Tatsächliche Steuerung:")
    print("   - Nutze die Hub-Tasten am Roboter")
    print("   - Starte: uv run pybricksdev run ble src/main_advanced.py")
    print("\n⚠️  Drücke Ctrl+C zum Beenden")
    print("="*70 + "\n")
    
    app.run(debug=True, host='0.0.0.0', port=8080)
