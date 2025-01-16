import asyncio
import websockets
import json

# async def test_websocket():
#     uri = "ws://127.0.0.1:8000/ws/messages/"
#     async with websockets.connect(uri) as websocket:
#         json_data = json.dumps( {
#             "type": "users_chats",
#             "chat_creator_id": "e95802fe-6b5f-4055-a416-d7b9e8061432"
#         })
#         await websocket.send(json_data)
        
#         response = await websocket.recv()
#         print(f"Received: {response}")
#         response = await websocket.recv()
#         print(f"Received: {response}")

async def test_websocket():
    uri = "ws://127.0.0.1:8000/ws/messages/81da7fc5-4027-4b94-8374-dfa040d9b9a3"
    async with websockets.connect(uri) as websocket:
        await websocket.send(json.dumps({'type':'message', 'message': 'salom vashe', 'sender':'Psadu5tRXdb1LQHbRtFKp1LRiDZ2'}))
        response = await websocket.recv()
        print(f"Received: {response}")


asyncio.get_event_loop().run_until_complete(test_websocket())

