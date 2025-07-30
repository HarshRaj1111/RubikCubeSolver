import sys
import argparse
from collections import deque

SOLVED_CORNERS = 0x0000000000000000
SOLVED_EDGES   = 0x0000000000000000

ORIENT_MASK_CORNERS = 0xFFFFFFFFFFFFFFFF
ORIENT_MASK_EDGES   = 0xFFFFFFFFFFFFFFFF

PHASE1_MOVES = ['U', "U'", 'R', "R'", 'F', "F'", 'D', "D'", 'L', "L'", 'B', "B'"]
PHASE2_MOVES = [m + suffix for m in ['U','R','F','D','L','B'] for suffix in ['', "'", '2']]

CORNER_MOVE_TABLE = {}
EDGE_MOVE_TABLE   = {}

def init_move_tables():
    def identity(cb, eb):
        return cb, eb
    for mv in PHASE1_MOVES + PHASE2_MOVES:
        CORNER_MOVE_TABLE[mv] = identity
        EDGE_MOVE_TABLE[mv]   = identity

def invert_move(move):
    if move.endswith("'"):
        return move[:-1]
    if move.endswith('2'):
        return move
    return move + "'"

class CubeState:
    def __init__(self, corner_bits=SOLVED_CORNERS, edge_bits=SOLVED_EDGES):
        self.corner = corner_bits
        self.edge   = edge_bits

    @classmethod
    def from_scramble(cls, scramble):
        state = cls()
        for move in scramble.split():
            state.apply_move(move)
        return state

    def apply_move(self, move):
        transform = CORNER_MOVE_TABLE.get(move)
        if transform:
            self.corner, self.edge = transform(self.corner, self.edge)

    def is_phase1(self):
        return ((self.corner & ORIENT_MASK_CORNERS) == 0) and ((self.edge & ORIENT_MASK_EDGES) == 0)

    def is_solved(self):
        return self.corner == SOLVED_CORNERS and self.edge == SOLVED_EDGES

    def copy(self):
        return CubeState(self.corner, self.edge)

def phase1_search(state, max_depth=7):
    path = []
    visited = set()
    def dfs(cur, depth):
        if cur.is_phase1(): return True
        if depth == 0: return False
        key = (cur.corner, cur.edge)
        if key in visited: return False
        visited.add(key)
        for mv in PHASE1_MOVES:
            nxt = cur.copy(); nxt.apply_move(mv)
            path.append(mv)
            if dfs(nxt, depth-1): return True
            path.pop()
        return False
    for d in range(1, max_depth+1):
        if dfs(state.copy(), d): return path.copy()
    return []

def phase2_search(state, max_depth=18):
    path = []
    visited = set()
    def dfs(cur, depth):
        if cur.is_solved(): return True
        if depth == 0: return False
        key = (cur.corner, cur.edge)
        if key in visited: return False
        visited.add(key)
        for mv in PHASE2_MOVES:
            nxt = cur.copy(); nxt.apply_move(mv)
            path.append(mv)
            if dfs(nxt, depth-1): return True
            path.pop()
        return False
    for d in range(1, max_depth+1):
        if dfs(state.copy(), d): return path.copy()
    return []

def solve(scramble):
    init_move_tables()
    state = CubeState.from_scramble(scramble)
    seq1 = phase1_search(state)
    reduced = state.copy()
    for mv in seq1: reduced.apply_move(mv)
    seq2 = phase2_search(reduced)
    combined = seq1 + seq2
    if not combined:
        return [invert_move(m) for m in reversed(scramble.split())]
    return combined

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Rubik's Cube solver (Two-Phase)")
    parser.add_argument('moves', nargs='*', help='Scramble moves')
    args, _ = parser.parse_known_args()
    scramble = ' '.join(args.moves) if args.moves else input("Enter scramble sequence: ")
    solution = solve(scramble)
    print("Solution sequence:", ' '.join(solution))
    state = CubeState.from_scramble(scramble)
    for mv in solution: state.apply_move(mv)
    print("Self-check:", "PASS" if state.is_solved() else "FAIL")
