import requests
import re
import asyncio
from tokens.github_token import GITHUB_TOKEN

headers = {
    'Authorization': GITHUB_TOKEN,
}


async def get_available_action_dirs() -> list:
    api_endpoint = f'https://api.github.com/repos/Thundermaker300/ScriptedEvents/contents/ScriptedEvents/Actions/'
    response = requests.get(
        api_endpoint,
        headers=headers
    )
    r: list = []

    if not response.status_code == 200:
        print(response.content)
        return r

    for x in response.json():
        if x['type'] == 'dir':
            r.append(x['name'])

    return r


async def get_available_actions(directory: str) -> list:
    api_endpoint = f'https://api.github.com/repos/Thundermaker300/ScriptedEvents/contents/ScriptedEvents/Actions/{directory}'
    response = requests.get(api_endpoint, headers=headers)
    r: list = []

    if not response.status_code == 200:
        return r

    for x in response.json():
        if x['type'] == 'file':
            r.append(x['name'])

    return r


async def get_action_shelp_info(file_path) -> list:
    url = f'https://raw.githubusercontent.com/Thundermaker300/ScriptedEvents/main/ScriptedEvents/Actions/{file_path}'
    response = requests.get(url, headers=headers)

    async def get_params() -> list:
        parameters: list = re.findall(r'new Argument\((.*?)\),\\r\\n', original_string)
        exit_list: list = []

        def format_param(param_str: str):
            exit_list = []
            extracted_param: str = ""
            current_param_formatting: int = 0

            for char in param_str:
                if current_param_formatting == 2:
                    break

                if char != ",":
                    extracted_param += char
                    continue

                if current_param_formatting == 0:
                    extracted_param = extracted_param.strip().strip("\"").strip("\'")

                elif current_param_formatting == 1:
                    extracted_param = extracted_param.strip().removeprefix("typeof(").removesuffix(")")

                extracted_param = extracted_param.strip()
                exit_list.append(extracted_param)
                extracted_param = ""
                current_param_formatting += 1

            for char in param_str[::-1]:
                if char != ",":
                    extracted_param += char
                    continue

                extracted_param = extracted_param[::-1].strip()
                exit_list.append(extracted_param)
                current_param_formatting -= 1
                break

            exit_list.append(
                param_str.split(exit_list[1])[1].split(exit_list[2])[0].removeprefix("), \"").removesuffix("\", ")
            )

            return exit_list

        for param in parameters:
            exit_list.append(format_param(param))

        return exit_list

    if response.status_code != 200:
        print(response.content)
        print("ERROR")
        return []

    original_string = str(response.content)

    try:
        params = await get_params()
    except:
        params = None

    try:
        description = re.findall(r'Description => (.*?);', original_string)[0].strip("\"").strip("\'")
    except:
        description = None

    try:
        name = re.findall(r'Name => (.*?);', original_string)[0].strip("\"").strip("\'")
    except:
        name = None
    return [name, description, params]


async def update():
    for dir_available in await get_available_action_dirs():
        for act in await get_available_actions(dir_available):
            info = await get_action_shelp_info(f"{dir_available}/{act}")
            if info[0] is None:
                continue

            with open("shelp_info.py", "a") as file:
                file.write(f"{info[0]}: list = {info}\n")

            print("DONE " + info[0])

    with open("shelp/shelp_info.py", "r") as file:
        text = file.read()
        text = text.replace("\\\\\\", "")
        text = text.replace("\\\\", "\\")

    with open("shelp/shelp_info.py", "w") as file:
        file.write(text)


if __name__ == "__main__":
    asyncio.run(update())
