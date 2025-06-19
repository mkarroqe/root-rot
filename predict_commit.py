# predict_commit.py
import json
import sys

def load_examples(file_path="commit_examples.json"):
    """Loads the commit message examples from a JSON file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: Database file '{file_path}' not found.")
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"Error: Could not parse JSON from '{file_path}'. Check its format.")
        sys.exit(1)

def predict_commit_quality(commit_message, examples):
    """
    Predicts if a commit message is problematic based on keywords from examples.
    This is a simple POC using basic keyword matching.
    """
    lower_message = commit_message.lower()

    # Define keywords for problematic and unproblematic based on your examples
    problematic_keywords = set()
    unproblematic_keywords = set()

    for example in examples:
        msg = example.get("message", "").lower()
        msg_type = example.get("type")

        # For a simple POC, let's extract words from example messages
        # and categorize them. This is very basic and would be improved
        # with actual NLP techniques or more sophisticated rules.
        words = set(word.strip(".,!?;:\"'").lower() for word in msg.split() if len(word) > 2)

        if msg_type == "problematic":
            problematic_keywords.update(words)
        elif msg_type == "unproblematic":
            unproblematic_keywords.update(words)

    # Check for problematic keywords in the commit message
    for keyword in problematic_keywords:
        if keyword in lower_message:
            return "Problematic"

    # For this POC, if no problematic keywords are found, we'll lean towards unproblematic.
    # In a real scenario, you'd have more robust rules/models.
    # You could also check for "unproblematic" keywords if you have strict conventions.
    for keyword in unproblematic_keywords:
        if keyword in lower_message:
            # If it contains unproblematic keywords, and no problematic ones were caught
            return "Unproblematic"

    # Default if no clear match (you might refine this)
    if "fix" in lower_message or "update" in lower_message:
         return "Potentially Problematic (needs review)" # Catches general short messages
    
    return "Unproblematic" # Assume unproblematic if no specific problematic signs

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python predict_commit.py \"Your commit message here\"")
        sys.exit(1)

    # The commit message is passed as the first argument
    commit_message = sys.argv[1]

    print(f"Analyzing commit message: \"{commit_message}\"")

    # Load the database
    db_examples = load_examples()

    # Predict quality
    prediction = predict_commit_quality(commit_message, db_examples)

    print(f"Prediction: {prediction}")

    # You could add logic here to fail the workflow if problematic
    if prediction == "Problematic":
        print("::error ::This commit message has been flagged as problematic. Please review.")
        sys.exit(1) # Fail the action
    elif prediction == "Potentially Problematic (needs review)":
        print("::warning ::This commit message is potentially problematic. Consider revising.")
        # Do not exit(1) for warnings, allow the workflow to continue
