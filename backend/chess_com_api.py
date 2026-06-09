# backend/chess_com_api.py

import requests
from typing import List, Dict, Optional
from datetime import datetime
import time

CHESS_COM_API = "https://api.chess.com/pub"


def fetch_user_games(username: str, max_games: Optional[int] = None) -> List[Dict]:
    """
    Fetch all games from Chess.com for a user
    
    Returns list of games in PGN format
    """
    try:
        print(f"Fetching games for {username}...")
        
        # Get user's game archives (list of months)
        archives_url = f"{CHESS_COM_API}/player/{username}/games/archives"
        response = requests.get(archives_url, timeout=10)
        response.raise_for_status()
        
        archives = response.json().get("archives", [])
        
        if not archives:
            print(f"No game archives found for {username}")
            return []
        
        print(f"Found {len(archives)} archive months")
        
        all_games = []
        games_count = 0
        
        # Fetch games from each month (most recent first)
        for archive_url in reversed(archives):
            try:
                print(f"Fetching {archive_url}...")
                response = requests.get(archive_url, timeout=10)
                response.raise_for_status()
                
                games = response.json().get("games", [])
                print(f"  Found {len(games)} games in this month")
                
                for game in games:
                    all_games.append(game)
                    games_count += 1
                    
                    # Stop if we have enough games
                    if max_games and games_count >= max_games:
                        print(f"Reached max games limit: {max_games}")
                        return all_games
                
                # Rate limiting: Chess.com allows ~600 requests/hour
                time.sleep(0.2)  # Small delay between requests
            
            except Exception as e:
                print(f"Error fetching archive {archive_url}: {e}")
                continue
        
        print(f"✅ Total games fetched: {games_count}")
        return all_games
    
    except Exception as e:
        print(f"❌ Error fetching games: {e}")
        return []


def convert_chess_com_game(game: Dict) -> Dict:
    """
    Convert Chess.com game format to our format
    """
    try:
        # Extract PGN
        pgn = game.get("pgn", "")
        if not pgn:
            return None
        
        # Parse headers from PGN
        headers = parse_pgn_headers(pgn)
        
        # Determine player color and result
        player_white = headers.get("White", "").lower()
        player_black = headers.get("Black", "").lower()
        result = headers.get("Result", "*")
        
        # You need to know which player is you!
        # For now, assume the first player is you
        player_color = "white"
        opponent = player_black
        opponent_username = player_black
        
        # Convert result
        if result == "1-0":
            game_result = "win" if player_color == "white" else "loss"
        elif result == "0-1":
            game_result = "loss" if player_color == "white" else "win"
        elif result == "1/2-1/2":
            game_result = "draw"
        else:
            game_result = "unknown"
        
        # Parse date
        date_str = headers.get("Date", "2026.01.01")
        try:
            date_parts = date_str.split(".")
            if len(date_parts) == 3:
                played_at = datetime(
                    int(date_parts[0]),
                    int(date_parts[1]),
                    int(date_parts[2])
                )
            else:
                played_at = datetime.now()
        except:
            played_at = datetime.now()
        
        # Extract moves from PGN
        moves_str = extract_moves_from_pgn(pgn)
        
        return {
            "white_player": player_white,
            "black_player": player_black,
            "played_at": played_at,
            "result": game_result,
            "moves": moves_str,
            "opponent_username": opponent_username,
            "white_elo": try_int(headers.get("WhiteElo")),
            "black_elo": try_int(headers.get("BlackElo")),
            "opening_eco": headers.get("ECO"),
            "opening_name": headers.get("Opening"),
            "time_control": headers.get("TimeControl"),
            "pgn": pgn
        }
    
    except Exception as e:
        print(f"Error converting game: {e}")
        return None


def parse_pgn_headers(pgn: str) -> Dict:
    """
    Extract headers from PGN string
    """
    headers = {}
    
    for line in pgn.split("\n"):
        if line.startswith("["):
            # Format: [Key "Value"]
            try:
                parts = line.strip("[]").split(' "')
                if len(parts) == 2:
                    key = parts[0]
                    value = parts[1].rstrip('"')
                    headers[key] = value
            except:
                continue
    
    return headers


def extract_moves_from_pgn(pgn: str) -> str:
    """
    Extract moves from PGN (everything after headers)
    """
    lines = pgn.split("\n")
    moves_lines = []
    
    in_moves = False
    for line in lines:
        if not line.startswith("["):
            in_moves = True
        
        if in_moves and line.strip():
            moves_lines.append(line.strip())
    
    moves_str = " ".join(moves_lines)
    # Remove move numbers and extra whitespace
    moves_str = " ".join(moves_str.split())
    
    return moves_str


def try_int(value: Optional[str]) -> Optional[int]:
    """
    Try to convert string to int
    """
    try:
        return int(value) if value else None
    except:
        return None