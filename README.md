# ai-comment-skill

> **GenPark AI Agent Skill** -- # AI Comment Skill 🚀

A decision-intent marketing agent skill inspired by the growth strategies of tools like Xiaowa AI. This skill helps you capture high-intent users directly from social media comment sections.

## 🎯 What is it?
Traditional ads target *Search Intent* (Google) or *Behavioral Intent* (Meta). This skill targets **Decision Intent**. 
When users are in comment sections on Reddit, X, YouTube, or TikTok comparing products, complaining about pricing, or asking for recommendations, this skill analyzes the context and generates a natural, helpful reply that subtly introduces your product.

## 📦 What's included?
- `skill.json`: The core Agent Skill definition. It includes the system prompt, input schema, and output schema.
- `example_usage.py`: A Python script demonstrating how to use this skill with the OpenAI API.

## 🛠️ How to use

### Option 1: Import to an Agent Platform
You can import `skill.json` into platforms like Dify, Coze, or custom GPTs. Map the inputs (product details, platform, comment text) to the prompt variables.

### Option 2: Use in your Python Backend
1. Install OpenAI SDK: `pip install openai`
2. Set your API key: `export OPENAI_API_KEY="your-key-here"`
3. Run the example: `python example_usage.py`

## 🧠 Core Strategy
- **Platform Adaptation**: Automatically adjusts tone (e.g., Reddit needs detailed, objective answers; TikTok needs fast, casual replies).
- **Empathy First**: Acknowledges the user's pain point before mentioning the product.
- **Value-Driven**: Highlights specific features that solve the user's exact problem, avoiding generic "Buy Now" spam.