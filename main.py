from quart import Quart, jsonify, request
from langchain_google_genai import ChatGoogleGenerativeAI
from pydantic import SecretStr
from browser_use import Agent
from dotenv import load_dotenv
import os
import asyncio
import uuid

load_dotenv()

app = Quart(__name__)

api_key = SecretStr(os.getenv("GEMINI_API_KEY"))
llm = ChatGoogleGenerativeAI(model='gemini-2.0-flash-exp', api_key=api_key)

# Tạo hàng đợi để lưu trữ các task
task_queue = asyncio.Queue()
task_results = {}

async def worker():
    while True:
        task_id, task = await task_queue.get()
        agent = Agent(task=task, llm=llm)
        try:
            result = await agent.run()
            task_results[task_id] = result.model_dump()
        except Exception as e:
            task_results[task_id] = {"error": str(e)}
        finally:
            task_queue.task_done()

# Khởi động worker
@app.before_serving
async def startup():
    asyncio.create_task(worker())

@app.route('/browser-use', methods=['POST'])
async def compare_prices():
    data = await request.get_json()
    task = data.get('task', '')
    task_id = str(uuid.uuid4())  # Tạo taskId duy nhất

    # Thêm task vào hàng đợi
    await task_queue.put((task_id, task))

    return jsonify({"taskId": task_id}), 202  # Trả về 202 Accepted

@app.route('/browser-use/<task_id>', methods=['GET'])
async def get_task_result(task_id):
    result = task_results.get(task_id, None)
    if result is not None:
        return jsonify(result)
    else:
        return jsonify({"error": "Task not found or still processing."}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
