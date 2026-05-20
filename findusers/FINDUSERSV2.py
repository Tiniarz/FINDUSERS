import asyncio
import aiohttp
import sys
import os
import time
import re
import colorama
from colorama import Fore, Style

colorama.init()

DARK_RED = Fore.RED
LIGHT_GREEN = Fore.LIGHTGREEN_EX
BRIGHT_GREEN = Fore.GREEN + Style.BRIGHT
BRIGHT_RED = Fore.RED + Style.BRIGHT
RESET = Style.RESET_ALL

RAW_ASCII = [
    "███████╗██╗███╗   ██╗██████╗ ███████╗██████╗     ██╗   ██╗██████╗ ",
    "██╔════╝██║████╗  ██║██╔══██╗██╔════╝██╔══██╗    ██║   ██║╚════██╗",
    "█████╗  ██║██╔██╗ ██║██║  ██║█████╗  ██████╔╝    ██║   ██║ █████╔╝",
    "██╔══╝  ██║██║╚██╗██║██║  ██║██╔══╝  ██╔══██╗    ╚██╗ ██╔╝██╔═══╝ ",
    "██║     ██║██║ ╚████║██████╔╝███████╗██║  ██║     ╚████╔╝ ███████╗",
    "╚═╝     ╚═╝╚═╝  ╚═══╝╚═════╝ ╚══════╝╚═╝  ╚═╝      ╚═══╝  ╚══════╝"
]

ASCII_ART = "\n".join(f"{DARK_RED}{line}{RESET}" for line in RAW_ASCII)

PLATFORMS = {
    "GitHub": "https://github.com/{}",
    "Reddit": "https://www.reddit.com/user/{}",
    "X-Twitter": "https://x.com/{}",
    "Instagram": "https://www.instagram.com/{}",
    "TikTok": "https://www.tiktok.com/@{}",
    "YouTube": "https://www.youtube.com/@{}",
    "Twitch": "https://www.twitch.fxtv/{}",
    "Pinterest": "https://www.pinterest.com/{}",
    "Steam": "https://steamcommunity.com/id/{}",
    "Vimeo": "https://vimeo.com/{}",
    "SoundCloud": "https://soundcloud.com/{}",
    "Medium": "https://medium.com/@{}",
    "DeviantArt": "https://www.deviantart.com/{}",
    "About.me": "https://about.me/{}",
    "Imgur": "https://imgur.com/user/{}",
    "Flipboard": "https://flipboard.com/@{}",
    "Spotify": "https://open.spotify.com/user/{}",
    "Slack": "https://{}.slack.com",
    "Snapchat": "https://www.snapchat.com/add/{}",
    "Letterboxd": "https://letterboxd.com/{}",
    "Disqus": "https://disqus.com/by/{}",
    "Behance": "https://www.behance.net/{}",
    "Codepen": "https://codepen.io/{}",
    "Dribbble": "https://dribbble.com/{}",
    "Patreon": "https://www.patreon.com/{}",
    "DockerHub": "https://hub.docker.com/u/{}",
    "Basecamp": "https://{}.basecamphq.com",
    "DailyMotion": "https://www.dailymotion.com/{}",
    "Etsy": "https://www.etsy.com/people/{}",
    "Goodreads": "https://www.goodreads.com/{}",
    "Instructables": "https://www.instructables.com/member/{}",
    "Keybase": "https://keybase.io/{}",
    "Kickstarter": "https://www.kickstarter.com/profile/{}",
    "Last.fm": "https://www.last.fm/user/{}",
    "Linktree": "https://linktr.ee/{}",
    "SlideShare": "https://www.slideshare.net/{}",
    "Scribd": "https://www.scribd.com/{}",
    "Tumblr": "https://{}.tumblr.com",
    "WordPress": "https://{}.wordpress.com",
    "LiveJournal": "https://{}.livejournal.com",
    "Gfycat": "https://gfycat.com/@{}",
    "Giphy": "https://giphy.com/{}",
    "Bandcamp": "https://bandcamp.com/{}",
    "ReverbNation": "https://www.reverbnation.com/{}",
    "Wattpad": "https://www.wattpad.com/user/{}",
    "Crunchyroll": "https://www.crunchyroll.com/user/{}",
    "ProductHunt": "https://www.producthunt.com/@{}",
    "Itch.io": "https://{}.itch.io",
    "Kaggle": "https://www.kaggle.com/{}",
    "AskFM": "https://ask.fm/{}",
    "SmugMug": "https://{}.smugmug.com",
    "Trackmania": "https://player.trackmania.com/player/{}",
    "Mixcloud": "https://www.mixcloud.com/{}",
    "Freesound": "https://freesound.org/people/{}/",
    "Vero": "https://vero.co/{}",
    "Wikipedia": "https://en.wikipedia.org/wiki/User:{}",
    "Wix": "https://{}.wixsite.com",
    "Blogger": "https://{}.blogspot.com",
    "Chess.com": "https://www.chess.com/member/{}",
    "Duolingo": "https://www.duolingo.com/profile/{}",
    "Codecademy": "https://www.codecademy.com/profiles/{}",
    "Pastebin": "https://pastebin.com/u/{}",
    "Bitbucket": "https://bitbucket.org/{}/",
    "GitLab": "https://gitlab.com/{}",
    "HackerNews": "https://news.ycombinator.com/user?id={}",
    "Lobsters": "https://lobste.rs/u/{}",
    "Quora": "https://www.quora.com/profile/{}",
    "StackOverflow": "https://stackoverflow.com/users/{}",
    "Roblox": "https://www.roblox.com/user.aspx?username={}",
    "FortniteTracker": "https://fortnitetracker.com/profile/all/{}",
    "ApexTracker": "https://apex.tracker.gg/apex/profile/psn/{}/overview",
    "Trakt": "https://trakt.tv/users/{}",
    "Letterboxd_Alt": "https://letterboxd.com/{}/",
    "Newgrounds": "https://{}.newgrounds.com",
    "Speedrun.com": "https://www.speedrun.com/user/{}",
    "AllMyLinks": "https://allmylinks.com/{}",
    "BuyMeACoffee": "https://www.buymeacoffee.com/{}",
    "Substack": "https://{}.substack.com",
    "Gumroad": "https://{}.gumroad.com",
    "Ko-fi": "https://ko-fi.com/{}",
    "Triller": "https://triller.co/@{}",
    "Periscope": "https://www.pscp.tv/{}",
    "Mix": "https://mix.com/{}",
    "Houzz": "https://www.houzz.com/user/{}",
    "TripAdvisor": "https://www.tripadvisor.com/Profile/{}",
    "Foursquare": "https://foursquare.com/user/{}",
    "Airtable": "https://airtable.com/@{}",
    "AngelList": "https://wellfound.com/u/{}",
    "Fiverr": "https://www.fiverr.com/{}",
    "Upwork": "https://www.upwork.com/freelancers/~{}",
    "Freelancer": "https://www.freelancer.com/u/{}",
    "Behance_Alt": "https://www.behance.net/{}/",
    "Contently": "https://{}.contently.com",
    "Hashnode": "https://{}.hashnode.dev",
    "Dev.to": "https://dev.to/{}",
    "Hackerrank": "https://www.hackerrank.com/{}",
    "LeetCode": "https://leetcode.com/u/{}",
    "CodeChef": "https://www.codechef.com/users/{}",
    "TopCoder": "https://www.topcoder.com/members/{}",
    "GeeksForGeeks": "https://auth.geeksforgeeks.org/user/{}/profile",
    "VulnerabilityLab": "https://www.vulnerability-lab.com/show.php?user={}",
    "ExploitDB": "https://www.exploit-db.com/author/{}",
    "PacketStorm": "https://packetstormsecurity.com/files/author/{}/",
    "Bugcrowd": "https://bugcrowd.com/{}",
    "HackerOne": "https://hackerone.com/{}",
    "RootMe": "https://www.root-me.org/{}",
    "HackTheBox": "https://www.hackthebox.eu/home/users/profile/{}",
    "TryHackMe": "https://tryhackme.com/p/{}",
    "CTFtime": "https://ctftime.org/user/{}",
    "OpenBugBounty": "https://www.openbugbounty.org/bugbounty/{}/",
    "Crowdin": "https://crowdin.com/profile/{}",
    "Blip.tv": "https://blip.tv/{}",
    "Clubhouse": "https://www.clubhouse.com/@{}",
    "EyeEm": "https://www.eyeem.com/u/{}",
    "Flickr": "https://www.flickr.com/photos/{}",
    "Fotolog": "https://fotolog.com/{}",
    "Photobucket": "https://photobucket.com/user/{}/library",
    "Shutterstock": "https://www.shutterstock.com/g/{}",
    "500px": "https://500px.com/p/{}",
    "VSCO": "https://vsco.co/{}",
    "Unsplash": "https://unsplash.com/@{}",
    "Pixabay": "https://pixabay.com/users/{}",
    "Pexels": "https://www.pexels.com/@{}",
    "Gfycat_Alt": "https://gfycat.com/user/{}",
    "Streamable": "https://streamable.com/{}",
    "Vimeo_Alt": "https://vimeo.com/channels/{}",
    "Twitch_Alt": "https://www.twitch.tv/{}",
    "Dlive": "https://dlive.tv/{}",
    "Rumble": "https://rumble.com/user/{}",
    "Odysee": "https://odysee.com/@{}",
    "Bitchute": "https://www.bitchute.com/channel/{}/",
    "PeerTube": "https://peertube.cpy.re/u/{}",
    "Mixcloud_Alt": "https://www.mixcloud.com/{}/listeners/",
    "HearThisAt": "https://hearthis.at/{}/",
    "Audiomack": "https://audiomack.com/{}",
    "ReverbNation_Alt": "https://www.reverbnation.com/page/search?q={}",
    "Bandcamp_Alt": "https://bandcamp.com/search?q={}",
    "SoundCloud_Alt": "https://soundcloud.com/search/users?q={}",
    "UltimateGuitar": "https://ultimate-guitar.com/u/{}",
    "Genius": "https://genius.com/{}",
    "Discogs": "https://www.discogs.com/user/{}",
    "MusicBrainz": "https://musicbrainz.org/user/{}",
    "Lastfm_Alt": "https://www.last.fm/user/{}/library",
    "RateYourMusic": "https://rateyourmusic.com/~{}",
    "Sputnikmusic": "https://www.sputnikmusic.com/user/{}",
    "MyAnimeList": "https://myanimelist.net/profile/{}",
    "AnimeNewsNetwork": "https://www.animenewsnetwork.com/bbs/phpBB2/profile.php?mode=viewprofile&u={}",
    "AniList": "https://anilist.co/user/{}",
    "Kitsu": "https://kitsu.io/users/{}",
    "OtakuBootcamp": "https://otakubootcamp.com/user/{}",
    "VNDB": "https://vndb.org/u/{}",
    "Goodreads_Alt": "https://www.goodreads.com/user/show/{}",
    "LibraryThing": "https://www.librarything.com/profile/{}",
    "BookCrossing": "https://www.bookcrossing.com/mybookshelf/{}/",
    "Wattpad_Alt": "https://www.wattpad.com/user/{}",
    "ArchiveOfOurOwn": "https://archiveofourown.org/users/{}",
    "FanFiction": "https://www.fanfiction.net/u/{}",
    "FictionPress": "https://www.fictionpress.com/u/{}",
    "DeviantArt_Alt": "https://www.deviantart.com/{}/gallery",
    "ArtStation": "https://www.artstation.com/{}",
    "Pixiv": "https://www.pixiv.net/users/{}",
    "FurAffinity": "https://www.furaffinity.net/user/{}",
    "Inkbunny": "https://inkbunny.net/{}",
    "Weasyl": "https://www.weasyl.com/~{}",
    "Derpibooru": "https://derpibooru.org/profiles/{}",
    "E621": "https://e621.net/users/{}",
    "Newgrounds_Alt": "https://{}.newgrounds.com/audio",
    "GameJolt": "https://gamejolt.com/@{}",
    "Itchio_Alt": "https://itch.io/profile/{}",
    "ModDB": "https://www.moddb.com/members/{}",
    "NexusMods": "https://www.nexusmods.com/users/{}",
    "GameFront": "https://www.gamefront.com/members/{}",
    "CurseForge": "https://www.curseforge.com/members/{}/projects",
    "PlanetMinecraft": "https://www.planetminecraft.com/member/{}",
    "MinecraftForum": "https://www.minecraftforum.net/members/{}",
    "Roblox_Alt": "https://www.roblox.com/users/{}/profile",
    "Steam_Alt": "https://steamcommunity.com/search/users/#text={}",
    "XboxGamertag": "https://account.xbox.com/en-us/profile?gamertag={}",
    "PlayStationNetwork": "https://psnprofiles.com/{}",
    "NintendoLife": "https://www.nintendolife.com/users/{}",
    "SegaNerds": "https://www.seganerds.com/members/{}",
    "PCGamer": "https://www.pcgamer.com/members/{}",
    "IGN": "https://www.ign.com/users/{}",
    "GameSpot": "https://www.gamespot.com/profile/{}/",
    "GiantBomb": "https://www.giantbomb.com/profile/{}/",
    "Metacritic": "https://www.metacritic.com/user/{}",
    "Reddit_Alt": "https://old.reddit.com/user/{}",
    "Quora_Alt": "https://quora.com/profile/{}",
    "StackExchange": "https://stackexchange.com/users/{}",
    "ServerFault": "https://serverfault.com/users/{}",
    "SuperUser": "https://superuser.com/users/{}",
    "AskUbuntu": "https://askubuntu.com/users/{}",
    "MathOverflow": "https://mathoverflow.net/users/{}",
    "YahooAnswers": "https://answers.yahoo.com/activity/questions?show={}",
    "Answers.com": "https://www.answers.com/u/{}",
    "WikiHow": "https://www.wikihow.com/User:{}",
    "Instructables_Alt": "https://www.instructables.com/member/{}/about/",
    "Wikipedia_Alt": "https://en.wikipedia.org/wiki/Special:Contributions/{}",
    "WikimediaCommons": "https://commons.wikimedia.org/wiki/User:{}",
    "Wikidata": "https://www.wikidata.org/wiki/User:{}",
    "Wiktionary": "https://en.wiktionary.org/wiki/User:{}",
    "Wikibooks": "https://en.wikibooks.org/wiki/User:{}",
    "Wikiquote": "https://en.wikiquote.org/wiki/User:{}",
    "Wikisource": "https://en.wikisource.org/wiki/User:{}",
    "Wikivoyage": "https://en.wikivoyage.org/wiki/User:{}",
    "Wikinews": "https://en.wikinews.org/wiki/User:{}",
    "MediaWiki": "https://www.mediawiki.org/wiki/User:{}",
    "OpenStreetMap": "https://www.openstreetmap.org/user/{}",
    "SourceForge": "https://sourceforge.net/u/{}/profile",
    "Launchpad": "https://launchpad.net/~{}",
    "Gitee": "https://gitee.com/{}",
    "Bitbucket_Alt": "https://bitbucket.org/{}",
    "PornHub": "https://www.pornhub.com/users/{}",
    "TikTok": "https://www.tiktok.com/@{}"
}

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9"
}

async def check_platform(semaphore, session, platform_name, url_template, username):
    async with semaphore:
        url = url_template.format(username)
        try:
            async with session.get(url, headers=HEADERS, timeout=12, allow_redirects=True) as response:
                if response.status == 200:
                    print(f"{BRIGHT_GREEN}[+] {LIGHT_GREEN}{platform_name}: {url}{RESET}")
                    return platform_name, url, True
                else:
                    print(f"{BRIGHT_RED}[x] {BRIGHT_RED}{platform_name}{RESET}")
                    return platform_name, url, False
        except (aiohttp.ClientError, asyncio.TimeoutError):
            print(f"{BRIGHT_RED}[!] Error: {BRIGHT_RED}{platform_name} connection dropped/timeout.{RESET}")
            return platform_name, url, False
        except Exception as e:
            print(f"{BRIGHT_RED}[!] Error: {BRIGHT_RED}{platform_name} generic failure: {str(e)}{RESET}")
            return platform_name, url, False

def clear_terminal():
    if sys.platform == 'win32':
        os.system('cls')
    else:
        os.system('clear')

def print_slow(text):
    for line in text.splitlines():
        print(line)
        time.sleep(0.05)

def extract_meta_tags(html):
    profile_data = {
        "Display Name": "Unknown / Not Set",
        "Biography": "No custom biography or status statement discovered.",
        "Followers/Subscribers": "Hidden / Not Extracted",
        "Account Status": "Active / Visible Alignment"
    }
    
    title_match = re.search(r"<title>(.*?)</title>", html, re.IGNORECASE)
    if title_match:
        raw_title = title_match.group(1).strip()
        if raw_title:
            profile_data["Display Name"] = raw_title

    og_desc = re.search(r'<meta[^>]*property=["\']og:description["\'][^>]*content=["\'](.*?)["\']', html, re.IGNORECASE)
    if not og_desc:
        og_desc = re.search(r'<meta[^>]*name=["\']description["\'][^>]*content=["\'](.*?)["\']', html, re.IGNORECASE)
    
    if og_desc:
        desc_content = og_desc.group(1).strip()
        if desc_content:
            profile_data["Biography"] = desc_content
            
            followers = re.search(r'(\d+[\d,.\s]*[kKmM]?)\s*(Followers|Subscribers|Fans|Friends)', desc_content, re.IGNORECASE)
            if followers:
                profile_data["Followers/Subscribers"] = f"{followers.group(1)} ({followers.group(2)})"

    verify_indicators = ["verified", "badge", "check-mark", "vip", "official-user"]
    for indicator in verify_indicators:
        if indicator in html.lower():
            profile_data["Account Status"] = "Active (Potential Verification Vector / Established Profile Presence)"
            break

    return profile_data

async def dump_platform_info(platform_name, url_template, username):
    url = url_template.format(username)
    clear_terminal()
    print_slow(f"{BRIGHT_GREEN}========================================")
    print_slow(f" INFORMATION OF USERNAME")
    print_slow(f" USERNAME: {username}")
    print_slow(f" SELECTED PLATFORM: {platform_name.upper()}")
    print_slow(f"========================================{RESET}\n")
    print_slow(f"[*] Grabbing information about user........")
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=HEADERS, timeout=15, allow_redirects=True) as response:
                if response.status != 200:
                    print_slow(f"{BRIGHT_RED}[!] Extraction engine returned anomalous status code: {response.status}{RESET}")
                    return
                
                html_payload = await response.text(errors='ignore')
                user_metrics = extract_meta_tags(html_payload)
                
                print_slow(f"\n[+] Extracting structured network database definitions:")
                print_slow(f"    -> Profile Handle ID : @{username}")
                print_slow(f"    -> Native View Title : {user_metrics['Display Name']}")
                print_slow(f"    -> Identified Audits : {user_metrics['Followers/Subscribers']}")
                print_slow(f"    -> Verified Badges   : {user_metrics['Account Status']}")
                print_slow(f"    -> Base Resource URL : {url}")
                
                print_slow(f"\n[+] Extracted User Biography Context:")
                print_slow(f"    \"\"\"")
                for bio_line in user_metrics["Biography"].split(". "):
                    if bio_line.strip():
                        print_slow(f"    {bio_line.strip()}")
                print_slow(f"    \"\"\"")
                print_slow(f"\n========================================================={RESET}")
                
    except Exception as e:
        print_slow(f"{BRIGHT_RED}[!] Error: Profile decoding engine context failure: {str(e)}{RESET}")

async def main():
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stdin.reconfigure(encoding='utf-8')
    
    print(ASCII_ART)
    print("")
    
    try:
        username = input(f"Enter target username:").strip()
        if not username:
            print(f"{BRIGHT_RED}[!] ERROR: Missing critical string expression input.{RESET}")
            while True:
                await asyncio.sleep(3600)

        print(f"\n\033[92mSearching for user across {len(PLATFORMS)} networks...\n\033[0m")
        
        semaphore = asyncio.Semaphore(20)
        
        async with aiohttp.ClientSession() as session:
            tasks = [
                check_platform(semaphore, session, name, template, username)
                for name, template in PLATFORMS.items()
            ]
            await asyncio.gather(*tasks)

        print(f"\n{BRIGHT_GREEN}[+] Finding has been successfully finished.{RESET}")
        choice = input(f"Do you want to check the users entire information? (y/n): ").strip().lower()
        
        if choice == 'y':
            target_platform = input(f"Enter the platform name to extract full metadata: ").strip()
            matched_key = None
            for key in PLATFORMS.keys():
                if key.lower() == target_platform.lower():
                    matched_key = key
                    break
            
            if matched_key:
                await dump_platform_info(matched_key, PLATFORMS[matched_key], username)
            else:
                print(f"{BRIGHT_RED}[!] Platform match criteria not found inside target lists.{RESET}")
        
    except Exception as general_error:
        print(f"\n{BRIGHT_RED}[!] Critical runtime anomaly: {str(general_error)}{RESET}")
    
    while True:
        await asyncio.sleep(3600)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        while True:
            time.sleep(3600)
    except Exception:
        while True:
            time.sleep(3600)