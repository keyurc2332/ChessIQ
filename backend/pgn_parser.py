# backend/pgn_parser.py - CORRECTED VERSION
# Handles corrupted PGN files gracefully AND Windows line endings

import chess
import chess.pgn
import io
import re
import logging

# Setup logging
logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(__name__)


def parse_pgn_string(pgn_string):
    """Parse a PGN string and extract game metadata"""
    try:
        pgn_io = io.StringIO(pgn_string)
        game = chess.pgn.read_game(pgn_io)
        
        if game is None:
            return None
        
        return {
            "game": game,
            "headers": dict(game.headers)
        }
    
    except Exception as e:
        logger.warning(f"Error parsing PGN: {str(e)[:100]}")
        return None


def extract_moves_safely(game):
    """Extract moves from a game, skipping invalid ones"""
    try:
        moves = []
        board = game.board()
        
        for move in game.mainline_moves():
            try:
                if move in board.legal_moves:
                    moves.append(board.san(move))
                    board.push(move)
            except:
                continue
        
        return moves
    except:
        return []


def validate_game(pgn_string):
    """Validate if a PGN game is playable"""
    try:
        pgn_io = io.StringIO(pgn_string)
        game = chess.pgn.read_game(pgn_io)
        
        if game is None:
            return False
        
        board = game.board()
        move_count = 0
        
        for move in game.mainline_moves():
            try:
                if move not in board.legal_moves:
                    return False
                board.push(move)
                move_count += 1
            except:
                return False
        
        return move_count > 0
    except:
        return False


def extract_game_info(game_dict):
    """Extract relevant info from a parsed game"""
    try:
        if not game_dict or "headers" not in game_dict:
            return None
        
        headers = game_dict["headers"]
        game = game_dict["game"]
        
        if "White" not in headers or "Black" not in headers:
            return None
        
        moves = extract_moves_safely(game)
        if not moves:
            return None
        
        result_str = headers.get("Result", "*")
        if result_str == "1-0":
            result = "win"
        elif result_str == "0-1":
            result = "loss"
        elif result_str == "1/2-1/2":
            result = "draw"
        else:
            result = "unknown"
        
        try:
            date_str = headers.get("Date", "2026.01.01")
            date_parts = date_str.split(".")
            if len(date_parts) == 3:
                from datetime import datetime
                played_at = datetime(
                    int(date_parts[0]),
                    int(date_parts[1]),
                    int(date_parts[2])
                )
            else:
                from datetime import datetime
                played_at = datetime.now()
        except:
            from datetime import datetime
            played_at = datetime.now()
        
        return {
            "white_player": headers.get("White", ""),
            "black_player": headers.get("Black", ""),
            "result": result,
            "played_at": played_at,
            "moves": " ".join(moves),
            "white_elo": try_int(headers.get("WhiteElo")),
            "black_elo": try_int(headers.get("BlackElo")),
            "opening_eco": headers.get("ECO", ""),
            "opening_name": headers.get("ECOUrl", ""),
            "time_control": headers.get("TimeControl", ""),
            "opponent_username": headers.get("Black", ""),
        }
    except:
        return None


def try_int(value):
    """Convert to int or return None"""
    try:
        return int(value) if value else None
    except:
        return None


def parse_pgn_file(pgn_text):
    """Parse multiple games from a PGN file"""
    
    # FIX: Normalize Windows line endings to Unix style
    pgn_text = pgn_text.replace('\r\n', '\n')
    
    valid_games = []
    invalid_games = 0
    
    try:
        # Split on double newline followed by [Event
        game_strings = re.split(r'\n\n\[Event', pgn_text)
        
        print(f"\n📊 Found {len(game_strings)} potential game blocks")
        
        for i, game_str in enumerate(game_strings):
            try:
                if i > 0:
                    game_str = "[Event" + game_str
                
                if not game_str.strip():
                    continue
                
                if not validate_game(game_str):
                    invalid_games += 1
                    continue
                
                game_dict = parse_pgn_string(game_str)
                if not game_dict:
                    invalid_games += 1
                    continue
                
                game_info = extract_game_info(game_dict)
                if not game_info:
                    invalid_games += 1
                    continue
                
                valid_games.append(game_info)
                
                if (len(valid_games) + invalid_games) % 500 == 0:
                    print(f"  Processed {len(valid_games) + invalid_games} games ({len(valid_games)} valid, {invalid_games} invalid)")
            
            except:
                invalid_games += 1
                continue
        
        print(f"\n✅ Parse complete: {len(valid_games)} valid, {invalid_games} invalid")
        return valid_games
    
    except:
        return valid_games