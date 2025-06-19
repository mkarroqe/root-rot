import json
import os
import requests
from typing import List, Dict

async def analyze_commit_with_claude(commit_message: str, examples: List[Dict]) -> str:
    """
    Analyzes the commit message using the Claude AI model to predict root rot,
    using examples provided from a JSON file.
    """
    print("Calling Claude AI to analyze commit message with dynamic examples...")

    claude_api_key = os.getenv('CLAUDE_API_KEY')
    if not claude_api_key:
        print("Error: CLAUDE_API_KEY environment variable not set.")
        return "Error (API Key Missing)"

    claude_api_url = "https://api.anthropic.com/v1/messages"
    claude_model = "claude-3-haiku-20240307" # Or sonnet-20240229, opus-20240229 for stronger models

    # Dynamically build example strings from the loaded JSON
    problematic_examples = [ex["message"] for ex in examples if ex["type"] == "problematic"]
    healthy_examples = [ex["message"] for ex in examples if ex["type"] == "unproblematic"]

    problematic_examples_str = ", ".join([f'"{msg}"' for msg in problematic_examples]) if problematic_examples else "N/A"
    healthy_examples_str = ", ".join([f'"{msg}"' for msg in healthy_examples]) if healthy_examples else "N/A"

    prompt_content = f"""
    You are an AI assistant specialized in analyzing software commit messages.
    Your task is to determine if a given commit message indicates "root rot" (problematic, unprofessional, vague, or quick-fix oriented) or is a "healthy commit" (clear, follows conventions like Conventional Commits, professional).
    If it's not clearly problematic but also not perfectly healthy, classify it as "Potentially Rotting (needs review)".

    Consider the following examples of problematic messages: {problematic_examples_str}.
    Consider the following examples of healthy messages: {healthy_examples_str}.

    Analyze the following commit message and provide a concise classification.
    Your response MUST be a JSON object with a single key "status" and its value being one of the following strings:
    "Root Rot Detected", "Healthy Commit", "Potentially Rotting (needs review)".

    Commit Message: "{commit_message}"
    """

    headers = {
        "x-api-key": claude_api_key,
        "anthropic-version": "2023-06-01",
        "Content-Type": "application/json"
    }

    payload = {
        "model": claude_model,
        "max_tokens": 100,
        "messages": [
            {"role": "user", "content": prompt_content}
        ],
        "temperature": 0.0
    }

    try:
        response = requests.post(claude_api_url, headers=headers, json=payload)
        response.raise_for_status()

        result = response.json()

        if result and result.get("content") and len(result["content"]) > 0 and \
           result["content"][0].get("type") == "text" and result["content"][0].get("text"):
            
            json_string = result["content"][0]["text"]
            parsed_json = json.loads(json_string)
            return parsed_json.get("status", "Unknown Status")
        else:
            print("Claude AI response structure unexpected or content missing.")
            print(f"Raw AI response: {response.text}")
            return "Unknown Status"
    except requests.exceptions.RequestException as e:
        print(f"Error calling Claude API: {e}")
        return "Error (API Call Failed)"
    except json.JSONDecodeError as e:
        print(f"Error parsing Claude response JSON: {e}")
        print(f"Raw AI response: {response.text}")
        return "Error (Invalid AI Response)"
    except Exception as e:
        print(f"An unexpected error occurred during AI analysis: {e}")
        return "Error (Unexpected)"
