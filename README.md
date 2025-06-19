# root-rot
GHA that analyzes commit messages and predicts how rotten they are

# GitHub Action: Root Rot Commit Message Predictor (POC)

This is a Proof of Concept (POC) GitHub Action that attempts to predict if a commit message indicates "root rot" (problematic) or is a "healthy commit" (unproblematic) based on a small, example-based JSON database. It's a simple demonstration using keyword matching, implemented in Python.

## How it Works

1. **Trigger:** The action runs on `push` events to the `main` branch.

2. **Get Commit Message:** It fetches the message of the latest commit that triggered the push.

3. **Predict:** A Python script `predict_commit.py` loads examples from `commit_examples.json` and uses simple keyword matching to classify the commit message.

4. **Output:** It prints a prediction ("Root Rot Detected", "Healthy Commit", or "Potentially Rotting (needs review)"). If a message is flagged as "Root Rot Detected", the GitHub Action will fail, providing a clear indication in your workflow run.

## Setup Instructions

To use this GitHub Action in your repository:

