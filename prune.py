import asyncio
import sys
import discord

# Prompt user for the Bot Token safely at runtime
BOT_TOKEN = input("Enter your Bot Token: ").strip()

if not BOT_TOKEN:
    print("No token provided. Exiting...")
    sys.exit(1)

# Enable required intents
intents = discord.Intents.default()
intents.guilds = True
intents.members = True

client = discord.Client(intents=intents)


@client.event
async def on_ready():
    print(f"\n[+] Logged in as: {client.user} (ID: {client.user.id})")
    print(f"[+] Total Servers Found: {len(client.guilds)}\n")

    # Ask user for confirmation
    choice = input("Wanna start prune & leave? (y/n): ").strip().lower()

    if choice != "y":
        print("Operation cancelled. Logging out...")
        await client.close()
        return

    print("\nStarting process...\n" + "=" * 40)

    # Make a copy of the list of guilds to safely iterate over
    guilds = list(client.guilds)

    for guild in guilds:
        print(f"\n[Processing Server]: {guild.name} (ID: {guild.id})")

        # Step 1: Fetch all roles in the server
        all_roles = guild.roles
        print(f" -> Selected {len(all_roles)} roles for pruning.")

        # Step 2: Perform the Prune operation
        try:
            # Setting roles=all_roles includes members with any of these roles
            # compute_prune_count=False speeds up the request
            pruned_count = await guild.prune_members(
                days=1,
                roles=all_roles,
                reason="Automated prune and leave action.",
            )
            print(
                f" -> Successfully pruned {pruned_count} members from '{guild.name}'."
            )
        except discord.Forbidden:
            print(
                f" [!] Missing Permissions: Cannot prune members in '{guild.name}' (Requires 'Kick Members' permission & proper role hierarchy)."
            )
        except discord.HTTPException as e:
            print(f" [!] Failed to prune in '{guild.name}': {e}")

        # Short pause between actions
        await asyncio.sleep(1.5)

        # Step 3: Leave the server
        try:
            await guild.leave()
            print(f" -> Successfully left server: '{guild.name}'")
        except discord.HTTPException as e:
            print(f" [!] Failed to leave server '{guild.name}': {e}")

        await asyncio.sleep(2)

    print("\n" + "=" * 40)
    print("[+] Finished pruning and leaving all servers.")
    await client.close()


# Start the bot
try:
    client.run(BOT_TOKEN)
except discord.LoginError:
    print("Invalid Bot Token provided.")
