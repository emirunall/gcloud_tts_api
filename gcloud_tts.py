import os
from flask import Flask, request, send_file, render_template
from google.cloud import texttospeech

# Google Cloud servis hesabı tanımı
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "gcloud_key.json"

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        text = request.form['text']
        filename = synthesize_text_to_mp3(text)
        return send_file(filename, as_attachment=True)

    return render_template('index.html')


def synthesize_text_to_mp3(text):
    client = texttospeech.TextToSpeechClient()

    synthesis_input = texttospeech.SynthesisInput(text=text)

    voice = texttospeech.VoiceSelectionParams(
        language_code="tr-TR",
        name="tr-TR-Chirp3-HD-Erinome",
    )

    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3,
        speaking_rate=0.96,
    )

    response = client.synthesize_speech(
        input=synthesis_input,
        voice=voice,
        audio_config=audio_config,
    )

    output_path = "output.mp3"
    with open(output_path, "wb") as out:
        out.write(response.audio_content)

    return output_path

if __name__ == '__main__':
    app.run(debug=True)
