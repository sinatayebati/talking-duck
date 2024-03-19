import gradio as gr
import requests
import json
import os

API_TOKEN = os.getenv("HF_API_TOKEN")
TRANSCRIBE_API_URL = "https://api-inference.huggingface.co/models/facebook/wav2vec2-base-960h"
LLM_API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-v0.1"

def transcribe_audio(audio_file):
    """Transcribe audio file to text."""
    headers = {"Authorization": f"Bearer {API_TOKEN}"}
    with open(audio_file, "rb") as f:
        data = f.read()
    response = requests.post(TRANSCRIBE_API_URL, headers=headers, data=data)
    transcription = json.loads(response.content.decode("utf-8")).get("text", "Transcription not available")
    return transcription

def get_answer(context, question):
    """Get an answer from the LLM based on the context and question."""
    prompt = f"Context: {context}\nQuestion: {question}\nAnswer:"
    headers = {"Authorization": f"Bearer {API_TOKEN}"}
    response = requests.post(LLM_API_URL, headers=headers, json={"inputs": prompt})
    answer = json.loads(response.content.decode("utf-8"))[0].get("generated_text", "Answer not available")
    return answer

def transcribe_and_answer(audio_file, question):
    """Process the audio file for transcription and use the result to get an answer to a question."""
    transcription = transcribe_audio(audio_file)
    answer = get_answer(transcription, question)
    return transcription, answer

# Create the Gradio app
with gr.Blocks() as app:
    gr.Markdown("### Audio to Text and Q&A Chatbot")
    with gr.Row():
        # Corrected 'type' parameter value to 'filepath'
        audio_input = gr.Audio(type="filepath", label="Upload your audio question")
        question_input = gr.Textbox(label="Type your question here")
    answer_button = gr.Button("Get Answer")
    with gr.Row():
        transcription_output = gr.Textbox(label="Transcription")
        answer_output = gr.Textbox(label="Answer")
    
    answer_button.click(transcribe_and_answer, inputs=[audio_input, question_input], outputs=[transcription_output, answer_output])


if __name__ == "__main__":
    app.launch()




