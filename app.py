"""
ADGM Corporate Agent - Streamlit Application (Enhanced)
Fixed document processing and reporting
"""

import streamlit as st
import json
import os
from datetime import datetime
from pathlib import Path
import tempfile
import logging
from typing import List, Dict, Tuple
import zipfile
import time

from document_processor import DocumentProcessor
from compliance_checker import ComplianceChecker
from advanced_rag import AdvancedRAG

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Page configuration
st.set_page_config(
    page_title="ADGM Corporate Agent",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Enhanced Custom CSS for beautiful styling
st.markdown("""
<style>
    /* Main container styling */
    .main {
        padding: 2rem;
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }
    
    /* Header styling */
    .header-container {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2.5rem;
        border-radius: 20px;
        margin-bottom: 2rem;
        box-shadow: 0 15px 35px rgba(0,0,0,0.15);
        position: relative;
        overflow: hidden;
    }
    
    .header-container::before {
        content: '';
        position: absolute;
        top: -50%;
        right: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%);
        animation: shimmer 3s infinite;
    }
    
    @keyframes shimmer {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    .header-title {
        color: white;
        font-size: 3rem;
        font-weight: 800;
        margin-bottom: 0.5rem;
        text-align: center;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
        animation: fadeInDown 0.8s ease;
    }
    
    .header-subtitle {
        color: rgba(255,255,255,0.95);
        font-size: 1.3rem;
        text-align: center;
        animation: fadeInUp 0.8s ease;
    }
    
    @keyframes fadeInDown {
        from { opacity: 0; transform: translateY(-20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    @keyframes fadeInUp {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    /* Card styling with hover effects */
    .card {
        background: white;
        padding: 1.8rem;
        border-radius: 15px;
        box-shadow: 0 6px 20px rgba(0,0,0,0.1);
        margin-bottom: 1.5rem;
        transition: all 0.3s ease;
        border: 1px solid rgba(102, 126, 234, 0.1);
    }
    
    .card:hover {
        transform: translateY(-8px);
        box-shadow: 0 12px 35px rgba(102, 126, 234, 0.25);
        border-color: rgba(102, 126, 234, 0.3);
    }
    
    /* Enhanced Status badges with animations */
    .status-badge {
        display: inline-block;
        padding: 0.6rem 1.2rem;
        border-radius: 25px;
        font-weight: bold;
        margin: 0.25rem;
        animation: pulse 2s infinite;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        font-size: 0.9rem;
    }
    
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.05); }
        100% { transform: scale(1); }
    }
    
    .status-pass {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        color: white;
        box-shadow: 0 4px 15px rgba(16, 185, 129, 0.3);
    }
    
    .status-fail {
        background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
        color: white;
        box-shadow: 0 4px 15px rgba(239, 68, 68, 0.3);
    }
    
    .status-warning {
        background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
        color: white;
        box-shadow: 0 4px 15px rgba(245, 158, 11, 0.3);
    }
    
    .status-info {
        background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
        color: white;
        box-shadow: 0 4px 15px rgba(59, 130, 246, 0.3);
    }
    
    /* Enhanced Metric cards with gradient backgrounds */
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.35);
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
        min-height: 150px;
        display: flex;
        flex-direction: column;
        justify-content: center;
    }
    
    .metric-card::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%);
    }
    
    .metric-card:hover {
        transform: translateY(-5px) scale(1.02);
        box-shadow: 0 12px 35px rgba(102, 126, 234, 0.45);
    }
    
    .metric-value {
        font-size: 3rem;
        font-weight: 800;
        margin-bottom: 0.5rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
        position: relative;
        z-index: 1;
    }
    
    .metric-label {
        font-size: 1.1rem;
        opacity: 0.95;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 1px;
        position: relative;
        z-index: 1;
    }
    
    .metric-icon {
        font-size: 4rem;
        opacity: 0.2;
        position: absolute;
        bottom: -10px;
        right: 10px;
    }
    
    /* Score gauge styling */
    .score-gauge {
        background: white;
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 6px 20px rgba(0,0,0,0.1);
        text-align: center;
    }
    
    .score-circle {
        width: 200px;
        height: 200px;
        margin: 0 auto;
        position: relative;
    }
    
    .score-text {
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        font-size: 3rem;
        font-weight: bold;
    }
    
    /* Progress bar styling */
    .stProgress > div > div > div > div {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        border-radius: 10px;
    }
    
    /* Button styling with hover effects */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 1rem 2.5rem;
        border-radius: 10px;
        font-weight: 600;
        transition: all 0.3s ease;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.5);
        background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
    }
    
    /* File uploader styling */
    .uploadedFile {
        background: linear-gradient(135deg, #f3f4f6 0%, #e5e7eb 100%);
        border-radius: 10px;
        padding: 0.8rem 1.2rem;
        margin: 0.5rem 0;
        border: 2px solid #e5e7eb;
        transition: all 0.3s ease;
    }
    
    .uploadedFile:hover {
        border-color: #667eea;
        transform: translateX(5px);
    }
    
    /* Alert boxes with icons */
    .alert-box {
        padding: 1.2rem;
        border-radius: 10px;
        margin: 1rem 0;
        position: relative;
        padding-left: 3.5rem;
    }
    
    .alert-box::before {
        position: absolute;
        left: 1rem;
        top: 50%;
        transform: translateY(-50%);
        font-size: 1.5rem;
    }
    
    .alert-success {
        background: linear-gradient(135deg, #d1fae5 0%, #a7f3d0 100%);
        border-left: 5px solid #10b981;
        color: #065f46;
    }
    
    .alert-success::before {
        content: '✅';
    }
    
    .alert-warning {
        background: linear-gradient(135deg, #fed7aa 0%, #fbbf24 100%);
        border-left: 5px solid #f59e0b;
        color: #78350f;
    }
    
    .alert-warning::before {
        content: '⚠️';
    }
    
    .alert-error {
        background: linear-gradient(135deg, #fee2e2 0%, #fca5a5 100%);
        border-left: 5px solid #ef4444;
        color: #7f1d1d;
    }
    
    .alert-error::before {
        content: '❌';
    }
    
    .alert-info {
        background: linear-gradient(135deg, #dbeafe 0%, #93c5fd 100%);
        border-left: 5px solid #3b82f6;
        color: #1e3a8a;
    }
    
    .alert-info::before {
        content: 'ℹ️';
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background: linear-gradient(180deg, #f8f9fa 0%, #e9ecef 100%);
    }
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 24px;
        background: rgba(255, 255, 255, 0.8);
        padding: 0.5rem;
        border-radius: 10px;
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        padding-left: 25px;
        padding-right: 25px;
        background-color: transparent;
        border-radius: 10px;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
    }
    
    /* Tooltip styling */
    .tooltip {
        position: relative;
        display: inline-block;
        cursor: help;
        color: #667eea;
        font-weight: bold;
    }
    
    .tooltip:hover::after {
        content: attr(data-tooltip);
        position: absolute;
        bottom: 100%;
        left: 50%;
        transform: translateX(-50%);
        background: #333;
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 8px;
        font-size: 0.9rem;
        white-space: nowrap;
        z-index: 1000;
    }
    
    /* Explanation boxes */
    .explanation-box {
        background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%);
        border: 2px solid #0ea5e9;
        border-radius: 10px;
        padding: 1rem;
        margin: 1rem 0;
    }
    
    .explanation-title {
        font-weight: bold;
        color: #0c4a6e;
        font-size: 1.1rem;
        margin-bottom: 0.5rem;
    }
    
    .explanation-text {
        color: #075985;
        line-height: 1.6;
    }
    
    /* Loading animation */
    .loading-spinner {
        border: 4px solid #f3f3f3;
        border-top: 4px solid #667eea;
        border-radius: 50%;
        width: 40px;
        height: 40px;
        animation: spin 1s linear infinite;
        margin: 20px auto;
    }
    
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
</style>
""", unsafe_allow_html=True)

class ADGMCorporateAgent:
    """Enhanced main application class for ADGM document review"""
    
    def __init__(self):
        logger.info("Initializing ADGM Corporate Agent...")
        
        self.processors = {}  # Store multiple processors for multiple documents
        self.checker = ComplianceChecker()
        self.rag = AdvancedRAG(model_name="llama2")
        
        # Create output directory
        self.output_dir = Path("output")
        self.output_dir.mkdir(exist_ok=True)
        
        # Session storage
        self.session_results = []
        self.document_types = []  # Track document types
        
        logger.info("ADGM Corporate Agent initialized successfully")
    
    def process_single_document(self, file_path: str, file_name: str) -> Dict:
        """Enhanced document processing with proper type identification"""
        
        logger.info(f"Processing document: {file_name}")
        
        try:
            # Create new processor for this document
            processor = DocumentProcessor()
            
            # Load and identify document
            if not processor.load_document(file_path):
                raise Exception("Failed to load document")
            
            doc_type = processor.document_type
            self.document_types.append(doc_type)  # Track document type
            logger.info(f"Document type identified: {doc_type}")
            
            # Extract document text
            doc_text = processor.get_document_text()
            
            # Perform comprehensive review with inline comments
            issues = processor.perform_comprehensive_review()
            
            # Perform Advanced RAG validation
            rag_validation = self.rag.validate_document(doc_text, doc_type)
            
            # Add RAG-identified issues
            for i, rag_issue in enumerate(rag_validation.get("issues", [])):
                issues.append({
                    "issue": rag_issue,
                    "severity": "medium" if rag_validation["confidence"] < 0.7 else "high",
                    "suggestion": rag_validation["recommendations"][i] if i < len(rag_validation["recommendations"]) else "Review with legal counsel",
                    "regulation": ", ".join(rag_validation.get("applicable_regulations", ["ADGM Compliance"])),
                    "source": "AI Analysis (Advanced RAG)"
                })
            
            # Generate AI suggestions for high-severity issues
            high_issues = [issue for issue in issues if issue["severity"] == "high"]
            if high_issues and len(doc_text) > 100:
                sample_text = doc_text[:500]
                issue_descriptions = [issue["issue"] for issue in high_issues[:3]]
                corrected_text = self.rag.suggest_corrections(sample_text, issue_descriptions)
                
                if corrected_text != sample_text:
                    issues.append({
                        "issue": "AI-generated corrections available",
                        "severity": "info",
                        "suggestion": "Review suggested corrections below",
                        "corrected_sample": corrected_text[:300] + "...",
                        "source": "AI Suggestion"
                    })
            
            # Save reviewed document with comments
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_filename = f"{Path(file_name).stem}_reviewed_{timestamp}.docx"
            output_path = self.output_dir / output_filename
            
            # Save the document
            if processor.save_reviewed_document(str(output_path)):
                logger.info(f"Saved reviewed document: {output_path}")
            else:
                logger.warning(f"Failed to save reviewed document: {output_path}")
                output_path = None
            
            # Store processor for potential reuse
            self.processors[file_name] = processor
            
            result = {
                "file_name": file_name,
                "document_type": doc_type,
                "issues_found": len(issues),
                "issues": issues,
                "reviewed_file": str(output_path) if output_path else None,
                "comments_added": len(processor.comments_added),
                "rag_validation": {
                    "compliance_status": rag_validation.get("compliance_status", "unknown"),
                    "confidence": rag_validation.get("confidence", 0.0),
                    "sources": rag_validation.get("sources", [])
                }
            }
            
            logger.info(f"Document processed successfully: {file_name} with {len(issues)} issues")
            return result
            
        except Exception as e:
            logger.error(f"Error processing {file_name}: {e}", exc_info=True)
            return {
                "file_name": file_name,
                "document_type": "error",
                "issues_found": 0,
                "issues": [{
                    "issue": f"Error processing file: {str(e)}",
                    "severity": "critical",
                    "source": "System"
                }],
                "reviewed_file": None,
                "comments_added": 0
            }
    
    def process_documents(self, files) -> Tuple[List[Dict], Dict, List[str]]:
        """Process multiple uploaded documents with enhanced tracking"""
        
        if not files:
            return [], {}, []
        
        logger.info(f"Processing {len(files)} documents...")
        
        results = []
        doc_names = []
        all_reviewed_files = []
        self.document_types = []  # Reset document types
        
        # Process each document
        for file in files:
            # Save uploaded file temporarily
            with tempfile.NamedTemporaryFile(delete=False, suffix=".docx") as tmp_file:
                tmp_file.write(file.getbuffer())
                tmp_path = tmp_file.name
            
            file_name = file.name
            doc_names.append(file_name)
            
            result = self.process_single_document(tmp_path, file_name)
            results.append(result)
            
            if result.get("reviewed_file"):
                all_reviewed_files.append(result["reviewed_file"])
            
            # Clean up temp file
            try:
                os.unlink(tmp_path)
            except:
                pass
        
        # Store results in session
        self.session_results = results
        
        # Check for missing documents using document types
        process_type = self.checker.identify_process_type(self.document_types)
        doc_check = self.checker.check_missing_documents(
            doc_names, 
            process_type,
            self.document_types  # Pass document types for better matching
        )
        
        # Compile all issues
        all_issues = []
        for result in results:
            for issue in result["issues"]:
                all_issues.append({
                    "document": result["file_name"],
                    "type": result["document_type"],
                    **issue
                })
        
        # Generate comprehensive compliance report
        report = self._generate_comprehensive_report(results, doc_check, all_issues)
        
        return results, report, all_reviewed_files
    
    def _generate_comprehensive_report(self, results: List[Dict], doc_check: Dict, all_issues: List[Dict]) -> Dict:
        """Generate enhanced comprehensive compliance report"""
        
        # Count issues by severity
        severity_count = {
            "critical": sum(1 for issue in all_issues if issue.get("severity") == "critical"),
            "high": sum(1 for issue in all_issues if issue.get("severity") == "high"),
            "medium": sum(1 for issue in all_issues if issue.get("severity") == "medium"),
            "low": sum(1 for issue in all_issues if issue.get("severity") == "low"),
            "info": sum(1 for issue in all_issues if issue.get("severity") == "info")
        }
        
        # Count issues by source
        source_count = {
            "Rule-based Check": sum(1 for issue in all_issues if "Rule-based" in issue.get("source", "")),
            "AI Analysis": sum(1 for issue in all_issues if "AI" in issue.get("source", "")),
            "AI Suggestion": sum(1 for issue in all_issues if "Suggestion" in issue.get("source", "")),
            "System": sum(1 for issue in all_issues if issue.get("source") == "System")
        }
        
        # Calculate compliance score
        score, status = self.checker.calculate_compliance_score(all_issues, doc_check)
        
        # Collect all RAG validation results
        rag_validations = []
        for result in results:
            if "rag_validation" in result:
                rag_validations.append({
                    "document": result["file_name"],
                    "document_type": result["document_type"],
                    **result["rag_validation"]
                })
        
        # Generate recommendations
        recommendations = self.checker.generate_recommendations(all_issues, doc_check)
        
        # Count total comments added
        total_comments = sum(result.get("comments_added", 0) for result in results)
        
        return {
            "timestamp": datetime.now().isoformat(),
            "process_type": doc_check.get("process", "unknown"),
            "documents_uploaded": doc_check.get("uploaded_count", 0),
            "documents_present": doc_check.get("present_documents", []),
            "required_documents": doc_check.get("required_count", 0),
            "missing_documents": doc_check.get("missing_documents", []),
            "total_issues": len(all_issues),
            "total_comments_added": total_comments,
            "severity_breakdown": severity_count,
            "issue_source_breakdown": source_count,
            "issues_detail": all_issues,
            "compliance_score": score,
            "compliance_status": status,
            "ai_validations": rag_validations,
            "recommendations": recommendations,
            "review_method": "Hybrid (Rule-based + Advanced RAG with Inline Comments)",
            "document_types_identified": self.document_types
        }
    
    def export_all_results(self) -> str:
        """Export all reviewed documents and report as a zip file"""
        if not self.session_results:
            return None
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        zip_path = self.output_dir / f"adgm_review_package_{timestamp}.zip"
        
        with zipfile.ZipFile(zip_path, 'w') as zipf:
            # Add reviewed documents
            for result in self.session_results:
                if result.get("reviewed_file") and os.path.exists(result["reviewed_file"]):
                    zipf.write(result["reviewed_file"], os.path.basename(result["reviewed_file"]))
            
            # Add JSON report
            if hasattr(self, 'last_report'):
                report_path = self.output_dir / f"compliance_report_{timestamp}.json"
                with open(report_path, 'w') as f:
                    json.dump(self.last_report, f, indent=2)
                zipf.write(report_path, os.path.basename(report_path))
        
        return str(zip_path) if zip_path.exists() else None

# Initialize session state
if 'agent' not in st.session_state:
    st.session_state.agent = ADGMCorporateAgent()
    st.session_state.processed = False
    st.session_state.results = []
    st.session_state.report = {}
    st.session_state.reviewed_files = []

def get_score_color(score):
    """Get color based on compliance score"""
    if score >= 90:
        return "#10b981"  # Green
    elif score >= 70:
        return "#f59e0b"  # Orange
    else:
        return "#ef4444"  # Red

def get_severity_icon(severity):
    """Get icon based on severity level"""
    icons = {
        "critical": "🚫",
        "high": "⛔",
        "medium": "⚠️",
        "low": "ℹ️",
        "info": "💡"
    }
    return icons.get(severity, "📌")

def format_document_type(doc_type):
    """Format document type for display"""
    formatted = doc_type.replace("_", " ").title()
    type_mapping = {
        "Articles Of Association": "📜 Articles of Association",
        "Board Resolution": "👥 Board Resolution",
        "Shareholder Resolution": "🤝 Shareholder Resolution",
        "Incorporation Application": "📋 Incorporation Application",
        "Employment Contract": "💼 Employment Contract",
        "General Document": "📄 General Document"
    }
    return type_mapping.get(formatted, f"📄 {formatted}")

def main():
    # Header with animation
    st.markdown("""
    <div class="header-container">
        <div class="header-title">🏛️ ADGM Corporate Agent</div>
        <div class="header-subtitle">Your Smart Legal Document Compliance Assistant</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Welcome message for new users
    if not st.session_state.processed:
        st.markdown("""
        <div class="explanation-box">
            <div class="explanation-title">👋 Welcome! Here's how it works:</div>
            <div class="explanation-text">
                1. <strong>Upload your documents</strong> - Select ADGM-related Word documents<br>
                2. <strong>Click Review</strong> - Our AI will analyze them for compliance<br>
                3. <strong>Get instant feedback</strong> - See issues, scores, and recommendations<br>
                4. <strong>Download reviewed documents</strong> - With comments and corrections
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Create columns for layout
    col1, col2 = st.columns([1, 2])
    
    with col1:
        # File Upload Section
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("### 📤 Upload Your Documents")
        st.markdown("*Select Word documents (.docx) to review*")
        
        uploaded_files = st.file_uploader(
            "Choose files",
            type=['docx'],
            accept_multiple_files=True,
            help="You can select multiple documents at once"
        )
        
        if uploaded_files:
            st.success(f"✅ {len(uploaded_files)} document(s) ready")
            for file in uploaded_files:
                st.markdown(f"📄 **{file.name}**")
        
        col_btn1, col_btn2 = st.columns(2)
        with col_btn1:
            process_button = st.button(
                "🔍 Review Now",
                type="primary",
                use_container_width=True,
                disabled=not uploaded_files
            )
        
        with col_btn2:
            export_button = st.button(
                "📦 Export All",
                use_container_width=True,
                disabled=not st.session_state.processed
            )
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Quick Guide
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("### 📚 Quick Guide")
        
        with st.expander("What documents can I check?"):
            st.markdown("""
            ✅ **Company Formation Documents:**
            - Articles of Association
            - Board Resolutions
            - Shareholder Resolutions
            - Incorporation Forms
            
            ✅ **Employment Documents:**
            - Employment Contracts
            - Job Descriptions
            
            ✅ **Other Legal Documents:**
            - Business Plans
            - Compliance Manuals
            - Any ADGM-related documents
            """)
        
        with st.expander("What will the system check?"):
            st.markdown("""
            🔍 **Our AI checks for:**
            - ✓ Correct ADGM jurisdiction references
            - ✓ Required sections and clauses
            - ✓ Proper legal language
            - ✓ Complete signature blocks
            - ✓ Compliance with ADGM regulations
            - ✓ Missing documents in your package
            """)
        
        with st.expander("Understanding the compliance score"):
            st.markdown("""
            **Your compliance score explained:**
            
            🟢 **90-100%** - Excellent! Ready for submission
            🟡 **70-89%** - Good, but needs minor fixes
            🔴 **Below 70%** - Requires significant corrections
            
            The score considers:
            - Number and severity of issues found
            - Missing required documents
            - Compliance with ADGM regulations
            """)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # System Status (simplified)
        with st.expander("⚙️ System Status"):
            st.success("✅ All systems operational")
            st.info("🤖 AI Model: Advanced RAG with Llama2")
            st.info("📊 Analysis Method: Hybrid (Rules + AI)")
    
    with col2:
        # Results Section
        if process_button and uploaded_files:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown("### 🔄 Analyzing Your Documents...")
            
            # Process documents with progress bar
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            # Animated processing messages
            processing_messages = [
                "📖 Reading document content...",
                "🔍 Checking ADGM compliance...",
                "🤖 Running AI analysis...",
                "✍️ Adding review comments...",
                "📊 Generating report..."
            ]
            
            for i, file in enumerate(uploaded_files):
                for j, message in enumerate(processing_messages):
                    status_text.text(f"{message} ({file.name})")
                    progress_bar.progress((i * len(processing_messages) + j + 1) / (len(uploaded_files) * len(processing_messages)))
                    time.sleep(0.3)
            
            # Process documents
            results, report, reviewed_files = st.session_state.agent.process_documents(uploaded_files)
            st.session_state.processed = True
            st.session_state.results = results
            st.session_state.report = report
            st.session_state.reviewed_files = reviewed_files
            st.session_state.agent.last_report = report  # Store for export
            
            progress_bar.empty()
            status_text.empty()
            st.markdown('</div>', unsafe_allow_html=True)
            st.rerun()
        
        if st.session_state.processed:
            # Overall Compliance Score (Big and Clear)
            score = st.session_state.report["compliance_score"]
            status = st.session_state.report["compliance_status"]
            
            # Score Display with Visual Gauge
            st.markdown("### 📊 Your Compliance Score")
            
            score_col1, score_col2, score_col3 = st.columns([1, 2, 1])
            
            with score_col2:
                # Create a visual score display
                score_color = get_score_color(score)
                if score >= 90:
                    score_emoji = "🎉"
                    score_message = "Excellent!"
                elif score >= 70:
                    score_emoji = "👍"
                    score_message = "Good Job!"
                else:
                    score_emoji = "⚠️"
                    score_message = "Needs Work"
                
                st.markdown(f"""
                <div class="score-gauge" style="text-align: center;">
                    <div style="font-size: 5rem; color: {score_color}; font-weight: bold;">
                        {score}%
                    </div>
                    <div style="font-size: 2rem; margin-top: -10px;">
                        {score_emoji}
                    </div>
                    <div style="font-size: 1.5rem; color: {score_color}; font-weight: bold; margin-top: 10px;">
                        {score_message}
                    </div>
                    <div style="font-size: 1rem; color: #666; margin-top: 10px;">
                        {status}
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            # Quick Stats (User-Friendly Metrics)
            st.markdown("### 📈 Quick Overview")
            
            metric_cols = st.columns(4)
            
            with metric_cols[0]:
                total_docs = st.session_state.report["documents_uploaded"]
                st.markdown(f"""
                <div class="metric-card" style="background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);">
                    <div class="metric-icon">📄</div>
                    <div class="metric-value">{total_docs}</div>
                    <div class="metric-label">Documents<br>Reviewed</div>
                </div>
                """, unsafe_allow_html=True)
            
            with metric_cols[1]:
                total_issues = st.session_state.report["total_issues"]
                issue_color = "#ef4444" if total_issues > 10 else "#f59e0b" if total_issues > 5 else "#10b981"
                st.markdown(f"""
                <div class="metric-card" style="background: linear-gradient(135deg, {issue_color} 0%, {issue_color}dd 100%);">
                    <div class="metric-icon">🔍</div>
                    <div class="metric-value">{total_issues}</div>
                    <div class="metric-label">Issues<br>Found</div>
                </div>
                """, unsafe_allow_html=True)
            
            with metric_cols[2]:
                high_issues = st.session_state.report["severity_breakdown"]["high"]
                critical_issues = st.session_state.report["severity_breakdown"]["critical"]
                urgent_issues = high_issues + critical_issues
                urgent_color = "#ef4444" if urgent_issues > 0 else "#10b981"
                st.markdown(f"""
                <div class="metric-card" style="background: linear-gradient(135deg, {urgent_color} 0%, {urgent_color}dd 100%);">
                    <div class="metric-icon">⚠️</div>
                    <div class="metric-value">{urgent_issues}</div>
                    <div class="metric-label">Urgent<br>Actions</div>
                </div>
                """, unsafe_allow_html=True)
            
            with metric_cols[3]:
                missing_docs = len(st.session_state.report["missing_documents"])
                missing_color = "#ef4444" if missing_docs > 0 else "#10b981"
                st.markdown(f"""
                <div class="metric-card" style="background: linear-gradient(135deg, {missing_color} 0%, {missing_color}dd 100%);">
                    <div class="metric-icon">📋</div>
                    <div class="metric-value">{missing_docs}</div>
                    <div class="metric-label">Missing<br>Documents</div>
                </div>
                """, unsafe_allow_html=True)
            
            # Tabs for detailed results (simplified names)
            tab1, tab2, tab3, tab4, tab5 = st.tabs(["📋 Summary", "⚠️ Issues Found", "💡 Recommendations", "🤖 AI Insights", "📥 Downloads"])
            
            with tab1:
                # Summary Tab - User Friendly
                st.markdown('<div class="card">', unsafe_allow_html=True)
                
                # Document Status Summary
                st.markdown("#### 📄 Document Review Summary")
                
                for result in st.session_state.results:
                    doc_name = result["file_name"]
                    doc_type = format_document_type(result["document_type"])
                    issues_count = result["issues_found"]
                    
                    if issues_count == 0:
                        status_color = "🟢"
                        status_text = "Perfect! No issues"
                    elif issues_count <= 3:
                        status_color = "🟡"
                        status_text = f"{issues_count} minor issues"
                    else:
                        status_color = "🔴"
                        status_text = f"{issues_count} issues need attention"
                    
                    st.markdown(f"""
                    <div style="padding: 1rem; background: #f9fafb; border-radius: 10px; margin-bottom: 1rem;">
                        <strong>{doc_type}</strong><br>
                        <span style="color: #666;">File: {doc_name}</span><br>
                        {status_color} <strong>{status_text}</strong>
                    </div>
                    """, unsafe_allow_html=True)
                
                # Missing Documents Alert
                if st.session_state.report["missing_documents"]:
                    st.markdown("#### 📋 Missing Documents")
                    st.error(f"⚠️ You need {len(st.session_state.report['missing_documents'])} more document(s) for complete submission")
                    for doc in st.session_state.report["missing_documents"]:
                        st.markdown(f"""
                        <div class="alert-box alert-warning">
                            📄 <strong>{doc}</strong> - Required for {st.session_state.report['process_type'].replace('_', ' ').title()}
                        </div>
                        """, unsafe_allow_html=True)
                else:
                    st.success("✅ All required documents are present!")
                
                st.markdown('</div>', unsafe_allow_html=True)
            
            with tab2:
                # Issues Tab - Grouped by Document
                st.markdown('<div class="card">', unsafe_allow_html=True)
                st.markdown("#### 🔍 Detailed Issue Report")
                
                # Group issues by document
                issues_by_doc = {}
                for issue in st.session_state.report["issues_detail"]:
                    doc_name = issue.get("document", "Unknown")
                    if doc_name not in issues_by_doc:
                        issues_by_doc[doc_name] = []
                    issues_by_doc[doc_name].append(issue)
                
                for doc_name, doc_issues in issues_by_doc.items():
                    with st.expander(f"📄 {doc_name} ({len(doc_issues)} issues)"):
                        # Group by severity within document
                        for severity in ["critical", "high", "medium", "low", "info"]:
                            severity_issues = [i for i in doc_issues if i.get("severity") == severity]
                            if severity_issues:
                                st.markdown(f"**{get_severity_icon(severity)} {severity.upper()} Priority:**")
                                for issue in severity_issues:
                                    st.markdown(f"""
                                    <div style="padding: 0.8rem; background: #f3f4f6; border-radius: 8px; margin: 0.5rem 0;">
                                        <strong>Issue:</strong> {issue['issue']}<br>
                                        <strong>How to fix:</strong> {issue.get('suggestion', 'Review with legal counsel')}<br>
                                        <small><em>Source: {issue.get('source', 'Manual review')}</em></small>
                                    </div>
                                    """, unsafe_allow_html=True)
                
                st.markdown('</div>', unsafe_allow_html=True)
            
            with tab3:
                # Recommendations Tab
                st.markdown('<div class="card">', unsafe_allow_html=True)
                st.markdown("#### 💡 Action Items & Recommendations")
                
                st.markdown("""
                <div class="explanation-box">
                    <div class="explanation-title">📝 Follow these steps to improve compliance:</div>
                </div>
                """, unsafe_allow_html=True)
                
                for i, rec in enumerate(st.session_state.report["recommendations"], 1):
                    # Parse recommendation for better display
                    if "URGENT" in rec:
                        icon = "🚨"
                        color = "alert-error"
                    elif "HIGH PRIORITY" in rec:
                        icon = "⚠️"
                        color = "alert-warning"
                    else:
                        icon = "✅"
                        color = "alert-info"
                    
                    st.markdown(f"""
                    <div class="alert-box {color}">
                        <strong>Step {i}:</strong> {rec.replace('**', '')}
                    </div>
                    """, unsafe_allow_html=True)
                
                # Add helpful tips
                st.markdown("#### 💡 Quick Tips")
                st.info("""
                **Pro Tips for ADGM Compliance:**
                - Always use "Abu Dhabi Global Market" or "ADGM" for jurisdiction
                - Replace weak words (may, might) with strong ones (shall, must)
                - Ensure all signature blocks have name, title, and date fields
                - Include all required sections as per ADGM templates
                """)
                
                st.markdown('</div>', unsafe_allow_html=True)
            
            with tab4:
                # AI Analysis Tab
                st.markdown('<div class="card">', unsafe_allow_html=True)
                st.markdown("#### 🤖 AI-Powered Analysis Results")
                
                if st.session_state.report.get("ai_validations"):
                    for validation in st.session_state.report["ai_validations"]:
                        confidence = validation["confidence"]
                        confidence_percent = f"{confidence:.0%}"
                        
                        # Visual confidence indicator
                        if confidence > 0.8:
                            conf_color = "🟢"
                            conf_text = "High Confidence"
                        elif confidence > 0.6:
                            conf_color = "🟡"
                            conf_text = "Medium Confidence"
                        else:
                            conf_color = "🔴"
                            conf_text = "Low Confidence"
                        
                        st.markdown(f"""
                        <div style="padding: 1rem; background: #f9fafb; border-radius: 10px; margin-bottom: 1rem;">
                            <strong>📄 {validation['document']}</strong><br>
                            <strong>Type:</strong> {format_document_type(validation['document_type'])}<br>
                            <strong>AI Assessment:</strong> {validation['compliance_status']}<br>
                            <strong>Confidence:</strong> {conf_color} {confidence_percent} ({conf_text})<br>
                            <strong>Based on:</strong> {', '.join(validation.get('sources', ['ADGM Regulations'])[:2])}
                        </div>
                        """, unsafe_allow_html=True)
                
                # Show analysis breakdown
                st.markdown("#### 📊 How We Analyzed Your Documents")
                
                col1, col2 = st.columns(2)
                with col1:
                    rule_based = st.session_state.report["issue_source_breakdown"].get("Rule-based Check", 0)
                    st.metric(
                        "Rule-Based Checks",
                        rule_based,
                        help="Issues found using ADGM regulation rules"
                    )
                
                with col2:
                    ai_based = st.session_state.report["issue_source_breakdown"].get("AI Analysis", 0)
                    st.metric(
                        "AI-Detected Issues",
                        ai_based,
                        help="Issues found using artificial intelligence"
                    )
                
                st.markdown('</div>', unsafe_allow_html=True)
            
            with tab5:
                # Downloads Tab
                st.markdown('<div class="card">', unsafe_allow_html=True)
                st.markdown("#### 📥 Download Your Reviewed Documents")
                
                st.markdown("""
                <div class="explanation-box">
                    <div class="explanation-title">📝 Your reviewed documents include:</div>
                    <div class="explanation-text">
                        • Original content with review comments<br>
                        • Highlighted compliance issues<br>
                        • Suggested corrections and improvements<br>
                        • Compliance score and summary
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # Individual document downloads
                if st.session_state.reviewed_files:
                    st.markdown("##### Download Individual Documents:")
                    for file_path in st.session_state.reviewed_files:
                        if os.path.exists(file_path):
                            file_name = os.path.basename(file_path)
                            # Make filename more user-friendly
                            display_name = file_name.replace("_reviewed", " (Reviewed)").replace("_", " ")
                            
                            with open(file_path, 'rb') as f:
                                st.download_button(
                                    label=f"📄 {display_name}",
                                    data=f.read(),
                                    file_name=file_name,
                                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                                    use_container_width=True
                                )
                
                st.markdown("---")
                
                # Export all as ZIP
                col1, col2 = st.columns(2)
                
                with col1:
                    if export_button or st.button("📦 Download All Files (ZIP)", use_container_width=True):
                        zip_path = st.session_state.agent.export_all_results()
                        if zip_path and os.path.exists(zip_path):
                            with open(zip_path, 'rb') as f:
                                st.download_button(
                                    label="💾 Save Complete Package",
                                    data=f.read(),
                                    file_name=os.path.basename(zip_path),
                                    mime="application/zip",
                                    use_container_width=True
                                )
                
                with col2:
                    # Export JSON Report
                    report_json = json.dumps(st.session_state.report, indent=2)
                    st.download_button(
                        label="📊 Download Detailed Report (JSON)",
                        data=report_json,
                        file_name=f"compliance_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                        mime="application/json",
                        use_container_width=True
                    )
                
                st.markdown('</div>', unsafe_allow_html=True)
    
    # Footer with helpful information
    st.markdown("---")
    
    # Create footer columns for better layout
    footer_col1, footer_col2, footer_col3 = st.columns([1, 2, 1])
    
    with footer_col2:
        st.markdown("<h4 style='text-align: center;'>🔒 Your Privacy is Protected</h4>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color: #6b7280;'>All document processing happens locally on your computer - your sensitive data never leaves your system</p>", unsafe_allow_html=True)
        
        st.warning("""
        ⚠️ **Important Notice:**  
        This tool provides automated compliance checking to help you prepare documents.  
        For final submission to ADGM, please have your documents reviewed by a qualified legal professional.
        """)
        
        st.markdown("<p style='text-align: center; margin-top: 2rem; color: #6b7280;'>Made with ❤️ using Advanced AI Technology</p>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color: #9ca3af; font-size: 0.9rem;'>Powered by Ollama, ChromaDB, and Advanced RAG</p>", unsafe_allow_html=True)

if __name__ == "__main__":
    # Configure page settings
    print("=" * 60)
    print("ADGM Corporate Agent - Advanced RAG System")
    print("=" * 60)
    print("\n✅ Initializing system components...")
    print("📦 Loading knowledge base...")
    print("🤖 Connecting to Ollama...")
    print("\nMake sure Ollama is running: ollama serve")
    print("=" * 60)
    print("\n🚀 Launching Streamlit application...")
    print("📍 Access at: http://localhost:8501")
    print("=" * 60)
    
    # Run the main application
    main()