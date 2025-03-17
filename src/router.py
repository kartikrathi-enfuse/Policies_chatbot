# Define a list of general queries
general_queries = [
    "hi", "hello", "hey", "how are you", "good morning", "good evening",
    "good afternoon", "what's up", "how’s it going", "how do you do", "ok"
]

def is_general_question(query):
    """Check if the user query is a general/small talk question"""
    query = query.lower().strip()
    if query in general_queries:  # Check if query exactly matches a general query
        return "Hello! I'm Engene, your HR policies chatbot! How can I assist you today?"
    return False  # Return False if it's not an exact match

# Example usage
user_input = "Hi"
bot_response = is_general_question(user_input)
print(bot_response)  # Output: "Hello! How can I assist you today?"
