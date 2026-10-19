# Kri.sh Discord Bot - Fast Blue Edition
# Password Protected | Auto Rate-Limit Pause (2s) | ANSI Blue UI

import asyncio
import discord

# -----------------------------
# Color Tokens (Blue Theme)
# -----------------------------
BLUE = "\033[92m"
CYAN = "\033[96m"
WHITE = "\033[97m"
RESET = "\033[0m"
BOLD = "\033[1m"

# -----------------------------
# Global values
# -----------------------------
BOT = None
SERVER = None
SERVER_ID = None

# -----------------------------
# Mobile-friendly UI
# -----------------------------

def clear():
    print("\n" * 3)

def line():
    print(f"{BLUE}=========================================={RESET}")

def banner():
    print(f"""{BLUE}{BOLD}
██╗  ██╗██████╗ ██╗███████╗██╗  ██╗
██║ ██╔╝██╔══██╗██║██╔════╝██║  ██║
█████╔╝ ██████╔╝██║███████╗███████║
██╔═██╗ ██╔══██╗██║╚════██║██╔══██║
██║  ██╗██║  ██║██║███████║██║  ██║
╚═╝  ╚═╝╚═╝  ╚═╝╚═╝╚══════╝╚═╝  ╚═╝{RESET}""")

def title():
    clear()
    banner()
    line()
    print(f"       {CYAN}DISCORD BOT - MOBILE (TURBO BLUE){RESET}")
    line()

    if SERVER:
        print(f"{BLUE}Server :{RESET} {WHITE}{SERVER.name}{RESET}")
        print(f"{BLUE}ID     :{RESET} {WHITE}{SERVER.id}{RESET}")

    print()

def pause():
    input(f"\n{CYAN}Press Enter to continue...{RESET}")

def ask(text):
    return input(f"{CYAN}Kri.sh > {text}: {RESET}").strip()

def number(text, minimum=1, maximum=None):
    while True:
        value = ask(text)
        try:
            value = int(value)
        except ValueError:
            print(f"{BLUE}[!] Enter a valid number.{RESET}")
            continue

        if value < minimum:
            print(f"{BLUE}[!] Number is too small.{RESET}")
            continue

        if maximum is not None and value > maximum:
            print(f"{BLUE}[!] Number is too large.{RESET}")
            continue

        return value

def confirm(text):
    answer = input(f"{BLUE}{text} Type YES: {RESET}").strip()
    return answer == "YES"

# -----------------------------
# Discord permissions
# -----------------------------

def me():
    if SERVER is None:
        return None
    return SERVER.me

def permission(name):
    member = me()
    if member is None:
        return False
    return getattr(member.guild_permissions, name, False)

def can_manage_member(member):
    myself = me()
    if myself is None:
        return False
    if member == myself or member == SERVER.owner:
        return False
    return member.top_role < myself.top_role

def can_manage_role(role):
    myself = me()
    if myself is None or role.is_default():
        return False
    return role < myself.top_role

# -----------------------------
# Fast Concurrent Handlers
# -----------------------------

async def fast_ban(member):
    while True:
        try:
            await SERVER.ban(member, reason="Kri.sh moderation")
            print(f"{BLUE}[BAN]{RESET} {WHITE}{member.name} ({member.id}){RESET}")
            return 1
        except discord.Forbidden:
            print(f"{BLUE}[!] Cannot ban {member.name}{RESET}")
            return 0
        except discord.HTTPException as error:
            if error.status == 429:
                print(f"{CYAN}[!] Rate limit hit on ban! Pausing 2s...{RESET}")
                await asyncio.sleep(2)
                continue
            print(f"{BLUE}[!] Discord error: {error}{RESET}")
            return 0

async def fast_delete_channel(channel):
    while True:
        try:
            name = channel.name
            await channel.delete(reason="Kri.sh delete channel")
            print(f"{BLUE}[DELETE]{RESET} {WHITE}{name}{RESET}")
            return 1
        except discord.Forbidden:
            print(f"{BLUE}[!] Cannot delete: {channel.name}{RESET}")
            return 0
        except discord.HTTPException as error:
            if error.status == 429:
                print(f"{CYAN}[!] Rate limit hit on channel delete! Pausing 2s...{RESET}")
                await asyncio.sleep(2)
                continue
            print(f"{BLUE}[!] Discord error: {error}{RESET}")
            return 0

async def fast_create_channel(name, index, amount):
    channel_name = name if amount == 1 else f"{name}-{index + 1}"
    while True:
        try:
            channel = await SERVER.create_text_channel(
                channel_name,
                reason="Kri.sh channel management"
            )
            print(f"{CYAN}[CREATE]{RESET} {WHITE}#{channel.name}{RESET}")
            return 1
        except discord.Forbidden:
            print(f"{BLUE}[!] Cannot create channel.{RESET}")
            return 0
        except discord.HTTPException as error:
            if error.status == 429:
                print(f"{CYAN}[!] Rate limit hit on channel create! Pausing 2s...{RESET}")
                await asyncio.sleep(2)
                continue
            print(f"{BLUE}[!] Discord error: {error}{RESET}")
            return 0

async def fast_create_role(name, index, amount):
    role_name = name if amount == 1 else f"{name} {index + 1}"
    while True:
        try:
            role = await SERVER.create_role(
                name=role_name,
                reason="Kri.sh role management"
            )
            print(f"{CYAN}[CREATE]{RESET} {WHITE}{role.name}{RESET}")
            return 1
        except discord.Forbidden:
            print(f"{BLUE}[!] Cannot create role.{RESET}")
            return 0
        except discord.HTTPException as error:
            if error.status == 429:
                print(f"{CYAN}[!] Rate limit hit on role create! Pausing 2s...{RESET}")
                await asyncio.sleep(2)
                continue
            print(f"{BLUE}[!] Discord error: {error}{RESET}")
            return 0

async def fast_delete_role(role):
    while True:
        try:
            name = role.name
            await role.delete(reason="Kri.sh role management")
            print(f"{BLUE}[DELETE]{RESET} {WHITE}{name}{RESET}")
            return 1
        except discord.Forbidden:
            print(f"{BLUE}[!] Cannot delete {role.name}{RESET}")
            return 0
        except discord.HTTPException as error:
            if error.status == 429:
                print(f"{CYAN}[!] Rate limit hit on role delete! Pausing 2s...{RESET}")
                await asyncio.sleep(2)
                continue
            print(f"{BLUE}[!] Discord error: {error}{RESET}")
            return 0

async def fast_send_ping(channel, message):
    while True:
        try:
            await channel.send(
                "@everyone | " + message,
                allowed_mentions=discord.AllowedMentions(everyone=True)
            )
            print(f"{CYAN}[PING]{RESET} #{channel.name} -> @everyone")
            return 1
        except discord.Forbidden:
            print(f"{BLUE}[!] Cannot send in #{channel.name}{RESET}")
            return 0
        except discord.HTTPException as error:
            if error.status == 429:
                print(f"{CYAN}[!] Rate limit hit on ping! Pausing 2s...{RESET}")
                await asyncio.sleep(2)
                continue
            print(f"{BLUE}[!] Discord error in #{channel.name}: {error}{RESET}")
            return 0

# -----------------------------
# Discord Operations
# -----------------------------

async def prune_members():
    if not permission("kick_members"):
        print(f"{BLUE}[!] Bot needs Kick Members permission.{RESET}")
        return

    days = number("Inactive for how many days (1-30)", 1, 30)

    if not confirm(f"REAL prune on {SERVER.name} for {days} days?"):
        print(f"{BLUE}[!] Cancelled.{RESET}")
        return

    print(f"{CYAN}[*] Executing prune operation...{RESET}")
    while True:
        try:
            result = await SERVER.prune_members(days=days, reason="Kri.sh prune")
            print(f"{CYAN}[+]{RESET} Discord reported {WHITE}{result}{RESET} member(s) pruned.")
            break
        except discord.Forbidden:
            print(f"{BLUE}[!] Discord denied the prune permission.{RESET}")
            break
        except discord.HTTPException as error:
            if error.status == 429:
                print(f"{CYAN}[!] Rate limit hit on prune! Pausing 2s...{RESET}")
                await asyncio.sleep(2)
                continue
            print(f"{BLUE}[!] Discord prune error: {error}{RESET}")
            break

async def ban_members():
    if not permission("ban_members"):
        print(f"{BLUE}[!] Bot needs Ban Members permission.{RESET}")
        return

    amount = number("How many members to ban", 1)

    print(f"{CYAN}[*] Fetching member list from Discord API...{RESET}")
    fetched_members = []
    try:
        async for member in SERVER.fetch_members(limit=None):
            fetched_members.append(member)
    except Exception:
        fetched_members = list(SERVER.members)

    targets = [m for m in fetched_members if not m.bot and can_manage_member(m)][:amount]

    if not targets:
        print(f"{BLUE}[!] No bannable members found (check bot hierarchy or intents).{RESET}")
        return

    if not confirm(f"REAL ban {len(targets)} members concurrently?"):
        print(f"{BLUE}[!] Cancelled.{RESET}")
        return

    print(f"{CYAN}[*] Executing fast concurrent bans...{RESET}")
    tasks = [fast_ban(member) for member in targets]
    results = await asyncio.gather(*tasks)

    print(f"{CYAN}[+]{RESET} Banned: {sum(results)} | Failed/Skipped: {len(targets) - sum(results)}")

async def delete_channel():
    if not permission("manage_channels"):
        print(f"{BLUE}[!] Bot needs Manage Channels permission.{RESET}")
        return

    channels = list(SERVER.channels)

    if not channels:
        print(f"{BLUE}[!] No channels found.{RESET}")
        return

    if not confirm(f"REAL delete ALL {len(channels)} channels/categories concurrently?"):
        print(f"{BLUE}[!] Cancelled.{RESET}")
        return

    print(f"{CYAN}[*] Executing fast channel deletion...{RESET}")
    tasks = [fast_delete_channel(ch) for ch in channels]
    results = await asyncio.gather(*tasks)

    print(f"\n{CYAN}[+]{RESET} Deleted {sum(results)} channel(s)/category(ies).")

async def create_channel():
    if not permission("manage_channels"):
        print(f"{BLUE}[!] Bot needs Manage Channels permission.{RESET}")
        return

    amount = number("How many channels", 1)
    name = ask("Channel name") or "channel"

    if not confirm(f"Create {amount} channel(s) concurrently?"):
        print(f"{BLUE}[!] Cancelled.{RESET}")
        return

    print(f"{CYAN}[*] Creating channels concurrently...{RESET}")
    tasks = [fast_create_channel(name, i, amount) for i in range(amount)]
    results = await asyncio.gather(*tasks)

    print(f"{CYAN}[+]{RESET} Created {sum(results)} channel(s).")

async def create_role():
    if not permission("manage_roles"):
        print(f"{BLUE}[!] Bot needs Manage Roles permission.{RESET}")
        return

    amount = number("How many roles", 1)
    name = ask("Role name") or "Role"

    if not confirm(f"Create {amount} role(s) concurrently?"):
        print(f"{BLUE}[!] Cancelled.{RESET}")
        return

    print(f"{CYAN}[*] Creating roles concurrently...{RESET}")
    tasks = [fast_create_role(name, i, amount) for i in range(amount)]
    results = await asyncio.gather(*tasks)

    print(f"{CYAN}[+]{RESET} Created {sum(results)} role(s).")

async def delete_role():
    if not permission("manage_roles"):
        print(f"{BLUE}[!] Bot needs Manage Roles permission.{RESET}")
        return

    roles = [role for role in SERVER.roles if can_manage_role(role)]

    if not roles:
        print(f"{BLUE}[!] No manageable roles.{RESET}")
        return

    amount = number("How many roles to delete", 1, len(roles))

    if not confirm(f"REAL delete {amount} role(s) concurrently?"):
        print(f"{BLUE}[!] Cancelled.{RESET}")
        return

    targets = roles[:amount]
    print(f"{CYAN}[*] Deleting roles concurrently...{RESET}")
    tasks = [fast_delete_role(role) for role in targets]
    results = await asyncio.gather(*tasks)

    print(f"{CYAN}[+]{RESET} Deleted {sum(results)} role(s).")

async def mass_ping():
    if not permission("send_messages") or not permission("mention_everyone"):
        print(f"{BLUE}[!] Bot needs Send Messages and Mention Everyone permissions.{RESET}")
        return

    amount = number("Amount per channel", 1)
    message = ask("Message") or "hello"

    channels = [
        c for c in SERVER.text_channels
        if c.permissions_for(SERVER.me).view_channel and c.permissions_for(SERVER.me).send_messages
    ]

    if not channels:
        print(f"{BLUE}[!] No available text channels.{RESET}")
        return

    if not confirm(f"Send {amount} ping(s) in ALL {len(channels)} channel(s) concurrently?"):
        print(f"{BLUE}[!] Cancelled.{RESET}")
        return

    print(f"{CYAN}[*] Sending mass pings concurrently...{RESET}")
    tasks = []
    for channel in channels:
        for _ in range(amount):
            tasks.append(fast_send_ping(channel, message))

    results = await asyncio.gather(*tasks)
    print(f"\n{CYAN}[+]{RESET} Sent {sum(results)} message(s) across {len(channels)} channel(s).")

# -----------------------------
# Menu
# -----------------------------

async def menu():
    while True:
        title()

        print(f"{CYAN}1.{RESET} Prune Members")
        print(f"{CYAN}2.{RESET} Ban Members (Fast)")
        print(f"{CYAN}3.{RESET} Delete ALL Channels (Fast)")
        print(f"{CYAN}4.{RESET} Create Channel (Fast)")
        print(f"{CYAN}5.{RESET} Create Role (Fast)")
        print(f"{CYAN}6.{RESET} Delete Role (Fast)")
        print(f"{CYAN}7.{RESET} Mass Ping (Fast)")
        print(f"{CYAN}8.{RESET} Exit\n")

        choice = ask("Select an option")

        try:
            if choice == "1":
                await prune_members()
            elif choice == "2":
                await ban_members()
            elif choice == "3":
                await delete_channel()
            elif choice == "4":
                await create_channel()
            elif choice == "5":
                await create_role()
            elif choice == "6":
                await delete_role()
            elif choice == "7":
                await mass_ping()
            elif choice == "8":
                print(f"{CYAN}[+] Closing bot...{RESET}")
                return
            else:
                print(f"{BLUE}[!] Choose 1-8.{RESET}")

        except Exception as error:
            print(f"{BLUE}[!] Operation error: {error}{RESET}")

        pause()

# -----------------------------
# Main
# -----------------------------

async def main():
    global BOT, SERVER_ID, SERVER

    clear()
    banner()
    line()
    print(f"       {CYAN}DISCORD BOT - MOBILE (TURBO BLUE){RESET}")
    line()
    print()

    token = ask("Bot Token")

    if not token:
        print(f"{BLUE}[!] Bot token is required.{RESET}")
        return

    server_text = ask("Server ID")

    try:
        SERVER_ID = int(server_text)
    except ValueError:
        print(f"{BLUE}[!] Server ID must be a number.{RESET}")
        return

    password = ask("Password")

    if password != "KRI.SH":
        print(f"{BLUE}[!] Incorrect password. Access denied.{RESET}")
        return

    print(f"\n{CYAN}[*] Connecting to Discord API...{RESET}")

    intents = discord.Intents.default()
    intents.guilds = True
    intents.members = True
    intents.message_content = True

    BOT = discord.Client(intents=intents)

    ready_event = asyncio.Event()
    connection_error = None

    @BOT.event
    async def on_ready():
        global SERVER

        print(f"\n{CYAN}[+]{RESET} Logged in as {WHITE}{BOT.user}{RESET}")
        SERVER = BOT.get_guild(SERVER_ID)

        if SERVER is None:
            print(f"{BLUE}[!] Server not found. Check the Server ID and ensure the bot is in the server.{RESET}")
        else:
            print(f"{CYAN}[+]{RESET} Server: {WHITE}{SERVER.name}{RESET}")
            print(f"{CYAN}[+]{RESET} Members cached: {WHITE}{len(SERVER.members)}{RESET}")
            print(f"{CYAN}[+]{RESET} Bot is ready.")

        ready_event.set()

    async def run_discord():
        nonlocal connection_error
        try:
            await BOT.start(token)
        except discord.LoginFailure:
            connection_error = "Invalid Discord bot token."
        except discord.PrivilegedIntentsRequired:
            connection_error = "Enable Privileged Intents in the Discord Developer Portal."
        except discord.HTTPException as error:
            connection_error = f"Discord API error: {error}"
            if error.status == 429:
                print(f"{CYAN}[!] Rate limit detected on startup! Pausing 2s...{RESET}")
                await asyncio.sleep(2)
        except Exception as error:
            connection_error = str(error)
        finally:
            ready_event.set()

    discord_task = asyncio.create_task(run_discord())

    try:
        await asyncio.wait_for(ready_event.wait(), timeout=30)
    except asyncio.TimeoutError:
        print(f"{BLUE}[!] Discord connection timed out.{RESET}")
        if not BOT.is_closed():
            await BOT.close()
        discord_task.cancel()
        return

    if connection_error:
        print(f"{BLUE}[!] {connection_error}{RESET}")
        if not BOT.is_closed():
            await BOT.close()
        return

    if SERVER is None:
        if not BOT.is_closed():
            await BOT.close()
        return

    print(f"\n{CYAN}[+] Opening mobile menu...{RESET}")
    await menu()

    if not BOT.is_closed():
        await BOT.close()

    if not discord_task.done():
        discord_task.cancel()
        try:
            await discord_task
        except asyncio.CancelledError:
            pass

    print(f"{CYAN}Kri.sh closed.{RESET}")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print(f"\n{BLUE}[!] Stopped.{RESET}")
    except Exception as error:
        print(f"\n{BLUE}[!] Fatal error: {error}{RESET}")
