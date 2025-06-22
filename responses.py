import random

messages = [
    # 🟢 Friendly & Casual
    "Heads up! 👀 Looks like {name} just dropped by your place!",
    "Ding dong! 🔔 {name} is at your door — should we roll out the red carpet?",
    "📸 Smile! {name} just made a surprise appearance at your doorstep.",
    "Guess who? 🤔 It’s {name}! You've got company.",

    # 🧠 Witty & Playful
    "Alert: One {name} has been spotted in the wild near your door. Should we feed them?",
    "🏠 Your fortress has been visited by: {name}. Intruder or guest? You decide!",
    "🕵️‍♂️ Motion detected: {name} is sneaking around like it’s Mission Impossible.",
    "🚨 Breaking news: {name} just arrived! Are we ready to party or panic?",

    # 🤖 Quirky & Robotic
    "🤖 Facial recognition complete. Visitor = {name}. Initiating hospitality protocol...",
    "🧠 SmartCam reports: {name} is here. Probability of friendliness: 99.7%."
]

def generate_visitor_message(visitor_name):
    template = random.choice(messages)
    return template.format(name=visitor_name)
