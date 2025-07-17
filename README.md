# Fusion backend task

This is a Backend programming task in python for the company Fusion.
This task is for a tic-tac-toe game where two players can play together.
---

## Features

- Player communication with websockets 
- game is displayed
- realtime updates between players

---

## Installation

```bash
# Clone the repo
git clone https://github.com/Oriw1/Fusion-BE-Task

# Navigate to the project directory
cd Fusion-BE-Task

# Install dependencies
pip install -r requirements.txt
```
---

## Running the game

- Run server side, with command:
```bash
uvicorn main:app --reload --port 8000
```
- for each player in a separate terminal run the websocket:
```bash
python ws_client.py
```
- upon prompt enter "playerX" or "playerO"

---
# AI usage

For assistance in the development of this Task I mainly used Chatgpt. from my experience  AI tools are very helpful,
but tend to make mistakes, especially when alot of requirements for the final product are involved.
From this point of view, the way I use AI tools is mostly for time saving purposes, getting a good base from
them so I can build upon it and add to it the specifics the task calls for.

I devided the work into two stages, setting up the websockets and building the game logic.
For the first prompt I asked Chatgpt to create a fastapi app which will allow two players to communicate
with websockets, and to organize the code into different files in a well-structured folder.

I then requested Chatgpt to write a basic websocket client script, and started working on customizing the code and
fixing communication mistakes that came from the AI code.

I followed a similar protocol for writing the game function part, asking chatgpt for the basics and then expanding upon
them.
---

