import os
import json
from flask import Flask, request, send_file, render_template
from google.cloud import texttospeech
from google.oauth2 import service_account

app = Flask(__name__, template_folder="templates")

# Google servis hesabı kimliği (Render ortam değişkeninden alınır)
keyfile_dict = json.loads(os.environ["GOOGLE_APPLICATION_CREDENTIALS_JSON"])
credentials = service_account.Credentials.from_service_account_info(keyfile_dict)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        text = request.form['text']
        filename = synthesize_text_to_mp3(text)
        return send_file(filename, as_attachment=True, download_name="dogal_ses.mp3")  # 🔧 Güncellenen satır

    return render_template('index.html')


def synthesize_text_to_mp3(text):
    client = texttospeech.TextToSpeechClient(credentials=credentials)

    synthesis_input = texttospeech.SynthesisInput(text=text)

    voice = texttospeech.VoiceSelectionParams(
        language_code="tr-TR",
        name="tr-TR-Chirp3-HD-Erinome",
    )

    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3,
        speaking_rate=0.92,
    )

    output_path = "/tmp/output.mp3"  # Render uyumlu dosya yolu
    response = client.synthesize_speech(
        input=synthesis_input,
        voice=voice,
        audio_config=audio_config,
    )

    with open(output_path, "wb") as out:
        out.write(response.audio_content)

    return output_path
