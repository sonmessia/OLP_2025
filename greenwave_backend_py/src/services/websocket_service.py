"""
WebSocket service for real-time communication with frontend
"""
import asyncio
import json
import logging
from typing import Set
from fastapi import WebSocket
from datetime import datetime

from ..models.simulation import SimulationState, WebSocketMessage

logger = logging.getLogger(__name__)


class WebSocketService:
    """WebSocket service for managing client connections"""
    
    def __init__(self):
        self.active_connections: Set[WebSocket] = set()
        self.event_handlers = {}
    
    async def connect(self, websocket: WebSocket):
        """Accept a new WebSocket connection"""
        await websocket.accept()
        self.active_connections.add(websocket)
        logger.info(f"New WebSocket client connected. Total: {len(self.active_connections)}")
        
        # Send welcome message
        await self.send_to_client(websocket, {
            "type": "connection",
            "data": {"status": "connected", "message": "Welcome to GreenWave Backend"},
            "timestamp": int(datetime.now().timestamp() * 1000)
        })
    
    def disconnect(self, websocket: WebSocket):
        """Remove a WebSocket connection"""
        self.active_connections.discard(websocket)
        logger.info(f"WebSocket client disconnected. Total: {len(self.active_connections)}")
    
    async def send_to_client(self, websocket: WebSocket, message: dict):
        """Send message to a specific client"""
        try:
            await websocket.send_json(message)
        except Exception as e:
            logger.error(f"Error sending to client: {e}")
            self.disconnect(websocket)
    
    async def broadcast(self, message: dict):
        """Broadcast message to all connected clients"""
        disconnected = set()
        
        for connection in self.active_connections:
            try:
                await connection.send_json(message)
            except Exception as e:
                logger.error(f"Error broadcasting to client: {e}")
                disconnected.add(connection)
        
        # Remove disconnected clients
        for connection in disconnected:
            self.disconnect(connection)
    
    async def broadcast_simulation_state(self, state: SimulationState):
        """Broadcast simulation state to all clients"""
        message = {
            "type": "simulation_update",
            "data": state.model_dump(),
            "timestamp": int(datetime.now().timestamp() * 1000)
        }
        await self.broadcast(message)
    
    async def broadcast_error(self, error: str):
        """Broadcast error message to all clients"""
        message = {
            "type": "error",
            "data": {"error": error},
            "timestamp": int(datetime.now().timestamp() * 1000)
        }
        await self.broadcast(message)
    
    async def handle_message(self, websocket: WebSocket, data: str):
        """Handle incoming message from client"""
        try:
            message = json.loads(data)
            msg_type = message.get("type")
            msg_data = message.get("data", {})
            
            logger.info(f"Received message: {msg_type}")
            
            # Emit event to handlers
            if msg_type in self.event_handlers:
                for handler in self.event_handlers[msg_type]:
                    await handler(msg_data)
            
        except json.JSONDecodeError as e:
            logger.error(f"Error parsing message: {e}")
        except Exception as e:
            logger.error(f"Error handling message: {e}")
    
    def on(self, event: str, handler):
        """Register event handler"""
        if event not in self.event_handlers:
            self.event_handlers[event] = []
        self.event_handlers[event].append(handler)
    
    def get_client_count(self) -> int:
        """Get number of connected clients"""
        return len(self.active_connections)
