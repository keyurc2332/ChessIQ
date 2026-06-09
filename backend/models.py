# backend/models.py - CORRECTED VERSION with Eval Columns

from sqlalchemy import Column, String, Integer, Float, DateTime, ForeignKey, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid

Base = declarative_base()


class User(Base):
    __tablename__ = "users"
    
    user_id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    email = Column(String, unique=True, nullable=False, index=True)
    password_hash = Column(String, nullable=False)
    chess_com_username = Column(String, nullable=True)
    lichess_username = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    games = relationship("Game", back_populates="user")


class Game(Base):
    __tablename__ = "games"
    
    game_id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("users.user_id"), nullable=False, index=True)
    played_at = Column(DateTime, nullable=False, index=True)
    source = Column(String, nullable=False)  # chess_com, lichess, manual, etc.
    source_game_id = Column(String, nullable=False)  # For deduplication
    player_color = Column(String, nullable=False)  # white or black
    player_rating_before = Column(Integer, nullable=True)
    opponent_username = Column(String, nullable=False)
    opponent_rating = Column(Integer, nullable=True)
    time_control = Column(String, nullable=True)
    opening_eco = Column(String, nullable=True)
    opening_name = Column(String, nullable=True)
    result = Column(String, nullable=False)  # win, loss, draw
    moves = Column(Text, nullable=False)  # PGN moves
    is_analyzed = Column(Integer, default=0)  # 0 or 1
    accuracy = Column(Integer, nullable=True)  # Percentage (0-100)
    avg_centipawn_loss = Column(Integer, nullable=True)  # CPL in centipawns
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="games")
    moves_list = relationship("Move", back_populates="game", cascade="all, delete-orphan")


class Move(Base):
    __tablename__ = "moves"
    
    move_id = Column(Integer, primary_key=True, autoincrement=True)
    game_id = Column(String, ForeignKey("games.game_id"), nullable=False, index=True)
    move_number = Column(Integer, nullable=False)
    move_san = Column(String, nullable=False)  # e.g., "e4", "Nf3"
    move_uci = Column(String, nullable=False)  # e.g., "e2e4"
    eval_before = Column(Float, nullable=True)  # Stockfish eval before move (in pawns)
    eval_after = Column(Float, nullable=True)  # Stockfish eval after move (in pawns)
    centipawn_loss = Column(Integer, nullable=True)  # CPL for this move
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    game = relationship("Game", back_populates="moves_list")