import time
import pywifi
from pywifi import const
import matplotlib.pyplot as plt

wifi = pywifi.PyWiFi()
iface = wifi.interfaces()[0]

def get_signal_strength(target_ssid=None):
    iface.scan()
    time.sleep(1)
    results = iface.scan_results()
    for network in results:
        if target_ssid:
            if network.ssid == target_ssid:
                return network.signal
        else:
            if network.ssid:
                return network.signal
    return None

def plot_signal_strength(duration=60, ssid=None):
    plt.ion()
    fig, ax = plt.subplots()
    x_data, y_data = [], []
    line, = ax.plot(x_data, y_data, label="Signal Strength (dBm)", color='blue')

    start_time = time.time()

    while (time.time() - start_time) < duration:
        signal = get_signal_strength(ssid)
        if signal is not None:
            x_data.append(int(time.time() - start_time))
            y_data.append(signal)
            line.set_xdata(x_data)
            line.set_ydata(y_data)
            ax.relim()
            ax.autoscale_view()
            ax.set_title(f"Live Signal Strength {'for ' + ssid if ssid else ''}")
            ax.set_xlabel("Time (s)")
            ax.set_ylabel("Signal Strength (dBm)")
            ax.legend()
            plt.pause(1)
        else:
            print("No signal detected. Retrying...")
            time.sleep(1)

    plt.ioff()
    plt.show()
