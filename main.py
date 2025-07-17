from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from connections import ConnectionManager
from game_manager import GameManager
import json

app = FastAPI()
manager = ConnectionManager()
game = GameManager()


@app.websocket("/ws/{player_id}")
async def websocket_endpoint(websocket: WebSocket, player_id: str):
    await manager.connect(websocket, player_id)
    game.add_player(player_id, websocket)
    await websocket.send_json(game.game.get_state())

    try:
        while True:
            message = await websocket.receive_text()
            try:
                data = json.loads(message)
                position = data.get("position")
                if isinstance(position, int):
                    await game.receive_move(player_id, position)
                else:
                    await websocket.send_json({"error": "Invalid format"})
            except json.JSONDecodeError:
                await websocket.send_json({"error": "Message must be JSON"})
    except WebSocketDisconnect:
        print(f"{player_id} disconnected")
        manager.disconnect(player_id)
        game.remove_player(player_id)
