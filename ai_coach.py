import os
from typing import List, Dict
from groq_client import GroqClientSingleton

class UserFitnessData:
    def __init__(self, goals: str, progress: str, last_workouts: List[Dict], fitness_level: str, user_type: str):
        self.goals = goals
        self.progress = progress
        self.last_workouts = last_workouts
        self.fitness_level = fitness_level
        self.user_type = user_type

def get_ai_coach_response(user_data: UserFitnessData, question: str) -> str:
    # Get the singleton instance
    groq_client = GroqClientSingleton()
    
    # Format the user data and question into a clear prompt
    prompt = f"""You are an AI fitness coach. Based on the following user data, provide a helpful and personalized response to their question.
    
    User Profile:
    - Fitness Level: {user_data.fitness_level}
    - User Type: {user_data.user_type}
    
    Current Goals: {user_data.goals}
    Recent Progress: {user_data.progress}
    Last 3 Workouts: {user_data.last_workouts}
    
    User's Question: {question}
    
    Provide a concise response in 2-3 sentences maximum. Focus on the most important advice. Do not use bold text, bullet points, or numbering."""

    chat_completion = groq_client.get_chat_completion(
        messages=[
            {
                "role": "system",
                "content": "You are an experienced fitness coach. Keep responses brief and to the point (2-3 sentences max). No formatting or lists."
            },
            {
                "role": "user",
                "content": prompt,
            }
        ]
    )
    
    return chat_completion.choices[0].message.content.strip()

# Example usage
if __name__ == "__main__":
    # Example data - replace with actual user data
    sample_data = UserFitnessData(
        goals="Build muscle and improve endurance",
        progress="Weight: 180 lbs, Body Fat: 15%, Strength: Increased by 20%",
        last_workouts=[
            {"date": "2024-03-20", "type": "Strength", "duration": "60 min"},
            {"date": "2024-03-18", "type": "Cardio", "duration": "30 min"},
            {"date": "2024-03-16", "type": "HIIT", "duration": "45 min"}
        ],
        fitness_level="intermediate",
        user_type="user"
    )
    
    question = "How can I improve my bench press form?"
    response = get_ai_coach_response(sample_data, question)
    print("\nAI Coach Response:")
    print(response) 