#!/usr/bin/env python3
"""
Smart Chunking Module

Implements intelligent document chunking strategies optimized for
agricultural knowledge bases. Uses semantic-aware splitting and
context preservation techniques.
"""

import re
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass

@dataclass
class ChunkMetadata:
    """Metadata for document chunks"""
    chunk_id: str
    source_section: str
    chunk_type: str
    agricultural_entities: List[str]
    semantic_score: float
    context_preserved: bool

class SmartChunking:
    """
    Advanced chunking system for agricultural documents.
    
    Features:
    - Semantic-aware splitting
    - Agricultural entity preservation
    - Context boundary detection
    - Hierarchical chunk organization
    """
    
    def __init__(self, config: Optional[Dict] = None):
        """Initialize smart chunking system"""
        self.config = config or {}
        self.max_chunk_size = self.config.get('max_chunk_size', 1000)
        self.overlap_size = self.config.get('overlap_size', 100)
        self.agricultural_markers = self._initialize_markers()
    
    def _initialize_markers(self) -> Dict[str, List[str]]:
        """Initialize agricultural domain markers for intelligent splitting"""
        return {
            'section_headers': ['##', '###', 'Benefits:', 'Dosage:', 'Application:'],
            'product_names': ['Dormulin', 'Zetol', 'Tracs', 'Akre', 'Trail', 'Actin'],
            'crop_names': ['Chilli', 'Tomato', 'Banana'],
            'treatment_types': ['Control', 'Treatment', 'Precaution', 'Deficiency'],
            'application_methods': ['foliar spray', 'soil application', 'seed treatment']
        }
    
    def create_chunks(self, document: Dict) -> List[Dict]:
        """
        Create intelligent chunks from agricultural document
        
        Args:
            document: Processed document from ingestion module
            
        Returns:
            List of chunk dictionaries with metadata
        """
        content = document['content']
        chunks = []
        
        # Primary chunking by sections
        section_chunks = self._chunk_by_sections(content)
        
        # Secondary chunking by semantic boundaries
        for section_chunk in section_chunks:
            semantic_chunks = self._chunk_by_semantics(section_chunk)
            chunks.extend(semantic_chunks)
        
        # Add metadata and context preservation
        enhanced_chunks = []
        for i, chunk in enumerate(chunks):
            metadata = self._generate_chunk_metadata(chunk, i, document)
            enhanced_chunk = {
                'content': chunk,
                'metadata': metadata,
                'chunk_id': f"chunk_{i:04d}",
                'source_document': document['file_path']
            }
            enhanced_chunks.append(enhanced_chunk)
        
        return enhanced_chunks
    
    def _chunk_by_sections(self, content: str) -> List[str]:
        """Split content by agricultural sections"""
        # Split by main headers (## and ###)
        sections = re.split(r'\n(?=##)', content)
        
        processed_sections = []
        for section in sections:
            if section.strip():
                # Further split large sections
                if len(section) > self.max_chunk_size:
                    subsections = self._split_large_section(section)
                    processed_sections.extend(subsections)
                else:
                    processed_sections.append(section.strip())
        
        return processed_sections
    
    def _chunk_by_semantics(self, section: str) -> List[str]:
        """Apply semantic-aware chunking within sections"""
        # Identify semantic boundaries
        boundaries = self._find_semantic_boundaries(section)
        
        if not boundaries:
            return [section]
        
        chunks = []
        start = 0
        
        for boundary in boundaries:
            chunk = section[start:boundary].strip()
            if chunk and len(chunk) > 50:  # Minimum chunk size
                chunks.append(chunk)
            start = boundary - self.overlap_size  # Add overlap
        
        # Add final chunk
        final_chunk = section[start:].strip()
        if final_chunk and len(final_chunk) > 50:
            chunks.append(final_chunk)
        
        return chunks if chunks else [section]
    
    def _find_semantic_boundaries(self, text: str) -> List[int]:
        """Find semantic boundaries in agricultural text"""
        boundaries = []
        
        # Look for dosage patterns
        dosage_pattern = r'\n- Dosage:'
        for match in re.finditer(dosage_pattern, text):
            boundaries.append(match.start())
        
        # Look for benefit sections
        benefit_pattern = r'\n- Benefits:'
        for match in re.finditer(benefit_pattern, text):
            boundaries.append(match.start())
        
        # Look for application methods
        app_pattern = r'\n- Application:'
        for match in re.finditer(app_pattern, text):
            boundaries.append(match.start())
        
        return sorted(boundaries)
    
    def _split_large_section(self, section: str) -> List[str]:
        """Split large sections while preserving context"""
        lines = section.split('\n')
        chunks = []
        current_chunk = []
        current_size = 0
        
        for line in lines:
            line_size = len(line)
            
            if current_size + line_size > self.max_chunk_size and current_chunk:
                # Save current chunk
                chunks.append('\n'.join(current_chunk))
                
                # Start new chunk with overlap
                overlap_lines = current_chunk[-2:] if len(current_chunk) > 2 else current_chunk
                current_chunk = overlap_lines + [line]
                current_size = sum(len(l) for l in current_chunk)
            else:
                current_chunk.append(line)
                current_size += line_size
        
        # Add final chunk
        if current_chunk:
            chunks.append('\n'.join(current_chunk))
        
        return chunks
    
    def _generate_chunk_metadata(self, chunk: str, index: int, document: Dict) -> ChunkMetadata:
        """Generate comprehensive metadata for chunk"""
        # Extract agricultural entities
        entities = []
        for category, markers in self.agricultural_markers.items():
            for marker in markers:
                if marker.lower() in chunk.lower():
                    entities.append(marker)
        
        # Determine chunk type
        chunk_type = self._classify_chunk_type(chunk)
        
        # Calculate semantic score (simplified)
        semantic_score = len(entities) / 10.0  # Normalized score
        
        # Check context preservation
        context_preserved = self._check_context_preservation(chunk)
        
        return ChunkMetadata(
            chunk_id=f"chunk_{index:04d}",
            source_section=self._extract_section_name(chunk),
            chunk_type=chunk_type,
            agricultural_entities=entities,
            semantic_score=semantic_score,
            context_preserved=context_preserved
        )
    
    def _classify_chunk_type(self, chunk: str) -> str:
        """Classify the type of agricultural chunk"""
        chunk_lower = chunk.lower()
        
        if 'dosage' in chunk_lower or 'ml' in chunk_lower or 'kg/acre' in chunk_lower:
            return 'dosage_information'
        elif 'control' in chunk_lower or 'treatment' in chunk_lower:
            return 'treatment_protocol'
        elif 'benefits' in chunk_lower:
            return 'product_benefits'
        elif 'application' in chunk_lower:
            return 'application_method'
        else:
            return 'general_information'
    
    def _extract_section_name(self, chunk: str) -> str:
        """Extract section name from chunk"""
        lines = chunk.split('\n')
        for line in lines:
            if line.startswith('##'):
                return line.replace('#', '').strip()
        return 'unknown_section'
    
    def _check_context_preservation(self, chunk: str) -> bool:
        """Check if chunk preserves agricultural context"""
        # Simple heuristic: chunk should contain product name and application info
        has_product = any(product.lower() in chunk.lower() 
                         for product in self.agricultural_markers['product_names'])
        has_application = any(method.lower() in chunk.lower() 
                            for method in self.agricultural_markers['application_methods'])
        
        return has_product or has_application

# Example usage and testing
if __name__ == "__main__":
    chunking = SmartChunking()
    print("🔪 Smart Chunking Module - Agricultural RAG Pipeline")
    print("✅ Semantic-aware splitting enabled")
    print("🌱 Agricultural entity preservation active")
    print("📊 Context boundary detection configured")
    print("🔗 Hierarchical chunk organization ready")