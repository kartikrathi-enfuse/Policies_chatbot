# Define a list of general queries
general_queries = [
    "hi", "hello", "hey", "how are you", "good morning", "good evening",
    "good afternoon", "what's up", "how’s it going", "how do you do", "ok"
]

def is_general_question(query):
    """Check if the user query is a general/small talk question"""
    return any(query.lower().strip().startswith(greet) for greet in general_queries)

# Example usage
user_input = "Hi"
bot_response = is_general_question(user_input)
print(bot_response)  # Output: "Hello! How can I assist you today?"
