# PHO24 Chatbot

A FastAPI application that serves as a chatbot for answering questions about PHO24, a Vietnamese Pho brand. The chatbot is designed to respond in both English and Vietnamese, positioning the brand as high-tech and progressive to attract potential franchise buyers.

## Project Structure

```
pho24-chatbot/
├── main.py  # Main application entry point
├── app/
│   ├── agent/
│   │   └── agent_pho24.py  # PHO24 agent implementation
│   ├── config/
│   │   ├── env_config.py  # Configuration
│   │   └── supabase_config.py  # Supabase client
│   ├── models/
│   │   └── request_models.py  # API request/response models
│   ├── services/
│   │   └── embeddings.py  # Embedding service
│   ├── templates/
│   │   └── prompt_templates.py  # System prompts
│   ├── tools/
│   │   ├── base_tool.py  # Abstract base class for tools
│   │   └── search/
│   │       ├── english_faq_tool.py  # English FAQ search tool
│   │       └── vietnamese_faq_tool.py  # Vietnamese FAQ search tool
│   ├── utils/
│   │   ├── response_utils.py  # API response utilities
│   │   └── pdf_loader.py  # PDF loading utility
│   └── vectorstore/
│       └── supabase_vectorstore.py  # Supabase vector store
├── data/
│   ├── english_faq.json  # English FAQ data
│   ├── vietnamese_faq.json  # Vietnamese FAQ data
│   └── english_faqs.pdf  # PDF file with English FAQs
├── scripts/
│   ├── process_pdf.py  # Script to process PDF files (custom implementation)
│   ├── llamaindex_supabase.py  # Script to process PDF files (LlamaIndex implementation)
│   └── README.md  # Instructions for using the PDF processing scripts
├── process_pdf_faq.sh  # Shell script to run PDF processing
└── requirements.txt
```

## Key Components

- **Agent**: The main agent that orchestrates the tools and handles user queries.
- **Tools**: Two main tools for searching FAQs in English and Vietnamese.
- **FAQ Data**: Structured data with questions and answers about PHO24 in both languages.
- **PDF Processing**: Tools to process PDF files, create embeddings, and store them in Supabase.

## Setup and Usage

1. Copy `.env.example` to `.env` and fill in the required variables
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Run the application:
   ```
   python main.py
   ```

The API will be available at `http://localhost:8000`.

## API Endpoints

- **POST /ask**: Send a question to the agent
- **GET /health**: Simple health check endpoint

## Example Usage

```bash
# Send a question to the chatbot
curl -X POST "http://localhost:8000/ask" \
  -H "Content-Type: application/json" \
  -d '{"query": "What is PHO24s vision?"}'

# Response:
# {"response": "PHO24's vision is to be the most recognized and trusted Vietnamese Pho brand worldwide."}
```

## Key Features

1. **Bilingual Support**: Responds to queries in both English and Vietnamese.
2. **Brand-Focused Responses**: Emphasizes PHO24's authenticity, innovation, quality, and community.
3. **Language Detection**: Automatically detects the language of the query and responds accordingly.
4. **Conversation Context**: Maintains conversation history for context-aware responses.
5. **PDF Processing**: Ability to process PDF files, create embeddings, and store them in Supabase for enhanced FAQ capabilities.

## Extending the FAQ

### JSON Files

To add new FAQs, update the JSON files in the `data` directory:

- `english_faq.json` for English FAQs
- `vietnamese_faq.json` for Vietnamese FAQs

### PDF Processing

To process PDF files containing FAQ data:

1. Place your PDF file in the `data` directory (e.g., `english_faqs.pdf`)
2. Run the processing script:
   ```
   # Using the shell script (Unix/Linux/macOS)
   chmod +x process_pdf_faq.sh  # Make the script executable (first time only)
   ./process_pdf_faq.sh
   
   # Or using Python directly
   python scripts/llamaindex_supabase.py data/english_faqs.pdf
   ```
3. The script will:
   - Load the PDF file
   - Split it into manageable chunks
   - Create embeddings using OpenAI's API
   - Store the embeddings in your Supabase database

See `scripts/README.md` for more detailed instructions on PDF processing. 