"""AI opponent service — Calypso and Traka bot players."""

import asyncio
import logging
from typing import Callable, Optional

logger = logging.getLogger(__name__)


class BotProfile:
    def __init__(self, name: str, skill_level: int, response_delay_ms: int):
        self.name = name
        self.skill_level = skill_level
        self.response_delay_ms = response_delay_ms


BOT_PROFILES = {
    "Calypso": BotProfile(name="Calypso", skill_level=3, response_delay_ms=800),
    "Traka": BotProfile(name="Traka", skill_level=2, response_delay_ms=500),
}


class ChessBot:
    def __init__(self, depth: int = 3):
        self.depth = depth

    def get_move(self, fen: str) -> dict:
        import chess
        try:
            board = chess.Board(fen)
            if board.is_game_over():
                return {"error": "game_over"}
            move = self._find_best_move(board)
            if move:
                return {
                    "from": chess.square_name(move.from_square),
                    "to": chess.square_name(move.to_square),
                }
            return {"error": "no_move"}
        except Exception as e:
            logger.error(f"ChessBot error: {e}")
            return {"error": str(e)}

    def _find_best_move(self, board):
        import chess
        piece_values = {
            chess.PAWN: 100, chess.KNIGHT: 320, chess.BISHOP: 330,
            chess.ROOK: 500, chess.QUEEN: 900, chess.KING: 20000,
        }

        def evaluate(b: chess.Board) -> float:
            if b.is_checkmate():
                return -99999 if b.turn else 99999
            if b.is_stalemate() or b.is_draw():
                return 0
            score = 0
            for piece in b.piece_map().values():
                val = piece_values[piece.piece_type]
                score += val if piece.color == chess.WHITE else -val
            score += len(list(b.legal_moves)) * 3
            return score

        def minimax(b, d, alpha, beta, maximizing):
            if d == 0 or b.is_game_over():
                return evaluate(b)
            if maximizing:
                max_eval = float("-inf")
                for mv in b.legal_moves:
                    b.push(mv)
                    eval_score = minimax(b, d - 1, alpha, beta, False)
                    b.pop()
                    max_eval = max(max_eval, eval_score)
                    alpha = max(alpha, eval_score)
                    if beta <= alpha:
                        break
                return max_eval
            else:
                min_eval = float("inf")
                for mv in b.legal_moves:
                    b.push(mv)
                    eval_score = minimax(b, d - 1, alpha, beta, True)
                    b.pop()
                    min_eval = min(min_eval, eval_score)
                    beta = min(beta, eval_score)
                    if beta <= alpha:
                        break
                return min_eval

        best_move = None
        best_value = float("-inf") if board.turn else float("inf")
        for mv in list(board.legal_moves):
            board.push(mv)
            val = minimax(board, self.depth - 1, float("-inf"), float("inf"), not board.turn)
            board.pop()
            if board.turn:
                if val > best_value:
                    best_value = val
                    best_move = mv
            else:
                if val < best_value:
                    best_value = val
                    best_move = mv
        return best_move


class BotService:
    """AI bot manager. Handles chess AI for Calypso and Traka."""

    def __init__(self):
        self._bots = {name: ChessBot(profile.skill_level) for name, profile in BOT_PROFILES.items()}
        self._profiles = BOT_PROFILES

    async def request_chess_move(self, bot_name: str, fen: str, callback: Callable[[dict], None]) -> None:
        profile = self._profiles.get(bot_name)
        if not profile:
            callback({"error": "unknown_bot"})
            return

        await asyncio.sleep(profile.response_delay_ms / 1000.0)
        bot = self._bots.get(bot_name)
        if bot:
            result = bot.get_move(fen)
            callback(result)
        else:
            callback({"error": "no_bot"})

    def get_profile(self, bot_name: str) -> Optional[BotProfile]:
        return self._profiles.get(bot_name)


bot_service = BotService()