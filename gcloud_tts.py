from flask import Flask, render_template, request, jsonify, send_file
from google.cloud import texttospeech
import os
from io import BytesIO

app = Flask(__name__)
char_log_path = "used_chars.txt"

# Servis hesabı otomatik olarak yüklenecek şekilde ayarlanmalı (Render'da ayarlanmıştı)

# İlk çalıştırmada karakter log dosyası oluştur
if not os.path.exists(char_log_path):
    with open(char_log_path, "w") as f:
        f.write("0")

def update_character_count(new_count):
    with open(char_log_path, "r+") as f:
        total = int(f.read())
        total += new_count
        f.seek(0)
        f.write(str(total))
        f.truncate()

def get_total_characters():
    with open(char_log_path, "r") as f:
        return int(f.read())

@app.route("/", methods=["GET"])
def index():
    total_chars = get_total_characters()
    return render_template("index.html", used_chars=total_chars)

@app.route("/speak", methods=["POST"])
def speak():
    text = request.form.get("text")
    if not text:
        return jsonify({"error": "Metin alanı boş"}), 400

    update_character_count(len(text))

    client = texttospeech.TextToSpeechClient()
    input_text = texttospeech.SynthesisInput(text=text)

    voice = texttospeech.VoiceSelectionParams(
        language_code="tr-TR",
        ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
    )

    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    response = client.synthesize_speech(
        input=input_text, voice=voice, audio_config=audio_config
    )

    return send_file(BytesIO(response.audio_content),
                     mimetype="audio/mpeg",
                     as_attachment=False,
                     download_name="speech.mp3")

@app.route("/reset", methods=["POST"])
def reset_counter():
    with open(char_log_path, "w") as f:
        f.write("0")
    return jsonify({"message": "Sayaç sıfırlandı."})
