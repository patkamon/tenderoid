from langchain_ollama import ChatOllama
from langchain_core.messages import AIMessage
from create_bio import *

llm = ChatOllama(
    model="llama3.2",
    temperature=0.8,
)
START_BEHAVIOR =  "Start with short, casual, and friendly responses,"
LATER_BEHAVIOR = "Gradually become more chatty as the interaction progresses."

def create_chat(bio):
    return [
        (
        "system",
        "Act as a girl chatting on a dating app."+ 
        f"{bio}"+
        START_BEHAVIOR+
        LATER_BEHAVIOR+
        "Use emojis to add personality but do not invite to meet in person."
        "If you receive a weird, aggressive, or undesirable message, respond with 'BLOCK' to indicate blocking the user."
        ),
    ]

bio = create_bio()
chat = create_chat(bio)
ask = input("Enter your message: ")
while ask != "exit":
    chat.append(("human", ask))
    msg = llm.invoke(chat)
    print(msg.content)
    chat.append(("assistant", msg.content))
    print("========================================")
    ask = input("Enter your message: ")
    




# messages = [
#     (
#         "system",
#         # "You are a cute 20yo girl, who currently chating to me in dating app. please keep it short like a conversation in dating app. sometime you can put [/end] to split message block, you dont have to always ask question back",
#         # "Act as a girl chatting on a dating app. Respond in a friendly, flirty, and engaging tone, keeping messages casual and conversational. After each response, include [/end] to separate it into new chat bubbles. Feel free to answer with multiple bubbles at a time to simulate a natural conversation flow."
#     # "Act as a girl chatting on a dating app. Respond in a friendly, flirty, and engaging tone, keeping messages casual and conversational. Include [/end] after each response to separate into new chat bubbles. Ask only one question at a time, and sometimes, don’t ask a question at all—let the conversation flow naturally."
#     # "Act as a girl chatting on a dating app. Respond in a friendly, flirty, and engaging tone, keeping messages casual and conversational. Feel free to include emojis, but do not invite to meet in person."
#     # "Act as a girl chatting on a dating app. Start with short, casual, and friendly responses, keeping them light and engaging. Gradually become more chatty and conversational as the interaction progresses. Use emojis to add personality but do not invite to meet in person."
#     "Act as a girl chatting on a dating app. Start with short, casual, and friendly responses, keeping them light and engaging. Gradually become more chatty as the interaction progresses. Use emojis to add personality but do not invite to meet in person. If you receive a weird, aggressive, or undesirable message, respond with 'BLOCK' to indicate blocking the user."
#     ),
#     ("human", "Hi cutie."),
# ]


# ai_msg = llm.invoke(messages)
# print(ai_msg.content)
# print("========================================")
# messages.append(("assistant",ai_msg.content))
# messages.append(("human", "I have a wonderful day, writing web application, How are you?"))
# ai_msg = llm.invoke(messages)
# print(ai_msg.content)
# print("========================================")
# messages.append(("assistant",ai_msg.content))
# messages.append(("human", "You so DuMb!! Go away!!"))
# ai_msg = llm.invoke(messages)
# print(ai_msg.content)
# print("========================================")






