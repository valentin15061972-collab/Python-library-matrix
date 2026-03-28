import asyncio
from aiohttp import ClientSession
from typing import List


def parse_matrix(text: str) -> List[List[int]]:
    matrix = []
    for line in text.strip().splitlines():
        line = line.strip()

        if line.startswith('+') and line.endswith('+'):
            continue

        if '|' in line:
            cells = line.split('|')[1:-1]
            row = [int(cell.strip()) for cell in cells]
            matrix.append(row)

    return matrix


def spiral_move_matrix(matrix: List[List[int]]) -> List[int]:
    if not matrix or not matrix[0]:
        return []

    result = []
    top, bottom = 0, len(matrix) - 1
    left, right = 0, len(matrix[0]) - 1

    while top <= bottom and left <= right:
        for i in range(top, bottom + 1):
            result.append(matrix[i][left])
        left += 1

        if left <= right:
            for j in range(left, right + 1):
                result.append(matrix[bottom][j])
        bottom -= 1

        if top <= bottom:
            for i in range(bottom, top - 1, -1):
                result.append(matrix[i][right])
        right -= 1

        if left <= right:
            for j in range(right, left - 1, -1):
                result.append(matrix[top][j])
        top += 1

    return result


async def get_matrix(url: str) -> List[int]:
    try:
        async with ClientSession() as session:
            async with session.get(url, timeout=10) as response:
                if response.status != 200:
                    raise ValueError(f"Сервер вернул HTTP {response.status}: {response.reason}")
                text = await response.text()

        matrix_2d = parse_matrix(text)
        return spiral_move_matrix(matrix_2d)

    except TimeoutError as t:
        raise ValueError(f"Время запроса истекло: {t}")
    except Exception as ex:
        raise ValueError(f"Непредвиденная ошибка: {ex}")


URL = 'https://raw.githubusercontent.com/avito-tech/python-trainee-assignment/main/matrix.txt'


if __name__ == '__main__':
    start = asyncio.run(get_matrix(URL))
    print(start)
