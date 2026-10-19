import asyncio
import discord


def print_banner():
    print("=" * 40)
    print("      DISCORD SERVER CLONER (cloner.py)")
    print("=" * 40 + "\n")


async def clone_server(client, source_id, target_id):
    source_guild = client.get_guild(source_id)
    target_guild = client.get_guild(target_id)

    if source_guild is None:
        print("[!] Could not find the source server. Make sure the bot is in it.")
        return

    if target_guild is None:
        print("[!] Could not find the target server. Make sure the bot is in it.")
        return

    print(f"\n[+] Source Server: {source_guild.name}")
    print(f"[+] Target Server: {target_guild.name}")
    print("[*] Copying roles and channel structure. Existing content and messages are not copied.")

    # Roles: create lower-priority roles first. Discord's managed/default roles
    # cannot be recreated, and role positions may need manual adjustment.
    print("\n[->] Cloning roles...")
    for role in reversed(source_guild.roles):
        if role.is_default() or role.managed:
            continue
        try:
            await target_guild.create_role(
                name=role.name,
                permissions=role.permissions,
                colour=role.colour,
                hoist=role.hoist,
                mentionable=role.mentionable,
                reason="Copy role structure from an authorized source server",
            )
            print(f"  [+] Created role: {role.name}")
        except discord.HTTPException as exc:
            print(f"  [!] Failed to create role {role.name}: {exc}")

    # Categories
    print("\n[->] Cloning categories...")
    category_mapping = {}
    for category in source_guild.categories:
        try:
            new_category = await target_guild.create_category(
                name=category.name,
                reason="Copy channel structure from an authorized source server",
            )
            category_mapping[category.id] = new_category
            print(f"  [+] Created category: {category.name}")
        except discord.HTTPException as exc:
            print(f"  [!] Failed to create category {category.name}: {exc}")

    # Text channels
    print("\n[->] Cloning text channels...")
    for channel in source_guild.text_channels:
        try:
            parent = category_mapping.get(channel.category_id)
            await target_guild.create_text_channel(
                name=channel.name,
                topic=channel.topic,
                slowmode_delay=channel.slowmode_delay,
                nsfw=channel.nsfw,
                category=parent,
                reason="Copy channel structure from an authorized source server",
            )
            print(f"  [+] Created text channel: #{channel.name}")
        except discord.HTTPException as exc:
            print(f"  [!] Failed to create text channel {channel.name}: {exc}")

    # Voice channels
    print("\n[->] Cloning voice channels...")
    for channel in source_guild.voice_channels:
        try:
            parent = category_mapping.get(channel.category_id)
            await target_guild.create_voice_channel(
                name=channel.name,
                bitrate=min(channel.bitrate, target_guild.bitrate_limit),
                user_limit=channel.user_limit,
                category=parent,
                reason="Copy channel structure from an authorized source server",
            )
            print(f"  [+] Created voice channel: {channel.name}")
        except discord.HTTPException as exc:
            print(f"  [!] Failed to create voice channel {channel.name}: {exc}")

    print("\n[+] Copy attempt finished. Check the messages above for any failures.")


async def run_cloner(token, source_id, target_id):
    intents = discord.Intents.default()
    intents.guilds = True
    client = discord.Client(intents=intents)

    @client.event
    async def on_ready():
        print(f"\n[+] Logged in as bot: {client.user}")
        try:
            await clone_server(client, source_id, target_id)
        finally:
            await client.close()

    await client.start(token)


def main():
    print_banner()
    print("Use a Discord bot token only. Self/user tokens are not supported.\n")

    token = input("Enter Bot Token: ").strip()
    if not token:
        print("[!] Missing bot token.")
        return

    try:
        source_id = int(input("Source Server ID: ").strip())
        target_id = int(input("Target Server ID: ").strip())
    except ValueError:
        print("[!] Server IDs must be numbers.")
        return

    try:
        asyncio.run(run_cloner(token, source_id, target_id))
    except discord.LoginFailure:
        print("[!] Login failed. Check the bot token.")
    except discord.HTTPException as exc:
        print(f"[!] Discord API error: {exc}")
    except KeyboardInterrupt:
        print("\n[!] Stopped by user.")
    except Exception as exc:
        print(f"[!] Error: {exc}")


if __name__ == "__main__":
    main()
