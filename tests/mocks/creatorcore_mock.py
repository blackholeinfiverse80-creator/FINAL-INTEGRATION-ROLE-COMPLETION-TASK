#!/usr/bin/env python3
"""
Mock CreatorCore Server for testing Core Integrator
Provides all required endpoints for integration testing
"""

from flask import Flask, request, jsonify
import json
from datetime import datetime

app = Flask(__name__)

# In-memory storage for testing
logs = []
feedback_data = []
context_data = [
    {"id": 1, "content": "Sample context 1", "timestamp": "2025-01-01T00:00:00"},
    {"id": 2, "content": "Sample context 2", "timestamp": "2025-01-01T01:00:00"},
    {"id": 3, "content": "Sample context 3", "timestamp": "2025-01-01T02:00:00"}
]

@app.route('/core/log', methods=['POST'])
def log_endpoint():
    """Accept log entries from Core Integrator"""
    try:
        data = request.get_json()
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "data": data,
            "id": len(logs) + 1
        }
        logs.append(log_entry)
        return jsonify({"status": "logged", "id": log_entry["id"]}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/core/feedback', methods=['POST'])
def feedback_endpoint():
    """Handle feedback data from Core Integrator"""
    try:
        data = request.get_json()
        feedback_entry = {
            "timestamp": datetime.now().isoformat(),
            "feedback": data,
            "id": len(feedback_data) + 1
        }
        feedback_data.append(feedback_entry)
        return jsonify({"status": "feedback_received", "id": feedback_entry["id"]}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/core/context', methods=['GET'])
def context_endpoint():
    """Return context data for Core Integrator"""
    try:
        limit = request.args.get('limit', 3, type=int)
        return jsonify({
            "context": context_data[:limit],
            "total": len(context_data)
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/system/health', methods=['GET'])
def health_endpoint():
    """Health check for Core Integrator"""
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "logs_count": len(logs),
        "feedback_count": len(feedback_data),
        "context_count": len(context_data)
    }), 200

# Debug endpoints for testing
@app.route('/debug/logs', methods=['GET'])
def debug_logs():
    """Get all stored logs"""
    return jsonify({"logs": logs}), 200

@app.route('/debug/feedback', methods=['GET'])
def debug_feedback():
    """Get all stored feedback"""
    return jsonify({"feedback": feedback_data}), 200

@app.route('/debug/reset', methods=['POST'])
def debug_reset():
    """Reset all stored data"""
    global logs, feedback_data
    logs.clear()
    feedback_data.clear()
    return jsonify({"status": "reset_complete"}), 200

if __name__ == '__main__':
    print("Starting CreatorCore Mock Server on port 5002...")
    app.run(host='0.0.0.0', port=5002, debug=True)