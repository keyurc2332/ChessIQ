# backend/download_all_games.py - FIXED VERSION

import requests
import time

HEADERS = {
    "User-Agent": "ChessIQ-App/1.0 (Contact: keyur@example.com)"
}

def fetch_all_games(username):
    """Fetch ALL games from Chess.com"""
    try:
        print(f"Fetching game archives for {username}...")
        
        archives_url = f"https://api.chess.com/pub/player/{username}/games/archives"
        response = requests.get(archives_url, headers=HEADERS, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        archives = data.get('archives', [])
        
        if not archives:
            print(f"❌ No archives found for {username}")
            return []
        
        print(f"✅ Found {len(archives)} archive months\n")
        
        all_games_pgn = []  # Store PGN strings, not parsed games
        
        for i, archive_url in enumerate(reversed(archives)):
            try:
                year_month = archive_url.split('/')[-2:]
                print(f"[{i+1}/{len(archives)}] Fetching {year_month[0]}-{year_month[1]}...", end=" ")
                
                # Get PGN format directly!
                pgn_url = f"{archive_url}/pgn"
                response = requests.get(pgn_url, headers=HEADERS, timeout=10)
                response.raise_for_status()
                
                # Get raw PGN text
                pgn_text = response.text
                games_in_month = pgn_text.count('[Event')
                
                all_games_pgn.append(pgn_text)
                
                print(f"✅ {games_in_month} games")
                
                time.sleep(0.5)  # Rate limiting
            
            except Exception as e:
                print(f"❌ Error: {e}")
                continue
        
        print(f"\n✅ SUCCESS! Total archives processed: {len(all_games_pgn)}")
        return all_games_pgn
    
    except Exception as e:
        print(f"❌ Fatal error: {e}")
        return []


def save_games_to_pgn(pgn_list, filename):
    """Save raw PGN data to file"""
    try:
        print(f"\n💾 Saving games to {filename}...")
        
        with open(filename, 'w', encoding='utf-8') as f:
            for pgn_text in pgn_list:
                f.write(pgn_text)
                if not pgn_text.endswith('\n\n'):
                    f.write('\n\n')
        
        # Count games
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()
            game_count = content.count('[Event')
        
        file_size_mb = len(content) / 1024 / 1024
        
        print(f"✅ Saved to {filename}")
        print(f"   Games: {game_count}")
        print(f"   File size: {file_size_mb:.2f} MB")
        
        return filename
    
    except Exception as e:
        print(f"❌ Error saving: {e}")
        return None


if __name__ == "__main__":
    username = "keyur_2332"
    
    print("="*60)
    print(f"ChessIQ - Game Downloader (PGN Format)")
    print("="*60)
    
    pgn_list = fetch_all_games(username)
    
    if pgn_list:
        filename = save_games_to_pgn(pgn_list, "all_games.pgn")
        
        if filename:
            print("\n" + "="*60)
            print(f"✅ READY TO UPLOAD!")
            print(f"   File: {filename}")
            print("="*60)
    else:
        print("❌ Could not fetch games")