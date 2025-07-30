from solver import solve, CubeState

moves = "R' B U2 B' L2 B' U2 L2 R2 F' U2 F U F L2 F' R2 D2 L"
solution = solve(moves)
print("Solution:", solution)

# Verify:
state = CubeState.from_scramble(moves)
for m in solution:
    state.apply_move(m)
print("Solved?", state.is_solved())
