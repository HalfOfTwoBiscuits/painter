from .tcase_bases import TestUsingGameLoop
from .tcase_states import GameplayTester

class FinalTest(TestUsingGameLoop):
    def test_gameplay(self):
        print ('Testing Painter Graphic and Floor Graphic With Controls')
        self._do_test(GameplayTester)
