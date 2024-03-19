import gradio as gr
import requests
import json
import os

API_TOKEN = os.getenv("HF_API_TOKEN")
TRANSCRIBE_API_URL = "https://api-inference.huggingface.co/models/openai/whisper-base.en"
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
    prompt = (
        "As an intelligent coding assistant, your task is to provide clear, concise, and accurate answers to coding-related questions. "
        "Below are examples of questions and the kind of direct answers expected:\n\n"
        "Example Question 1: How can I remove duplicates from a list in Python?\n"
        "Example Answer 1: Use the set() function to convert the list to a set, which removes duplicates, then convert it back to a list.\n\n"
        "Example Question 2: What's the difference between '==' and '===' in JavaScript?\n"
        "Example Answer 2: '==' checks for equality of values after type coercion, while '===' checks for both value and type equality without coercion.\n\n"
        "Example Question 3: How to check if a key exists in a dictionary in Python?\n"
        "Example Answer 3: Use the 'in' keyword, like 'if key in my_dict:'.\n\n"
        "Based on the above examples, answer the following question:\n\n"
        f"Question: {question}\n"
        "Answer:"
    )
    headers = {"Authorization": f"Bearer {API_TOKEN}"}
    
    # Adjust generation parameters for more focused and relevant responses
    payload = {
        "inputs": prompt,
        "parameters": {
            "temperature": 0.3,  # More deterministic
            "top_p": 0.95,  # Consider top 90% probable tokens at each step
            "max_new_tokens": 100,  # Limit the response length
            "repetition_penalty": 1.2,  # Discourage repetition
            "num_return_sequences": 1,  # Number of responses to generate
            "return_full_text": False,  # Return only generated text, not the full prompt
            "top_k" : 50,
            "truncate" : 24576,
            "max_new_tokens" : 8192,
            "stop" : ["</s>"]
        },
        "options": {
            "use_cache": True  # Use cached responses when available
        }
    }

    response = requests.post(LLM_API_URL, headers=headers, json=payload)
    answer = json.loads(response.content.decode("utf-8"))[0].get("generated_text", "Answer not available")
    return answer


def transcribe_and_answer(audio_file, question):
    """Process the audio file for transcription and use the result to get an answer to a question."""
    transcription = transcribe_audio(audio_file)
    answer = get_answer(transcription, question)
    return transcription, answer

# Create the Gradio app
import gradio as gr

# Create the Gradio app
with gr.Blocks() as app:
    gr.HTML("""
    <div style="display: flex; align-items: center; justify-content: center; margin-bottom: 20px;">
        <img src="https://huggingface.co/spaces/sinatayebati/Talking-Duck/resolve/main/assets/talking-duck-logo.webp" alt="Talking Duck Logo" style="width: 120px;"/> 
        <div style="margin-left: 20px;">
            <h1 style="font-weight: bold; font-size: 32px; margin: 0;">TALKING DUCK</h1>
            <h3 style="margin: 0;">An Audio to Text Q&A Chatbot</h3>
        </div>
    </div>
    <p style="text-align: center;">Your swift coding sidekick. Speak your code queries, and let the duck do the magic.</p>
    """)

    gr.Markdown("""
    <div style="background-color: #0A192F; color: white; padding: 20px; border-radius: 10px; margin-bottom: 20px;">
        <div style="font-size: 16px; font-weight: bold; text-align: center; margin-bottom: 10px;">Models running on backend</div>
        <div style="display: flex; justify-content: space-around; align-items: center;">
            <div>
                <img src="https://huggingface.co/datasets/huggingchat/models-logo/resolve/main/mistral-logo.png" alt="Mistral Logo" style="width: 40px; margin-bottom: 10px;"/>
                <div style="font-size: 14px;">mistralai/Mistral-7B-v0.1</div>
                <a href="https://huggingface.co/mistralai/Mistral-7B-v0.1" target="_blank" style="color: white; text-decoration: none; font-size: 12px;">Model Page</a>
            </div>
            <div>
                <img src="https://aeiljuispo.cloudimg.io/v7/https://cdn-uploads.huggingface.co/production/uploads/1620805164087-5ec0135ded25d76864d553f1.png?w=200&h=200&f=face" alt="Second Model Logo" style="width: 40px; margin-bottom: 10px;"/>
                <div style="font-size: 14px;">openai/whisper-base.en</div>
                <a href="https://huggingface.co/openai/whisper-base.en" target="_blank" style="color: white; text-decoration: none; font-size: 12px;">Model Page</a>
            </div>
        </div>
    </div>
    """)


    with gr.Row():
        audio_input = gr.Audio(type="filepath", label="Upload your audio question")
        question_input = gr.Textbox(label="Type your question here")
    answer_button = gr.Button("Get Answer")
    with gr.Row():
        transcription_output = gr.Textbox(label="Transcription")
        answer_output = gr.Textbox(label="Answer")
    
    answer_button.click(transcribe_and_answer, inputs=[audio_input, question_input], outputs=[transcription_output, answer_output])



if __name__ == "__main__":
    app.launch(server_name="0.0.0.0")




