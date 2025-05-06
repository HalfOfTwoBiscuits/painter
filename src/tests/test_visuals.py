from .tcase_bases import TestUsingWindow, TestUsingGameLoop
from .tcase_states import PainterViewer, FloorViewer, FloorViewerWithPainter, GameplayTester

class GraphicsTest(TestUsingWindow):
    def test_a(self):
        print ('Testing Painter Graphic')
        self._do_test(PainterViewer)

    def test_floor(self):
        print ('Testing Floor Graphic')
        self._do_test(FloorViewer)

    def test_painter_onfloor(self):
        print ('Testing Painter and Floor Graphics')
        self._do_test(FloorViewerWithPainter)

class VfxTest(TestUsingGameLoop):
    def test_painter_onfloor_withvfx(self):
        print ('Testing Painter and Floor Graphics with Rotate and Shake')
        self._do_test(FloorViewerWithPainter)

'''
class FinalTest(TestUsingGameLoop):
    def test_gameplay(self):
        print ('Testing Painter Graphic and Floor Graphic With Controls')
        self._do_test(GameplayTester)
'''