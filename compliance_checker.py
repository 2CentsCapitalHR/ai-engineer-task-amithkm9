"""
Compliance Checker Module - Enhanced Version
Validates documents against ADGM requirements with improved accuracy
"""

class ComplianceChecker:
    """Check compliance with ADGM regulations"""
    
    def __init__(self):
        self.adgm_requirements = {
            "company_incorporation": {
                "required": [
                    "Articles of Association",
                    "Board Resolution", 
                    "Shareholder Resolution",
                    "Incorporation Application Form",
                    "Register of Members and Directors"
                ],
                "optional": [
                    "UBO Declaration Form",
                    "Memorandum of Association",
                    "Power of Attorney"
                ]
            },
            "licensing": {
                "required": [
                    "License Application Form",
                    "Business Plan",
                    "Compliance Manual",
                    "Board Resolution for License",
                    "Financial Projections"
                ],
                "optional": [
                    "Reference Letters",
                    "CV of Key Personnel"
                ]
            },
            "employment": {
                "required": [
                    "Employment Contract",
                    "Job Description",
                    "Salary Certificate"
                ],
                "optional": [
                    "Offer Letter",
                    "Non-Disclosure Agreement"
                ]
            }
        }
        
        # Enhanced document type mappings for better matching
        self.document_type_mappings = {
            "articles_of_association": "Articles of Association",
            "board_resolution": "Board Resolution",
            "shareholder_resolution": "Shareholder Resolution", 
            "incorporation_application": "Incorporation Application Form",
            "register": "Register of Members and Directors",
            "memorandum": "Memorandum of Association",
            "ubo_declaration": "UBO Declaration Form",
            "employment_contract": "Employment Contract",
            "license_application": "License Application Form",
            "business_plan": "Business Plan",
            "compliance_manual": "Compliance Manual",
            "commercial_agreement": "Commercial Agreement",
            "general_document": "General Document"
        }
    
    def identify_process_type(self, document_types: list[str]) -> str:
        """Identify which ADGM process based on document types"""
        
        # Convert document types to standard names
        standard_names = []
        for doc_type in document_types:
            # Check if it's a document type identifier
            mapped_name = self.document_type_mappings.get(doc_type)
            if mapped_name:
                standard_names.append(mapped_name)
            else:
                # Fallback: try to match partial names
                for key, value in self.document_type_mappings.items():
                    if key in doc_type.lower() or doc_type.lower() in key:
                        standard_names.append(value)
                        break
        
        # Check for incorporation documents
        incorporation_docs = self.adgm_requirements["company_incorporation"]["required"]
        incorporation_matches = sum(1 for doc in standard_names if doc in incorporation_docs)
        
        # Check for licensing documents  
        licensing_docs = self.adgm_requirements["licensing"]["required"]
        licensing_matches = sum(1 for doc in standard_names if doc in licensing_docs)
        
        # Check for employment documents
        employment_docs = self.adgm_requirements["employment"]["required"]
        employment_matches = sum(1 for doc in standard_names if doc in employment_docs)
        
        # Return the process with most matches
        if incorporation_matches > 0:
            return "company_incorporation"
        elif licensing_matches > employment_matches:
            return "licensing"
        elif employment_matches > 0:
            return "employment"
        else:
            return "company_incorporation"  # Default to most common
    
    def check_missing_documents(self, uploaded_docs: list[str], process_type: str, 
                               document_types: list[str] = None) -> dict:
        """Enhanced missing document check using document types"""
        
        if process_type not in self.adgm_requirements:
            return {
                "process": "unknown",
                "missing_documents": [],
                "uploaded_count": len(uploaded_docs),
                "required_count": 0,
                "present_documents": []
            }
        
        required_docs = self.adgm_requirements[process_type]["required"]
        present_docs = []
        missing_docs = []
        
        # If we have document types, use them for more accurate matching
        if document_types:
            standard_names = []
            for doc_type in document_types:
                mapped_name = self.document_type_mappings.get(doc_type)
                if mapped_name:
                    standard_names.append(mapped_name)
            
            # Check which required documents are present
            for required in required_docs:
                if required in standard_names:
                    present_docs.append(required)
                else:
                    missing_docs.append(required)
        else:
            # Fallback to filename matching
            uploaded_lower = [doc.lower() for doc in uploaded_docs]
            
            for required in required_docs:
                found = False
                required_keywords = required.lower().split()
                
                for uploaded in uploaded_lower:
                    # Check if key terms from required doc name are in uploaded filename
                    matches = sum(1 for keyword in required_keywords 
                                if keyword in uploaded and len(keyword) > 3)
                    if matches >= len(required_keywords) * 0.5:  # At least 50% match
                        found = True
                        break
                
                if found:
                    present_docs.append(required)
                else:
                    missing_docs.append(required)
        
        return {
            "process": process_type,
            "missing_documents": missing_docs,
            "present_documents": present_docs,
            "uploaded_count": len(uploaded_docs),
            "required_count": len(required_docs)
        }
    
    def calculate_compliance_score(self, issues: list[dict], doc_check: dict) -> tuple[int, str]:
        """Calculate overall compliance score and status with balanced scoring"""
        
        # Updated scoring weights (more balanced)
        weights = {
            "critical": -15,  # Critical issues
            "high": -5,       # Reduced from -8 (was too harsh)
            "medium": -2,     # Reduced from -3
            "low": -1,        # Low severity issues
            "info": 0         # Informational only
        }
        
        # Start with perfect score
        score = 100
        
        # Deduct for issues (exclude AI suggestions from penalties)
        actual_issues_count = 0
        for issue in issues:
            severity = issue.get("severity", "low")
            source = issue.get("source", "")
            
            # Don't count AI suggestions as penalties
            if "AI Suggestion" in source:
                continue
                
            actual_issues_count += 1
            score += weights.get(severity, 0)
        
        # Deduct for missing documents (more balanced scoring)
        missing_count = len(doc_check.get("missing_documents", []))
        required_count = doc_check.get("required_count", 5)
        
        if required_count > 0:
            # Calculate percentage of missing documents
            missing_percentage = missing_count / required_count
            # Deduct up to 25 points for missing documents (reduced from 30)
            missing_penalty = int(missing_percentage * 25)
            score -= missing_penalty
        
        # Bonus points for having required documents present
        present_count = len(doc_check.get("present_documents", []))
        if present_count > 0 and required_count > 0:
            completion_bonus = (present_count / required_count) * 15  # Increased bonus
            score += completion_bonus
        
        # Additional bonus for low issue count relative to document complexity
        if actual_issues_count <= 2 and present_count > 0:
            score += 5  # Small bonus for well-prepared documents
        
        # Ensure score is between 0 and 100
        score = max(0, min(100, score))
        
        # Determine status based on score (adjusted thresholds)
        if score >= 85:
            status = "PASS - Excellent compliance, ready for submission"
        elif score >= 70:
            status = "PASS - Good compliance, minor review recommended"
        elif score >= 55:  # Lowered threshold
            status = "REVIEW REQUIRED - Minor corrections needed"
        elif score >= 35:  # Lowered threshold
            status = "FAIL - Significant corrections required"
        else:
            status = "CRITICAL - Major non-compliance detected"
        
        return int(score), status
    
    def generate_recommendations(self, issues: list[dict], doc_check: dict) -> list[str]:
        """Generate comprehensive compliance recommendations"""
        recommendations = []
        
        # Priority 1: Missing documents
        if doc_check.get("missing_documents"):
            missing_list = ", ".join(doc_check['missing_documents'])
            recommendations.append(
                f"📄 **URGENT**: Upload missing documents: {missing_list}"
            )
        
        # Priority 2: Critical and high-severity issues
        critical_count = sum(1 for issue in issues if issue.get("severity") == "critical")
        high_count = sum(1 for issue in issues if issue.get("severity") == "high" and "AI Suggestion" not in issue.get("source", ""))
        
        if critical_count > 0:
            recommendations.append(
                f"🚫 **CRITICAL**: Fix {critical_count} critical compliance issues immediately"
            )
        
        if high_count > 0:
            recommendations.append(
                f"🔴 **HIGH PRIORITY**: Address {high_count} high-severity issues before submission"
            )
        
        # Priority 3: Common issue patterns
        jurisdiction_issues = sum(1 for issue in issues if "jurisdiction" in issue.get("issue", "").lower())
        weak_language_issues = sum(1 for issue in issues if "weak language" in issue.get("issue", "").lower())
        signature_issues = sum(1 for issue in issues if "signature" in issue.get("issue", "").lower())
        missing_section_issues = sum(1 for issue in issues if "missing required section" in issue.get("issue", "").lower())
        
        # Specific recommendations based on issue patterns
        if jurisdiction_issues > 0:
            recommendations.append(
                "⚖️ **JURISDICTION**: Update all references to specify 'Abu Dhabi Global Market (ADGM)' instead of UAE/DIFC"
            )
        
        if weak_language_issues > 0:
            recommendations.append(
                "📝 **LANGUAGE**: Replace weak terms (may, might, could, perhaps) with binding language (shall, must, will)"
            )
        
        if missing_section_issues > 0:
            recommendations.append(
                "➕ **SECTIONS**: Add missing required sections as per ADGM regulatory templates"
            )
        
        if signature_issues > 0:
            recommendations.append(
                "✍️ **SIGNATURES**: Complete all signature blocks with full names, titles, and dates"
            )
        
        # Priority 4: Medium severity issues
        medium_count = sum(1 for issue in issues if issue.get("severity") == "medium" and "AI Suggestion" not in issue.get("source", ""))
        if medium_count > 0:
            recommendations.append(
                f"🟡 **REVIEW**: Address {medium_count} medium-priority issues for better compliance"
            )
        
        # Add positive feedback if applicable
        if not doc_check.get("missing_documents") and high_count == 0 and critical_count == 0:
            if medium_count > 0:
                recommendations.append(
                    "✅ **GOOD**: Documents are largely compliant - address minor issues and submit"
                )
            else:
                recommendations.append(
                    "✅ **EXCELLENT**: Documents appear fully compliant with ADGM regulations"
                )
        
        # Add guidance for next steps
        if doc_check.get("missing_documents") or high_count > 0 or critical_count > 0:
            recommendations.append(
                "📋 **NEXT STEPS**: 1) Address high-priority issues, 2) Upload missing documents, 3) Review recommendations, 4) Re-submit for validation"
            )
        
        return recommendations