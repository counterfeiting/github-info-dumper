import requests

def get_user_id(username):
    url = f"https://api.github.com/users/{username}"
    response = requests.get(url)
    data = response.json()
    return data

def get_commit_history(user, order):
    commits = []
    page = 1
    while True:
        url = f"https://api.github.com/search/commits?q=author:{user}&per_page=100&sort=author-date&order={order}&page={page}"
        response = requests.get(url)
        data = response.json()
        if isinstance(data, dict) and 'items' in data and not data['items']:
            break
        if isinstance(data, dict) and 'items' in data:
            commits.extend(data['items'])
        else:
            break
        page += 1
    return commits

def extract_user_info(commits, user_id):
    user_info = set()
    commit_count = 0
    repos = set()
    for commit_data in commits:
        commit_count += 1
        repos.add(commit_data['repository']['full_name'])
        commit_detail = commit_data.get('commit', {})
        author_data = commit_data.get('author', {})
        committer_data = commit_data.get('committer', {})
        author = commit_detail.get('author', {})
        committer = commit_detail.get('committer', {})

        if author and author_data and author_data.get('id') == user_id:
            user_info.add((author.get('name'), author.get('email')))
        if committer and committer_data and committer_data.get('id') == user_id:
            user_info.add((committer.get('name'), committer.get('email')))
    return user_info, commit_count, len(repos)

def display_profile_visual(user_data, user_details, commit_count, repo_count):
    print("=" * 50)
    print(f"GitHub Profile for {user_data['login']}")
    print("=" * 50)
    print(f"Name: {user_data.get('name', 'N/A')}")
    print(f"Bio: {user_data.get('bio', 'N/A')}")
    print(f"Location: {user_data.get('location', 'N/A')}")
    print(f"Company: {user_data.get('company', 'N/A')}")
    print(f"Public Repos: {user_data['public_repos']}")
    print(f"Public Gists: {user_data['public_gists']}")
    print(f"Followers: {user_data['followers']}")
    print(f"Following: {user_data['following']}")
    print("-" * 50)
    print("Commit History Summary:")
    print(f"Total Commits Found: {commit_count}")
    print(f"Repositories Involved: {repo_count}")
    print("-" * 50)
    print("User Details Extracted from Commits:")
    for name, email in user_details:
        print(f"  Name: {name}, Email: {email}")
    print("=" * 50)

if __name__ == "__main__":
    username = 'GITHUB_USERNAME'
    user_data = get_user_id(username)
    if user_data and 'login' in user_data:
        commit_data_asc = get_commit_history(username, 'asc')
        commit_data_desc = get_commit_history(username, 'desc')
        all_commits = commit_data_asc + commit_data_desc
        user_details, commit_count, repo_count = extract_user_info(all_commits, user_data['id'])
        display_profile_visual(user_data, user_details, commit_count, repo_count)
    else:
        print(f"Could not retrieve user data for {username}")
