from quart import Quart, jsonify, request
from langchain_google_genai import ChatGoogleGenerativeAI
from pydantic import SecretStr
from browser_use import Agent
from dotenv import load_dotenv
import os

load_dotenv()

app = Quart(__name__)

api_key = SecretStr(os.getenv("GEMINI_API_KEY"))

# Initialize the model
llm = ChatGoogleGenerativeAI(model='gemini-2.0-flash-exp', api_key=api_key)

@app.route('/browser-use', methods=['POST'])
async def compare_prices():
    # Get the task from the JSON body
    data = await request.get_json()
    task = data.get('task', '')

    agent = Agent(
        task=task,
        llm=llm,
    )
    result = await agent.run()
    return jsonify(result.model_dump())

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
