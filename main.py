# app.py
from flask import Flask, jsonify, request
from langchain_openai import ChatOpenAI
from browser_use import Agent
import asyncio
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

@app.route('/browser-ui', methods=['POST'])
def compare_prices():
    # Get the task from the JSON body
    data = request.get_json()
    task = data.get('task', '')

    async def run_agent():
        agent = Agent(
            task=task,
            llm=ChatOpenAI(model="gpt-4o"),
        )
        result = await agent.run()
        return result

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    result = loop.run_until_complete(run_agent())
    return jsonify(result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
