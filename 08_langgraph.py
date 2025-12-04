# LangChain生态学习系列 - LangGraph循环对话示例
from langgraph.graph import StateGraph, END
from typing import TypedDict, Annotated
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage, BaseMessage

import operator
import os

# -----------------------------
# 定义对话状态
# -----------------------------
class ChatState(TypedDict):
    messages: Annotated[list[BaseMessage], operator.add]   # 自动累积消息
    user_input: str
    round_count: int

# 初始化LLM
llm = ChatOpenAI(
            base_url=os.getenv("OPENAI_API_BASE"),
            api_key=os.getenv("OPENAI_API_KEY"),
            model="deepseek-ai/DeepSeek-V3", temperature=0.7
        )

# -----------------------------
# 节点1：处理用户输入
# -----------------------------
def handle_user_input(state: ChatState) -> ChatState:
    user_text = state["user_input"]
    return {
        "messages": [HumanMessage(content=user_text)],
        "round_count": state["round_count"] + 1
    }

# -----------------------------
# 节点2：生成 AI 回复
# -----------------------------
def generate_response(state: ChatState) -> ChatState:
    response = llm.invoke(state["messages"])
    return {
        "messages": [AIMessage(content=response.content)]
    }

# -----------------------------
# 判断是否继续
# -----------------------------
def should_continue_chat(state: ChatState) -> str:
    user_input = state["user_input"].lower()

    if any(word in user_input for word in ["再见", "拜拜", "结束", "quit"]):
        return "end"

    if state["round_count"] >= 10:
        return "end"

    return "continue"

# -----------------------------
# 构建图
# -----------------------------
workflow = StateGraph(ChatState)

workflow.add_node("process_input", handle_user_input)
workflow.add_node("generate_reply", generate_response)

workflow.set_entry_point("process_input")

workflow.add_edge("process_input", "generate_reply")

workflow.add_conditional_edges(
    "generate_reply",
    should_continue_chat,
    {
        "continue": "process_input",
        "end": END
    }
)

chat_app = workflow.compile()

# -----------------------------
# 运行对话
# -----------------------------
if __name__ == "__main__":
    print("聊天机器人已启动（输入'再见'结束对话）\n")

    state = {"messages": [], "user_input": "", "round_count": 0}

    while True:
        user_input = input("你: ")
        state["user_input"] = user_input

        result = chat_app.invoke(state)

        ai_message = result["messages"][-1]
        print(f"助手: {ai_message.content}\n")

        state = result

        if should_continue_chat(state) == "end":
            print("对话结束，再见！")
            break
