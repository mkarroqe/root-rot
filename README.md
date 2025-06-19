# root-rot
GHA that analyzes commit messages and predicts if their roots (underlying code) may be rotten (likely to cause an incident).

This is a Proof of Concept (POC) GitHub Action that attempts to predict if a commit message indicates "root rot" (problematic) or is a "healthy commit" (unproblematic) based on a small, example-based JSON database. It uses Anthropic's Claude to evaluate the contents of the commit message, and flags it as **problematic** if it detects trends that could reflect rushed fixes.

## How it Works

1. **Trigger:** The action runs on `push` events to the `main` branch.

2. **Get Commit Message:** It fetches the message of the latest commit that triggered the push.

3. **AI Prediction:**: A Python script, `predict_commit.py` makes an API call to the Claude AI model (specifically claude-3-haiku-20240307), sending the commit message along with a prompt and example classifications. The AI then determines the "Root Rot Status" based on its understanding.

4. **Output:** It prints the AI's prediction ("Root Rot Detected", "Healthy Commit", or "Potentially Rotting (needs review)"). If a message is flagged as "Root Rot Detected" or an API error occurs (including missing API key), the GitHub Action will fail, providing a clear indication in your workflow run.

## Setup Instructions
To use this GitHub Action in your repository:

- Obtain a `CLAUDE_API_KEY` generated from Anthropic Console.
- Run locally:
  - set your `CLAUDE_API_KEY` env variable in your terminal
  - run `python3 predict_commit.py "sample commit message"`
- Run in repo:
  - Fork code and add `predict_commit.yml` to your `.github/workflows` directory
  - Make sure to add your Claude API Key to GitHub Secrets:
    - In your GitHub repository, go to Settings > Secrets and variables > Actions.
    - Click `New repository secret` and add a new secret named CLAUDE_API_KEY.
   
 ## Example Output
 | Prediction | Output |
 | ---------- | ------ |
 | `Healthy Commit` | ![image](https://github.com/user-attachments/assets/7704ee76-ae76-4c2d-b485-5900784f5743) |
 | `Potentially Rotting` | ![image](https://github.com/user-attachments/assets/b8fed743-3e45-4d58-8191-d0ea92fc4272) |
 | `Root Rot Detected` | ![image](https://github.com/user-attachments/assets/305a3230-0add-4acc-9ecf-d5a205047532) |
