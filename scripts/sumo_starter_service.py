#!/usr/bin/env python3
"""
SUMO Starter Service
HTTP server that runs on the HOST and allows the backend container to start SUMO
Run this on the host: python3 scripts/sumo_starter_service.py
"""

from http.server import HTTPServer, BaseHTTPRequestHandler
import subprocess
import json
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

PORT = 9999  # Port for this service


class SUMOStarterHandler(BaseHTTPRequestHandler):
    
    def do_POST(self):
        """Handle POST request to start SUMO"""
        if self.path == '/start':
            try:
                # Read request body
                content_length = int(self.headers['Content-Length'])
                body = self.rfile.read(content_length)
                data = json.loads(body)
                
                scenario = data.get('scenario', 'Nga4ThuDuc')
                
                # Call the start script
                script_path = "/home/thaianh/OLP2025/OLP_2025/scripts/start_sumo.sh"
                result = subprocess.run(
                    ['bash', script_path, scenario],
                    capture_output=True,
                    text=True,
                    timeout=15
                )
                
                if result.returncode == 0:
                    self.send_response(200)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    response = {
                        'status': 'success',
                        'message': f'SUMO started for scenario {scenario}',
                        'output': result.stdout
                    }
                    self.wfile.write(json.dumps(response).encode())
                    logger.info(f"✅ Started SUMO for {scenario}")
                else:
                    self.send_response(500)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    response = {
                        'status': 'error',
                        'message': 'Failed to start SUMO',
                        'error': result.stderr
                    }
                    self.wfile.write(json.dumps(response).encode())
                    logger.error(f"❌ Failed to start SUMO: {result.stderr}")
                    
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                response = {'status': 'error', 'message': str(e)}
                self.wfile.write(json.dumps(response).encode())
                logger.error(f"Error: {e}")
        else:
            self.send_response(404)
            self.end_headers()
    
    def log_message(self, format, *args):
        """Override to use logger"""
        logger.info(f"{self.address_string()} - {format%args}")


if __name__ == '__main__':
    server = HTTPServer(('0.0.0.0', PORT), SUMOStarterHandler)
    logger.info(f"🚀 SUMO Starter Service running on port {PORT}")
    logger.info(f"Backend can POST to http://172.17.0.1:{PORT}/start with {{\"scenario\": \"Nga4ThuDuc\"}}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        logger.info("\n👋 Shutting down...")
        server.shutdown()
