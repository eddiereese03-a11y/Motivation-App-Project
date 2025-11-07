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

# Motivational messages by category
MOTIVATIONAL_MESSAGES = {
    "Success": [
        "Believe you can and you're halfway there. - Theodore Roosevelt",
        "The only way to do great work is to love what you do. - Steve Jobs",
        "Success is not final, failure is not fatal: it is the courage to continue that counts. - Winston Churchill",
        "The future belongs to those who believe in the beauty of their dreams. - Eleanor Roosevelt",
        "It does not matter how slowly you go as long as you do not stop. - Confucius",
        "Everything you've ever wanted is on the other side of fear. - George Addair",
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
        "I learned that courage was not the absence of fear, but the triumph over it. - Nelson Mandela",
    ],
    "Love": [
        "Love is not about how much you say 'I love you,' but how much you prove that it's true.",
        "The best thing to hold onto in life is each other. - Audrey Hepburn",
        "Where there is love there is life. - Mahatma Gandhi",
        "Love yourself first and everything else falls into line. - Lucille Ball",
        "To love and be loved is to feel the sun from both sides. - David Viscott",
        "The greatest happiness of life is the conviction that we are loved. - Victor Hugo",
        "Love is composed of a single soul inhabiting two bodies. - Aristotle",
        "In the end, only three things matter: how much you loved, how gently you lived, and how gracefully you let go.",
        "Love recognizes no barriers. It jumps hurdles, leaps fences, penetrates walls to arrive at its destination. - Maya Angelou",
        "The best and most beautiful things in this world cannot be seen or even heard, but must be felt with the heart. - Helen Keller",
        "You know you're in love when you can't fall asleep because reality is finally better than your dreams. - Dr. Seuss",
        "Love grows by giving. The love we give away is the only love we keep. - Elbert Hubbard",
        "Being deeply loved by someone gives you strength, while loving someone deeply gives you courage. - Lao Tzu",
        "Life without love is like a tree without blossoms or fruit. - Khalil Gibran",
        "The giving of love is an education in itself. - Eleanor Roosevelt",
    ],
    "Funny": [
        "I'm not lazy, I'm just on energy-saving mode.",
        "Coffee: because adulting is hard.",
        "I don't need a hair stylist, my pillow gives me a new hairstyle every morning.",
        "I'm not arguing, I'm just explaining why I'm right.",
        "The road to success is dotted with many tempting parking spaces. - Will Rogers",
        "I always wanted to be somebody, but now I realize I should have been more specific. - Lily Tomlin",
        "If at first you don't succeed, then skydiving definitely isn't for you. - Steven Wright",
        "The only mystery in life is why the kamikaze pilots wore helmets. - Al McGuire",
        "I find television very educational. Every time someone turns it on, I go in the other room and read a book. - Groucho Marx",
        "Behind every great man is a woman rolling her eyes. - Jim Carrey",
        "The difference between genius and stupidity is that genius has its limits. - Albert Einstein",
        "I'm not superstitious, but I am a little stitious. - Michael Scott",
        "The elevator to success is out of order. You'll have to use the stairs... one step at a time. - Joe Girard",
        "Do not take life too seriously. You will never get out of it alive. - Elbert Hubbard",
        "People say nothing is impossible, but I do nothing every day. - A.A. Milne",
    ]
}

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

def get_daily_message(user_id, category="Success"):
    """Get the daily message for a user"""
    today = datetime.now().strftime("%Y-%m-%d")
    user_data = load_user_data()
    
    # Create a unique key for user + category + date
    data_key = f"{user_id}_{category}_{today}"
    
    # Check if user exists and if they've already gotten today's message for this category
    if data_key in user_data:
        return user_data[data_key]["message"]
    
    # Generate new message for today
    # Use date and category as seed for consistent daily message
    random.seed(f"{today}_{category}")
    message = random.choice(MOTIVATIONAL_MESSAGES[category])
    
    # Save the message
    user_data[data_key] = {
        "last_date": today,
        "category": category,
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

# Category selector
st.markdown("")
st.markdown("#### Choose your motivation category:")
category = st.selectbox(
    "Select a category",
    options=["Success", "Love", "Funny"],
    index=0,
    label_visibility="collapsed"
)

# Get and display daily message
daily_message = get_daily_message(st.session_state.user_id, category)

st.markdown("")
st.info(f"**Your daily motivation:**\n\n{daily_message}")

# Share buttons
st.markdown("")
col1, col2, col3, col4 = st.columns(4)

# Prepare share text
share_text = f"Today's motivation: {daily_message}"
encoded_text = share_text.replace(" ", "%20").replace("\n", "%0A")

with col1:
    twitter_url = f"https://twitter.com/intent/tweet?text={encoded_text}"
    st.markdown(f"[🐦 Twitter]({twitter_url})")

with col2:
    facebook_url = f"https://www.facebook.com/sharer/sharer.php?quote={encoded_text}"
    st.markdown(f"[📘 Facebook]({facebook_url})")

with col3:
    linkedin_url = f"https://www.linkedin.com/sharing/share-offsite/?url=&summary={encoded_text}"
    st.markdown(f"[💼 LinkedIn]({linkedin_url})")

with col4:
    whatsapp_url = f"https://wa.me/?text={encoded_text}"
    st.markdown(f"[💬 WhatsApp]({whatsapp_url})")

# Copy to clipboard button
st.markdown("")
if st.button("📋 Copy to Clipboard"):
    st.code(daily_message, language=None)
    st.success("✅ Message displayed above - select and copy it!")

st.markdown("---")
st.markdown("*Come back tomorrow for a new inspiring message! 🌟*")

# Optional: Add a motivational image
st.markdown("")
st.markdown("### 💪 You've got this!")
