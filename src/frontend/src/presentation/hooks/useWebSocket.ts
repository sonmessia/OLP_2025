// Copyright (c) 2025 Green Wave Team
// 
// This software is released under the MIT License.
// https://opensource.org/licenses/MIT

import { useEffect, useRef, useState, useCallback } from "react";
import type {
  SimulationState,
  WebSocketMessage,
} from "../../domain/models/simulation.types";

type CommandData = { command: string; params?: Record<string, unknown> };

interface UseWebSocketOptions {
  url: string;
  onMessage?: (data: SimulationState) => void;
  onError?: (error: Event) => void;
  onConnect?: () => void;
  onDisconnect?: () => void;
  autoReconnect?: boolean;
  reconnectInterval?: number;
}

export const useWebSocket = (options: UseWebSocketOptions) => {
  const {
    url,
    onMessage,
    onError,
    onConnect,
    onDisconnect,
    autoReconnect = true,
    reconnectInterval = 3000,
  } = options;

  const [isConnected, setIsConnected] = useState(false);
  const [lastMessage, setLastMessage] = useState<SimulationState | null>(null);
  const wsRef = useRef<WebSocket | null>(null);
  const reconnectTimeoutRef = useRef<number | null>(null);

  const connect = useCallback(() => {
    try {
      const ws = new WebSocket(url);

      ws.onopen = () => {
        console.log("[WebSocket] Connected to", url);
        setIsConnected(true);
        onConnect?.();
      };

      ws.onmessage = (event) => {
        try {
          const message: WebSocketMessage = JSON.parse(event.data);

          if (message.type === "simulation_update") {
            setLastMessage(message.data);
            onMessage?.(message.data);
          } else if (message.type === "error") {
            console.error("[WebSocket] Error from server:", message.data);
          } else if (message.type === "connection") {
            console.log("[WebSocket] Connection message:", message.data);
          }
        } catch (error) {
          console.error("[WebSocket] Error parsing message:", error);
        }
      };

      ws.onerror = (error) => {
        console.error("[WebSocket] Error:", error);
        onError?.(error);
      };

      ws.onclose = () => {
        console.log("[WebSocket] Disconnected");
        setIsConnected(false);
        onDisconnect?.();

        // Auto reconnect
        if (autoReconnect) {
          reconnectTimeoutRef.current = setTimeout(() => {
            console.log("[WebSocket] Attempting to reconnect...");
            connect();
          }, reconnectInterval);
        }
      };

      wsRef.current = ws;
    } catch (error) {
      console.error("[WebSocket] Connection error:", error);
    }
  }, [
    url,
    onMessage,
    onError,
    onConnect,
    onDisconnect,
    autoReconnect,
    reconnectInterval,
  ]);

  const disconnect = useCallback(() => {
    if (reconnectTimeoutRef.current) {
      clearTimeout(reconnectTimeoutRef.current);
    }
    if (wsRef.current) {
      wsRef.current.close();
      wsRef.current = null;
    }
  }, []);

  const sendCommand = useCallback((command: CommandData) => {
    if (wsRef.current && wsRef.current.readyState === WebSocket.OPEN) {
      const message: WebSocketMessage = {
        type: "command",
        data: command,
        timestamp: Date.now(),
      };
      wsRef.current.send(JSON.stringify(message));
    } else {
      console.warn("[WebSocket] Cannot send command: not connected");
    }
  }, []);

  const subscribe = useCallback((area: string) => {
    if (wsRef.current && wsRef.current.readyState === WebSocket.OPEN) {
      const message: WebSocketMessage = {
        type: "command",
        data: { command: "subscribe", params: { area } },
        timestamp: Date.now(),
      };
      wsRef.current.send(JSON.stringify(message));
    }
  }, []);

  useEffect(() => {
    connect();

    return () => {
      disconnect();
    };
  }, [connect, disconnect]);

  return {
    isConnected,
    lastMessage,
    sendCommand,
    subscribe,
    reconnect: connect,
    disconnect,
  };
};
