# (C) Copyright 2004-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

from pyface.qt import QtGui, QtCore


class RangeSlider(QtGui.QSlider):
    """A slider for ranges.

    This class provides a dual-slider for ranges, where there is a defined
    maximum and minimum, as is a normal slider, but instead of having a
    single slider value, there are 2 slider values.

    This class emits the same signals as the QSlider base class, with the
    exception of valueChanged
    """

    def __init__(self, *args):
        super().__init__(*args)

        self._low = self.minimum()
        self._high = self.maximum()

        self.pressed_control = QtGui.QStyle.SubControl.SC_None
        self.hover_control = QtGui.QStyle.SubControl.SC_None
        self.click_offset = 0

        # 0 for the low, 1 for the high, -1 for both
        self.active_slider = 0

    def low(self):
        return self._low

    def setLow(self, low):
        self._low = low
        self.update()

    def high(self):
        return self._high

    def setHigh(self, high):
        self._high = high
        self.update()

    def paintEvent(self, event):
        # based on
        # http://qt.gitorious.org/qt/qt/blobs/master/src/gui/widgets/qslider.cpp

        painter = QtGui.QPainter(self)
        style = QtGui.QApplication.style()

        for i, value in enumerate([self._low, self._high]):
            opt = QtGui.QStyleOptionSlider()
            self.initStyleOption(opt)

            # Only draw the groove for the first slider so it doesn't get drawn
            # on top of the existing ones every time
            if i == 0:
                opt.subControls = (
                    QtGui.QStyle.SC_SliderGroove | QtGui.QStyle.SC_SliderHandle
                )
            else:
                opt.subControls = QtGui.QStyle.SC_SliderHandle

            if self.tickPosition() != self.NoTicks:
                opt.subControls |= QtGui.QStyle.SC_SliderTickmarks

            if self.pressed_control:
                opt.activeSubControls = self.pressed_control
                opt.state |= QtGui.QStyle.StateFlag.State_Sunken
            else:
                opt.activeSubControls = self.hover_control

            opt.sliderPosition = int(value)
            opt.sliderValue = int(value)
            style.drawComplexControl(
                QtGui.QStyle.ComplexControl.CC_Slider, opt, painter, self
            )

    def mousePressEvent(self, event):
        event.accept()

        style = QtGui.QApplication.style()
        button = event.button()

        # In a normal slider control, when the user clicks on a point in the
        # slider's total range, but not on the slider part of the control the
        # control would jump the slider value to where the user clicked.
        # For this control, clicks which are not direct hits will slide both
        # slider parts

        if button:
            opt = QtGui.QStyleOptionSlider()
            self.initStyleOption(opt)

            self.active_slider = -1

            for i, value in enumerate([self._low, self._high]):
                opt.sliderPosition = int(value)
                hit = style.hitTestComplexControl(
                    style.CC_Slider, opt, event.pos(), self
                )
                if hit == style.SC_SliderHandle:
                    self.active_slider = i
                    self.pressed_control = hit

                    self.triggerAction(self.SliderMove)
                    self.setRepeatAction(self.SliderNoAction)
                    self.setSliderDown(True)
                    break

            if self.active_slider < 0:
                self.pressed_control = QtGui.QStyle.SC_SliderHandle
                self.click_offset = self.__pixelPosToRangeValue(
                    self.__pick(event.pos())
                )
                self.triggerAction(self.SliderMove)
                self.setRepeatAction(self.SliderNoAction)
        else:
            event.ignore()

    def mouseMoveEvent(self, event):
        if self.pressed_control != QtGui.QStyle.SC_SliderHandle:
            event.ignore()
            return

        event.accept()
        new_pos = int(self.__pixelPosToRangeValue(self.__pick(event.pos())))
        opt = QtGui.QStyleOptionSlider()
        self.initStyleOption(opt)

        if self.active_slider < 0:
            offset = new_pos - self.click_offset
            self._high += offset
            self._low += offset
            if self._low < self.minimum():
                diff = self.minimum() - self._low
                self._low += diff
                self._high += diff
            if self._high > self.maximum():
                diff = self.maximum() - self._high
                self._low += diff
                self._high += diff
        elif self.active_slider == 0:
            if new_pos >= self._high:
                new_pos = self._high - 1
            self._low = new_pos
        else:
            if new_pos <= self._low:
                new_pos = self._low + 1
            self._high = new_pos

        self.click_offset = new_pos

        self.update()

        self.sliderMoved.emit(new_pos)

    def __pick(self, pt):
        if self.orientation() == QtCore.Qt.Orientation.Horizontal:
            return pt.x()
        else:
            return pt.y()

    def __pixelPosToRangeValue(self, pos):
        opt = QtGui.QStyleOptionSlider()
        self.initStyleOption(opt)
        style = QtGui.QApplication.style()

        gr = style.subControlRect(
            style.CC_Slider, opt, style.SC_SliderGroove, self
        )
        sr = style.subControlRect(
            style.CC_Slider, opt, style.SC_SliderHandle, self
        )

        if self.orientation() == QtCore.Qt.Orientation.Horizontal:
            slider_length = sr.width()
            slider_min = gr.x()
            slider_max = gr.right() - slider_length + 1
        else:
            slider_length = sr.height()
            slider_min = gr.y()
            slider_max = gr.bottom() - slider_length + 1

        return style.sliderValueFromPosition(
            self.minimum(),
            self.maximum(),
            pos - slider_min,
            slider_max - slider_min,
            opt.upsideDown,
        )


if __name__ == "__main__":
    import sys

    def echo(value):
        print(value)

    app = QtGui.QApplication(sys.argv)
    slider = RangeSlider()
    slider.setMinimum(0)
    slider.setMaximum(10000)
    slider.setLow(0)
    slider.setHigh(10000)
    slider.sliderMoved.connect(echo)
    slider.show()
    app.exec_()
