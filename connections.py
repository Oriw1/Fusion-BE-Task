from fastapi import WebSocket
from typing import Optional


class ConnectionManager:
    def __init__(self):
        self.playerX: Optional[WebSocket] = None
        self.playerO: Optional[WebSocket] = None

    async def connect(self, websocket: WebSocket, player_id: str):
        await websocket.accept()
        if player_id == "playerX":
            self.playerX = websocket
        elif player_id == "playerO":
            self.playerO = websocket

    def disconnect(self, player_id: str):
        if player_id == "playerX":
            self.playerX = None
        elif player_id == "playerO":
            self.playerO = None

    def get(self, player_id: str) -> Optional[WebSocket]:
        return self.playerX if player_id == "playerX" else self.playerO
