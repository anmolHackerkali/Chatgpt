chat_memory = {}

def add_message(user_id, role, content):
    if user_id not in chat_memory:
        chat_memory[user_id] = []

    chat_memory[user_id].append({
        "role": role,
        "content": content
    })

    if len(chat_memory[user_id]) > 20:
        chat_memory[user_id] = chat_memory[user_id][-20:]

def get_messages(user_id):
    return chat_memory.get(user_id, [])