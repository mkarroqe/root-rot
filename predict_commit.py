import json
import sys
import asyncio
import os
from claude_service import analyze_commit_with_claude # Import the AI analysis function

# This is a comment.
def load_examples(file_path="commit_examples.json"):
    """Loads the commit message examples from a JSON file.
    This function is kept for structural consistency and if you later decide
    to use these examples for more than just AI prompt context.
    """
    try:
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        else:
            print(f"Warning: Database file '{file_path}' not found. Proceeding without examples.")
            return []
    except json.JSONDecodeError:
        print(f"Error: Could not parse JSON from '{file_path}'. Check its format. Proceeding without examples.")
        return []


async def main():
    if len(sys.argv) < 2:
        print("Usage: python predict_commit.py \"Your commit message here\"")
        sys.exit(1)

    commit_message = sys.argv[1]
    print(f"🌱⏳ Analyzing commit message for root rot: \"{commit_message}\"")

    # Examples are loaded but primarily for context in the AI prompt defined in claude_service.py
    db_examples = load_examples()

    prediction = await analyze_commit_with_claude(commit_message, db_examples)

    print(f"Root Rot Status: {prediction}")

    # GitHub Actions specific output
    if prediction == "Root Rot Detected":
        print("🪵💩 This commit message indicates potential root rot. Please review and revise.")
        sys.exit(1) # Fail the action
    elif prediction == "Potentially Rotting (needs review)":
        print("🪵🐛 This commit message is potentially rotting. Consider revising for clarity.")
        # Do not exit(1) for warnings, allow the workflow to continue
    elif prediction.startswith("Error"):
        print(f"⚠️😣 Failed to analyze commit message due to an error: {prediction}")
        sys.exit(1) # Fail on API errors

if __name__ == "__main__":
    asyncio.run(main())
