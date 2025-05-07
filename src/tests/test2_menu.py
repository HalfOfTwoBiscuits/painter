from .tcase_bases import TestUsingWindow
from .tcase_states import MenuTester

class MenuTest(TestUsingWindow):
    def test_selectmenu(self):
        print ('Testing Menu Graphics')
        self._do_test(MenuTester)