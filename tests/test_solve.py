import pytest

from str8ts_solver.solver import solve

from . import samples


def _extract_test_case(
    sample: samples.Sample,
) -> tuple[
    tuple[int, int],
    set[tuple[int, int]],
    dict[tuple[int, int], int],
    dict[tuple[int, int], int],
]:
    return sample.size, sample.blocked, sample.known, sample.solved


@pytest.mark.parametrize(
    ("size", "blocked", "known", "expected"),
    [
        _extract_test_case(samples.SAMPLE_1),
        _extract_test_case(samples.SAMPLE_2),
        _extract_test_case(samples.SAMPLE_3),
    ],
)
def test_solve(
    size: tuple[int, int],
    blocked: set[tuple[int, int]],
    known: dict[tuple[int, int], int],
    expected: dict[tuple[int, int], int],
) -> None:
    assert solve(size, blocked, known) == expected
