# WiFi Analyzer

A Flask-based WiFi network analyzer and real-time signal strength visualizer using Python.This project scans available WiFi networks,
analyzes their security, and displays a live signal strength graph for a chosen WiFi network (SSID).

Features
- Scan nearby WiFi networks and display SSID, BSSID, signal strength, and encryption details.
- Analyze WiFi security status (Open, WEP, WPA2/WPA3).
- Real-time signal strength graph for a target SSID.
- JSON API endpoint for network data.
- Simple web frontend to visualize results.

Technologies Used
- Python 3
- Flask (web framework)
- pywifi (cross-platform WiFi scanning)
- Matplotlib (plotting graphs)

Running the Flask Server
-Clone the repository or copy the project files.
-Install the required packages (flask, pywifi, matplotlib)
-Run the Flask app: python app.py
-Open your browser and navigate to http://127.0.0.1:5000/

Deployment Details
- The application is packaged with all dependencies in `requirements.txt`.
- The `application.py` (or your main Flask script) is configured as the entry point.
- Environment variables and configuration can be managed via the Elastic Beanstalk console.
- Logging and monitoring are handled via AWS CloudWatch.
