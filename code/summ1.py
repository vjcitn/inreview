#!/usr/bin/env python3

# produced by perplexity
# note uses gpt-4 and analyses open issues at repo specified in argument
# thus tailored for https://github.com/bioconductor/contributions

import os
import sys
import requests
import base64
import openai

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

def get_repo_file(owner, repo, path):
    url = f"https://api.github.com/repos/{owner}/{repo}/contents/{path}"
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}
    r = requests.get(url, headers=headers)
    if r.status_code == 200:
        data = r.json()
        if data.get('encoding') == 'base64':
            return base64.b64decode(data['content']).decode("utf-8", errors="replace")
        elif 'content' in data:
            return data['content']
    return ""

def get_repo_metadata(owner, repo):
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}
    repo_url = f"https://api.github.com/repos/{owner}/{repo}"
    repo_resp = requests.get(repo_url, headers=headers)
    repo_resp.raise_for_status()
    repo_data = repo_resp.json()
    readme = get_repo_file(owner, repo, "README.md")
    if not readme:
        readme = get_repo_file(owner, repo, "README")
    description = get_repo_file(owner, repo, "DESCRIPTION")
    return repo_data, readme, description

def summarize_purpose_with_openai(repo_data, readme, description):
    client = openai.OpenAI(api_key=OPENAI_API_KEY)
    prompt = (
        "Summarize the primary purpose and intended use of the following GitHub repository. "
        "Base your answer on the provided metadata, README, and DESCRIPTION file (if present). "
        "Write a concise and insightful paragraph for a technical audience.\n\n"
        f"Name: {repo_data.get('full_name')}\n"
        f"Description field: {repo_data.get('description')}\n"
        "DESCRIPTION file:\n"
        f"{description[:2000]}\n\n"
        "README:\n"
        f"{readme[:4000]}\n"
    )
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.4,
        max_tokens=350
    )
    return response.choices[0].message.content

def main():
    if len(sys.argv) != 2:
        print("Usage: python summarize_repo_purpose_plus_desc.py <owner/repo>")
        sys.exit(1)
    owner, repo = sys.argv[1].split("/")
    repo_data, readme, description = get_repo_metadata(owner, repo)
    summary = summarize_purpose_with_openai(repo_data, readme, description)
    print(f"\nRepository: {owner}/{repo}\n")
    print(summary)

if __name__ == "__main__":
    main()

