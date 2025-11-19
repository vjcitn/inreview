import os
import re
import sys
import requests

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

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

def get_first_url_issue_and_comments(issue, headers):
    # Check for a URL in the issue body
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

def main():
    if len(sys.argv) != 2:
        print("Usage: python get_first_url_issue_and_comments.py <owner/repo>")
        sys.exit(1)
    owner, repo = sys.argv[1].split('/')
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}
    issues = get_issues(owner, repo)
    for issue in issues:
        url, source = get_first_url_issue_and_comments(issue, headers)
        which = source if source else "not found"
        print(f"Issue #{issue['number']}: {url if url else 'No URL found'} ({which})")

if __name__ == "__main__":
    main()

