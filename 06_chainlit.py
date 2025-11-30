# LangChain生态学习系列 - Chainlit界面集成
# chainlit run 06_chainlit.py --host 0.0.0.0

import chainlit as cl
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_classic.chains import ConversationalRetrievalChain
from langchain_classic.memory import ConversationBufferMemory
import os

# 应用启动时执行一次
@cl.on_chat_start
async def start():
    # 加载已有的向量数据库
    # embeddings = OpenAIEmbeddings()
    # 其他供应商
    embeddings = OpenAIEmbeddings(
        base_url=os.getenv("OPENAI_API_BASE"),
        api_key=os.getenv("OPENAI_API_KEY"),
        model="Qwen/Qwen3-Embedding-4B"
    )
    vectordb = Chroma(
        persist_directory="./files/pdf_vectordb",
        embedding_function=embeddings
    )
    
    # 配置检索器
    retriever = vectordb.as_retriever(
        search_type="similarity",
        search_kwargs={"k": 4}
    )
    
    # 初始化对话记忆
    memory = ConversationBufferMemory(
        memory_key="chat_history",
        output_key="answer",
        return_messages=True
    )
    
    # 创建对话链
    qa_chain = ConversationalRetrievalChain.from_llm(
        llm= ChatOpenAI(
            base_url=os.getenv("OPENAI_API_BASE"),
            api_key=os.getenv("OPENAI_API_KEY"),
            model="deepseek-ai/DeepSeek-V3", temperature=0.7
        ),
        retriever=retriever,
        memory=memory,
        return_source_documents=True
    )
    
    # 保存到用户会话中
    cl.user_session.set("qa_chain", qa_chain)
    
    # 发送欢迎消息
    await cl.Message(content="你好！我是PDF问答助手，可以回答文档相关的任何问题。").send()

# 处理用户消息
@cl.on_message
async def main(message: cl.Message):
    # 获取对话链
    qa_chain = cl.user_session.get("qa_chain")
    
    # 调用对话链
    result = await qa_chain.ainvoke(
        {"question": message.content}
    )
    
    # 构建回复内容
    response_content = result["answer"]
    
    # 添加来源信息
    if result.get("source_documents"):
        sources = "\n\n**参考来源：**\n"
        for idx, doc in enumerate(result["source_documents"][:3], 1):
            source = doc.metadata.get("source", "未知")
            page = doc.metadata.get("page", "?")
            sources += f"{idx}. {source} (第{page}页)\n"
        response_content += sources
    
    # 发送消息
    await cl.Message(content=response_content).send()