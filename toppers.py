import os
import sys
import subprocess

def clear():
    os.system("cls" if os.name == "nt" else "clear")

def banner():
    print("\033[96m" + "=" * 50)
    print("       DISCORD TOOL LAUNCHER (tools.py)      ")
    print("=" * 50 + "\033[0m")

def pause():
    input("\n\033[93mPress Enter to return to the menu...\033[0m")

def run_script(filename):
    clear()
    if os.path.exists(filename):
        print(f"[*] Launching {filename}...\n" + "-" * 40)
        try:
            subprocess.run([sys.executable, filename])
        except Exception as e:
            print(f"[!] Error running {filename}: {e}")
    else:
        print(f"[!] Error: '{filename}' not found in this folder!")
        print(f"[!] Make sure {filename} is saved in the same directory.")

def handle_dist_option():
    clear()
    banner()
    print(" \033[92m[2] Dist Selector\033[0m\n")
    print("1. Krish (Bot Token mode -> krish.py)")
    print("2. Self (User Token mode -> self.py)\n")
    
    choice = input("Select mode (1-2): ").strip()
    if choice == "1":
        run_script("krish.py")
    elif choice == "2":
        run_script("self.py")
    else:
        print("\n[!] Invalid choice.")

def main():
    while True:
        clear()
        banner()
        print("1. Webhook Sender (spam.py)")
        print("2. Dist (krish.py or self.py)")
        print("3. Prune & Leave (prune.py)")
        print("4. Vanity Exchanger (vanity.py)")
        print("5. Server Cloner (cloner.py)")
        print("6. Exit")
        print("=" * 50)

        choice = input("\nSelect an option (1-6): ").strip()

        if choice == "1":
            run_script("spam.py")
            pause()
        elif choice == "2":
            handle_dist_option()
            pause()
        elif choice == "3":
            run_script("prune.py")
            pause()
        elif choice == "4":
            run_script("vanity.py")
            pause()
        elif choice == "5":
            run_script("cloner.py")
            pause()
        elif choice == "6":
            print("\nExiting tools.py. Goodbye!")
            sys.exit(0)
        else:
            print("\n[!] Invalid choice. Choose between 1-6.")
            pause()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n[!] Terminated by user.")
      
