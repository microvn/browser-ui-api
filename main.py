from flask import Flask, jsonify, request
from langchain_google_genai import ChatGoogleGenerativeAI
from pydantic import SecretStr
from browser_use import Agent
import asyncio
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

api_key = SecretStr(os.getenv("GEMINI_API_KEY"))

# Initialize the model
llm = ChatGoogleGenerativeAI(model='gemini-2.0-flash-exp', api_key=api_key)

def convert_to_dict(agent_history_list):
    return {
        'all_results': agent_history_list,
    }

@app.route('/browser-ui', methods=['POST'])
def compare_prices():
    # Get the task from the JSON body
    data = request.get_json()
    task = data.get('task', '')

    async def run_agent():
        agent = Agent(
            task=task,
            llm=llm,
        )
        result = await agent.run()
        return result

    # Sử dụng asyncio.run() để chạy coroutine
    result = asyncio.run(run_agent())
    return jsonify(result.model_dump())

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)