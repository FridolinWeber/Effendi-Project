"""
PyAudio example: Record a few seconds of audio and save to a WAVE
file.
parts of the code taken from:  https://github.com/jleb/pyaudio/blob/master/test/record.py
"""

import pyaudio
import wave
import sys

time_of_record = 10
filename = "output"


class SaveAudio:

    def __init__(self, time_of_record, filename):
        self.chunk = 1024
        self.format = pyaudio.paInt16
        self.rate = 44100
        self.record_seconds = time_of_record
        self.wave_output_filename = filename + "." + "wav"
        self.channels = 2

        self.p = pyaudio.PyAudio()

        self.stream = self.p.open(format=self.format, channels=self.channels, rate=self.rate, input=True, frames_per_buffer=self.chunk)

        print("* recording")

        self.frames = []

    def run(self):
        for i in range(0, int(self.rate / self.chunk * self.record_seconds)):
            data = self.stream.read(self.chunk)
            self.frames.append(data)

        print("* done recording")

    def finish_and_save(self):
        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()

        wf = wave.open(self.wave_output_filename, 'wb')
        wf.setnchannels(self.channels)
        wf.setsampwidth(self.p.get_sample_size(self.format))
        wf.setframerate(self.rate)
        wf.writeframes(b''.join(self.frames))
        wf.close()


def main():
    Record = SaveAudio(time_of_record, filename)
    Record.run()
    Record.finish_and_save()


if __name__ == '__main__':
    main()



