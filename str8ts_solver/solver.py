import itertools

import z3  # type: ignore


def _shift(pos: tuple[int, int], shift: tuple[int, int]) -> tuple[int, int]:
    res = tuple(sum(_) for _ in zip(pos, shift, strict=True))
    assert len(res) == 2
    return res


def _extract_block(
    unknowns, pos: tuple[int, int], direction: tuple[int, int]
) -> list[tuple[int, int]]:
    assert pos in unknowns
    res = [pos]
    cur_pos = _shift(pos, direction)
    while cur_pos in unknowns:
        res.append(cur_pos)
        cur_pos = _shift(cur_pos, direction)
    return res


def _gen_horizontal_blocks(size: tuple[int, int], unknowns):
    for y_pos in range(size[1]):
        x_pos = 0
        while x_pos < size[0]:
            if (x_pos, y_pos) in unknowns:
                cur_block = _extract_block(unknowns, (x_pos, y_pos), (1, 0))
                if len(cur_block) > 1:
                    yield cur_block
                x_pos += len(cur_block)
            else:
                x_pos += 1


def _gen_vertical_blocks(size: tuple[int, int], unknowns):
    for x_pos in range(size[0]):
        y_pos = 0
        while y_pos < size[1]:
            if (x_pos, y_pos) in unknowns:
                cur_block = _extract_block(unknowns, (x_pos, y_pos), (0, 1))
                if len(cur_block) > 1:
                    yield cur_block
                y_pos += len(cur_block)
            else:
                y_pos += 1


def _define_unknowns(size: tuple[int, int], blocked: set[tuple[int, int]]):
    return {
        (x_pos, y_pos): z3.Int(f"u_{x_pos}_{y_pos}")
        for x_pos, y_pos in itertools.product(range(size[0]), range(size[1]))
        if (x_pos, y_pos) not in blocked
    }


def _add_basic_constrains(solver, unknowns, known, value_limit) -> None:
    for pos, unknown in unknowns.items():
        if pos in known:
            solver.add(unknown == known[pos])
        else:
            solver.add(0 < unknown)
            solver.add(unknown <= value_limit)


def _add_different_than_if_exists(
    solver, unknowns, unknown_id: tuple[int, int], value: int
) -> None:
    if unknown_id in unknowns:
        solver.add(unknowns[unknown_id] != value)


def _add_constrains_from_blocked(
    solver,
    unknowns,
    size: tuple[int, int],
    blocked: set[tuple[int, int]],
    known: dict[tuple[int, int], int],
) -> None:
    for cur_blocked in blocked:
        if cur_blocked in known:
            cur_blocked_x, cur_blocked_y = cur_blocked
            for x_pos in range(size[0]):
                _add_different_than_if_exists(
                    solver, unknowns, (x_pos, cur_blocked_y), known[cur_blocked]
                )
            for y_pos in range(size[1]):
                _add_different_than_if_exists(
                    solver, unknowns, (cur_blocked_x, y_pos), known[cur_blocked]
                )


def _add_block_constrain(
    solver, unknowns, block: list[tuple[int, int]], block_id: str
) -> None:
    cur_limit = z3.Int(block_id)
    solver.add(cur_limit > 0)
    for _ in block:
        solver.add(cur_limit <= unknowns[_])
        solver.add(unknowns[_] < cur_limit + len(block))
    solver.add(z3.Distinct(*(unknowns[_] for _ in block)))


def _add_all_block_constrains(solver, unknowns, size: tuple[int, int]) -> None:
    for block_num, cur_block in enumerate(_gen_horizontal_blocks(size, unknowns)):
        _add_block_constrain(solver, unknowns, cur_block, f"h_{block_num}")

    for block_num, cur_block in enumerate(_gen_vertical_blocks(size, unknowns)):
        _add_block_constrain(solver, unknowns, cur_block, f"v_{block_num}")


def _add_entries_in_all_rows_are_unique_constrains(
    solver, unknowns, size: tuple[int, int]
):
    for y_pos in range(size[1]):
        cur_row = [
            unknowns[(x_pos, y_pos)]
            for x_pos in range(size[0])
            if (x_pos, y_pos) in unknowns
        ]
        solver.add(z3.Distinct(*cur_row))


def _add_entries_in_all_cols_are_unique_constrains(
    solver, unknowns, size: tuple[int, int]
):
    for x_pos in range(size[0]):
        cur_col = [
            unknowns[(x_pos, y_pos)]
            for y_pos in range(size[1])
            if (x_pos, y_pos) in unknowns
        ]
        solver.add(z3.Distinct(*cur_col))


def _create_solver(
    size: tuple[int, int],
    blocked: set[tuple[int, int]],
    known: dict[tuple[int, int], int],
):
    solver = z3.Solver()
    unknowns = _define_unknowns(size, blocked)
    _add_basic_constrains(solver, unknowns, known, max(size))
    _add_constrains_from_blocked(solver, unknowns, size, blocked, known)
    _add_all_block_constrains(solver, unknowns, size)
    _add_entries_in_all_cols_are_unique_constrains(solver, unknowns, size)
    _add_entries_in_all_rows_are_unique_constrains(solver, unknowns, size)

    return unknowns, solver


def _read_solution(unknowns, solver) -> dict[tuple[int, int], int]:
    assert solver.check() == z3.sat
    model = solver.model()
    return {_: model[unknowns[_]].as_long() for _ in unknowns}


def solve(
    size: tuple[int, int],
    blocked: set[tuple[int, int]],
    known: dict[tuple[int, int], int],
) -> dict[tuple[int, int], int] | None:
    unknowns, solver = _create_solver(size, blocked, known)
    if solver.check() != z3.sat:
        return None
    solved = _read_solution(unknowns, solver)
    assert all(solved[_] == known[_] for _ in solved if _ in known)
    for cur_block in itertools.chain(
        _gen_horizontal_blocks(size, unknowns), _gen_vertical_blocks(size, unknowns)
    ):
        solved_values = {solved[_] for _ in cur_block}
        assert len(solved_values) == len(cur_block)
        assert solved_values == set(range(min(solved_values), max(solved_values) + 1))

    return solved
