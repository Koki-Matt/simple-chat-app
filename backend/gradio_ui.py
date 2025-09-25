"""Gradio UI for the Simple Chat App."""

from typing import Tuple

import gradio as gr
import requests


# API Configuration
API_BASE_URL = "http://localhost:8000/api/v1"


def call_api_health() -> str:
    """Check if the API is running."""
    try:
        response = requests.get(f"{API_BASE_URL}/health", timeout=5)
        if response.status_code == 200:
            return "✅ API is running"
        return f"❌ API returned status {response.status_code}"
    except requests.exceptions.RequestException as error:
        return f"❌ Cannot connect to API: {str(error)}"


def generate_text(prompt: str, max_length: int, temperature: float) -> Tuple[str, str]:
    """Generate text using the FastAPI backend."""
    try:
        payload = {
            "prompt": prompt,
            "max_length": max_length,
            "temperature": temperature
        }

        response = requests.post(
            f"{API_BASE_URL}/generate",
            json=payload,
            timeout=30
        )

        if response.status_code == 200:
            result = response.json()
            return result["generated_text"], "✅ Text generated successfully"

        error_msg = f"❌ API error: {response.status_code}"
        try:
            error_detail = response.json().get("detail", "Unknown error")
            error_msg += f" - {error_detail}"
        except (ValueError, KeyError):
            pass
        return "", error_msg

    except requests.exceptions.RequestException as error:
        return "", f"❌ Connection error: {str(error)}"


def create_interface() -> gr.Blocks:
    """Create the Gradio interface."""
    with gr.Blocks(title="Simple Chat App", theme=gr.themes.Soft()) as interface:
        gr.Markdown("# 🤖 Simple Chat App")
        gr.Markdown("Generate text using AI models via FastAPI backend")

        # API Status
        with gr.Row():
            status_btn = gr.Button("Check API Status", variant="secondary")
            status_output = gr.Textbox(label="API Status", interactive=False)

        status_btn.click(
            fn=call_api_health,
            outputs=status_output
        )

        gr.Markdown("---")

        # Text Generation
        with gr.Row():
            with gr.Column(scale=2):
                prompt_input = gr.Textbox(
                    label="Prompt",
                    placeholder="Enter your prompt here...",
                    lines=3,
                    max_lines=10
                )

                with gr.Row():
                    max_length_slider = gr.Slider(
                        minimum=10,
                        maximum=200,
                        value=50,
                        step=10,
                        label="Max Length"
                    )
                    temperature_slider = gr.Slider(
                        minimum=0.1,
                        maximum=2.0,
                        value=0.7,
                        step=0.1,
                        label="Temperature"
                    )

                generate_btn = gr.Button("Generate Text", variant="primary")

            with gr.Column(scale=2):
                generated_text = gr.Textbox(
                    label="Generated Text",
                    lines=8,
                    max_lines=15,
                    interactive=False
                )
                status_text = gr.Textbox(
                    label="Status",
                    interactive=False
                )

        # Event handlers
        generate_btn.click(
            fn=generate_text,
            inputs=[prompt_input, max_length_slider, temperature_slider],
            outputs=[generated_text, status_text]
        )

        # Example prompts
        gr.Markdown("### 💡 Example Prompts")
        examples = [
            "The future of artificial intelligence is",
            "Once upon a time, in a distant galaxy",
            "The key to success in life is",
            "In the year 2050, technology will",
            "The most important lesson I learned is"
        ]

        gr.Examples(
            examples=examples,
            inputs=prompt_input,
            label="Click to use example prompts"
        )

        # Instructions
        gr.Markdown("""
        ### 📋 Instructions
        1. **Start the API**: Make sure your FastAPI backend is running on `http://localhost:8000`
        2. **Check Status**: Click "Check API Status" to verify the connection
        3. **Generate Text**: Enter a prompt and adjust parameters as needed
        4. **Parameters**:
           - **Max Length**: Maximum number of tokens to generate (10-200)
           - **Temperature**: Controls randomness (0.1 = deterministic, 2.0 = very random)
        """)

    return interface


if __name__ == "__main__":
    # Create and launch the interface
    demo = create_interface()
    demo.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=False,
        show_error=True
    )
