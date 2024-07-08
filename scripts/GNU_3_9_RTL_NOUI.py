#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Options 0
# GNU Radio version: 3.10.1.1

from gnuradio import analog
import math
from gnuradio import blocks
from gnuradio import digital
from gnuradio import filter
from gnuradio.filter import firdes
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
import numpy




class options_0(gr.top_block):

    def __init__(self, rx_offset=6600, tx_offset=6500, uri='ip:192.168.2.1'):
        gr.top_block.__init__(self, "Options 0", catch_exceptions=True)

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
        self.connect((self.analog_const_source_x_0_0, 0), (self.blocks_float_to_complex_0_0_0, 1))
        self.connect((self.analog_pwr_squelch_xx_0, 0), (self.rational_resampler_xxx_1_0, 0))
        self.connect((self.analog_quadrature_demod_cf_0, 0), (self.low_pass_filter_0_0_0, 0))
        self.connect((self.analog_quadrature_demod_cf_0_0, 0), (self.digital_clock_recovery_mm_xx_0, 0))
        self.connect((self.analog_sig_source_x_1_0, 0), (self.blocks_multiply_xx_1_0, 1))
        self.connect((self.blocks_and_const_xx_1, 0), (self.blocks_pack_k_bits_bb_0_0, 0))
        self.connect((self.blocks_float_to_complex_0_0_0, 0), (self.blocks_multiply_xx_1_0, 0))
        self.connect((self.blocks_multiply_xx_1_0, 0), (self.low_pass_filter_0_0, 0))
        self.connect((self.blocks_not_xx_0_0, 0), (self.blocks_and_const_xx_1, 0))
        self.connect((self.blocks_pack_k_bits_bb_0_0, 0), (self.blocks_stream_to_tagged_stream_0, 0))
        self.connect((self.blocks_stream_to_tagged_stream_0, 0), (self.pdu_tagged_stream_to_pdu_0, 0))
        self.connect((self.digital_binary_slicer_fb_0, 0), (self.digital_diff_decoder_bb_0, 0))
        self.connect((self.digital_clock_recovery_mm_xx_0, 0), (self.digital_binary_slicer_fb_0, 0))
        self.connect((self.digital_diff_decoder_bb_0, 0), (self.blocks_not_xx_0_0, 0))
        self.connect((self.low_pass_filter_0_0, 0), (self.analog_quadrature_demod_cf_0_0, 0))
        self.connect((self.low_pass_filter_0_0_0, 0), (self.single_pole_iir_filter_xx_0, 0))
        self.connect((self.low_pass_filter_0_1, 0), (self.analog_agc3_xx_0, 0))
        self.connect((self.rational_resampler_xxx_1_0, 0), (self.low_pass_filter_0_1, 0))
        self.connect((self.single_pole_iir_filter_xx_0, 0), (self.blocks_float_to_complex_0_0_0, 0))
        self.connect((self.soapy_rtlsdr_source_0, 0), (self.analog_pwr_squelch_xx_0, 0))


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

    def get_sample_rate(self):
        return self.sample_rate

    def set_sample_rate(self, sample_rate):
        self.sample_rate = sample_rate
        self.analog_sig_source_x_1_0.set_sampling_freq(self.sample_rate)
        self.digital_clock_recovery_mm_xx_0.set_omega(self.sample_rate/self.RX_decimation/self.bit_rate)
        self.low_pass_filter_0_0.set_taps(firdes.low_pass(1, self.sample_rate, 1200, 200, window.WIN_HAMMING, 6.76))
        self.low_pass_filter_0_0_0.set_taps(firdes.low_pass(1, self.sample_rate, 3000, 200, window.WIN_HAMMING, 6.76))
        self.low_pass_filter_0_1.set_taps(firdes.low_pass(1, self.sample_rate, 9600, 1000, window.WIN_HAMMING, 6.76))
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



def argument_parser():
    parser = ArgumentParser()
    parser.add_argument(
        "--rx-offset", dest="rx_offset", type=intx, default=6600,
        help="Set rx_offset [default=%(default)r]")
    parser.add_argument(
        "--tx-offset", dest="tx_offset", type=intx, default=6500,
        help="Set tx_offset [default=%(default)r]")
    return parser


def main(top_block_cls=options_0, options=None):
    if options is None:
        options = argument_parser().parse_args()
    tb = top_block_cls(rx_offset=options.rx_offset, tx_offset=options.tx_offset)

    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()

        sys.exit(0)

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    tb.start()

    try:
        input('Press Enter to quit: ')
    except EOFError:
        pass
    tb.stop()
    tb.wait()


if __name__ == '__main__':
    main()
