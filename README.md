# ChatGPT-like Web Application

A minimal, extensible ChatGPT-like chatbot web application built with Flask. This application provides a clean, modern chat interface that supports multiple language models including OpenAI's GPT-3.5-turbo and Microsoft's DialoGPT.

## Features

- 🤖 ChatGPT-like conversational UI
- 🔄 Multiple model support:
  - OpenAI GPT-3.5-turbo (online)
  - Microsoft DialoGPT (local)
  - Dummy fallback model
- 💻 Clean, responsive web interface
- 🚀 Easy to extend with new models
- 📱 Mobile-friendly design

## Prerequisites

- Python 3.x
- pip (Python package manager)

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

3. (Optional) For local model support, install additional dependencies:
   ```bash
   pip install transformers torch
   ```

## Configuration

1. Set up your OpenAI API key (required for GPT-3.5-turbo):
   ```bash
   export OPENAI_API_KEY='your-api-key-here'
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

3. **Dummy**
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

## Security Considerations

- Never commit your OpenAI API key to version control
- Use environment variables for sensitive configuration
- The application runs in debug mode by default - disable this in production

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is open source and available under the [MIT License](LICENSE).

## Acknowledgments

- Flask web framework
- OpenAI API
- Hugging Face Transformers library
