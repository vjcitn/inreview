#!/usr/bin/env python3

# produced by perplexity
# note uses gpt-4 and analyses open issues at repo specified in argument
# thus tailored for https://github.com/bioconductor/contributions

import os
import sys
import requests
import base64
import openai
import re

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


def get_issues(owner, repo):
    url = f"https://api.github.com/repos/{owner}/{repo}/issues"
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}
    params = {"state": "open", "per_page": 100, "page": 1}
    all_issues = []
    while True:
        resp = requests.get(url, headers=headers, params=params)
        resp.raise_for_status()
        batch = resp.json()
        if not batch:
            break
        all_issues.extend(batch)
        params["page"] += 1
    # Exclude pull requests
    return [issue for issue in all_issues if 'pull_request' not in issue]

def get_first_url_issue_and_comments(issue):
    # Check for a URL in the issue body
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}
    match = re.search(r"Repository:\s*https?://[^\s]+", issue.get("body", ""))
    if match:
        return match.group(0), 'issue body'
    # If none, check for a URL in the first comment (if any)
    if issue["comments"] > 0:
        comments_resp = requests.get(issue["comments_url"], headers=headers)
        comments_resp.raise_for_status()
        comments = comments_resp.json()
        if comments:
            match = re.search(r"Repository:\s*(https?://[^\s]+)git", text, re.IGNORECASE)
            if match:
                return match.group(0), 'first comment'
    return None, None


def get_open_issues(owner, repo):
    url = f"https://api.github.com/repos/{owner}/{repo}/issues"
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}
    params = {"state": "open", "per_page": 100, "page": 1}
    all_issues = []
    while True:
        resp = requests.get(url, headers=headers, params=params)
        resp.raise_for_status()
        batch = resp.json()
        if not batch:
            break
        all_issues.extend(batch)
        params["page"] += 1
    # Filter out PRs
    return [i for i in all_issues if 'pull_request' not in i]


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
        "Write a concise and insightful paragraph for an audience skilled in computational biology and genomics. "
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

#def main():
#    if len(sys.argv) != 2:
#        print("Usage: python summarize_repo_purpose_plus_desc.py <owner/repo>")
#        sys.exit(1)
#    owner, repo = sys.argv[1].split("/")
#    repo_data, readme, description = get_repo_metadata(owner, repo)
#    summary = summarize_purpose_with_openai(repo_data, readme, description)
#    print(f"\nRepository: {owner}/{repo}\n")
#    print(summary)
#
#if __name__ == "__main__":
#    main()

