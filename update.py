import requests
import re

M3U_FILE = "slv.m3u"
TOKEN_SOURCE = "https://sonyliv.joker-verse.workers.dev/master.m3u8?id=sony-hd&uid=1045595420&pass=169ae613"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36",
    "Origin": "https://www.sonyliv.com",
    "Referer": "https://www.sonyliv.com/"
}

def fetch_new_token():
    """Get the latest token from API response (last URL)"""
    resp = requests.get(TOKEN_SOURCE, headers=HEADERS, timeout=10)
    resp.raise_for_status()
    text = resp.text.strip()
    # Assuming token is in URL as hdntl=...
    matches = re.findall(r"(hdntl=[^ \n&]+)", text)
    if matches:
        return matches[-1]
    else:
        raise ValueError("⚠️ Token not found in API response!")

def clean_base_url(url):
    """
    Remove old token and any master_*.m3u8 suffix to avoid double append
    """
    # Remove hdntl=... and everything after it
    url = re.sub(r"hdntl=[^&/]+.*", "", url)
    return url.rstrip("/") + "/"  # ensure single trailing /

def update_m3u_file(file_path, new_token):
    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    updated_lines = []
    for line in lines:
        if line.strip().startswith("http"):
            base = clean_base_url(line.strip())
            new_line = f"{base}{new_token}\n"
            updated_lines.append(new_line)
        else:
            updated_lines.append(line)

    # overwrite same file
    with open(file_path, "w", encoding="utf-8") as f:
        f.writelines(updated_lines)

    print(f"✅ Playlist updated → {file_path}")

if __name__ == "__main__":
    token = fetch_new_token()
    print("🎯 New token fetched:", token[:100], "...")
    update_m3u_file(M3U_FILE, token)
