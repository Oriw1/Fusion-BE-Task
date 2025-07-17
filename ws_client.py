import asyncio
import websockets
import json


def print_board(board):
    for i in range(0, 9, 3):
        print(f" {board[i]} | {board[i+1]} | {board[i+2]} ")
        if i < 6:
            print("---|---|---")


async def play(player_id):
    uri = f"ws://localhost:8000/ws/{player_id}"
    async with websockets.connect(uri) as websocket:
        print(f"Connected as {player_id}. Waiting for game state...")
        waiting_for_input = False

        while True:
            response = await websocket.recv()
            data = json.loads(response)

            if "error" in data:
                print(f"Error: {data['error']}")
                if waiting_for_input:
                    while True:
                        move = input(f"{player_id}, retry your move (0-8): ")
                        try:
                            position = int(move)
                            if 0 <= position <= 8:
                                await websocket.send(json.dumps({"position": position}))
                                break
                            else:
                                print("Move must be between 0 and 8.")
                        except ValueError:
                            print("Invalid input. Enter a number from 0 to 8.")
                continue

            if "board" in data:
                print("\nGame State:")
                print_board(data["board"])
                print(f"Current turn: {data['current_player']}")

                if data["winner"]:
                    print(f"\nWinner: {data['winner']}")
                    break

                if data["current_player"] == player_id[-1]:  # 'X' or 'O'
                    waiting_for_input = True
                    while True:
                        move = input(f"{player_id}, your move (0-8): ")
                        try:
                            position = int(move)
                            if 0 <= position <= 8:
                                await websocket.send(json.dumps({"position": position}))
                                break
                            else:
                                print("Move must be between 0 and 8.")
                        except ValueError:
                            print("Invalid input. Enter a number from 0 to 8.")
                    waiting_for_input = False


if __name__ == "__main__":
    player = input("Enter player ID (playerX/playerO): ")
    asyncio.run(play(player))