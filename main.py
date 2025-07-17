from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from connections import ConnectionManager

app = FastAPI()
manager = ConnectionManager()


@app.websocket("/ws/{player_id}")
async def websocket_endpoint(websocket: WebSocket, player_id: str):
    await manager.connect(websocket, player_id)
    try:
        while True:
            data = await websocket.receive_text()
            print(f"Received from {player_id}: {data}")

            # Determine the other player
            other_player_id = "player2" if player_id == "player1" else "player1"
            other_socket = manager.get(other_player_id)

            if other_socket is not None:
                await other_socket.send_text(f"{player_id}: {data}")
            else:
                print(f"{other_player_id} is not connected. Cannot forward message.")
    except WebSocketDisconnect:
        print(f"{player_id} disconnected")
        manager.disconnect(player_id)
