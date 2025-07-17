from fastapi import WebSocket
from typing import Optional


class ConnectionManager:
    def __init__(self):
        self.player1: Optional[WebSocket] = None
        self.player2: Optional[WebSocket] = None

    async def connect(self, websocket: WebSocket, player_id: str):
        await websocket.accept()
        if player_id == "player1":
            self.player1 = websocket
        elif player_id == "player2":
            self.player2 = websocket

    def disconnect(self, player_id: str):
        if player_id == "player1":
            self.player1 = None
        elif player_id == "player2":
            self.player2 = None

    def get(self, player_id: str) -> Optional[WebSocket]:
        return self.player1 if player_id == "player1" else self.player2
