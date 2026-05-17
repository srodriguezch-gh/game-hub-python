"""Chess AI using minimax search with alpha-beta pruning."""

import chess
import logging

logger = logging.getLogger(__name__)

PIECE_VALUES = {
    chess.PAWN: 100,
    chess.KNIGHT: 320,
    chess.BISHOP: 330,
    chess.ROOK: 500,
    chess.QUEEN: 900,
    chess.KING: 20000,
}

PAWN_TABLE = [
    0,  0,  0,  0,  0,  0,  0,  0,
    50, 50, 50, 50, 50, 50, 50, 50,
    10, 10, 20, 30, 30, 20, 10, 10,
    5,  5, 10, 25, 25, 5,  5,  5,
    0,  0,  0, 20, 20,  0,  0,  0,
    5, -5,-10,  0,  0,-10, -5,  5,
    5, 10, 10,-20,-20, 10, 10,  5,
    0,  0,  0,  0,  0,  0,  0,  0,
]

KNIGHT_TABLE = [
    -50,-40,-30,-30,-30,-30,-40,-50,
    -40,-20,  0,  0,  0,  0,-20,-40,
    -30,  0, 10, 15, 15, 10,  0,-30,
    -30,  5, 15, 20, 20, 15,  5,-30,
    -30,  0, 15, 20, 20, 15,  0,-30,
    -30,  5, 10, 15, 15, 10,  5,-30,
    -40,-20,  0,  5,  5,  0,-20,-40,
    -50,-40,-30,-30,-30,-30,-40,-50,
]


def evaluate_board(board: chess.Board) -> float:
    if board.is_checkmate():
        return -99999 if board.turn else 99999
    if board.is_stalemate():
        return 0

    score = 0
    for square, piece in board.piece_map().items():
        value = PIECE_VALUES[piece.piece_type]
        if piece.color == chess.WHITE:
            score += value
            if piece.piece_type == chess.PAWN:
                score += PAWN_TABLE[chess.square_file(square) + 8 * (7 - chess.square_rank(square))]
            elif piece.piece_type == chess.KNIGHT:
                score += KNIGHT_TABLE[square]
        else:
            score -= value
            if piece.piece_type == chess.PAWN:
                score -= PAWN_TABLE[chess.square_file(square) + 8 * chess.square_rank(square)]
            elif piece.piece_type == chess.KNIGHT:
                score -= KNIGHT_TABLE[square]

    score += len(list(board.legal_moves)) * 5
    return score


def minimax(board: chess.Board, depth: int, alpha: float, beta: float, maximizing: bool) -> float:
    if depth == 0 or board.is_game_over():
        return evaluate_board(board)

    if maximizing:
        max_eval = float("-inf")
        for move in board.legal_moves:
            board.push(move)
            eval_score = minimax(board, depth - 1, alpha, beta, False)
            board.pop()
            max_eval = max(max_eval, eval_score)
            alpha = max(alpha, eval_score)
            if beta <= alpha:
                break
        return max_eval
    else:
        min_eval = float("inf")
        for move in board.legal_moves:
            board.push(move)
            eval_score = minimax(board, depth - 1, alpha, beta, True)
            board.pop()
            min_eval = min(min_eval, eval_score)
            beta = min(beta, eval_score)
            if beta <= alpha:
                break
        return min_eval


def find_best_move(board: chess.Board, depth: int = 3) -> chess.Move | None:
    best_move = None
    best_value = float("-inf") if board.turn else float("inf")
    moves = list(board.legal_moves)

    def capture_priority(move):
        return -1 if board.is_capture(move) else 0

    moves.sort(key=capture_priority)

    for move in moves:
        board.push(move)
        value = minimax(board, depth - 1, float("-inf"), float("inf"), not board.turn)
        board.pop()

        if board.turn:
            if value > best_value:
                best_value = value
                best_move = move
        else:
            if value < best_value:
                best_value = value
                best_move = move

    return best_move


def get_ai_move(fen: str) -> dict:
    try:
        board = chess.Board(fen)
        if board.is_game_over():
            return {"error": "game_over"}
        move = find_best_move(board, depth=3)
        if move:
            board.push(move)
            return {
                "from": chess.square_name(move.from_square),
                "to": chess.square_name(move.to_square),
                "fen": board.fen(),
            }
        return {"error": "no_move"}
    except Exception as e:
        logger.error(f"AI error: {e}")
        return {"error": str(e)}