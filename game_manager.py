import asyncio
from fastapi import WebSocket
from tic_tac_toe import TicTacToe


class GameManager:
    def __init__(self):
        self.game = TicTacToe()
        self.players = {}

    def add_player(self, player_id: str, ws: WebSocket):
        self.players[player_id] = ws

    def remove_player(self, player_id: str):
        self.players.pop(player_id, None)

    async def receive_move(self, player_id: str, position: int):
        if player_id[6] != self.game.current_player:
            await self.players[player_id].send_json({"error": "Not your turn"})
            return

        if not self.game.make_move(position):
            await self.players[player_id].send_json({"error": "Invalid move"})
            return

        state = self.game.get_state()
        await self.broadcast(state)

        if state["winner"]:
            await asyncio.sleep(5)
            self.game.reset()
            reset_state = self.game.get_state()
            await self.broadcast(reset_state)

    async def broadcast(self, message: dict):
        for ws in self.players.values():
            await ws.send_json(message)
