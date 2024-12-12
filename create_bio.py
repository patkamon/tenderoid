from langchain_ollama import ChatOllama
import random


messages = [
    ("system", "You are a helpful assistant."),
    ("human", "generate me, random anime girl can be any nationality, and gimme personality, "
    "hobby, and biometric (age (prefer 18+), height (prefer 140-170 cm), hair & color, build (slim, chubby, etc), and eye color)"
    "example"
    "PERSONALITY = sweet, devoted, and quietly confident despite her initial shy demeanor. Rem has a self-sacrificing streak and an incredible sense of loyalty, especially towards people she loves. Her personality is a blend of tenderness and fierce protectiveness, with a dash of playful teasing when she's comfortable with someone"
    "HOBBY = into gardening? 🌱 She loves tending to flowers and finds peace in nurturing her little garden"
    "BIO = Age: 19 Height: 5'4 (163 cm) Weight: 110 lbs (50 kg) Hair: Sky blue Eyes: Big and ocean blue"
    "follow the format like given example"
    ),
]


def create_bio(random_seed):
    print(random_seed)
    llm = ChatOllama(
        model="llama3.2",
        temperature=1,
        seed=random_seed,
        top_p=0.9,
        top_k=80,
    )

    msg = llm.invoke(messages)
    print(msg.content)
    return str(msg.content)














