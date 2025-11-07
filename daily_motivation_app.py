import streamlit as st
import random
from datetime import datetime
import json
import os

# Set page config
st.set_page_config(
    page_title="Daily Motivation",
    page_icon="✨",
    layout="centered"
)

# Motivational messages
MOTIVATIONAL_MESSAGES = [
    "Believe you can and you're halfway there. - Theodore Roosevelt",
    "The only way to do great work is to love what you do. - Steve Jobs",
    "Success is not final, failure is not fatal: it is the courage to continue that counts. - Winston Churchill",
    "You are never too old to set another goal or to dream a new dream. - C.S. Lewis",
    "The future belongs to those who believe in the beauty of their dreams. - Eleanor Roosevelt",
    "It does not matter how slowly you go as long as you do not stop. - Confucius",
    "Everything you've ever wanted is on the other side of fear. - George Addair",
    "Believe in yourself. You are braver than you think, more talented than you know, and capable of more than you imagine.",
    "I learned that courage was not the absence of fear, but the triumph over it. - Nelson Mandela",
    "The only impossible journey is the one you never begin. - Tony Robbins",
    "Your limitation—it's only your imagination.",
    "Push yourself, because no one else is going to do it for you.",
    "Great things never come from comfort zones.",
    "Dream it. Wish it. Do it.",
    "Success doesn't just find you. You have to go out and get it.",
    "The harder you work for something, the greater you'll feel when you achieve it.",
    "Dream bigger. Do bigger.",
    "Don't stop when you're tired. Stop when you're done.",
    "Wake up with determination. Go to bed with satisfaction.",
    "Do something today that your future self will thank you for.",
]

# File to store user data
DATA_FILE = "user_data.json"

def load_user_data():
    """Load user data from file"""
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_user_data(data):
    """Save user data to file"""
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f)

def get_daily_message(user_id):
    """Get the daily message for a user"""
    today = datetime.now().strftime("%Y-%m-%d")
    user_data = load_user_data()
    
    # Check if user exists and if they've already gotten today's message
    if user_id in user_data and user_data[user_id].get("last_date") == today:
        return user_data[user_id]["message"]
    
    # Generate new message for today
    # Use date as seed for consistent daily message across all users
    random.seed(today)
    message = random.choice(MOTIVATIONAL_MESSAGES)
    
    # Save the message
    user_data[user_id] = {
        "last_date": today,
        "message": message
    }
    save_user_data(user_data)
    
    return message

# Main app
st.title("✨ Daily Motivation")
st.markdown("---")

# Get or create user ID
if 'user_id' not in st.session_state:
    st.session_state.user_id = f"user_{random.randint(100000, 999999)}"

# Display welcome message
st.markdown(f"### Welcome back! 👋")
st.markdown(f"*{datetime.now().strftime('%B %d, %Y')}*")

# Get and display daily message
daily_message = get_daily_message(st.session_state.user_id)

st.markdown("")
st.info(f"**Your daily motivation:**\n\n{daily_message}")

st.markdown("---")
st.markdown("*Come back tomorrow for a new inspiring message! 🌟*")

# Optional: Add a motivational image
st.markdown("")
st.markdown("### 💪 You've got this!")
