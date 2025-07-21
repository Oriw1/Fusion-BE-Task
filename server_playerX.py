from fastapi import FastAPI, WebSocket
from redis_game import r, get_game_state, make_move, reset_game
import asyncio
import json

app = FastAPI()


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()

    pubsub = r.pubsub()
    await pubsub.subscribe("game:channel")

    await websocket.send_json(await get_game_state())

    async def listen():
        async for message in pubsub.listen():
            if message["type"] == "message":
                await websocket.send_text(message["data"])

    asyncio.create_task(listen())

    try:
        while True:
            data = await websocket.receive_json()
            pos = data.get("position")
            if isinstance(pos, int):
                error = await make_move("X", pos)
                if error:
                    await websocket.send_json(error)
    except:
        await pubsub.unsubscribe("game:channel")
        print("Client disconnected")
        await reset_game()
