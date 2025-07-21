import redis.asyncio as redis
import json

r = redis.Redis(host="localhost", port=6379, decode_responses=True)


def check_winner(board):
    lines = [
        [0,1,2], [3,4,5], [6,7,8],
        [0,3,6], [1,4,7], [2,5,8],
        [0,4,8], [2,4,6]
    ]
    for a, b, c in lines:
        if board[a] != " " and board[a] == board[b] == board[c]:
            return board[a]
    return ""


async def get_game_state():
    board = await r.lrange("game:board", 0, 8)
    turn = await r.get("game:turn") or "X"
    winner = await r.get("game:winner") or ""
    return {
        "board": board,
        "current_player": turn,
        "winner": winner
    }


async def reset_game():
    await r.delete("game:board", "game:turn", "game:winner")
    await r.rpush("game:board", *[" "] * 9)
    await r.set("game:turn", "X")
    await r.set("game:winner", "")
    print("[reset_game] Game state has been reset.")


async def make_move(player: str, position: int):
    async with r.pipeline(transaction=True) as pipe:
        while True:
            try:
                await pipe.watch("game:turn", "game:winner", "game:board")

                board = await r.lrange("game:board", 0, 8)
                turn = await r.get("game:turn") or "X"
                winner = await r.get("game:winner") or ""

                if winner:
                    await pipe.unwatch()
                    return {"error": f"Game over. {winner} won."}

                if turn != player:
                    await pipe.unwatch()
                    return {"error": "Not your turn"}

                if board[position] != " ":
                    await pipe.unwatch()
                    return {"error": "Invalid move"}

                board[position] = player
                new_winner = check_winner(board)
                next_turn = "O" if player == "X" else "X"

                pipe.multi()
                pipe.delete("game:board")
                pipe.rpush("game:board", *board)
                pipe.set("game:winner", new_winner)
                pipe.set("game:turn", "" if new_winner else next_turn)
                await pipe.execute()

                message = {
                    "board": board,
                    "current_player": next_turn if not new_winner else "",
                    "winner": new_winner
                }
                await r.publish("game:channel", json.dumps(message))
                return None

            except:
                continue
