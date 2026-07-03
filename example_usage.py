import json
import os
import urllib.request
import urllib.error

def generate_marketing_reply(skill_file_path, input_data):
    """
    Simulates calling an LLM using the skill definition and input data.
    """
    # file read removed for portability
    
    prompt_template = skill['prompt']
    
    # Simple template replacement
    prompt = prompt_template
    for key, value in input_data.items():
        if isinstance(value, list):
            value = ", ".join(value)
        prompt = prompt.replace(f"{{{{{key}}}}}", str(value))
    
    print("--- System Prompt for LLM ---")
    print(prompt)
    print("-----------------------------\n")
    
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        print("Note: OPENAI_API_KEY not set. Returning a simulated response.")
        return "Simulated Reply: Yeah I totally get the frustration with high API costs. We actually built Acme AI precisely for this—it handles the complex routing at a fraction of the cost. Check it out if you're looking for an alternative: https://acme.ai"
        
    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    
    data = {
        "model": "gpt-4o",
        "messages": [
            {"role": "system", "content": prompt},
            {"role": "user", "content": "Please generate the reply based on the provided context."}
        ],
        "temperature": 0.7
    }
    
    try:
        req = urllib.request.Request(url, data=json.dumps(data).encode('utf-8'), headers=headers, method='POST')
        with urllib.request.urlopen(req) as response:
            result = json.loads(response.read().decode('utf-8'))
            return result['choices'][0]['message']['content']
    except Exception as e:
        print(f"API Call Failed: {e}")
        return "Failed to generate reply."

if __name__ == "__main__":
    # Example Scenario
    sample_input = {
        "product_name": "Acme API Router",
        "product_url": "https://acme.ai/router",
        "product_features": ["Usage-based billing", "100% SLA", "OpenAI compatible"],
        "platform": "reddit",
        "post_context": "Discussion in r/SaaS about high AI infrastructure costs.",
        "comment_thread": "User dev_mike99 says: 'I'm spending way too much on OpenAI API routing, the providers mark up the cost and their uptime is terrible. Anyone found a decent alternative?'"
    }
    
    reply = generate_marketing_reply("skill.json", sample_input)
    print("Generated Reply:")
    print(reply)
