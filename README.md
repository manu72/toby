# ChatGPT-like Web Application

A minimal, extensible ChatGPT-like chatbot web application built with Flask. This application provides a clean, modern chat interface that supports multiple language models including OpenAI's GPT-3.5-turbo, Microsoft's DialoGPT, and local LLMs via Ollama.

## Features

- 🤖 ChatGPT-like conversational UI
- 🔄 Multiple model support:
  - OpenAI GPT-3.5-turbo (online)
  - Microsoft DialoGPT (local)
  - Local LLMs via Ollama (LLama3.2, Deepseekr1 7b)
  - Dummy fallback model
- 💻 Clean, responsive web interface
- 🚀 Easy to extend with new models
- 📱 Mobile-friendly design
- 🏠 Support for running models locally

## Prerequisites

- Python 3.x
- pip (Python package manager)
- Ollama CLI (for local LLM support)

## Installation

1. Clone the repository:

   ```bash
   git clone [your-repository-url]
   cd [repository-name]
   ```

2. Install the required dependencies:

   ```bash
   pip install flask openai
   ```

3. (Optional) For DialoGPT support, install additional dependencies:

   ```bash
   pip install transformers torch
   ```

4. (Optional) For local LLM support:
   - Install Ollama from [Ollama's official website](https://ollama.ai)
   - Pull the required models:
     ```bash
     ollama pull llama3.2
     ollama pull deepseekr1-7b
     ```

## Configuration

1. Set up your OpenAI API key (required only for GPT-3.5-turbo):

   ```bash
   export OPENAI_API_KEY='your-api-key-here'
   ```

2. Ensure Ollama is running (required for local LLMs):
   ```bash
   # Start the Ollama service
   ollama serve
   ```

## Usage

1. Start the application:

   ```bash
   python app.py
   ```

2. Open your web browser and navigate to:

   ```
   http://localhost:5000
   ```

3. Select your preferred model from the dropdown menu and start chatting!

## Available Models

1. **OpenAI GPT-3.5-turbo**

   - Requires valid OpenAI API key
   - Best quality responses
   - Internet connection required

2. **DialoGPT**

   - Local model, no API key required
   - Runs entirely on your machine
   - Requires additional dependencies

3. **LLama3.2 (Ollama)**

   - Runs locally via Ollama
   - No API key required
   - Requires Ollama installation

4. **Deepseekr1 7b (Ollama)**

   - Runs locally via Ollama
   - No API key required
   - Requires Ollama installation

5. **Dummy**
   - Simple echo response
   - Used as fallback
   - No dependencies required

## Project Structure

```
.
├── app.py          # Main application file
└── README.md       # Project documentation
```

## Customisation

The application is designed to be easily extensible. To add a new model:

1. Create a new chat function in `app.py`
2. Add the function to the `MODEL_FUNCTIONS` dictionary
3. The new model will automatically appear in the UI dropdown

### Adding a New Ollama Model

To add support for a new Ollama model:

1. Pull the model using Ollama CLI:

   ```bash
   ollama pull your-model-name
   ```

2. Add a new function in `app.py`:

   ```python
   def chat_with_new_model(conversation, prompt):
       result = subprocess.run(
           ["ollama", "run", "your-model-name", prompt],
           capture_output=True, text=True, check=True
       )
       return result.stdout.strip()
   ```

3. Add the model to `MODEL_FUNCTIONS` dictionary

## Security Considerations

- Never commit your OpenAI API key to version control
- Use environment variables for sensitive configuration
- The application runs in debug mode by default - disable this in production
- Be aware that local LLMs may consume significant system resources

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is open source and available under the [MIT License](LICENSE).

## Acknowledgments

- Flask web framework
- OpenAI API
- Hugging Face Transformers library
- Ollama project for local LLM support
