#!/usr/bin/env python3
"""
Voice Translator - Kivy App for Android
Real-time English speech → Bengali text translation
"""

import sys
import os
import time
import queue
import threading
import numpy as np
from pathlib import Path

# Kivy imports
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput
from kivy.clock import Clock
from kivy.logger import Logger

# Platform-specific audio
try:
    import sounddevice as sd
    AUDIO_BACKEND = 'sounddevice'
except ImportError:
    try:
        import pyaudio
        AUDIO_BACKEND = 'pyaudio'
    except ImportError:
        AUDIO_BACKEND = None

# Translation imports
try:
    import argostranslate.translate
    import argostranslate.package
    from vosk import Model, KaldiRecognizer
    import json
    HAS_VOSK = True
except ImportError:
    HAS_VOSK = False
    try:
        import speech_recognition as sr
        HAS_GOOGLE_STT = True
    except ImportError:
        HAS_GOOGLE_STT = False

# ── Config ─────────────────────────────────────────────────────
SAMPLE_RATE = 16000
CHUNK_DURATION = 0.2
CHUNK_SIZE = int(SAMPLE_RATE * CHUNK_DURATION)

# Model paths
VOSK_MODEL_PATH = os.path.join(os.path.dirname(__file__), 'vosk-model-small-en-us-0.15')
ARGOS_MODEL_DIR = os.path.expanduser('~/.local/share/argos-translate/packages')

# ── Translation Engine ─────────────────────────────────────────
class TranslationEngine:
    def __init__(self, callback):
        self.callback = callback
        self.running = False
        self.audio_queue = queue.Queue()
        self.result_queue = queue.Queue()
        self.recognizer = None
        self.vosk_model = None
        self.use_vosk = False
        self.use_google = False
        self.last_text = ""
        
    def initialize(self):
        """Initialize STT and MT models"""
        Logger.info("Translator: Initializing models...")
        
        # Initialize MT
        try:
            argostranslate.package.update_package_index()
            _ = argostranslate.translate.translate("warmup", 'en', 'bn')
            Logger.info("Translator: MT ready")
        except Exception as e:
            Logger.error(f"Translator: MT init failed: {e}")
            return False
        
        # Initialize STT - prefer Vosk, fallback to Google
        if HAS_VOSK and os.path.exists(VOSK_MODEL_PATH):
            try:
                self.vosk_model = Model(VOSK_MODEL_PATH)
                self.recognizer = KaldiRecognizer(self.vosk_model, SAMPLE_RATE)
                self.use_vosk = True
                Logger.info("Translator: Vosk STT ready")
            except Exception as e:
                Logger.warning(f"Translator: Vosk init failed: {e}")
        
        if not self.use_vosk and HAS_GOOGLE_STT:
            try:
                import speech_recognition as sr
                self.sr_recognizer = sr.Recognizer()
                self.sr_recognizer.energy_threshold = 300
                self.sr_recognizer.dynamic_energy_threshold = True
                self.use_google = True
                Logger.info("Translator: Google STT ready")
            except Exception as e:
                Logger.error(f"Translator: Google STT init failed: {e}")
        
        if not self.use_vosk and not self.use_google:
            Logger.error("Translator: No STT backend available")
            return False
            
        return True
    
    def start(self):
        self.running = True
        self.last_text = ""
        
        # Start worker threads
        self.stt_thread = threading.Thread(target=self._stt_worker, daemon=True)
        self.mt_thread = threading.Thread(target=self._mt_worker, daemon=True)
        self.stt_thread.start()
        self.mt_thread.start()
        
        Logger.info("Translator: Started")
    
    def stop(self):
        self.running = False
        self.audio_queue.put(None)
        self.result_queue.put(None)
        if hasattr(self, 'stt_thread'):
            self.stt_thread.join(timeout=1.0)
        if hasattr(self, 'mt_thread'):
            self.mt_thread.join(timeout=1.0)
        Logger.info("Translator: Stopped")
    
    def add_audio(self, audio_chunk):
        """Add audio chunk (numpy int16 array)"""
        if self.running:
            self.audio_queue.put(audio_chunk.tobytes())
    
    def get_result(self):
        """Get latest translation result"""
        try:
            return self.result_queue.get_nowait()
        except queue.Empty:
            return None
    
    def _stt_worker(self):
        while self.running:
            try:
                chunk = self.audio_queue.get(timeout=0.1)
                if chunk is None:
                    break
                
                start = time.perf_counter()
                text = ""
                
                if self.use_vosk:
                    if self.recognizer.AcceptWaveform(chunk):
                        result = json.loads(self.recognizer.Result())
                        text = result.get('text', '').strip()
                    else:
                        result = json.loads(self.recognizer.PartialResult())
                        text = result.get('partial', '').strip()
                
                elif self.use_google:
                    try:
                        audio_data = sr.AudioData(chunk, SAMPLE_RATE, 2)
                        text = self.sr_recognizer.recognize_google(audio_data, language='en-US')
                    except sr.UnknownValueError:
                        text = ""
                    except sr.RequestError:
                        text = ""
                
                stt_time = (time.perf_counter() - start) * 1000
                
                if text and text != self.last_text:
                    self.last_text = text
                    self.mt_queue.put((text, start))
                    
            except queue.Empty:
                continue
            except Exception as e:
                Logger.error(f"STT worker error: {e}")
    
    def _mt_worker(self):
        while self.running:
            try:
                item = self.mt_queue.get(timeout=0.1)
                if item is None:
                    break
                
                text, stt_start = item
                start = time.perf_counter()
                
                try:
                    bn_text = argostranslate.translate.translate(text, 'en', 'bn')
                except Exception as e:
                    Logger.error(f"MT error: {e}")
                    bn_text = ""
                
                mt_time = (time.perf_counter() - start) * 1000
                total_time = (time.perf_counter() - stt_start) * 1000
                
                self.result_queue.put({
                    'en': text,
                    'bn': bn_text,
                    'latency': total_time,
                    'timestamp': time.strftime("%H:%M:%S")
                })
                
            except queue.Empty:
                continue
            except Exception as e:
                Logger.error(f"MT worker error: {e}")


# ── Audio Capture ──────────────────────────────────────────────
class AudioCapture:
    def __init__(self, engine):
        self.engine = engine
        self.stream = None
        self.pa = None
    
    def start(self):
        if AUDIO_BACKEND == 'sounddevice':
            self._start_sounddevice()
        elif AUDIO_BACKEND == 'pyaudio':
            self._start_pyaudio()
        else:
            Logger.error("No audio backend available")
    
    def _start_sounddevice(self):
        def callback(indata, frames, time_info, status):
            if status:
                Logger.warning(f"Audio status: {status}")
            audio_int16 = (indata[:, 0] * 32767).astype(np.int16)
            self.engine.add_audio(audio_int16)
        
        self.stream = sd.InputStream(
            samplerate=SAMPLE_RATE,
            channels=1,
            dtype='float32',
            blocksize=CHUNK_SIZE,
            callback=callback
        )
        self.stream.start()
        Logger.info("Audio: sounddevice started")
    
    def _start_pyaudio(self):
        import pyaudio
        self.pa = pyaudio.PyAudio()
        self.stream = self.pa.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=SAMPLE_RATE,
            input=True,
            frames_per_buffer=CHUNK_SIZE,
            stream_callback=self._pyaudio_callback
        )
        self.stream.start_stream()
        Logger.info("Audio: pyaudio started")
    
    def _pyaudio_callback(self, in_data, frame_count, time_info, status):
        audio_int16 = np.frombuffer(in_data, dtype=np.int16)
        self.engine.add_audio(audio_int16)
        return (None, pyaudio.paContinue)
    
    def stop(self):
        if self.stream:
            if AUDIO_BACKEND == 'sounddevice':
                self.stream.stop()
                self.stream.close()
            elif AUDIO_BACKEND == 'pyaudio':
                self.stream.stop_stream()
                self.stream.close()
                if self.pa:
                    self.pa.terminate()


# ── Kivy UI ────────────────────────────────────────────────────
class TranslatorUI(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 20
        self.spacing = 15
        
        # Title
        self.title = Label(
            text='English → Bengali Translator',
            size_hint_y=None,
            height=50,
            font_size=24,
            bold=True
        )
        self.add_widget(self.title)
        
        # Status
        self.status = Label(
            text='Initializing...',
            size_hint_y=None,
            height=40,
            font_size=16,
            color=(1, 1, 0, 1)
        )
        self.add_widget(self.status)
        
        # Conversation display
        self.scroll = ScrollView()
        self.conversation = TextInput(
            readonly=True,
            multiline=True,
            font_size=18,
            size_hint_y=None,
            background_color=(0.1, 0.1, 0.1, 1),
            foreground_color=(1, 1, 1, 1)
        )
        self.conversation.bind(minimum_height=self.conversation.setter('height'))
        self.scroll.add_widget(self.conversation)
        self.add_widget(self.scroll)
        
        # Control buttons
        btn_layout = BoxLayout(size_hint_y=None, height=60, spacing=10)
        
        self.start_btn = Button(
            text='Start Listening',
            font_size=18,
            background_color=(0.2, 0.7, 0.2, 1)
        )
        self.start_btn.bind(on_press=self.start_listening)
        btn_layout.add_widget(self.start_btn)
        
        self.stop_btn = Button(
            text='Stop',
            font_size=18,
            background_color=(0.7, 0.2, 0.2, 1),
            disabled=True
        )
        self.stop_btn.bind(on_press=self.stop_listening)
        btn_layout.add_widget(self.stop_btn)
        
        self.clear_btn = Button(
            text='Clear',
            font_size=18,
            background_color=(0.5, 0.5, 0.5, 1)
        )
        self.clear_btn.bind(on_press=self.clear_conversation)
        btn_layout.add_widget(self.clear_btn)
        
        self.add_widget(btn_layout)
        
        # Latency display
        self.latency_label = Label(
            text='Latency: --ms',
            size_hint_y=None,
            height=30,
            font_size=14,
            color=(0.7, 0.7, 0.7, 1)
        )
        self.add_widget(self.latency_label)
        
        # Engine and audio
        self.engine = None
        self.audio = None
        self.running = False
    
    def start_listening(self, instance):
        if self.running:
            return
        
        self.status.text = 'Loading models...'
        self.start_btn.disabled = True
        
        # Initialize in background
        threading.Thread(target=self._init_and_start, daemon=True).start()
    
    def _init_and_start(self):
        try:
            self.engine = TranslationEngine(None)
            if not self.engine.initialize():
                Clock.schedule_once(lambda dt: self._show_error("Failed to initialize"))
                return
            
            self.engine.start()
            self.audio = AudioCapture(self.engine)
            self.audio.start()
            
            self.running = True
            
            # Schedule UI updates
            Clock.schedule_interval(self._update_ui, 0.1)
            
            Clock.schedule_once(lambda dt: self._on_started())
            
        except Exception as e:
            Logger.error(f"Start error: {e}")
            Clock.schedule_once(lambda dt: self._show_error(str(e)))
    
    def _on_started(self):
        self.status.text = 'Listening... (speak in English)'
        self.status.color = (0, 1, 0, 1)
        self.start_btn.disabled = True
        self.stop_btn.disabled = False
    
    def _show_error(self, msg):
        self.status.text = f'Error: {msg}'
        self.status.color = (1, 0, 0, 1)
        self.start_btn.disabled = False
    
    def stop_listening(self, instance):
        if not self.running:
            return
        
        if self.audio:
            self.audio.stop()
        if self.engine:
            self.engine.stop()
        
        self.running = False
        self.status.text = 'Stopped'
        self.status.color = (1, 1, 0, 1)
        self.start_btn.disabled = False
        self.stop_btn.disabled = True
    
    def clear_conversation(self, instance):
        self.conversation.text = ''
    
    def _update_ui(self, dt):
        if not self.running or not self.engine:
            return False
        
        result = self.engine.get_result()
        if result:
            timestamp = result['timestamp']
            en = result['en']
            bn = result['bn']
            latency = result['latency']
            
            # Add to conversation
            entry = f"[{timestamp}] EN: {en}\n[{timestamp}] BN: {bn}\n\n"
            self.conversation.text += entry
            self.conversation.cursor = (0, len(self.conversation.text))
            
            # Update latency
            self.latency_label.text = f'Latency: {latency:.0f}ms'
        
        return True  # Continue scheduling


class VoiceTranslatorApp(App):
    def build(self):
        self.title = 'Voice Translator'
        return TranslatorUI()
    
    def on_stop(self):
        # Clean up on app close
        root = self.root
        if hasattr(root, 'running') and root.running:
            if root.audio:
                root.audio.stop()
            if root.engine:
                root.engine.stop()


if __name__ == '__main__':
    VoiceTranslatorApp().run()