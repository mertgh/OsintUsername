import requests
from bs4 import BeautifulSoup
import time
import json
import re
import concurrent.futures
import argparse
import webbrowser
import urllib.parse
from colorama import Fore, Style, init

# Colorama'yı başlat
init(autoreset=True)

class UsernameOSINT:
    def __init__(self, username):
        self.username = username
        self.results = {}
        self.full_names_found = []
        self.sites = [
            {
                "name": "Twitter",
                "url": f"https://twitter.com/{username}",
                "check_type": "status_code",
                "valid_status": 200
            },
            {
                "name": "Instagram",
                "url": f"https://www.instagram.com/{username}/",
                "check_type": "status_code",
                "valid_status": 200
            },
            {
                "name": "GitHub",
                "url": f"https://github.com/{username}",
                "check_type": "status_code",
                "valid_status": 200
            },
            {
                "name": "Reddit",
                "url": f"https://www.reddit.com/user/{username}",
                "check_type": "status_code",
                "valid_status": 200
            },
            {
                "name": "Medium",
                "url": f"https://medium.com/@{username}",
                "check_type": "status_code",
                "valid_status": 200
            },
            {
                "name": "Quora",
                "url": f"https://www.quora.com/profile/{username}",
                "check_type": "status_code",
                "valid_status": 200
            },
            {
                "name": "Stackoverflow",
                "url": f"https://stackoverflow.com/users/{username}",
                "check_type": "status_code",
                "valid_status": 200
            },
            {
                "name": "Steam",
                "url": f"https://steamcommunity.com/id/{username}",
                "check_type": "status_code",
                "valid_status": 200
            },
            {
                "name": "Facebook",
                "url": f"https://www.facebook.com/{username}",
                "check_type": "status_code",
                "valid_status": 200
            },
            {
                "name": "Pinterest",
                "url": f"https://www.pinterest.com/{username}/",
                "check_type": "status_code",
                "valid_status": 200
            },
            {
                "name": "TikTok",
                "url": f"https://www.tiktok.com/@{username}",
                "check_type": "status_code",
                "valid_status": 200
            },
            {
                "name": "Soundcloud",
                "url": f"https://soundcloud.com/{username}",
                "check_type": "status_code",
                "valid_status": 200
            },
            {
                "name": "Twitch",
                "url": f"https://www.twitch.tv/{username}",
                "check_type": "status_code",
                "valid_status": 200
            },
            {
                "name": "VKontakte",
                "url": f"https://vk.com/{username}",
                "check_type": "status_code",
                "valid_status": 200
            },
            {
                "name": "Imgur",
                "url": f"https://imgur.com/user/{username}",
                "check_type": "status_code",
                "valid_status": 200
            },
            {
                "name": "Pastebin",
                "url": f"https://pastebin.com/u/{username}",
                "check_type": "status_code",
                "valid_status": 200
            },
            {
                "name": "HackForums",
                "url": f"https://hackforums.net/member.php?action=profile&username={username}",
                "check_type": "status_code",
                "valid_status": 200
            },
            {
                "name": "Cracked.to",
                "url": f"https://cracked.to/user-{username}",
                "check_type": "status_code",
                "valid_status": 200
            },
            {
                "name": "RaidForums",
                "url": f"https://raidforums.com/User-{username}",
                "check_type": "status_code",
                "valid_status": 200
            },
            {
                "name": "LinuxForums",
                "url": f"https://www.linuxforums.org/forum/members/{username}.html",
                "check_type": "status_code",
                "valid_status": 200
            },
            {
                "name": "Codecademy",
                "url": f"https://www.codecademy.com/profiles/{username}",
                "check_type": "status_code",
                "valid_status": 200
            },
        ]
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

    def check_site(self, site):
        try:
            response = requests.get(site["url"], headers=self.headers, timeout=10)
            
            if site["check_type"] == "status_code" and response.status_code == site["valid_status"]:
                print(f"{Fore.GREEN}[+] {site['name']}: {site['url']}")
                
                # Profil bilgilerini çekmeye çalış
                soup = BeautifulSoup(response.text, 'html.parser')
                profile_info = self.extract_profile_info(site["name"], soup, response.text)
                
                return {
                    "name": site["name"],
                    "url": site["url"],
                    "exists": True,
                    "profile_info": profile_info
                }
            else:
                print(f"{Fore.RED}[-] {site['name']}: Kullanıcı bulunamadı")
                return {
                    "name": site["name"],
                    "url": site["url"],
                    "exists": False,
                    "profile_info": {}
                }
        except Exception as e:
            print(f"{Fore.YELLOW}[!] {site['name']}: Hata oluştu - {str(e)}")
            return {
                "name": site["name"],
                "url": site["url"],
                "exists": False,
                "error": str(e),
                "profile_info": {}
            }

    def extract_profile_info(self, site_name, soup, html_content):
        """Siteden profil bilgilerini çıkarır"""
        info = {}
        
        try:
            if site_name == "Twitter":
                # Twitter'da JSON veri arama (yeni Twitter arayüzü için)
                json_data_match = re.search(r'<script id="__NEXT_DATA__" type="application/json">(.*?)</script>', html_content)
                if json_data_match:
                    try:
                        json_data = json.loads(json_data_match.group(1))
                        user_data = json_data.get('props', {}).get('pageProps', {}).get('userInfo', {})
                        if user_data:
                            info["name"] = user_data.get('name', '')
                            info["bio"] = user_data.get('description', '')
                            info["location"] = user_data.get('location', '')
                            info["followers"] = user_data.get('followers_count', '')
                            info["following"] = user_data.get('friends_count', '')
                    except:
                        pass
                
                # Fallback: Eski yöntem
                if not info:
                    name_elem = soup.find("span", {"class": "ProfileHeaderCard-nameLink"})
                    if name_elem:
                        info["name"] = name_elem.text.strip()
                    
                    bio_elem = soup.find("p", {"class": "ProfileHeaderCard-bio"})
                    if bio_elem:
                        info["bio"] = bio_elem.text.strip()
                    
                    location_elem = soup.find("span", {"class": "ProfileHeaderCard-locationText"})
                    if location_elem:
                        info["location"] = location_elem.text.strip()
                
            elif site_name == "GitHub":
                name_elem = soup.find("span", {"itemprop": "name"})
                if name_elem:
                    info["name"] = name_elem.text.strip()
                
                bio_elem = soup.find("div", {"class": "p-note user-profile-bio"})
                if bio_elem:
                    info["bio"] = bio_elem.text.strip()
                
                location_elem = soup.find("span", {"class": "p-label"})
                if location_elem:
                    info["location"] = location_elem.text.strip()
                
                # Ekstra GitHub bilgileri
                email_elem = soup.find("li", {"itemprop": "email"})
                if email_elem:
                    info["email"] = email_elem.text.strip()
                
                company_elem = soup.find("li", {"itemprop": "worksFor"})
                if company_elem:
                    info["company"] = company_elem.text.strip()
                
                # Repository ve contribution sayısı
                repo_count = soup.find("span", {"class": "Counter"})
                if repo_count:
                    info["repositories"] = repo_count.text.strip()
            
            elif site_name == "Instagram":
                # Instagram'dan JSON veri çıkarma
                json_data_match = re.search(r'window\._sharedData = (.*?);</script>', html_content)
                if json_data_match:
                    try:
                        json_data = json.loads(json_data_match.group(1))
                        user_data = json_data.get('entry_data', {}).get('ProfilePage', [{}])[0].get('graphql', {}).get('user', {})
                        if user_data:
                            info["name"] = user_data.get('full_name', '')
                            info["bio"] = user_data.get('biography', '')
                            info["followers"] = user_data.get('edge_followed_by', {}).get('count', '')
                            info["following"] = user_data.get('edge_follow', {}).get('count', '')
                            info["is_private"] = user_data.get('is_private', False)
                            info["posts"] = user_data.get('edge_owner_to_timeline_media', {}).get('count', '')
                            info["website"] = user_data.get('external_url', '')
                    except:
                        pass
            
            elif site_name == "Reddit":
                # Kullanıcı kartı
                name_elem = soup.find("h1", {"class": "_3LM4tRaExed4x1wBfK1pmg"})
                if name_elem:
                    info["username"] = name_elem.text.strip()
                
                # Karma bilgisi
                karma_elems = soup.find_all("span", {"class": "_1hNyZSklmcC7R_IfCUcXmZ"})
                if len(karma_elems) >= 2:
                    info["post_karma"] = karma_elems[0].text.strip()
                    info["comment_karma"] = karma_elems[1].text.strip()
                
                # Hesap yaşı
                age_elem = soup.find("span", {"class": "_2-cm5C"})
                if age_elem:
                    info["account_age"] = age_elem.text.strip()
            
            elif site_name == "Stackoverflow":
                # İsim ve skor
                name_elem = soup.find("h1")
                if name_elem:
                    info["name"] = name_elem.text.strip()
                
                rep_elem = soup.find("div", {"class": "reputation"})
                if rep_elem:
                    info["reputation"] = rep_elem.text.strip()
                
                # Rozet ve başka bilgiler
                badges = soup.find_all("div", {"class": "badge"})
                if badges:
                    badge_count = {}
                    for badge in badges:
                        badge_type = badge.get("class", [""])[1]
                        badge_count_elem = badge.find("span", {"class": "badge-count"})
                        if badge_count_elem:
                            badge_count[badge_type] = badge_count_elem.text.strip()
                    info["badges"] = badge_count
            
            elif site_name == "Steam":
                # Kullanıcı adı
                name_elem = soup.find("span", {"class": "actual_persona_name"})
                if name_elem:
                    info["name"] = name_elem.text.strip()
                
                # Ülke bilgisi
                location_elem = soup.find("div", {"class": "header_real_name"}).find("img")
                if location_elem:
                    info["country"] = location_elem.get("alt", "")
                
                # Level
                level_elem = soup.find("span", {"class": "friendPlayerLevelNum"})
                if level_elem:
                    info["level"] = level_elem.text.strip()
                
                # Status
                status_elem = soup.find("div", {"class": "profile_in_game_header"})
                if status_elem:
                    info["status"] = status_elem.text.strip()
            
            elif site_name == "HackForums" or site_name == "Cracked.to" or site_name == "RaidForums" or site_name == "LinuxForums":
                # Genel forum sistemleri için ortak yaklaşım
                
                # Kullanıcı adı ve unvan
                username_elem = soup.find("span", {"class": "username"})
                if username_elem:
                    info["username"] = username_elem.text.strip()
                
                # Mesaj sayısı
                post_count_elem = soup.find("span", {"class": "postcount"})
                if post_count_elem:
                    info["posts"] = post_count_elem.text.strip()
                
                # Üyelik tarihi
                join_date_elem = soup.find("span", {"class": "joindate"})
                if join_date_elem:
                    info["join_date"] = join_date_elem.text.strip()
                
                # Gruplar ve rütbeler
                groups_elem = soup.find("span", {"class": "usergroup"})
                if groups_elem:
                    info["groups"] = groups_elem.text.strip()
                
                # Alternatif arama
                for elem in soup.find_all("dt"):
                    if "Posts:" in elem.text:
                        post_count = elem.find_next("dd")
                        if post_count:
                            info["posts"] = post_count.text.strip()
                    elif "Join Date:" in elem.text:
                        join_date = elem.find_next("dd")
                        if join_date:
                            info["join_date"] = join_date.text.strip()
                    elif "Reputation:" in elem.text:
                        reputation = elem.find_next("dd")
                        if reputation:
                            info["reputation"] = reputation.text.strip()
                
            # Diğer siteler için benzer şekilde profil bilgisi çıkarma eklenir
                
        except Exception as e:
            print(f"{Fore.YELLOW}[!] {site_name} profil bilgileri çıkarılırken hata: {str(e)}")
        
        return info

    def search(self):
        print(f"{Fore.BLUE}[*] '{self.username}' kullanıcı adı için arama yapılıyor...")
        
        # İş parçacıkları kullanarak eşzamanlı arama
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            results = list(executor.map(self.check_site, self.sites))
        
        # Sonuçları işle
        self.results = {result["name"]: result for result in results if result["exists"]}
        
        return self.results
    
    def search_for_similar_accounts(self):
        """İsim ve soyisim gibi bilgileri kullanarak ek hesapları arama"""
        if not self.results:
            print(f"{Fore.YELLOW}[!] Önce hesap aramalarını tamamlayın.")
            return
        
        full_names = self.extract_full_names()
        
        if not full_names:
            print(f"{Fore.YELLOW}[!] Tam isim bilgisi bulunamadı.")
            return
        
        print(f"\n{Fore.BLUE}[*] Bulunan isimler ile ek hesaplar aranıyor...")
        
        for name_entry in full_names:
            full_name = name_entry["name"]
            source = name_entry["source"]
            
            # İsmi boşluklarla ayır ve muhtemel kullanıcı adlarını oluştur
            name_parts = full_name.lower().split()
            possible_usernames = [
                ".".join(name_parts),
                "_".join(name_parts),
                "".join(name_parts)
            ]
            
            if len(name_parts) >= 2:
                # İlk harf + soyisim
                possible_usernames.append(f"{name_parts[0][0]}{name_parts[-1]}")
                # İsim + ilk harf soyisim
                possible_usernames.append(f"{name_parts[0]}{name_parts[-1][0]}")
                # İsim soyisim baş harfleri
                possible_usernames.append("".join(part[0] for part in name_parts))
            
            print(f"{Fore.BLUE}[*] '{full_name}' ({source}) için muhtemel kullanıcı adları aranıyor:")
            for possible_username in possible_usernames:
                if possible_username != self.username:  # Kendisi değilse
                    print(f"{Fore.BLUE}  - {possible_username}")
                    # Burada ekstra arama yapmak gerekirse daha sonra eklenir
    
    def extract_full_names(self):
        """Bulunan profil bilgilerinden tam isimleri çıkarır"""
        full_names = []
        
        # Bulunan profil bilgilerinden tam isimleri çıkar
        for site_name, data in self.results.items():
            if "profile_info" in data and "name" in data["profile_info"] and data["profile_info"]["name"]:
                full_name = data["profile_info"]["name"]
                if full_name and full_name not in [entry["name"] for entry in full_names]:
                    full_names.append({
                        "name": full_name,
                        "source": site_name
                    })
        
        self.full_names_found = full_names
        return full_names
    
    def search_web_for_fullname(self, open_browser=False):
        """Bulunan isim soyisim bilgisini kullanarak web'de arama yapar"""
        if not self.results:
            print(f"{Fore.YELLOW}[!] Önce hesap aramalarını tamamlayın.")
            return
        
        if not self.full_names_found:
            full_names = self.extract_full_names()
            if not full_names:
                print(f"{Fore.YELLOW}[!] Tam isim bilgisi bulunamadı.")
                return
        else:
            full_names = self.full_names_found
        
        print(f"\n{Fore.BLUE}[*] Bulunan isimler için web araması yapılıyor...")
        
        for name_entry in full_names:
            full_name = name_entry["name"]
            source = name_entry["source"]
            
            print(f"\n{Fore.GREEN}[+] '{full_name}' ({source}) için arama sonuçları:")
            
            # Google arama URL'i
            google_search_url = f"https://www.google.com/search?q={urllib.parse.quote(full_name)}"
            print(f"{Fore.CYAN}  Google: {google_search_url}")
            
            # LinkedIn arama URL'i
            linkedin_search_url = f"https://www.linkedin.com/search/results/all/?keywords={urllib.parse.quote(full_name)}"
            print(f"{Fore.CYAN}  LinkedIn: {linkedin_search_url}")
            
            # Facebook arama URL'i
            facebook_search_url = f"https://www.facebook.com/search/top/?q={urllib.parse.quote(full_name)}"
            print(f"{Fore.CYAN}  Facebook: {facebook_search_url}")
            
            # Twitter arama URL'i
            twitter_search_url = f"https://twitter.com/search?q={urllib.parse.quote(full_name)}"
            print(f"{Fore.CYAN}  Twitter: {twitter_search_url}")
            
            # Daha spesifik arama yapmak için diğer kişisel bilgileri de kullanabiliriz
            location = ""
            for site_name, data in self.results.items():
                if "profile_info" in data and "location" in data["profile_info"] and data["profile_info"]["location"]:
                    location = data["profile_info"]["location"]
                    break
            
            if location:
                google_with_location = f"https://www.google.com/search?q={urllib.parse.quote(full_name + ' ' + location)}"
                print(f"{Fore.CYAN}  Google (konum ile): {google_with_location}")
            
            # Tarayıcıda aç seçeneği
            if open_browser:
                print(f"{Fore.YELLOW}[*] Tarayıcıda Google araması açılıyor...")
                webbrowser.open(google_search_url)
    
    def save_results(self, filename="results.json"):
        """Sonuçları JSON dosyasına kaydeder"""
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump({
                "username": self.username,
                "results": self.results,
                "search_date": time.strftime("%Y-%m-%d %H:%M:%S")
            }, f, indent=4, ensure_ascii=False)
        
        print(f"{Fore.GREEN}[+] Sonuçlar '{filename}' dosyasına kaydedildi.")
    
    def print_summary(self):
        """Özet bilgileri yazdırır"""
        print(f"\n{Fore.BLUE}=== ÖZET ===")
        print(f"{Fore.BLUE}Kullanıcı adı: {self.username}")
        print(f"{Fore.BLUE}Bulunan platformlar: {len(self.results)}")
        
        if self.results:
            print(f"\n{Fore.GREEN}Bulunan Hesaplar:")
            for site_name, data in self.results.items():
                print(f"{Fore.GREEN}- {site_name}: {data['url']}")
                
                if data.get("profile_info"):
                    print(f"  {Fore.CYAN}Profil Bilgileri:")
                    for key, value in data["profile_info"].items():
                        print(f"  {Fore.CYAN}  {key}: {value}")
            
            # Bulunan isim bilgileri
            full_names = self.extract_full_names()
            if full_names:
                print(f"\n{Fore.GREEN}Bulunan İsim Bilgileri:")
                for name_entry in full_names:
                    print(f"{Fore.GREEN}- {name_entry['name']} (Kaynak: {name_entry['source']})")
            
            # Benzer hesaplar için arama öner
            print(f"\n{Fore.YELLOW}[?] Bulunan isim bilgileri ile benzer hesapları aramak için:")
            print(f"{Fore.YELLOW}    python username_osint.py {self.username} --similar")
            
            # Web'de arama öner
            if full_names:
                print(f"\n{Fore.YELLOW}[?] Bulunan isim bilgileri ile web araması yapmak için:")
                print(f"{Fore.YELLOW}    python username_osint.py {self.username} --search-web")
                print(f"{Fore.YELLOW}    python username_osint.py {self.username} --search-web --open-browser")

def main():
    parser = argparse.ArgumentParser(description='Kullanıcı adı OSINT aracı')
    parser.add_argument('username', help='Araştırılacak kullanıcı adı')
    parser.add_argument('-o', '--output', help='Sonuçların kaydedileceği dosya adı', default='results.json')
    parser.add_argument('-s', '--similar', action='store_true', help='Bulunan isim bilgileri ile benzer hesapları ara')
    parser.add_argument('-w', '--search-web', action='store_true', help='Bulunan isim bilgileri ile web araması yap')
    parser.add_argument('-b', '--open-browser', action='store_true', help='Web araması sonuçlarını tarayıcıda aç')
    args = parser.parse_args()
    
    osint = UsernameOSINT(args.username)
    osint.search()
    
    if args.similar:
        osint.search_for_similar_accounts()
    
    if args.search_web:
        osint.search_web_for_fullname(args.open_browser)
    
    osint.print_summary()
    osint.save_results(args.output)

if __name__ == "__main__":
    main() 