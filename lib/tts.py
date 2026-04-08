#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ___        AlarmPi V 1.1.1 by nickpettican            ___
# ___   Your smart alarm clock for the Raspberry Pi     ___

# ___        Copyright 2017 Nicolas Pettican            ___

# ___    This software is licensed under the Apache 2   ___
# ___    license. You may not use this file except in   ___
# ___    compliance with the License.                   ___
# ___    You may obtain a copy of the License at        ___

# ___    http://www.apache.org/licenses/LICENSE-2.0     ___

# ___    Unless required by applicable law or agreed    ___
# ___    to in writing, software distributed under      ___
# ___    the License is distributed on an "AS IS"       ___
# ___    BASIS, WITHOUT WARRANTIES OR CONDITIONS OF     ___
# ___    ANY KIND, either express or implied. See the   ___
# ___    License for the specific language governing    ___
# ___    permissions and limitations under the License. ___

# TTS backends:
#   Linux (Raspberry Pi) — Piper TTS binary + ONNX voice model
#   macOS               — built-in `say` command (for local testing)
#
# Piper: https://github.com/rhasspy/piper
# Choose and download a voice model from https://huggingface.co/rhasspy/piper-voices

import os
import subprocess
import sys
import tempfile

import pygame


class Speaker:

    def __init__(self, piper_executable, piper_model):
        self.platform = 'macos' if sys.platform == 'darwin' else 'linux'

        if self.platform == 'linux':
            if not piper_executable or not piper_model:
                raise ValueError(
                    'piper_executable and piper_model are required on Linux. '
                    'See https://github.com/rhasspy/piper for setup instructions.'
                )
            if not os.path.isfile(piper_model):
                raise FileNotFoundError(f'Piper model not found: {piper_model}')
            self.piper_executable = piper_executable
            self.piper_model      = piper_model

    def talk(self, text):
        print(text)
        try:
            if self.platform == 'macos':
                subprocess.run(['say', text], check=True)
            else:
                self._piper(text)
        except Exception as e:
            print(f'TTS error: {e}')

    def _piper(self, text):
        tmp_fd, tmp_path = tempfile.mkstemp(suffix='.wav')
        os.close(tmp_fd)
        try:
            subprocess.run(
                [self.piper_executable,
                 '--model',       self.piper_model,
                 '--output_file', tmp_path],
                input=text.encode(),
                check=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
            pygame.mixer.init()
            pygame.mixer.music.load(tmp_path)
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():
                continue
        finally:
            if os.path.exists(tmp_path):
                os.unlink(tmp_path)
