import asyncio
import websockets
from aioconsole import ainput

async def send_msg(websocket):
    while True:
        msg = await ainput("> ")
        await websocket.send(msg)

async def recv_msg(websocket):
    try:
        async for message in websocket:
            print(f"\n{message}\n> ", end="", flush=True)
    except Exception as e:
        print(f"Receive error: {e}")

async def chat(player_id):
    uri = f"ws://localhost:8000/ws/{player_id}"
    async with websockets.connect(uri) as websocket:
        print(f"Connected as {player_id}")
        send_task = asyncio.create_task(send_msg(websocket))
        recv_task = asyncio.create_task(recv_msg(websocket))
        await asyncio.gather(send_task, recv_task)

if __name__ == "__main__":
    player = input("Enter player (player1/player2): ")
    asyncio.run(chat(player))
