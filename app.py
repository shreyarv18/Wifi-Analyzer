from flask import Flask, jsonify, render_template, Response
import subprocess
import re
import time
import io
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')  # Use non-GUI backend for Flask

app = Flask(__name__)

# --- Network Analyzer Functions ---

def parse_netsh_output():
    result = subprocess.run(["netsh", "wlan", "show", "networks", "mode=bssid"], capture_output=True, text=True)
    networks = []
    current_network = {}

    for line in result.stdout.splitlines():
        line = line.strip()

        ssid_match = re.match(r"^SSID\s+\d+\s+:\s+(.*)$", line)
        if ssid_match:
            if current_network:
                networks.append(current_network)
                current_network = {}
            current_network["SSID"] = ssid_match.group(1)

        bssid_match = re.match(r"^BSSID\s+\d+\s+:\s+([0-9a-f:]{17})$", line, re.I)
        if bssid_match:
            current_network["BSSID"] = bssid_match.group(1)

        signal_match = re.match(r"^Signal\s+:\s+(\d+)%$", line)
        if signal_match:
            current_network["Signal"] = signal_match.group(1)

        auth_match = re.match(r"^Authentication\s+:\s+(.*)$", line)
        if auth_match:
            current_network["Encryption"] = auth_match.group(1)

        enc_match = re.match(r"^Encryption\s+:\s+(.*)$", line)
        if enc_match:
            current_network["EncryptionType"] = enc_match.group(1)

    if current_network:
        networks.append(current_network)

    return networks

def analyze_security(encryption):
    if not encryption:
        return "❓ Unknown Encryption"

    encryption = encryption.lower()
    if "open" in encryption:
        return "⚠️ Open Network - High Risk"
    elif "wep" in encryption:
        return "⚠️ WEP - Weak Encryption"
    elif "wpa2" in encryption or "wpa3" in encryption:
        return "✅ Secure"
    else:
        return "❓ Unknown Encryption"

# --- Real-time Graph Route ---

signal_history = []

def get_signal_for_ssid(target_ssid):
    networks = parse_netsh_output()
    for net in networks:
        if net["SSID"] == target_ssid:
            return int(net["Signal"])
    return None

@app.route('/plot.png')
def plot_png():
    ssid = "LUCKY PG 5TH FLOOR"  # ← Change this to a target SSID or pass via query param

    signal = get_signal_for_ssid(ssid)
    if signal is not None:
        signal_history.append(signal)
        if len(signal_history) > 50:
            signal_history.pop(0)
    else:
        signal_history.append(0)

    fig, ax = plt.subplots()
    ax.plot(signal_history, color='blue')
    ax.set_title(f'Signal Strength for "{ssid}"')
    ax.set_ylabel("Signal (%)")
    ax.set_xlabel("Time (x1s)")
    fig.tight_layout()

    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)
    plt.close(fig)
    return Response(buf.getvalue(), mimetype='image/png')

@app.route('/signal-graph')
def signal_graph():
    return render_template('graph.html')

# --- Main Routes ---

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze')
def analyze():
    networks = parse_netsh_output()
    for net in networks:
        encryption = net.get("Encryption") or net.get("EncryptionType")
        net['Security Risk'] = analyze_security(encryption)
    return jsonify(networks)

if __name__ == '__main__':
    app.run(debug=True)
