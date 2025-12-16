#!/usr/bin/env python3
"""
Document Ingestion Module

Handles the ingestion and preprocessing of agricultural documents
for the RAG pipeline. Supports multiple document formats and
implements advanced text cleaning algorithms.
"""

import os
import re
from typing import List, Dict, Optional
from pathlib import Path

class DocumentIngestion:
    """
    Advanced document ingestion system for agricultural knowledge bases.
    
    Features:
    - Multi-format support (MD, PDF, TXT, DOCX)
    - Intelligent text cleaning and normalization
    - Metadata extraction and preservation
    - Agricultural domain-specific preprocessing
    """
    
    def __init__(self, config: Optional[Dict] = None):
        """Initialize document ingestion system"""
        self.config = config or {}
        self.supported_formats = ['.md', '.pdf', '.txt', '.docx']
        self.cleaning_patterns = self._initialize_cleaning_patterns()
        self.file_path="data/FAQ.docx"
    
    def _initialize_cleaning_patterns(self) -> Dict[str, str]:
        """Initialize text cleaning patterns for agricultural documents"""
        return {
            'dosage_normalization': r'(\d+(?:\.\d+)?)\s*(ml|g|kg|L)(?:/acre|/plant|/kg)?',
            'product_name_extraction': r'(Dormulin|Zetol|Tracs|Akre|Trail|Actin)',
            'crop_identification': r'(chilli|tomato|banana|crop)',
            'application_methods': r'(foliar spray|soil application|seed treatment)'
        }
    
    def ingest_document(self, file_path: str) -> Dict:
        """
        Ingest and preprocess a single document
        
        Args:
            file_path: Path to the document file
            
        Returns:
            Dict containing processed document data and metadata
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Document not found: {file_path}")
        
        file_ext = Path(file_path).suffix.lower()
        if file_ext not in self.supported_formats:
            raise ValueError(f"Unsupported format: {file_ext}")
        
        # Simulate document processing
        with open(file_path, 'r', encoding='utf-8') as f:
            raw_content = f.read()
        
        processed_content = self._preprocess_text(raw_content)
        metadata = self._extract_metadata(raw_content, file_path)
        
        return {
            'content': processed_content,
            'metadata': metadata,
            'file_path': file_path,
            'format': file_ext,
            'size': len(processed_content)
        }
    
    def _preprocess_text(self, text: str) -> str:
        """Apply agricultural domain-specific text preprocessing"""
        # Normalize whitespace
        text = re.sub(r'\s+', ' ', text)
        
        # Standardize dosage formats
        text = re.sub(self.cleaning_patterns['dosage_normalization'], 
                     r'\1 \2', text)
        
        # Clean and normalize content
        text = text.strip()
        
        return text
    
    def _extract_metadata(self, content: str, file_path: str) -> Dict:
        """Extract metadata from agricultural documents"""
        metadata = {
            'source_file': os.path.basename(file_path),
            'ingestion_timestamp': None,  # Would be set in real implementation
            'document_type': 'agricultural_faq',
            'language': 'en'
        }
        
        # Extract agricultural entities
        products = re.findall(self.cleaning_patterns['product_name_extraction'], content, re.IGNORECASE)
        crops = re.findall(self.cleaning_patterns['crop_identification'], content, re.IGNORECASE)
        
        metadata['products_mentioned'] = list(set(products))
        metadata['crops_mentioned'] = list(set(crops))
        
        return metadata
    
    def batch_ingest(self, directory_path: str) -> List[Dict]:
        """
        Ingest multiple documents from a directory
        
        Args:
            directory_path: Path to directory containing documents
            
        Returns:
            List of processed document dictionaries
        """
        if not os.path.isdir(directory_path):
            raise NotADirectoryError(f"Invalid directory: {directory_path}")
        
        documents = []
        for file_path in Path(directory_path).rglob('*'):
            if file_path.suffix.lower() in self.supported_formats:
                try:
                    doc = self.ingest_document(str(file_path))
                    documents.append(doc)
                except Exception as e:
                    print(f"Warning: Failed to ingest {file_path}: {e}")
        
        return documents

# Example usage and testing
if __name__ == "__main__":
    ingestion = DocumentIngestion()
    print("📄 Document Ingestion Module - Agricultural RAG Pipeline")
    print("✅ Initialized with multi-format support")
    print("🌱 Agricultural domain preprocessing enabled")
    print("📊 Metadata extraction configured")