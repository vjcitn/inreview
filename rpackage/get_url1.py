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
    # Exclude pull requests (they also show up as issues in the API)
    return [issue for issue in all_issues if 'pull_request' not in issue]

def get_first_comment_url(issue, headers):
    if issue["comments"] == 0:
        return None
    comments_resp = requests.get(issue["comments_url"], headers=headers)
    comments_resp.raise_for_status()
    comments = comments_resp.json()
    if not comments:
        return None
    first_comment_body = comments[0].get("body", "")
    print(first_comment_body)
#    match = re.search(r".*Repos.*https?://[^\s]+", first_comment_body)
    match = re.search(r"Repository:\s*(https?://[^\s]+)", text, re.IGNORECASE)
    return match.group(0) if match else None

def main():
    if len(sys.argv) != 2:
        print("Usage: python get_first_comment_url.py <owner/repo>")
        sys.exit(1)
    owner, repo = sys.argv[1].split('/')
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}
    issues = get_issues(owner, repo)
    for issue in issues:
        url = get_first_comment_url(issue, headers)
        print(f"Issue #{issue['number']}: {url if url else 'No URL found in first comment'}")

if __name__ == "__main__":
    main()

