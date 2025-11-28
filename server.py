from flask import Flask, request, jsonify
from datetime import datetime
import os

app = Flask(__name__)

# In-memory storage for device IDs and IPs
# Format: {device_id: {"ip": "x.x.x.x", "timestamp": 123456789}}
devices = {}

@app.route('/')
def home():
    return jsonify({
        "service": "SkyDesk ID Server",
        "version": "1.0",
        "active_devices": len(devices)
    })

@app.route('/register/<device_id>', methods=['POST'])
def register_device(device_id):
    """Register or update device IP"""
    try:
        data = request.get_json()
        ip = data.get('ip')
        
        if not ip:
            return jsonify({"error": "IP address required"}), 400
        
        devices[device_id] = {
            "ip": ip,
            "timestamp": int(datetime.now().timestamp())
        }
        
        return jsonify({
            "status": "success",
            "device_id": device_id,
            "ip": ip
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/lookup/<device_id>', methods=['GET'])
def lookup_device(device_id):
    """Get IP address for a device ID"""
    if device_id in devices:
        device = devices[device_id]
        return jsonify({
            "status": "success",
            "device_id": device_id,
            "ip": device["ip"],
            "last_seen": device["timestamp"]
        })
    else:
        return jsonify({
            "status": "error",
            "error": "Device not found"
        }), 404

@app.route('/devices', methods=['GET'])
def list_devices():
    """List all registered devices (for debugging)"""
    return jsonify({
        "total": len(devices),
        "devices": [
            {
                "id": device_id,
                "ip": info["ip"],
                "last_seen": info["timestamp"]
            }
            for device_id, info in devices.items()
        ]
    })

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({"status": "healthy"})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port, debug=False)
