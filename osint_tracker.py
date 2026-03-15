"""
==============================================
  OSINT Username Tracker
  Author: Abdulhakeem Umar Toyin
  GitHub: github.com/feliue
  Description: An open-source intelligence tool
               that searches for a username across
               multiple platforms to map a target's
               digital footprint
==============================================
"""

import urllib.request
import urllib.error
import threading
import time
import sys
from datetime import datetime


# ── COLOUR CODES ──────────────────────────────────────────────────────────────
GREEN  = "\033[92m"
RED    = "\033[91m"
YELLOW = "\033[93m"
CYAN   = "\033[96m"
PURPLE = "\033[95m"
WHITE  = "\033[97m"
BOLD   = "\033[1m"
RESET  = "\033[0m"


# ── BANNER ────────────────────────────────────────────────────────────────────
def banner():
    print(f"""
{PURPLE}{BOLD}
   ██████╗ ███████╗██╗███╗   ██╗████████╗
  ██╔═══██╗██╔════╝██║████╗  ██║╚══██╔══╝
  ██║   ██║███████╗██║██╔██╗ ██║   ██║
  ██║   ██║╚════██║██║██║╚██╗██║   ██║
  ╚██████╔╝███████║██║██║ ╚████║   ██║
   ╚═════╝ ╚══════╝╚═╝╚═╝  ╚═══╝   ╚═╝
{RESET}
{CYAN}{BOLD}
  ████████╗██████╗  █████╗  ██████╗██╗  ██╗███████╗██████╗
  ╚══██╔══╝██╔══██╗██╔══██╗██╔════╝██║ ██╔╝██╔════╝██╔══██╗
     ██║   ██████╔╝███████║██║     █████╔╝ █████╗  ██████╔╝
     ██║   ██╔══██╗██╔══██║██║     ██╔═██╗ ██╔══╝  ██╔══██╗
     ██║   ██║  ██║██║  ██║╚██████╗██║  ██╗███████╗██║  ██║
     ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝
{RESET}
{WHITE}  Author : {GREEN}Abdulhakeem Umar Toyin{RESET}
{WHITE}  GitHub : {CYAN}github.com/feliue{RESET}
{WHITE}  Tool   : {YELLOW}OSINT Username Tracker v1.0{RESET}
  {'─'*60}
""")


# ── PLATFORM DATABASE ─────────────────────────────────────────────────────────
# Format: "Platform Name": ("URL with {} for username", "check type")
# check type: "status" = check HTTP status code
#             "text"   = check if certain text exists in page

PLATFORMS = {
    # Social Media
    "GitHub":        ("https://github.com/{}", "status"),
    "Twitter/X":     ("https://twitter.com/{}", "status"),
    "Instagram":     ("https://www.instagram.com/{}/", "status"),
    "TikTok":        ("https://www.tiktok.com/@{}", "status"),
    "Reddit":        ("https://www.reddit.com/user/{}", "status"),
    "Pinterest":     ("https://www.pinterest.com/{}/", "status"),
    "Tumblr":        ("https://{}.tumblr.com", "status"),
    "Flickr":        ("https://www.flickr.com/people/{}", "status"),

    # Professional
    "LinkedIn":      ("https://www.linkedin.com/in/{}", "status"),
    "Dev.to":        ("https://dev.to/{}", "status"),
    "Hashnode":      ("https://hashnode.com/@{}", "status"),
    "Medium":        ("https://medium.com/@{}", "status"),
    "Behance":       ("https://www.behance.net/{}", "status"),
    "Dribbble":      ("https://dribbble.com/{}", "status"),

    # Tech / Gaming
    "HackerNews":    ("https://news.ycombinator.com/user?id={}", "status"),
    "GitLab":        ("https://gitlab.com/{}", "status"),
    "Bitbucket":     ("https://bitbucket.org/{}", "status"),
    "Steam":         ("https://steamcommunity.com/id/{}", "status"),
    "Twitch":        ("https://www.twitch.tv/{}", "status"),
    "Keybase":       ("https://keybase.io/{}", "status"),
    "HackTheBox":    ("https://app.hackthebox.com/users/profile/{}", "status"),
    "TryHackMe":     ("https://tryhackme.com/p/{}", "status"),

    # Forums / Communities
    "Pastebin":      ("https://pastebin.com/u/{}", "status"),
    "Replit":        ("https://replit.com/@{}", "status"),
    "CodePen":       ("https://codepen.io/{}", "status"),
    "Quora":         ("https://www.quora.com/profile/{}", "status"),
    "Fiverr":        ("https://www.fiverr.com/{}", "status"),
    "Upwork":        ("https://www.upwork.com/freelancers/~{}", "status"),

    # Video / Creative
    "YouTube":       ("https://www.youtube.com/@{}", "status"),
    "Vimeo":         ("https://vimeo.com/{}", "status"),
    "SoundCloud":    ("https://soundcloud.com/{}", "status"),
    "Spotify":       ("https://open.spotify.com/user/{}", "status"),
    "Mixcloud":      ("https://www.mixcloud.com/{}/", "status"),
}


# ── RESULTS STORAGE ───────────────────────────────────────────────────────────
found_profiles  = []
not_found       = []
errors          = []
lock            = threading.Lock()
checked_count   = [0]


# ── CHECK A SINGLE PLATFORM ───────────────────────────────────────────────────
def check_platform(username, platform, url_template, check_type):
    """Check if username exists on a platform."""
    url = url_template.format(username)

    try:
        req = urllib.request.Request(
            url,
            headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                              'AppleWebKit/537.36 (KHTML, like Gecko) '
                              'Chrome/91.0.4472.124 Safari/537.36'
            }
        )
        response = urllib.request.urlopen(req, timeout=8)
        status   = response.getcode()

        if status == 200:
            with lock:
                found_profiles.append((platform, url))
                checked_count[0] += 1
                print(f"\r  {GREEN}[FOUND]{RESET}    {WHITE}{platform:<20}{RESET} {CYAN}{url}{RESET}")
        else:
            with lock:
                not_found.append(platform)
                checked_count[0] += 1

    except urllib.error.HTTPError as e:
        with lock:
            if e.code == 404:
                not_found.append(platform)
            else:
                errors.append((platform, f"HTTP {e.code}"))
            checked_count[0] += 1

    except Exception as e:
        with lock:
            errors.append((platform, "Timeout/Error"))
            checked_count[0] += 1


# ── PROGRESS DISPLAY ──────────────────────────────────────────────────────────
def show_progress(total):
    """Show scanning progress."""
    while checked_count[0] < total:
        pct  = checked_count[0] / total * 100
        done = int(30 * checked_count[0] / total)
        bar  = "█" * done + "░" * (30 - done)
        print(f"\r  {CYAN}[{bar}]{RESET} {pct:5.1f}% "
              f"({checked_count[0]}/{total}) "
              f"{GREEN}{len(found_profiles)} found{RESET}  ", end="", flush=True)
        time.sleep(0.2)


# ── PRINT RESULTS ─────────────────────────────────────────────────────────────
def print_results(username, start_time):
    duration = time.time() - start_time
    total    = len(found_profiles) + len(not_found) + len(errors)

    print(f"\n\n  {'─'*60}")
    print(f"\n  {BOLD}{WHITE}OSINT SCAN COMPLETE{RESET}")
    print(f"  {WHITE}Username  :{RESET} {CYAN}{username}{RESET}")
    print(f"  {WHITE}Scanned   :{RESET} {total} platforms")
    print(f"  {WHITE}Duration  :{RESET} {duration:.1f} seconds")
    print(f"  {WHITE}Timestamp :{RESET} {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    # Found profiles
    print(f"\n  {'─'*60}")
    if found_profiles:
        print(f"\n  {GREEN}{BOLD}✅ FOUND ON {len(found_profiles)} PLATFORM(S):{RESET}\n")
        for i, (platform, url) in enumerate(found_profiles, 1):
            print(f"  {GREEN}{i:>2}.{RESET} {WHITE}{platform:<20}{RESET} {CYAN}{url}{RESET}")
    else:
        print(f"\n  {YELLOW}No profiles found for '{username}'.{RESET}")

    # Digital footprint score
    total_platforms = len(PLATFORMS)
    footprint_score = len(found_profiles) / total_platforms * 100

    print(f"\n  {'─'*60}")
    print(f"\n  {YELLOW}{BOLD}DIGITAL FOOTPRINT ANALYSIS:{RESET}")
    print(f"  {WHITE}Exposure Score:{RESET} {CYAN}{footprint_score:.0f}%{RESET} "
          f"({len(found_profiles)}/{total_platforms} platforms)")

    if footprint_score == 0:
        print(f"  {GREEN}Very low digital footprint — hard to find online{RESET}")
    elif footprint_score <= 20:
        print(f"  {GREEN}Low digital footprint — limited online presence{RESET}")
    elif footprint_score <= 40:
        print(f"  {YELLOW}Moderate digital footprint — average online presence{RESET}")
    elif footprint_score <= 60:
        print(f"  {YELLOW}High digital footprint — easily searchable online{RESET}")
    else:
        print(f"  {RED}Very high digital footprint — highly visible online{RESET}")

    # Privacy tips
    print(f"\n  {'─'*60}")
    print(f"\n  {PURPLE}{BOLD}PRIVACY TIPS:{RESET}")
    print(f"  {WHITE}• Use different usernames on different platforms{RESET}")
    print(f"  {WHITE}• Review privacy settings on all accounts{RESET}")
    print(f"  {WHITE}• Remove accounts you no longer use{RESET}")
    print(f"  {WHITE}• Never use your real name as a username{RESET}")
    print(f"\n  {'─'*60}\n")


# ── SAVE RESULTS TO FILE ──────────────────────────────────────────────────────
def save_results(username):
    """Save found profiles to a text file."""
    if not found_profiles:
        return

    filename = f"{username}_osint_results.txt"
    try:
        with open(filename, 'w') as f:
            f.write(f"OSINT USERNAME TRACKER RESULTS\n")
            f.write(f"{'='*50}\n")
            f.write(f"Username  : {username}\n")
            f.write(f"Date      : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Found on  : {len(found_profiles)} platforms\n")
            f.write(f"{'='*50}\n\n")
            for platform, url in found_profiles:
                f.write(f"{platform:<20} {url}\n")
        print(f"  {GREEN}[+]{RESET} Results saved to {CYAN}{filename}{RESET}\n")
    except Exception as e:
        print(f"  {RED}Could not save results: {e}{RESET}\n")


# ── SINGLE USERNAME SCAN ──────────────────────────────────────────────────────
def scan_username(username):
    """Scan a username across all platforms."""
    global found_profiles, not_found, errors, checked_count
    found_profiles = []
    not_found      = []
    errors         = []
    checked_count  = [0]

    total      = len(PLATFORMS)
    start_time = time.time()

    print(f"\n  {GREEN}[*]{RESET} Scanning username: {CYAN}{BOLD}{username}{RESET}")
    print(f"  {GREEN}[*]{RESET} Checking {total} platforms...\n")
    print(f"  {'─'*60}\n")

    # Start progress display thread
    progress_thread = threading.Thread(
        target=show_progress,
        args=(total,),
        daemon=True
    )
    progress_thread.start()

    # Scan all platforms with threads
    threads = []
    for platform, (url_template, check_type) in PLATFORMS.items():
        t = threading.Thread(
            target=check_platform,
            args=(username, platform, url_template, check_type)
        )
        threads.append(t)
        t.start()
        # Small delay to avoid overwhelming servers
        time.sleep(0.05)

    # Wait for all threads
    for t in threads:
        t.join()

    # Print results
    print_results(username, start_time)

    # Ask to save
    save = input(f"  {CYAN}Save results to file? (y/n):{RESET} ").strip().lower()
    if save == 'y':
        save_results(username)


# ── COMPARE TWO USERNAMES ─────────────────────────────────────────────────────
def compare_usernames():
    """Compare two usernames and find common platforms."""
    print(f"\n  {CYAN}{'─'*60}{RESET}")
    print(f"  {BOLD}{WHITE}COMPARE TWO USERNAMES{RESET}")
    print(f"  {CYAN}{'─'*60}{RESET}\n")

    user1 = input(f"  {CYAN}Enter first username:{RESET} ").strip()
    user2 = input(f"  {CYAN}Enter second username:{RESET} ").strip()

    if not user1 or not user2:
        print(f"  {RED}Please enter both usernames.{RESET}")
        return

    # Scan both
    print(f"\n  {YELLOW}Scanning {user1}...{RESET}")
    global found_profiles, not_found, errors, checked_count
    found_profiles = []; not_found = []; errors = []; checked_count = [0]
    scan_username(user1)
    profiles1 = set(p[0] for p in found_profiles)

    print(f"\n  {YELLOW}Scanning {user2}...{RESET}")
    found_profiles = []; not_found = []; errors = []; checked_count = [0]
    scan_username(user2)
    profiles2 = set(p[0] for p in found_profiles)

    # Find common platforms
    common = profiles1 & profiles2
    only1  = profiles1 - profiles2
    only2  = profiles2 - profiles1

    print(f"\n  {'─'*60}")
    print(f"  {BOLD}{WHITE}COMPARISON RESULTS{RESET}\n")
    print(f"  {GREEN}Common platforms ({len(common)}):{RESET}")
    for p in common:
        print(f"    {GREEN}✓{RESET} {p}")

    print(f"\n  {CYAN}Only on {user1} ({len(only1)}):{RESET}")
    for p in only1:
        print(f"    {CYAN}•{RESET} {p}")

    print(f"\n  {YELLOW}Only on {user2} ({len(only2)}):{RESET}")
    for p in only2:
        print(f"    {YELLOW}•{RESET} {p}")
    print()


# ── EDUCATION MODE ────────────────────────────────────────────────────────────
def osint_education():
    print(f"""
  {YELLOW}{BOLD}📚 WHAT IS OSINT?{RESET}

  {WHITE}OSINT stands for {CYAN}Open Source Intelligence{WHITE}.
  It means collecting information from {GREEN}publicly available
  sources{WHITE} — no hacking required!{RESET}

  {YELLOW}{BOLD}What OSINT investigators look for:{RESET}
  {WHITE}• Social media profiles and posts
  • Email addresses and phone numbers
  • Physical location clues in photos
  • Job history and professional info
  • Username patterns across platforms
  • Domain registration details (WHOIS){RESET}

  {YELLOW}{BOLD}Legal OSINT uses:{RESET}
  {GREEN}✓{WHITE} Penetration testing (with permission)
  {GREEN}✓{WHITE} Background checks (with consent)
  {GREEN}✓{WHITE} Cybersecurity investigations
  {GREEN}✓{WHITE} Journalism and research
  {GREEN}✓{WHITE} Finding missing persons
  {GREEN}✓{WHITE} Bug bounty reconnaissance{RESET}

  {RED}{BOLD}Illegal OSINT uses:{RESET}
  {RED}✗{WHITE} Stalking or harassing individuals
  {RED}✗{WHITE} Identity theft
  {RED}✗{WHITE} Doxxing (publishing private info)
  {RED}✗{WHITE} Unauthorized surveillance{RESET}

  {YELLOW}{BOLD}Famous OSINT tools:{RESET}
  {CYAN}• Maltego    {WHITE}— visual link analysis
  {CYAN}• Shodan     {WHITE}— search engine for devices
  {CYAN}• theHarvester{WHITE}— email & domain recon
  {CYAN}• Sherlock   {WHITE}— username hunting (like this tool!)
  {CYAN}• Recon-ng   {WHITE}— full recon framework{RESET}

  {GREEN}{BOLD}Golden Rule:{RESET}
  {WHITE}Only investigate yourself or targets you have
  explicit written permission to investigate.{RESET}
""")


# ── MAIN MENU ─────────────────────────────────────────────────────────────────
def main():
    banner()

    while True:
        print(f"  {BOLD}{WHITE}MAIN MENU{RESET}")
        print(f"  {'─'*40}")
        print(f"  {WHITE}[1]{RESET} 🔍 Search a username")
        print(f"  {WHITE}[2]{RESET} ⚖️  Compare two usernames")
        print(f"  {WHITE}[3]{RESET} 📚 What is OSINT?")
        print(f"  {WHITE}[4]{RESET} ❌ Exit")
        print(f"  {'─'*40}")

        choice = input(f"\n  {CYAN}Choose option (1-4):{RESET} ").strip()

        if choice == '1':
            username = input(f"\n  {CYAN}Enter username to search:{RESET} ").strip()
            if username:
                scan_username(username)
            else:
                print(f"  {RED}No username entered.{RESET}\n")

        elif choice == '2':
            compare_usernames()

        elif choice == '3':
            osint_education()

        elif choice == '4':
            print(f"\n  {GREEN}Stay ethical! Only investigate with permission. 🛡{RESET}\n")
            break

        else:
            print(f"\n  {RED}Invalid option. Choose 1-4.{RESET}\n")


if __name__ == "__main__":
    main()
