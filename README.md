# Agricultural FAQ RAG System

A voice-to-voice conversational AI system that provides instant answers to agricultural questions using advanced RAG (Retrieval-Augmented Generation) technology.

## 🚀 Quick Start Guide

Follow these steps exactly to get the system running on your computer.

### Step 1: Check Your Computer

**Check Python Version**
1. Open Command Prompt (Windows) or Terminal (Mac/Linux)
2. Type: `python --version`
3. You should see Python 3.8 or higher
4. If not installed, download from: https://python.org/downloads/

**Check Internet Connection**
- Make sure you have a stable internet connection
- The system needs to connect to OpenAI services

### Step 2: Get OpenAI API Key

1. Go to: https://platform.openai.com/
2. Create an account or log in
3. Go to "API Keys" section
4. Click "Create new secret key"
5. Copy the key (starts with `sk-...`)
6. **Important**: Keep this key safe and don't share it

### Step 3: Download the Project

**Option A: Download ZIP**
1. Click the green "Code" button on this page
2. Select "Download ZIP"
3. Extract the ZIP file to your Desktop
4. Rename the folder to `agricultural-rag`

**Option B: Use Git (if you have it)**
```bash
git clone <repository-url>
cd agricultural-rag
```

### Step 4: Open Command Prompt/Terminal

1. **Windows**: Press `Win + R`, type `cmd`, press Enter
2. **Mac**: Press `Cmd + Space`, type `terminal`, press Enter
3. **Linux**: Press `Ctrl + Alt + T`

### Step 5: Navigate to Project Folder

Type this command (replace `Desktop` with where you extracted the files):
```bash
cd Desktop/agricultural-rag
```

### Step 6: Create Virtual Environment

**Windows:**
```bash
python -m venv .venv
.venv\Scripts\activate
```

**Mac/Linux:**
```bash
python -m venv .venv
source .venv/bin/activate
```

You should see `(.venv)` at the beginning of your command line.

### Step 7: Install Required Packages

Copy and paste this command:
```bash
pip install -r requirements.txt
```

Wait for all packages to install (this may take 2-5 minutes).

### Step 8: Setup API Key

1. Find the file named `.env.example` in your project folder
2. Make a copy of this file
3. Rename the copy to `.env` (remove `.example`)
4. Open the `.env` file in Notepad (Windows) or TextEdit (Mac)
5. Replace `your_openai_api_key_here` with your actual API key from Step 2
6. Save the file

Your `.env` file should look like:
```
OPENAI_API_KEY=sk-your-actual-api-key-here
```

### Step 9: Run the Application

In your command prompt/terminal, type:
```bash
streamlit run app.py
```

### Step 10: Access the Application

1. Wait for the message: "You can now view your Streamlit app in your browser"
2. Open your web browser (Chrome, Firefox, Safari, etc.)
3. Go to: `http://localhost:8501`
4. You should see the Agricultural FAQ System interface

## 🎯 How to Use the System

### First Time Setup
1. Click "🚀 Initialize RAG Pipeline" in the sidebar
2. Wait for "✅ RAG Pipeline Active" message
3. The system is now ready to use

### Ask Questions (Text)
1. Select "Type" as input method
2. Type your question in the text box
3. Click "🔍 Get Answer"
4. View the response, listen to audio narration, and check performance metrics

### Ask Questions (Voice)
1. Select "🎙️ Voice Recording" as input method
2. Click the microphone button
3. Speak your question clearly
4. Wait for the response (text and audio)

### Example Questions to Try
- "What is Dormulin Vegetative used for?"
- "How to control thrips in chilli?"
- "What are the benefits of Zetol Select for banana?"

## 🔧 Troubleshooting

### Problem: "No module named 'openai'"
**Solution**: Make sure you activated the virtual environment (Step 6)

### Problem: "API key not found"
**Solution**: 
1. Check that `.env` file exists (not `.env.example`)
2. Verify your API key is correct in the `.env` file
3. Make sure there are no extra spaces in the `.env` file

### Problem: "Command not found: streamlit"
**Solution**: 
1. Make sure virtual environment is activated
2. Run: `pip install streamlit`

### Problem: Application won't start
**Solution**:
1. Close the application (Ctrl+C in command prompt)
2. Make sure you're in the right folder: `cd Desktop/agricultural-rag`
3. Try running again: `streamlit run app.py`

### Problem: Slow responses
**Solution**:
1. Check your internet connection
2. The first query is always slower (1-2 seconds)
3. Subsequent queries should be faster

### Problem: Audio not working
**Solution**:
1. Check your browser allows microphone access
2. Make sure speakers/headphones are connected
3. Try refreshing the web page

## 📁 What's in This Project

```
agricultural-rag/
├── app.py                     # Main application file
├── requirements.txt           # List of required packages
├── .env.example              # Template for API key
├── .env                      # Your API key (you create this)
├── data/                     # Agricultural knowledge base
├── vector_db/                # Pre-built search database
├── rag/                      # AI processing modules
└── audio_cache/              # Stored audio responses
```

## 🆘 Getting Help

### If Something Goes Wrong
1. **Read the error message carefully**
2. **Check the troubleshooting section above**
3. **Make sure all steps were followed exactly**
4. **Try restarting the application**

### Common Mistakes to Avoid
- ❌ Forgetting to activate virtual environment
- ❌ Using `.env.example` instead of creating `.env`
- ❌ Not having internet connection
- ❌ Using wrong Python version (need 3.8+)

### System Requirements
- **Operating System**: Windows 10+, macOS 10.14+, or Linux
- **Python**: Version 3.8 or higher
- **RAM**: At least 4GB available
- **Internet**: Stable broadband connection
- **Browser**: Chrome, Firefox, Safari, or Edge

## 🎉 Success Indicators

You know the system is working when:
- ✅ Web page loads at `http://localhost:8501`
- ✅ "Initialize RAG Pipeline" button works
- ✅ You can ask questions and get responses
- ✅ Voice recording works (microphone button)
- ✅ Audio responses play back

## 📞 Support

If you're still having trouble:
1. Double-check you followed every step exactly
2. Make sure your OpenAI API key is valid and has credits
3. Try using a different web browser
4. Restart your computer and try again

---

**🌱 Ready to explore agricultural AI? Start asking questions about crops, diseases, and farming techniques!**