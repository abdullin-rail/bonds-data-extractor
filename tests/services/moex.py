import pytest

from services.moex import MoexService


class TestMoexService:
    def test_get_bonds_list(self):
        service = MoexService()

        boards = service.get_boards()
        assert len(boards) > 0

        board = boards[1]
        bonds = service.get_bonds(board_id=board)
        assert len(bonds) > 0

