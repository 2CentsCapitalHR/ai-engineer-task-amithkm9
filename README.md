# 🏛️ ADGM Corporate Agent - Setup Guide

> AI-Powered Legal Document Compliance System for Abu Dhabi Global Market (ADGM)

## 📋 Quick Setup Checklist

- [ ] Python 3.8+ installed
- [ ] Ollama installed and running
- [ ] 4GB+ RAM available
- [ ] Internet connection for ADGM content fetching

## 🚀 Installation Steps

### 1. Clone the Repository
```bash
git clone <your-repository-url>
cd adgm-corporate-agent
```

### 2. Create Virtual Environment
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Install and Setup Ollama

#### Download Ollama
Visit [https://ollama.ai](https://ollama.ai) and download for your OS:
- **Windows**: Download the installer
- **macOS**: `brew install ollama`
- **Linux**: `curl -fsSL https://ollama.ai/install.sh | sh`

#### Start Ollama Server
```bash
# Start Ollama server (keep this terminal open)
ollama serve
```

#### Pull Required Models
In a new terminal:
```bash
# Pull the Llama2 model (required for AI analysis)
ollama pull llama2

# Optional: Pull other models for better performance
ollama pull mistral
```

### 5. Run the Application
```bash
# Make sure you're in the project directory with venv activated
streamlit run app.py
```

### 6. Access the Application
- Open your browser
- Navigate to: `http://localhost:8501`
- Start uploading ADGM documents!

## 📁 Project Structure
```
adgm-corporate-agent/
├── app.py                      # Main Streamlit application
├── document_processor.py       # Document processing engine
├── compliance_checker.py       # ADGM compliance validation
├── advanced_rag.py            # Web-enhanced RAG system
├── config.py                  # Configuration settings
├── requirements.txt           # Python dependencies
├── README.md                  # This file
├── output/                    # Generated reports and documents
└── chroma_db/                 # Vector database storage
```

## 🔧 Configuration

### Environment Variables (Optional)
Create a `.env` file in the project root:
```env
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama2
LOG_LEVEL=INFO
```

### Model Configuration
Edit `config.py` to customize:
```python
# Change AI model
OLLAMA_MODEL = "mistral"  # or "phi", "codellama"

# Adjust RAG settings
RAG_CHUNK_SIZE = 1000
RAG_CONFIDENCE_THRESHOLD = 0.7
```

## 🧪 Testing the Setup

### 1. Verify Ollama Installation
```bash
# Check if Ollama is running
curl http://localhost:11434/api/version

# List available models
ollama list
```

### 2. Test Document Upload
1. Launch the application: `streamlit run app.py`
2. Upload a sample .docx file
3. Click "Review Now"
4. Verify you get compliance analysis results

### 3. Check System Status
In the application sidebar, expand "⚙️ System Status" to verify:
- ✅ All systems operational
- 🤖 AI Model: Advanced RAG with Llama2
- 📊 Analysis Method: Hybrid (Rules + AI)

## 🐛 Troubleshooting

### Common Issues

#### Issue: "Connection refused" when starting
**Solution**: Make sure Ollama is running
```bash
# Start Ollama server
ollama serve
```

#### Issue: "Model not found"
**Solution**: Pull the required model
```bash
ollama pull llama2
```

#### Issue: "Module not found" errors
**Solution**: Ensure virtual environment is activated and dependencies installed
```bash
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
```

#### Issue: Slow processing
**Solutions**:
- Ensure you have 4GB+ RAM
- Close other applications
- Try a smaller model: `ollama pull phi`
- Reduce chunk size in `config.py`

#### Issue: Can't upload documents
**Solution**: Check file format - only .docx files are supported

### System Requirements
- **OS**: Windows 10+, macOS 12+, Ubuntu 20.04+
- **RAM**: 4GB minimum, 8GB recommended
- **Storage**: 2GB free space
- **Network**: Internet connection for ADGM content fetching

### Performance Optimization
```python
# For better performance, edit config.py:
RAG_CHUNK_SIZE = 500          # Smaller chunks = faster processing
RAG_TOP_K_RETRIEVAL = 5       # Fewer retrievals = faster search
OLLAMA_MODEL = "phi"          # Smaller model = faster inference
```

## 🔒 Security Notes

- **Local Processing**: All documents are processed locally
- **No Data Upload**: Your documents never leave your computer
- **Automatic Cleanup**: Temporary files are automatically deleted
- **Privacy First**: No personal data is stored permanently

## 📊 Usage Tips

### Best Practices
1. **Upload Related Documents Together**: Upload all documents for a process (e.g., incorporation) at once
2. **Check File Size**: Keep documents under 10MB for optimal performance
3. **Use Official Templates**: Start with ADGM official templates when possible
4. **Review Comments**: Pay attention to AI-generated inline comments
5. **Download Results**: Save reviewed documents and reports for your records

### Supported Document Types
- ✅ Articles of Association
- ✅ Board Resolutions
- ✅ Shareholder Resolutions
- ✅ Employment Contracts
- ✅ Incorporation Applications
- ✅ UBO Declarations
- ✅ Commercial Agreements

## 🆘 Getting Help

### Documentation
- Check the project overview document for detailed feature explanations
- Review the compliance rules in `compliance_checker.py`
- Examine sample test documents for examples

### Support
- **Issues**: Create GitHub issues for bugs
- **Questions**: Check the FAQ in the application
- **Performance**: Monitor system resources during processing

## 🔄 Updates

### Updating the Application
```bash
# Pull latest changes
git pull origin main

# Update dependencies
pip install -r requirements.txt --upgrade

# Update Ollama models
ollama pull llama2
```

### Version Compatibility
- **Python**: 3.8, 3.9, 3.10, 3.11 tested
- **Ollama**: Latest version recommended
- **OS**: Cross-platform compatible

## 📈 Development Mode

### For Developers
```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Run tests
python -m pytest tests/

# Start with debug logging
LOG_LEVEL=DEBUG streamlit run app.py

# Monitor performance
streamlit run app.py --logger.level=debug
```

---

**🎉 You're all set! Start uploading your ADGM documents and enjoy AI-powered compliance checking!**

For detailed feature explanations and technical specifications, see the project overview document.
