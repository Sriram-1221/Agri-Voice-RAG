#!/usr/bin/env python3
"""
Vocabulary Corrector for Agricultural Terms
Autocorrects common mispronunciations and transcription errors in agricultural product names
"""

import json
import re
import os

class VocabularyCorrector:
    def __init__(self):
        self.vocabulary = self._load_vocabulary()
        self.correction_map = self._build_correction_map()
    
    def _load_vocabulary(self):
        """Load vocabulary corrections from JSON file"""
        try:
            vocab_path = os.path.join(os.path.dirname(__file__), 'vocabulary.json')
            with open(vocab_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Warning: Could not load vocabulary.json: {e}")
            return {}
    
    def _build_correction_map(self):
        """Build a flat correction map for fast lookup"""
        correction_map = {}
        
        for category, terms in self.vocabulary.items():
            for correct_term, variations in terms.items():
                # Add the correct term (maps to itself)
                correction_map[correct_term.lower()] = correct_term
                
                # Add all variations (map to correct term)
                for variation in variations:
                    correction_map[variation.lower()] = correct_term
        
        return correction_map
    
    def correct_query(self, query: str) -> str:
        """
        Correct agricultural terms in the query
        
        Args:
            query (str): Original query text
            
        Returns:
            str: Corrected query text
        """
        if not query or not self.correction_map:
            return query
        
        corrected_query = query
        
        # Sort by length (longest first) to avoid partial replacements
        sorted_terms = sorted(self.correction_map.keys(), key=len, reverse=True)
        
        for incorrect_term in sorted_terms:
            correct_term = self.correction_map[incorrect_term]
            
            # Use word boundaries to avoid partial matches
            pattern = r'\b' + re.escape(incorrect_term) + r'\b'
            corrected_query = re.sub(pattern, correct_term, corrected_query, flags=re.IGNORECASE)
        
        return corrected_query
    
    def get_corrections_applied(self, original_query: str, corrected_query: str) -> list:
        """
        Get list of corrections that were applied
        
        Args:
            original_query (str): Original query
            corrected_query (str): Corrected query
            
        Returns:
            list: List of corrections applied
        """
        corrections = []
        
        if original_query.lower() != corrected_query.lower():
            # Find differences (simplified approach)
            original_words = set(original_query.lower().split())
            corrected_words = set(corrected_query.lower().split())
            
            for word in original_words - corrected_words:
                if word in self.correction_map:
                    corrections.append({
                        'original': word,
                        'corrected': self.correction_map[word]
                    })
        
        return corrections

# Global vocabulary corrector instance
vocab_corrector = VocabularyCorrector()

def correct_agricultural_terms(query: str) -> tuple:
    """
    Convenience function to correct agricultural terms
    
    Args:
        query (str): Original query
        
    Returns:
        tuple: (corrected_query, corrections_applied)
    """
    corrected = vocab_corrector.correct_query(query)
    corrections = vocab_corrector.get_corrections_applied(query, corrected)
    
    return corrected, corrections

if __name__ == "__main__":
    # Test the vocabulary corrector
    test_queries = [
        "What is Dormolin Vegetative used for?",
        "How to control trips in chili?", 
        "What is Acre Shield dosage for tometo?",
        "How to apply Tracks Sure for chilli?",
        "What are the benefits of Zetal Select for banana?",
        "How to control powder mildew in chilly?",
        "What is the dosage of Acting granules?",
        "How to treat bacterial wilth in tomato?"
    ]
    
    print("🔧 Testing Vocabulary Corrector")
    print("=" * 50)
    
    for query in test_queries:
        corrected, corrections = correct_agricultural_terms(query)
        
        print(f"\nOriginal:  {query}")
        print(f"Corrected: {corrected}")
        
        if corrections:
            print("Corrections applied:")
            for correction in corrections:
                print(f"  • {correction['original']} → {correction['corrected']}")
        else:
            print("No corrections needed")
        
        print("-" * 30)