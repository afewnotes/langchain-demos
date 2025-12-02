# LangChain 1.0+ (LangGraph) - Agent与ReAct框架示例
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.agents import create_agent
from langchain.tools import tool
import os
from langchain_community.tools import DuckDuckGoSearchRun

# 加载环境变量
load_dotenv()

# os.environ["HTTP_PROXY"] = "http://127.0.0.1:7897"
# os.environ["HTTPS_PROXY"] = "http://127.0.0.1:7897"

# -----------------------------
# 定义工具
# -----------------------------

@tool
def 网络搜索(query: str) -> str:
    """
    用于搜索网络信息。当需要查询最新资讯、事实性问题时使用。
    输入：搜索查询语句
    输出：搜索结果字符串
    """
    
    search = DuckDuckGoSearchRun()
    return search.run(query)

@tool
def 计算器(expr: str) -> str:
    """
    用于执行数学计算或简单 Python 表达式
    输入：有效的 Python 表达式，例如 '2+2' 或 'import math; math.sqrt(16)'
    输出：结果字符串
    """
    # 注意：仅限受信任的表达式，实际可加入沙箱限制
    return str(eval(expr))

# -----------------------------
# 初始化 LLM
# -----------------------------
llm = ChatOpenAI(
            base_url=os.getenv("OPENAI_API_BASE"),
            api_key=os.getenv("OPENAI_API_KEY"),
            model="deepseek-ai/DeepSeek-V3", temperature=0.7
        )

# -----------------------------
# 创建 Agent (ReAct)
# -----------------------------
agent = create_agent(
    model=llm,
    tools=[网络搜索, 计算器],
    system_prompt="You are a helpful assistant. You can decide when to use the provided tools."
)

# -----------------------------
# 测试 Agent
# -----------------------------
if __name__ == "__main__":
    # 问题1：搜索 + 计算
    question1 = "OpenAI 的 ChatGPT 是哪一年发布的，距今多少年了？"
    print(f"问题：{question1}")
    ans1 = agent.invoke({"messages":[{"role":"user","content":question1}]})
    print(f"答案：{ans1['messages'][-1]['content']}\n")

    # 问题2：只搜索
    question2 = "LangChain 框架的主要作用是什么？"
    print(f"问题：{question2}")
    ans2 = agent.invoke({"messages":[{"role":"user","content":question2}]})
    print(f"答案：{ans2['messages'][-1]['content']}\n")

    # 问题3：只计算
    question3 = "计算 (2**10 + 3**5) * 4 的结果"
    print(f"问题：{question3}")
    ans3 = agent.invoke({"messages":[{"role":"user","content":question3}]})
    print(f"答案：{ans3['messages'][-1]['content']}\n")
