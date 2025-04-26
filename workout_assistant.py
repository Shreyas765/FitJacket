import os
from groq import Groq
from typing import List, Dict

class WorkoutData:
    def __init__(self, goals: str, progress: str, last_workouts: List[Dict]):
        self.goals = goals
        self.progress = progress
        self.last_workouts = last_workouts

def get_workout_tip(workout_data: WorkoutData) -> str:
    client = Groq(
        api_key="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"
    )
    
    # Format the workout data into a clear prompt
    prompt = f"""Based on the following user data, provide exactly one specific workout tip in a single sentence:
    Goals: {workout_data.goals}
    Current Progress: {workout_data.progress}
    Last 3 Workouts: {workout_data.last_workouts}
    
    Provide only one sentence as a tip, no additional text."""

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        model="llama-3.3-70b-versatile",
    )
    
    return chat_completion.choices[0].message.content.strip()

# Example usage
if __name__ == "__main__":
    # Example data - replace with actual user data
    sample_data = WorkoutData(
        goals="Build muscle and improve endurance",
        progress="Weight: 180 lbs, Body Fat: 15%, Strength: Increased by 20%",
        last_workouts=[
            {"date": "2024-03-20", "type": "Strength", "duration": "60 min"},
            {"date": "2024-03-18", "type": "Cardio", "duration": "30 min"},
            {"date": "2024-03-16", "type": "HIIT", "duration": "45 min"}
        ]
    )
    
    tip = get_workout_tip(sample_data)
    print("\nYour personalized workout tip:")
    print(tip) 
