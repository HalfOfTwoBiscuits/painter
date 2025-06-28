from ..floor_manager import FloorManager

class TestFloorManager(FloorManager):
    @classmethod
    def insert_test_floorpack(cls, pack: list):
        '''Add an already-loaded floorpack to the manager,
        and select it to be played.
        Used in tests, where the floor data is created manually
        and interacted with.'''
        TEST_FLOORPACK_ID = 'TEST'

        cls._floor_packs[TEST_FLOORPACK_ID] = pack
        cls.select_floorpack(TEST_FLOORPACK_ID)