# function-calling-tools

This library provides an easy-to-use interface for function calling.

## Installation

```bash
pip install function_calling_tools
```

## Usage

see `example` for more detail.

```bash
export OPENAI_API_KEY=xxx
```

```python
import os
import openai
from langchain.memory import ConversationBufferMemory
from langchain.prompts import MessagesPlaceholder
from langchain.chat_models import ChatOpenAI
from langchain.agents import initialize_agent
from langchain.agents import AgentType

from function_calling_tools.ntp import TimeZoneDatetimeFetcher

tools = [
  TimeZoneDatetimeFetcher(),
]

memory = ConversationBufferMemory(memory_key="memory", return_messages=True)

agent_kwargs = {
  "extra_prompt_messages": [MessagesPlaceholder(variable_name="memory")],
}

prompt = """
Don't make assumptions about what values to plug into functions. Ask for clarification if a user request is ambiguous.
"""

memory.save_context({"input": prompt}, {"output": "I got it!"})

openai.api_key = os.environ["OPENAI_API_KEY"]
llm = ChatOpenAI(model_name="gpt-3.5-turbo")

agent = initialize_agent(
    tools,
    llm,
    agent=AgentType.OPENAI_FUNCTIONS,
    verbose=True,
    agent_kwargs=agent_kwargs,
    memory=memory,
)

agent.run(input="What time is it now in Tokyo?")
```

| Module Name             | Description                                                                             | Additional Parameters                         |
| ----------------------- | --------------------------------------------------------------------------------------- | --------------------------------------------- |
| TimeZoneDatetimeFetcher | fetch current datetime in timezone                                                      | -                                             |
| WeatherFetcher          | fetch weather info using [piratewhether](https://docs.pirateweather.net/en/latest/API/) | PIRATE_WEATHER_API_KEY                        |
| RedmineInfo             | create redmine issue                                                                    | REDMINE_URL, REDMINE_PROJECT, REDMINE_API_KEY |
