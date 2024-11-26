# server.py
import asyncio
import websockets
import json
import random

# 假设这是我们会变化的9个变量
state_variables = {f'var_{i}': 0 for i in range(1, 10)}


async def notify_frontend(websocket):
    global state_variables
    while True:
        # 模拟变量的随机变化
        for key in state_variables:
            state_variables[key] = random.randint(0, 100)
        # 构建发送的数据
        data = json.dumps(state_variables)
        await websocket.send(data)
        # 每次发送后等待2秒模拟时间变化
        await asyncio.sleep(2)


async def handler(websocket, path):
    await notify_frontend(websocket)


async def main():
    async with websockets.serve(handler, "localhost", 8765):
        print("WebSocket Server started on ws://localhost:8765")
        await asyncio.Future()  # run forever


# 启动 WebSocket 服务器
if __name__ == "__main__":
    asyncio.run(main())
