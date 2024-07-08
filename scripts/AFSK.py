#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Afsk
# GNU Radio version: 3.10.1.1

from packaging.version import Version as StrictVersion

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print("Warning: failed to XInitThreads()")

from PyQt5 import Qt
from gnuradio import qtgui
from gnuradio.filter import firdes
import sip
from gnuradio import analog
import math
from gnuradio import blocks
from gnuradio import digital
from gnuradio import filter
from gnuradio import gr
from gnuradio.fft import window
import sys
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from gnuradio import gr, pdu
from gnuradio import network
from gnuradio import soapy
from gnuradio.qtgui import Range, RangeWidget
from PyQt5 import QtCore
import numpy



from gnuradio import qtgui

class AFSK(gr.top_block, Qt.QWidget):

    def __init__(self, rx_offset=6600, tx_offset=6500, uri='ip:192.168.2.1'):
        gr.top_block.__init__(self, "Afsk", catch_exceptions=True)
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Afsk")
        qtgui.util.check_set_qss()
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except:
            pass
        self.top_scroll_layout = Qt.QVBoxLayout()
        self.setLayout(self.top_scroll_layout)
        self.top_scroll = Qt.QScrollArea()
        self.top_scroll.setFrameStyle(Qt.QFrame.NoFrame)
        self.top_scroll_layout.addWidget(self.top_scroll)
        self.top_scroll.setWidgetResizable(True)
        self.top_widget = Qt.QWidget()
        self.top_scroll.setWidget(self.top_widget)
        self.top_layout = Qt.QVBoxLayout(self.top_widget)
        self.top_grid_layout = Qt.QGridLayout()
        self.top_layout.addLayout(self.top_grid_layout)

        self.settings = Qt.QSettings("GNU Radio", "AFSK")

        try:
            if StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
                self.restoreGeometry(self.settings.value("geometry").toByteArray())
            else:
                self.restoreGeometry(self.settings.value("geometry"))
        except:
            pass

        ##################################################
        # Parameters
        ##################################################
        self.rx_offset = rx_offset
        self.tx_offset = tx_offset
        self.uri = uri

        ##################################################
        # Variables
        ##################################################
        self.bit_rate = bit_rate = 1200
        self.sample_rate = sample_rate = bit_rate * 32
        self.gain = gain = 10
        self.freq_offset = freq_offset = 0
        self.freq = freq = 145895000
        self.alpha = alpha = 1
        self.RX_decimation = RX_decimation = 8

        ##################################################
        # Blocks
        ##################################################
        self._gain_range = Range(0, 50, 1, 10, 200)
        self._gain_win = RangeWidget(self._gain_range, self.set_gain, "'gain'", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_grid_layout.addWidget(self._gain_win, 2, 1, 1, 2)
        for r in range(2, 3):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(1, 3):
            self.top_grid_layout.setColumnStretch(c, 1)
        self._freq_offset_range = Range(-6000, 6000, 1, 0, 200)
        self._freq_offset_win = RangeWidget(self._freq_offset_range, self.set_freq_offset, "'freq_offset'", "counter_slider", int, QtCore.Qt.Horizontal)
        self.top_grid_layout.addWidget(self._freq_offset_win, 1, 1, 1, 2)
        for r in range(1, 2):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(1, 3):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.soapy_rtlsdr_source_0 = None
        dev = 'driver=rtlsdr'
        stream_args = ''
        tune_args = ['']
        settings = ['']

        self.soapy_rtlsdr_source_0 = soapy.source(dev, "fc32", 1, '',
                                  stream_args, tune_args, settings)
        self.soapy_rtlsdr_source_0.set_sample_rate(0, 1920000.000000)
        self.soapy_rtlsdr_source_0.set_gain_mode(0, False)
        self.soapy_rtlsdr_source_0.set_frequency(0, int(145895000-sample_rate/4)-freq_offset)
        self.soapy_rtlsdr_source_0.set_frequency_correction(0, 0)
        self.soapy_rtlsdr_source_0.set_gain(0, 'TUNER', gain)
        self.single_pole_iir_filter_xx_0 = filter.single_pole_iir_filter_ff(0.74227, 1)
        self.rational_resampler_xxx_1_0 = filter.rational_resampler_ccc(
                interpolation=1,
                decimation=50,
                taps=[],
                fractional_bw=0)
        self.qtgui_time_sink_x_0_0_1_1_0 = qtgui.time_sink_f(
            500, #size
            bit_rate, #samp_rate
            "Bits before decoder", #name
            1, #number of inputs
            None # parent
        )
        self.qtgui_time_sink_x_0_0_1_1_0.set_update_time(0.10)
        self.qtgui_time_sink_x_0_0_1_1_0.set_y_axis(0, 1)

        self.qtgui_time_sink_x_0_0_1_1_0.set_y_label('Amplitude', "")

        self.qtgui_time_sink_x_0_0_1_1_0.enable_tags(False)
        self.qtgui_time_sink_x_0_0_1_1_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.qtgui_time_sink_x_0_0_1_1_0.enable_autoscale(False)
        self.qtgui_time_sink_x_0_0_1_1_0.enable_grid(True)
        self.qtgui_time_sink_x_0_0_1_1_0.enable_axis_labels(True)
        self.qtgui_time_sink_x_0_0_1_1_0.enable_control_panel(False)
        self.qtgui_time_sink_x_0_0_1_1_0.enable_stem_plot(False)


        labels = ['', '', '', '', '',
            '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ['blue', 'red', 'green', 'black', 'cyan',
            'magenta', 'yellow', 'dark red', 'dark green', 'dark blue']
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]
        styles = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        markers = [-1, -1, -1, -1, -1,
            -1, -1, -1, -1, -1]


        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_time_sink_x_0_0_1_1_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_time_sink_x_0_0_1_1_0.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_0_0_1_1_0.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_0_0_1_1_0.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_0_0_1_1_0.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_0_0_1_1_0.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_0_0_1_1_0.set_line_alpha(i, alphas[i])

        self._qtgui_time_sink_x_0_0_1_1_0_win = sip.wrapinstance(self.qtgui_time_sink_x_0_0_1_1_0.qwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_time_sink_x_0_0_1_1_0_win, 11, 1, 1, 2)
        for r in range(11, 12):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(1, 3):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.qtgui_time_sink_x_0_0_1_1 = qtgui.time_sink_f(
            500, #size
            bit_rate, #samp_rate
            "Bits after Descrambler", #name
            1, #number of inputs
            None # parent
        )
        self.qtgui_time_sink_x_0_0_1_1.set_update_time(0.10)
        self.qtgui_time_sink_x_0_0_1_1.set_y_axis(0, 1)

        self.qtgui_time_sink_x_0_0_1_1.set_y_label('Amplitude', "")

        self.qtgui_time_sink_x_0_0_1_1.enable_tags(False)
        self.qtgui_time_sink_x_0_0_1_1.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.qtgui_time_sink_x_0_0_1_1.enable_autoscale(False)
        self.qtgui_time_sink_x_0_0_1_1.enable_grid(True)
        self.qtgui_time_sink_x_0_0_1_1.enable_axis_labels(True)
        self.qtgui_time_sink_x_0_0_1_1.enable_control_panel(False)
        self.qtgui_time_sink_x_0_0_1_1.enable_stem_plot(False)


        labels = ['', '', '', '', '',
            '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ['blue', 'red', 'green', 'black', 'cyan',
            'magenta', 'yellow', 'dark red', 'dark green', 'dark blue']
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]
        styles = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        markers = [-1, -1, -1, -1, -1,
            -1, -1, -1, -1, -1]


        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_time_sink_x_0_0_1_1.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_time_sink_x_0_0_1_1.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_0_0_1_1.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_0_0_1_1.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_0_0_1_1.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_0_0_1_1.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_0_0_1_1.set_line_alpha(i, alphas[i])

        self._qtgui_time_sink_x_0_0_1_1_win = sip.wrapinstance(self.qtgui_time_sink_x_0_0_1_1.qwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_time_sink_x_0_0_1_1_win, 12, 1, 1, 2)
        for r in range(12, 13):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(1, 3):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.qtgui_time_sink_x_0_0_1_0_0_0 = qtgui.time_sink_c(
            200, #size
            sample_rate/RX_decimation, #samp_rate
            "Received Bell 202 signal after de-emphasis", #name
            1, #number of inputs
            None # parent
        )
        self.qtgui_time_sink_x_0_0_1_0_0_0.set_update_time(0.10)
        self.qtgui_time_sink_x_0_0_1_0_0_0.set_y_axis(-1, 1)

        self.qtgui_time_sink_x_0_0_1_0_0_0.set_y_label('Amplitude', "")

        self.qtgui_time_sink_x_0_0_1_0_0_0.enable_tags(True)
        self.qtgui_time_sink_x_0_0_1_0_0_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.qtgui_time_sink_x_0_0_1_0_0_0.enable_autoscale(False)
        self.qtgui_time_sink_x_0_0_1_0_0_0.enable_grid(True)
        self.qtgui_time_sink_x_0_0_1_0_0_0.enable_axis_labels(True)
        self.qtgui_time_sink_x_0_0_1_0_0_0.enable_control_panel(False)
        self.qtgui_time_sink_x_0_0_1_0_0_0.enable_stem_plot(False)


        labels = ['', '', '', '', '',
            '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ['blue', 'red', 'green', 'black', 'cyan',
            'magenta', 'yellow', 'dark red', 'dark green', 'dark blue']
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]
        styles = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        markers = [-1, -1, -1, -1, -1,
            -1, -1, -1, -1, -1]


        for i in range(2):
            if len(labels[i]) == 0:
                if (i % 2 == 0):
                    self.qtgui_time_sink_x_0_0_1_0_0_0.set_line_label(i, "Re{{Data {0}}}".format(i/2))
                else:
                    self.qtgui_time_sink_x_0_0_1_0_0_0.set_line_label(i, "Im{{Data {0}}}".format(i/2))
            else:
                self.qtgui_time_sink_x_0_0_1_0_0_0.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_0_0_1_0_0_0.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_0_0_1_0_0_0.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_0_0_1_0_0_0.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_0_0_1_0_0_0.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_0_0_1_0_0_0.set_line_alpha(i, alphas[i])

        self._qtgui_time_sink_x_0_0_1_0_0_0_win = sip.wrapinstance(self.qtgui_time_sink_x_0_0_1_0_0_0.qwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_time_sink_x_0_0_1_0_0_0_win, 7, 1, 1, 2)
        for r in range(7, 8):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(1, 3):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.qtgui_time_sink_x_0_0_1_0_0 = qtgui.time_sink_f(
            1000, #size
            sample_rate/RX_decimation, #samp_rate
            "Received Bell 202 signal after de-emphasis", #name
            1, #number of inputs
            None # parent
        )
        self.qtgui_time_sink_x_0_0_1_0_0.set_update_time(0.10)
        self.qtgui_time_sink_x_0_0_1_0_0.set_y_axis(-1, 1)

        self.qtgui_time_sink_x_0_0_1_0_0.set_y_label('Amplitude', "")

        self.qtgui_time_sink_x_0_0_1_0_0.enable_tags(True)
        self.qtgui_time_sink_x_0_0_1_0_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.qtgui_time_sink_x_0_0_1_0_0.enable_autoscale(True)
        self.qtgui_time_sink_x_0_0_1_0_0.enable_grid(True)
        self.qtgui_time_sink_x_0_0_1_0_0.enable_axis_labels(True)
        self.qtgui_time_sink_x_0_0_1_0_0.enable_control_panel(False)
        self.qtgui_time_sink_x_0_0_1_0_0.enable_stem_plot(False)


        labels = ['', '', '', '', '',
            '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ['blue', 'red', 'green', 'black', 'cyan',
            'magenta', 'yellow', 'dark red', 'dark green', 'dark blue']
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]
        styles = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        markers = [-1, -1, -1, -1, -1,
            -1, -1, -1, -1, -1]


        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_time_sink_x_0_0_1_0_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_time_sink_x_0_0_1_0_0.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_0_0_1_0_0.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_0_0_1_0_0.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_0_0_1_0_0.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_0_0_1_0_0.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_0_0_1_0_0.set_line_alpha(i, alphas[i])

        self._qtgui_time_sink_x_0_0_1_0_0_win = sip.wrapinstance(self.qtgui_time_sink_x_0_0_1_0_0.qwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_time_sink_x_0_0_1_0_0_win, 8, 1, 1, 2)
        for r in range(8, 9):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(1, 3):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.qtgui_time_sink_x_0_0_1_0 = qtgui.time_sink_f(
            1000, #size
            sample_rate/RX_decimation, #samp_rate
            "Bell 202 signal before timing recovery, @4SPS", #name
            1, #number of inputs
            None # parent
        )
        self.qtgui_time_sink_x_0_0_1_0.set_update_time(0.10)
        self.qtgui_time_sink_x_0_0_1_0.set_y_axis(-1.5, 1.5)

        self.qtgui_time_sink_x_0_0_1_0.set_y_label('Amplitude', "")

        self.qtgui_time_sink_x_0_0_1_0.enable_tags(True)
        self.qtgui_time_sink_x_0_0_1_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.qtgui_time_sink_x_0_0_1_0.enable_autoscale(False)
        self.qtgui_time_sink_x_0_0_1_0.enable_grid(True)
        self.qtgui_time_sink_x_0_0_1_0.enable_axis_labels(True)
        self.qtgui_time_sink_x_0_0_1_0.enable_control_panel(False)
        self.qtgui_time_sink_x_0_0_1_0.enable_stem_plot(False)


        labels = ['', '', '', '', '',
            '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ['blue', 'red', 'green', 'black', 'cyan',
            'magenta', 'yellow', 'dark red', 'dark green', 'dark blue']
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]
        styles = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        markers = [-1, -1, -1, -1, -1,
            -1, -1, -1, -1, -1]


        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_time_sink_x_0_0_1_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_time_sink_x_0_0_1_0.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_0_0_1_0.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_0_0_1_0.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_0_0_1_0.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_0_0_1_0.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_0_0_1_0.set_line_alpha(i, alphas[i])

        self._qtgui_time_sink_x_0_0_1_0_win = sip.wrapinstance(self.qtgui_time_sink_x_0_0_1_0.qwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_time_sink_x_0_0_1_0_win, 9, 2, 1, 1)
        for r in range(9, 10):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(2, 3):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.qtgui_time_sink_x_0_0_1 = qtgui.time_sink_f(
            1000, #size
            bit_rate, #samp_rate
            "Signal after timing recovery, @1SPS", #name
            1, #number of inputs
            None # parent
        )
        self.qtgui_time_sink_x_0_0_1.set_update_time(0.10)
        self.qtgui_time_sink_x_0_0_1.set_y_axis(-1, 1)

        self.qtgui_time_sink_x_0_0_1.set_y_label('Amplitude', "")

        self.qtgui_time_sink_x_0_0_1.enable_tags(True)
        self.qtgui_time_sink_x_0_0_1.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.qtgui_time_sink_x_0_0_1.enable_autoscale(True)
        self.qtgui_time_sink_x_0_0_1.enable_grid(True)
        self.qtgui_time_sink_x_0_0_1.enable_axis_labels(True)
        self.qtgui_time_sink_x_0_0_1.enable_control_panel(False)
        self.qtgui_time_sink_x_0_0_1.enable_stem_plot(False)


        labels = ['', '', '', '', '',
            '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ['blue', 'red', 'green', 'black', 'cyan',
            'magenta', 'yellow', 'dark red', 'dark green', 'dark blue']
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]
        styles = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        markers = [-1, -1, -1, -1, -1,
            -1, -1, -1, -1, -1]


        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_time_sink_x_0_0_1.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_time_sink_x_0_0_1.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_0_0_1.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_0_0_1.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_0_0_1.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_0_0_1.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_0_0_1.set_line_alpha(i, alphas[i])

        self._qtgui_time_sink_x_0_0_1_win = sip.wrapinstance(self.qtgui_time_sink_x_0_0_1.qwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_time_sink_x_0_0_1_win, 10, 2, 1, 1)
        for r in range(10, 11):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(2, 3):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.qtgui_freq_sink_x_0_0_0_0 = qtgui.freq_sink_c(
            2048, #size
            window.WIN_BLACKMAN_hARRIS, #wintype
            0, #fc
            sample_rate, #bw
            "RX AFSK baseband signal spectrum", #name
            1,
            None # parent
        )
        self.qtgui_freq_sink_x_0_0_0_0.set_update_time(0.10)
        self.qtgui_freq_sink_x_0_0_0_0.set_y_axis(-140, 10)
        self.qtgui_freq_sink_x_0_0_0_0.set_y_label('Relative Gain', 'dB')
        self.qtgui_freq_sink_x_0_0_0_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, 0.0, 0, "")
        self.qtgui_freq_sink_x_0_0_0_0.enable_autoscale(True)
        self.qtgui_freq_sink_x_0_0_0_0.enable_grid(True)
        self.qtgui_freq_sink_x_0_0_0_0.set_fft_average(0.1)
        self.qtgui_freq_sink_x_0_0_0_0.enable_axis_labels(True)
        self.qtgui_freq_sink_x_0_0_0_0.enable_control_panel(False)
        self.qtgui_freq_sink_x_0_0_0_0.set_fft_window_normalized(False)



        labels = ['', '', '', '', '',
            '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
            "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_freq_sink_x_0_0_0_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_freq_sink_x_0_0_0_0.set_line_label(i, labels[i])
            self.qtgui_freq_sink_x_0_0_0_0.set_line_width(i, widths[i])
            self.qtgui_freq_sink_x_0_0_0_0.set_line_color(i, colors[i])
            self.qtgui_freq_sink_x_0_0_0_0.set_line_alpha(i, alphas[i])

        self._qtgui_freq_sink_x_0_0_0_0_win = sip.wrapinstance(self.qtgui_freq_sink_x_0_0_0_0.qwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_freq_sink_x_0_0_0_0_win, 6, 1, 1, 2)
        for r in range(6, 7):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(1, 3):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.qtgui_freq_sink_x_0_0_0 = qtgui.freq_sink_f(
            256, #size
            window.WIN_BLACKMAN_hARRIS, #wintype
            0, #fc
            sample_rate/RX_decimation, #bw
            "Bell 202 demodulated signal", #name
            1,
            None # parent
        )
        self.qtgui_freq_sink_x_0_0_0.set_update_time(0.10)
        self.qtgui_freq_sink_x_0_0_0.set_y_axis(-140, 10)
        self.qtgui_freq_sink_x_0_0_0.set_y_label('Relative Gain', 'dB')
        self.qtgui_freq_sink_x_0_0_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, 0.0, 0, "")
        self.qtgui_freq_sink_x_0_0_0.enable_autoscale(True)
        self.qtgui_freq_sink_x_0_0_0.enable_grid(True)
        self.qtgui_freq_sink_x_0_0_0.set_fft_average(0.1)
        self.qtgui_freq_sink_x_0_0_0.enable_axis_labels(True)
        self.qtgui_freq_sink_x_0_0_0.enable_control_panel(False)
        self.qtgui_freq_sink_x_0_0_0.set_fft_window_normalized(False)


        self.qtgui_freq_sink_x_0_0_0.set_plot_pos_half(not True)

        labels = ['', '', '', '', '',
            '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
            "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_freq_sink_x_0_0_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_freq_sink_x_0_0_0.set_line_label(i, labels[i])
            self.qtgui_freq_sink_x_0_0_0.set_line_width(i, widths[i])
            self.qtgui_freq_sink_x_0_0_0.set_line_color(i, colors[i])
            self.qtgui_freq_sink_x_0_0_0.set_line_alpha(i, alphas[i])

        self._qtgui_freq_sink_x_0_0_0_win = sip.wrapinstance(self.qtgui_freq_sink_x_0_0_0.qwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_freq_sink_x_0_0_0_win, 9, 1, 1, 1)
        for r in range(9, 10):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(1, 2):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.qtgui_const_sink_x_0_0 = qtgui.const_sink_c(
            840-84, #size
            'Received, synch constellation', #name
            1, #number of inputs
            None # parent
        )
        self.qtgui_const_sink_x_0_0.set_update_time(0.10)
        self.qtgui_const_sink_x_0_0.set_y_axis(-2, 2)
        self.qtgui_const_sink_x_0_0.set_x_axis(-2, 2)
        self.qtgui_const_sink_x_0_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, "")
        self.qtgui_const_sink_x_0_0.enable_autoscale(False)
        self.qtgui_const_sink_x_0_0.enable_grid(False)
        self.qtgui_const_sink_x_0_0.enable_axis_labels(True)


        labels = ['', '', '', '', '',
            '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["blue", "red", "red", "red", "red",
            "red", "red", "red", "red", "red"]
        styles = [0, 0, 0, 0, 0,
            0, 0, 0, 0, 0]
        markers = [0, 0, 0, 0, 0,
            0, 0, 0, 0, 0]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_const_sink_x_0_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_const_sink_x_0_0.set_line_label(i, labels[i])
            self.qtgui_const_sink_x_0_0.set_line_width(i, widths[i])
            self.qtgui_const_sink_x_0_0.set_line_color(i, colors[i])
            self.qtgui_const_sink_x_0_0.set_line_style(i, styles[i])
            self.qtgui_const_sink_x_0_0.set_line_marker(i, markers[i])
            self.qtgui_const_sink_x_0_0.set_line_alpha(i, alphas[i])

        self._qtgui_const_sink_x_0_0_win = sip.wrapinstance(self.qtgui_const_sink_x_0_0.qwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_const_sink_x_0_0_win, 10, 1, 1, 1)
        for r in range(10, 11):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(1, 2):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.pdu_tagged_stream_to_pdu_0 = pdu.tagged_stream_to_pdu(gr.types.byte_t, 'packet_len')
        self.network_socket_pdu_0 = network.socket_pdu('TCP_SERVER', '', '52001', 1500, False)
        self.low_pass_filter_0_1 = filter.fir_filter_ccf(
            1,
            firdes.low_pass(
                1,
                sample_rate,
                9600,
                1000,
                window.WIN_HAMMING,
                6.76))
        self.low_pass_filter_0_0_0 = filter.fir_filter_fff(
            1,
            firdes.low_pass(
                1,
                sample_rate,
                3000,
                200,
                window.WIN_HAMMING,
                6.76))
        self.low_pass_filter_0_0 = filter.fir_filter_ccf(
            RX_decimation,
            firdes.low_pass(
                1,
                sample_rate,
                1200,
                200,
                window.WIN_HAMMING,
                6.76))
        self.digital_diff_decoder_bb_0 = digital.diff_decoder_bb(2, digital.DIFF_DIFFERENTIAL)
        self.digital_clock_recovery_mm_xx_0 = digital.clock_recovery_mm_ff(sample_rate/RX_decimation/bit_rate, .1, .5, 0.175, 0.005)
        self.digital_binary_slicer_fb_0 = digital.binary_slicer_fb()
        self.blocks_stream_to_tagged_stream_0 = blocks.stream_to_tagged_stream(gr.sizeof_char, 1, 1, "packet_len")
        self.blocks_pack_k_bits_bb_0_0 = blocks.pack_k_bits_bb(8)
        self.blocks_not_xx_0_0 = blocks.not_bb()
        self.blocks_multiply_xx_1_0 = blocks.multiply_vcc(1)
        self.blocks_float_to_complex_0_0_0 = blocks.float_to_complex(1)
        self.blocks_float_to_complex_0 = blocks.float_to_complex(1)
        self.blocks_char_to_float_0_0_0 = blocks.char_to_float(1, 1)
        self.blocks_char_to_float_0_0 = blocks.char_to_float(1, 1)
        self.blocks_and_const_xx_1 = blocks.and_const_bb(1)
        self.analog_sig_source_x_1_0 = analog.sig_source_c(sample_rate, analog.GR_COS_WAVE, -1700, 1, 0, 0)
        self.analog_quadrature_demod_cf_0_0 = analog.quadrature_demod_cf(1.5)
        self.analog_quadrature_demod_cf_0 = analog.quadrature_demod_cf(1.2)
        self.analog_pwr_squelch_xx_0 = analog.pwr_squelch_cc(-40, 1e-4, 0, True)
        self.analog_const_source_x_0_0 = analog.sig_source_f(0, analog.GR_CONST_WAVE, 0, 0, 0)
        self.analog_agc3_xx_0 = analog.agc3_cc(1e-4, 1e-4, 1.0, 1.0, 1)
        self.analog_agc3_xx_0.set_max_gain(65536)


        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.pdu_tagged_stream_to_pdu_0, 'pdus'), (self.network_socket_pdu_0, 'pdus'))
        self.connect((self.analog_agc3_xx_0, 0), (self.analog_quadrature_demod_cf_0, 0))
        self.connect((self.analog_agc3_xx_0, 0), (self.qtgui_freq_sink_x_0_0_0_0, 0))
        self.connect((self.analog_agc3_xx_0, 0), (self.qtgui_time_sink_x_0_0_1_0_0_0, 0))
        self.connect((self.analog_const_source_x_0_0, 0), (self.blocks_float_to_complex_0_0_0, 1))
        self.connect((self.analog_pwr_squelch_xx_0, 0), (self.rational_resampler_xxx_1_0, 0))
        self.connect((self.analog_quadrature_demod_cf_0, 0), (self.low_pass_filter_0_0_0, 0))
        self.connect((self.analog_quadrature_demod_cf_0_0, 0), (self.digital_clock_recovery_mm_xx_0, 0))
        self.connect((self.analog_quadrature_demod_cf_0_0, 0), (self.qtgui_freq_sink_x_0_0_0, 0))
        self.connect((self.analog_quadrature_demod_cf_0_0, 0), (self.qtgui_time_sink_x_0_0_1_0, 0))
        self.connect((self.analog_sig_source_x_1_0, 0), (self.blocks_multiply_xx_1_0, 1))
        self.connect((self.blocks_and_const_xx_1, 0), (self.blocks_char_to_float_0_0, 0))
        self.connect((self.blocks_and_const_xx_1, 0), (self.blocks_pack_k_bits_bb_0_0, 0))
        self.connect((self.blocks_char_to_float_0_0, 0), (self.qtgui_time_sink_x_0_0_1_1, 0))
        self.connect((self.blocks_char_to_float_0_0_0, 0), (self.qtgui_time_sink_x_0_0_1_1_0, 0))
        self.connect((self.blocks_float_to_complex_0, 0), (self.qtgui_const_sink_x_0_0, 0))
        self.connect((self.blocks_float_to_complex_0_0_0, 0), (self.blocks_multiply_xx_1_0, 0))
        self.connect((self.blocks_multiply_xx_1_0, 0), (self.low_pass_filter_0_0, 0))
        self.connect((self.blocks_not_xx_0_0, 0), (self.blocks_and_const_xx_1, 0))
        self.connect((self.blocks_pack_k_bits_bb_0_0, 0), (self.blocks_stream_to_tagged_stream_0, 0))
        self.connect((self.blocks_stream_to_tagged_stream_0, 0), (self.pdu_tagged_stream_to_pdu_0, 0))
        self.connect((self.digital_binary_slicer_fb_0, 0), (self.blocks_char_to_float_0_0_0, 0))
        self.connect((self.digital_binary_slicer_fb_0, 0), (self.digital_diff_decoder_bb_0, 0))
        self.connect((self.digital_clock_recovery_mm_xx_0, 0), (self.blocks_float_to_complex_0, 0))
        self.connect((self.digital_clock_recovery_mm_xx_0, 0), (self.digital_binary_slicer_fb_0, 0))
        self.connect((self.digital_clock_recovery_mm_xx_0, 0), (self.qtgui_time_sink_x_0_0_1, 0))
        self.connect((self.digital_diff_decoder_bb_0, 0), (self.blocks_not_xx_0_0, 0))
        self.connect((self.low_pass_filter_0_0, 0), (self.analog_quadrature_demod_cf_0_0, 0))
        self.connect((self.low_pass_filter_0_0_0, 0), (self.single_pole_iir_filter_xx_0, 0))
        self.connect((self.low_pass_filter_0_1, 0), (self.analog_agc3_xx_0, 0))
        self.connect((self.rational_resampler_xxx_1_0, 0), (self.low_pass_filter_0_1, 0))
        self.connect((self.single_pole_iir_filter_xx_0, 0), (self.blocks_float_to_complex_0_0_0, 0))
        self.connect((self.single_pole_iir_filter_xx_0, 0), (self.qtgui_time_sink_x_0_0_1_0_0, 0))
        self.connect((self.soapy_rtlsdr_source_0, 0), (self.analog_pwr_squelch_xx_0, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "AFSK")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

    def get_rx_offset(self):
        return self.rx_offset

    def set_rx_offset(self, rx_offset):
        self.rx_offset = rx_offset

    def get_tx_offset(self):
        return self.tx_offset

    def set_tx_offset(self, tx_offset):
        self.tx_offset = tx_offset

    def get_uri(self):
        return self.uri

    def set_uri(self, uri):
        self.uri = uri

    def get_bit_rate(self):
        return self.bit_rate

    def set_bit_rate(self, bit_rate):
        self.bit_rate = bit_rate
        self.set_sample_rate(self.bit_rate * 32)
        self.digital_clock_recovery_mm_xx_0.set_omega(self.sample_rate/self.RX_decimation/self.bit_rate)
        self.qtgui_time_sink_x_0_0_1.set_samp_rate(self.bit_rate)
        self.qtgui_time_sink_x_0_0_1_1.set_samp_rate(self.bit_rate)
        self.qtgui_time_sink_x_0_0_1_1_0.set_samp_rate(self.bit_rate)

    def get_sample_rate(self):
        return self.sample_rate

    def set_sample_rate(self, sample_rate):
        self.sample_rate = sample_rate
        self.analog_sig_source_x_1_0.set_sampling_freq(self.sample_rate)
        self.digital_clock_recovery_mm_xx_0.set_omega(self.sample_rate/self.RX_decimation/self.bit_rate)
        self.low_pass_filter_0_0.set_taps(firdes.low_pass(1, self.sample_rate, 1200, 200, window.WIN_HAMMING, 6.76))
        self.low_pass_filter_0_0_0.set_taps(firdes.low_pass(1, self.sample_rate, 3000, 200, window.WIN_HAMMING, 6.76))
        self.low_pass_filter_0_1.set_taps(firdes.low_pass(1, self.sample_rate, 9600, 1000, window.WIN_HAMMING, 6.76))
        self.qtgui_freq_sink_x_0_0_0.set_frequency_range(0, self.sample_rate/self.RX_decimation)
        self.qtgui_freq_sink_x_0_0_0_0.set_frequency_range(0, self.sample_rate)
        self.qtgui_time_sink_x_0_0_1_0.set_samp_rate(self.sample_rate/self.RX_decimation)
        self.qtgui_time_sink_x_0_0_1_0_0.set_samp_rate(self.sample_rate/self.RX_decimation)
        self.qtgui_time_sink_x_0_0_1_0_0_0.set_samp_rate(self.sample_rate/self.RX_decimation)
        self.soapy_rtlsdr_source_0.set_frequency(0, int(145895000-self.sample_rate/4)-self.freq_offset)

    def get_gain(self):
        return self.gain

    def set_gain(self, gain):
        self.gain = gain
        self.soapy_rtlsdr_source_0.set_gain(0, 'TUNER', self.gain)

    def get_freq_offset(self):
        return self.freq_offset

    def set_freq_offset(self, freq_offset):
        self.freq_offset = freq_offset
        self.soapy_rtlsdr_source_0.set_frequency(0, int(145895000-self.sample_rate/4)-self.freq_offset)

    def get_freq(self):
        return self.freq

    def set_freq(self, freq):
        self.freq = freq

    def get_alpha(self):
        return self.alpha

    def set_alpha(self, alpha):
        self.alpha = alpha

    def get_RX_decimation(self):
        return self.RX_decimation

    def set_RX_decimation(self, RX_decimation):
        self.RX_decimation = RX_decimation
        self.digital_clock_recovery_mm_xx_0.set_omega(self.sample_rate/self.RX_decimation/self.bit_rate)
        self.qtgui_freq_sink_x_0_0_0.set_frequency_range(0, self.sample_rate/self.RX_decimation)
        self.qtgui_time_sink_x_0_0_1_0.set_samp_rate(self.sample_rate/self.RX_decimation)
        self.qtgui_time_sink_x_0_0_1_0_0.set_samp_rate(self.sample_rate/self.RX_decimation)
        self.qtgui_time_sink_x_0_0_1_0_0_0.set_samp_rate(self.sample_rate/self.RX_decimation)



def argument_parser():
    parser = ArgumentParser()
    parser.add_argument(
        "--rx-offset", dest="rx_offset", type=intx, default=6600,
        help="Set rx_offset [default=%(default)r]")
    parser.add_argument(
        "--tx-offset", dest="tx_offset", type=intx, default=6500,
        help="Set tx_offset [default=%(default)r]")
    return parser


def main(top_block_cls=AFSK, options=None):
    if options is None:
        options = argument_parser().parse_args()

    if StrictVersion("4.5.0") <= StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
        style = gr.prefs().get_string('qtgui', 'style', 'raster')
        Qt.QApplication.setGraphicsSystem(style)
    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls(rx_offset=options.rx_offset, tx_offset=options.tx_offset)

    tb.start()

    tb.show()

    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()

        Qt.QApplication.quit()

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    timer = Qt.QTimer()
    timer.start(500)
    timer.timeout.connect(lambda: None)

    qapp.exec_()

if __name__ == '__main__':
    main()
