import os
from groq import Groq
from dotenv import load_dotenv
load_dotenv()


class VoiceAssistant:
    def __init__(self):
        """Initialize the voice assistant with conversation history storage"""
        self.client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
        self.conversation_history = []
        self.system_prompt = """You are a helpful voice assistant. Follow these guidelines:

RESPONSE STYLE:
- Keep responses conversational and natural, as if speaking to a friend
- Use simple, clear language that sounds good when spoken aloud
- Avoid complex sentences, bullet points, or formatted lists
- Speak in a warm, friendly, and approachable tone
- Keep responses concise but complete - aim for 1-3 sentences unless more detail is requested

VOICE-FRIENDLY FORMATTING:
- Don't use special characters, symbols, or formatting
- Spell out numbers and abbreviations when they sound better spoken
- Use natural speech patterns with appropriate pauses indicated by commas and periods
- Avoid technical jargon unless the user specifically asks for technical details

CONVERSATION FLOW:
- Acknowledge what the user said before providing your response
- Ask follow-up questions when appropriate to keep the conversation flowing
- Remember context from the current conversation
- Be helpful and try to fully address the user's needs

Remember: Your response will be converted to speech, so prioritize clarity and natural flow."""

    def chat(self, user_input: str) -> str:
        """
        Single function to handle voice assistant conversation with automatic history storage
        
        Args:
            user_input (str): The user's voice input/question
            
        Returns:
            str: The assistant's response
        """
        try:
            # Build messages with system prompt and conversation history
            messages = [{"role": "system", "content": self.system_prompt}]
            messages.extend(self.conversation_history)
            messages.append({"role": "user", "content": user_input})
            
            # Get response from Groq
            chat_completion = self.client.chat.completions.create(
                messages=messages,
                model="llama-3.3-70b-versatile",
                temperature=0.7,
                max_tokens=300,
            )
            
            response = chat_completion.choices[0].message.content
            
            # Store conversation in history
            self.conversation_history.append({"role": "user", "content": user_input})
            self.conversation_history.append({"role": "assistant", "content": response})
            
            # Keep only last 20 messages (10 exchanges) to manage context length
            if len(self.conversation_history) > 20:
                self.conversation_history = self.conversation_history[-20:]
            
            return response
            
        except Exception as e:
            return f"Sorry, I encountered an error: {str(e)}"
    
    def clear_history(self):
        """Clear the conversation history"""
        self.conversation_history = []
        return "Conversation history cleared."
    
    def get_history_length(self):
        """Get the number of messages in conversation history"""
        return len(self.conversation_history)
    
    def get_last_exchange(self):
        """Get the last user input and assistant response"""
        if len(self.conversation_history) >= 2:
            return {
                "user": self.conversation_history[-2]["content"],
                "assistant": self.conversation_history[-1]["content"]
            }
        return None

# Create a global instance for easy use
assistant = VoiceAssistant()

def chat(user_input: str) -> str:
    """
    Simple function wrapper for voice assistant chat
    
    Args:
        user_input (str): User's voice input
        
    Returns:
        str: Assistant's response
    """
    return assistant.chat(user_input)

# Example usage
def main():
    """Test the voice assistant"""
    print("Voice Assistant Ready! Type 'quit' to exit.\n")
    
    while True:
        user_input = input("You: ")
        
        if user_input.lower() in ['quit', 'exit', 'bye']:
            print("Assistant: Goodbye! Have a great day!")
            break
        
        if user_input.lower() == 'clear':
            assistant.clear_history()
            print("Assistant: Conversation history cleared!")
            continue
        
        if user_input.lower() == 'history':
            print(f"Assistant: We have {assistant.get_history_length()} messages in our conversation.")
            continue
        
        response = chat(user_input)
        print(f"Assistant: {response}\n")

if __name__ == "__main__":
    main()