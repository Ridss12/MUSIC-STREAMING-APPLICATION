import sounddevice as sd
from scipy.io.wavfile import write
import whisper

SAMPLE_RATE = 16000
DURATION = 5

print("🎤 Speak now...")
audio = sd.rec(
    int(DURATION * SAMPLE_RATE),
    samplerate=SAMPLE_RATE,
    channels=1,
    dtype="int16"
)
sd.wait()

write("voice.wav", SAMPLE_RATE, audio)

print("🧠 Transcribing...")
model = whisper.load_model("tiny")
result = model.transcribe("voice.wav", language="hi")

print("\nYou said:")
print(result["text"])
