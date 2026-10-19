import requests


def main():
    print("=" * 40)
    print("          VANITY URL TOOL")
    print("=" * 40)
    print("Use a Discord BOT token only. Do not enter your personal account token.")
    print("The bot must have the required permissions, and the server must support vanity URLs.\n")

    token = input("Enter Bot Token: ").strip()
    guild_id = input("Enter Target Server ID: ").strip()
    vanity_code = input("Enter Vanity URL Code to set: ").strip()

    if not token or not guild_id or not vanity_code:
        print("[!] Missing required inputs.")
        return

    url = f"https://discord.com/api/v10/guilds/{guild_id}/vanity-url"
    headers = {
        "Authorization": f"Bot {token}",
        "Content-Type": "application/json",
        "User-Agent": "VanityURLTool/1.0",
    }

    try:
        response = requests.patch(
            url,
            json={"code": vanity_code},
            headers=headers,
            timeout=15,
        )

        if response.status_code in (200, 201):
            print(f"[+] Request succeeded: https://discord.gg/{vanity_code}")
            print(response.text)
        elif response.status_code == 429:
            try:
                retry_after = response.json().get("retry_after", "unknown")
            except ValueError:
                retry_after = "unknown"
            print(f"[!] Discord rate-limited the request. Retry after: {retry_after} seconds.")
        else:
            print(f"[-] Request failed: HTTP {response.status_code}")
            print(response.text)

    except requests.RequestException as exc:
        print(f"[!] Network error: {exc}")


if __name__ == "__main__":
    main()
