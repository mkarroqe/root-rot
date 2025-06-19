# root-rot
GHA that analyzes commit messages and predicts how rotten they are

# GitHub Action: Root Rot Commit Message Predictor (POC)

This is a Proof of Concept (POC) GitHub Action that attempts to predict if a commit message indicates "root rot" (problematic) or is a "healthy commit" (unproblematic) based on a small, example-based JSON database. It's a simple demonstration using keyword matching, implemented in Python.

## How it Works

1. **Trigger:** The action runs on `push` events to the `main` branch.

2. **Get Commit Message:** It fetches the message of the latest commit that triggered the push.

3. **AI Prediction:**: A Python script predict_commit.py makes an API call to the Claude AI model (specifically claude-3-haiku-20240307), sending the commit message along with a prompt and example classifications. The AI then determines the "Root Rot Status" based on its understanding.

4. **Output:** It prints the AI's prediction ("Root Rot Detected", "Healthy Commit", or "Potentially Rotting (needs review)"). If a message is flagged as "Root Rot Detected" or an API error occurs (including missing API key), the GitHub Action will fail, providing a clear indication in your workflow run.

## Setup Instructions
To use this GitHub Action in your repository:

Obtain a Claude API Key:
You will need an API key from Anthropic. Visit the Anthropic Console to sign up and generate one.

Add Claude API Key to GitHub Secrets:
In your GitHub repository, go to Settings > Secrets and variables > Actions.
If necessary, create a new Environment.
Click New repository secret and add a new secret named CLAUDE_API_KEY with the API key you obtained from Anthropic as its value. This keeps your API key secure.

