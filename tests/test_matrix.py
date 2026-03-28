from aioresponses import aioresponses
import pytest
from asyncio import TimeoutError
from src.matrix import parse_matrix, spiral_move_matrix, get_matrix


def test_parse_matrix_normal():
    text = """
    +----+-----+
    | 10 | 200 | 
    +----+-----+
    | 3  | 40  |
    +----+-----+
    """
    expected = [
        [10, 200],
        [3, 40]
    ]
    assert parse_matrix(text) == expected


def test_parse_matrix_empty():
    text = ""
    expected = []
    assert parse_matrix(text) == expected


def test_spiral_move_matrix():
    matrix = [
        [1, 2, 5],
        [3, 4, 6],
        [7, 8, 9]
    ]
    expected = [1, 3, 7, 8, 9, 6, 5, 2, 4]
    assert spiral_move_matrix(matrix) == expected


def test_spiral_move_matrix_empty():
    assert spiral_move_matrix([]) == []
    assert spiral_move_matrix([[]]) == []


@pytest.mark.asyncio
async def test_get_matrix_http_error():
    with aioresponses() as m:
        m.get("https://example.com/matrix.txt", status=404, reason="Not Found")
        with pytest.raises(ValueError, match="Сервер вернул HTTP 404: Not Found"):
            await get_matrix("https://example.com/matrix.txt")


@pytest.mark.asyncio
async def test_get_matrix_timeout():
    with aioresponses() as m:
        m.get("https://example.com/matrix.txt", exception=TimeoutError)
        with pytest.raises(ValueError, match="Время запроса истекло"):
            await get_matrix("https://example.com/matrix.txt")


@pytest.mark.asyncio
async def test_get_matrix_exception():
    with aioresponses() as m:
        m.get("https://example.com/matrix.txt", exception=Exception)
        with pytest.raises(ValueError, match="Непредвиденная ошибка"):
            await get_matrix("https://example.com/matrix.txt")
