from os import environ
from os.path import join
from typing import Dict

import requests
from dotenv import load_dotenv
from markdown import markdown
from mdx_gfm import GithubFlavoredMarkdownExtension

load_dotenv()

workspace = environ.get('GITHUB_WORKSPACE')
if not workspace:
    print('No workspace is set')
    exit(1)

envs: Dict[str, str] = {}
for key in ['from', 'to', 'cloud', 'user', 'token']:
    value = environ.get(f'INPUT_{key.upper()}')
    if not value:
        print(f'Missing value for {key}')
        exit(1)
    envs[key] = value

with open(join(workspace, envs['from'])) as f:
    md = f.read()

base_url = envs['cloud']
if '://' in base_url:  # It's a full URL
    # Remove trailing slash if present
    base_url = base_url.rstrip('/')
    url = f"{base_url}/wiki/rest/api/content/{envs['to']}"
else:  # It's a subdomain
    url = f"https://{base_url}.atlassian.net/wiki/rest/api/content/{envs['to']}"

response = requests.get(url, auth=(envs['user'], envs['token']))
response.raise_for_status()
current = response.json()

html = markdown(md, extensions=[GithubFlavoredMarkdownExtension()])
content = {
    'id': current['id'],
    'type': current['type'],
    'title': current['title'],
    'version': {'number': current['version']['number'] + 1},
    'body': {
        'storage': {
            'value': html,
            'representation': 'storage'
        }
    }
}

response = requests.put(url, json=content, auth=(envs['user'], envs['token']))
if not response.ok:
    print(f'Confluence rejected the update: {response.status_code} {response.reason}')
    print(response.text)
    exit(1)

updated = response.json()
links = updated.get('_links')
if not links:
    print('Update returned an unexpected payload:')
    print(response.text)
    exit(1)

link = links['base'] + links['webui']
print(f'Uploaded content successfully to page {link}')
