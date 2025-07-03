import os
import json
import subprocess
from pathlib import Path
import requests

class WikiGenerationError(Exception):
    """Custom exception for wiki generation errors."""
    pass

def run_command(cmd, check=True, cwd=None):
    """Executes a command and raises an error if it fails."""
    result = subprocess.run(cmd, capture_output=True, text=True, cwd=cwd)
    if check and result.returncode != 0:
        raise WikiGenerationError(f"Command failed: {' '.join(cmd)}\n{result.stderr}")
    return result

def get_repo_data(api_url, headers):
    """Fetches repository data from the GitHub API."""
    try:
        response = requests.get(api_url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        raise WikiGenerationError(f"Failed to fetch repository data: {e}")

def enable_wiki(api_url, headers):
    """Enables the wiki for the repository if it's disabled."""
    repo_data = get_repo_data(api_url, headers)
    if not repo_data.get('has_wiki'):
        print("Enabling wiki...")
        try:
            response = requests.patch(api_url, headers=headers, json={'has_wiki': True})
            response.raise_for_status()
        except requests.RequestException as e:
            raise WikiGenerationError(f"Failed to enable wiki: {e}")

def generate_wiki_content(wiki_dir, data_dir):
    """Generates the content for the wiki."""
    with open(data_dir / 'issues.json', 'r') as f:
        issues = json.load(f)
    with open(data_dir / 'milestones.json', 'r') as f:
        milestones = json.load(f)
    with open(data_dir / 'releases.json', 'r') as f:
        releases = json.load(f)

    # Home page
    with open(wiki_dir / 'Home.md', 'w') as f:
        f.write("# Welcome to the Eterea Eureka Service Wiki\n\n")
        f.write("This wiki contains detailed information about the project, including milestones, issues, and releases.\n\n")
        f.write("- [[Project Milestones]]\n")
        f.write("- [[Active Issues]]\n")
        f.write("- [[Closed Issues]]\n")
        f.write("- [[Releases]]\n")

    # Milestones page
    with open(wiki_dir / 'Project-Milestones.md', 'w') as f:
        f.write("# Project Milestones\n\n")
        for ms in milestones:
            f.write(f"## {ms['title']}\n")
            f.write(f"- **State:** {ms['state']}\n")
            if ms.get('due_on'):
                f.write(f"- **Due Date:** {ms['due_on']}\n")
            f.write(f"\n{ms.get('description', 'No description provided.')}\n\n")

    # Active Issues page
    with open(wiki_dir / 'Active-Issues.md', 'w') as f:
        f.write("# Active Issues\n\n")
        for issue in [i for i in issues if i['state'] == 'open']:
            f.write(f"## #{issue['number']}: {issue['title']}\n")
            f.write(f"- **Created:** {issue['created_at']}\n")
            if issue.get('milestone'):
                f.write(f"- **Milestone:** {issue['milestone']}\n")
            if issue.get('labels'):
                f.write(f"- **Labels:** {', '.join(issue['labels'])}\n")
            f.write(f"\n{issue.get('body', 'No description provided.')}\n\n")

    # Closed Issues page
    with open(wiki_dir / 'Closed-Issues.md', 'w') as f:
        f.write("# Closed Issues\n\n")
        for issue in [i for i in issues if i['state'] == 'closed']:
            f.write(f"## #{issue['number']}: {issue['title']}\n")
            f.write(f"- **Created:** {issue['created_at']}\n")
            f.write(f"- **Closed:** {issue['closed_at']}\n")
            if issue.get('milestone'):
                f.write(f"- **Milestone:** {issue['milestone']}\n")
            if issue.get('labels'):
                f.write(f"- **Labels:** {', '.join(issue['labels'])}\n")
            f.write(f"\n{issue.get('body', 'No description provided.')}\n\n")

    # Releases page
    with open(wiki_dir / 'Releases.md', 'w') as f:
        f.write("# Releases\n\n")
        for release in releases:
            f.write(f"## {release['name']} ({release['tag_name']})\n")
            f.write(f"- **Published:** {release['published_at']}\n")
            f.write(f"\n{release.get('body', 'No description provided.')}\n\n")

def main():
    """Main function to generate and publish the wiki."""
    token = os.environ.get('GITHUB_TOKEN')
    if not token:
        raise WikiGenerationError("GITHUB_TOKEN environment variable not set.")

    repo_slug = os.environ['GITHUB_REPOSITORY']
    api_url = f"https://api.github.com/repos/{repo_slug}"
    wiki_url = f"https://x-access-token:{token}@github.com/{repo_slug}.wiki.git"
    
    headers = {'Authorization': f'token {token}'}
    
    original_dir = Path.cwd()
    wiki_dir = original_dir / 'wiki_content'
    data_dir = original_dir / 'data'

    try:
        enable_wiki(api_url, headers)

        if wiki_dir.exists():
            run_command(['rm', '-rf', str(wiki_dir)])

        run_command(['git', 'clone', wiki_url, str(wiki_dir)])
        
        generate_wiki_content(wiki_dir, data_dir)

        run_command(['git', 'config', 'user.name', 'github-actions[bot]'], cwd=wiki_dir)
        run_command(['git', 'config', 'user.email', 'github-actions[bot]@users.noreply.github.com'], cwd=wiki_dir)
        
        run_command(['git', 'add', '.'], cwd=wiki_dir)
        
        status_result = run_command(['git', 'status', '--porcelain'], cwd=wiki_dir)
        if status_result.stdout:
            run_command(['git', 'commit', '-m', 'Update wiki documentation'], cwd=wiki_dir)
            run_command(['git', 'push'], cwd=wiki_dir)
            print("Wiki updated successfully.")
        else:
            print("No changes to the wiki.")

    except WikiGenerationError as e:
        print(f"Error: {e}")
    finally:
        if wiki_dir.exists():
            run_command(['rm', '-rf', str(wiki_dir)])

if __name__ == '__main__':
    main()