import requests
import re
import asyncio
import os
from git import Repo

def get_file_names(git_repo_url, folder_path):
    repo = Repo.clone_from(git_repo_url, "temp_repo")

    # Przechodzenie przez folder i zbieranie nazw plików
    file_names = []
    for root, dirs, files in os.walk(os.path.join("temp_repo", folder_path)):
        for file in files:
            file_names.append(os.path.join(root, file))

    return tuple(file_names)

# Przykładowe użycie






async def download_file_from_github(file_path):
    raw_url = f'https://raw.githubusercontent.com/Thundermaker300/ScriptedEvents/main/ScriptedEvents/{file_path}'
    response = requests.get(raw_url)

    if response.status_code != 200:
        return

    original_string = str(response.content)

    parameters = re.findall(r'new Argument\((.*?)\),\\r\\n', original_string)

    for match in parameters:
        print(match)

    description = re.findall(r'Description => (.*?);', original_string)[0]
    name = re.findall(r'Name => (.*?);', original_string)[0]
    print(f"{description = }"
          f"{name = }")




file_path = 'Actions/Broadcast/BroadcastAction.cs'
file_path = "Actions/Health/AdvSetAHPAction.cs"

file_names_tuple = get_file_names(
    'https://github.com/Thundermaker300/ScriptedEvents',
    'ScriptedEvents/ScriptedEvents/Actions/Broadcast/HintPlayerAction.cs')
print(file_names_tuple)

asyncio.run(download_file_from_github(file_path))
