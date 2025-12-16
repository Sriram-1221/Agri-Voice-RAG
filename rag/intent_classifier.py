#!/usr/bin/env python3
"""
Intent Classification Module

Advanced intent classification system for agricultural queries.
Implements multi-stage classification with domain-specific models
and confidence scoring for accurate query routing.
"""

import re
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from enum import Enum

class IntentType(Enum):
    """Agricultural intent types"""
    AGRICULTURE_WITH_CONTEXT = "agriculture_with_context"
    AGRICULTURE_WITHOUT_CONTEXT = "agriculture_without_context"
    NON_AGRICULTURE = "non_agriculture"

@dataclass
class ClassificationResult:
    """Result of intent classification"""
    intent: IntentType
    confidence: float
    reasoning: str
    agricultural_entities: List[str]
    context_availability: bool

class IntentClassifier:
    """
    Advanced intent classification system for agricultural queries.
    
    Features:
    - Multi-stage classification pipeline
    - Agricultural domain expertise
    - Confidence scoring and reasoning
    - Entity extraction and validation
    - Context availability assessment
    """
    
    def __init__(self, knowledge_base_path: Optional[str] = None):
        """Initialize intent classification system"""
        self.agricultural_keywords = self._load_agricultural_keywords()
        self.non_agricultural_keywords = self._load_non_agricultural_keywords()
        self.product_database = self._load_product_database()
        self.crop_database = self._load_crop_database()
        self.knowledge_base_path = knowledge_base_path
        self.classification_rules = self._initialize_classification_rules()
    
    def _load_agricultural_keywords(self) -> Dict[str, float]:
        """Load agricultural keywords with confidence weights"""
        return {
            # High confidence agricultural terms
            'agriculture': 0.95, 'farming': 0.95, 'crop': 0.9, 'plant': 0.8,
            'soil': 0.85, 'fertilizer': 0.9, 'pesticide': 0.9, 'herbicide': 0.9,
            'irrigation': 0.85, 'harvest': 0.85, 'cultivation': 0.9,
            
            # Specific agricultural processes
            'planting': 0.8, 'sowing': 0.8, 'transplanting': 0.8, 'pruning': 0.8,
            'grafting': 0.85, 'pollination': 0.8, 'germination': 0.8,
            
            # Agricultural problems and solutions
            'disease': 0.7, 'pest': 0.75, 'weed': 0.8, 'blight': 0.85,
            'fungus': 0.8, 'virus': 0.75, 'bacteria': 0.7, 'nematode': 0.8,
            
            # Nutrients and deficiencies
            'nitrogen': 0.7, 'phosphorus': 0.7, 'potassium': 0.7, 'calcium': 0.6,
            'magnesium': 0.6, 'sulfur': 0.6, 'iron': 0.6, 'zinc': 0.6,
            'boron': 0.7, 'manganese': 0.6, 'deficiency': 0.8,
            
            # Application methods
            'foliar': 0.85, 'spray': 0.6, 'drench': 0.7, 'broadcast': 0.7,
            'band': 0.6, 'sidedress': 0.8, 'topdress': 0.8,
            
            # Measurements and dosages
            'dosage': 0.8, 'rate': 0.6, 'concentration': 0.7, 'ppm': 0.7,
            'acre': 0.8, 'hectare': 0.8, 'kg': 0.5, 'gram': 0.5, 'ml': 0.5,
            
            # Growth stages
            'seedling': 0.8, 'vegetative': 0.85, 'flowering': 0.8, 'fruiting': 0.8,
            'maturity': 0.7, 'ripening': 0.8, 'dormancy': 0.7
        }
    
    def _load_non_agricultural_keywords(self) -> Dict[str, float]:
        """Load non-agricultural keywords with confidence weights"""
        return {
            # Technology
            'smartphone': 0.9, 'laptop': 0.9, 'computer': 0.8, 'software': 0.8,
            'app': 0.7, 'website': 0.7, 'internet': 0.7, 'wifi': 0.8,
            
            # Entertainment
            'movie': 0.9, 'music': 0.8, 'game': 0.7, 'sports': 0.8,
            'television': 0.8, 'streaming': 0.8, 'youtube': 0.8,
            
            # Finance
            'bank': 0.8, 'loan': 0.8, 'investment': 0.8, 'stock': 0.7,
            'insurance': 0.8, 'credit': 0.7, 'mortgage': 0.8,
            
            # Travel
            'hotel': 0.8, 'flight': 0.8, 'vacation': 0.8, 'tourism': 0.8,
            'restaurant': 0.7, 'booking': 0.6,
            
            # Health (non-plant)
            'doctor': 0.7, 'medicine': 0.6, 'hospital': 0.8, 'surgery': 0.8,
            'pharmacy': 0.7, 'treatment': 0.4,  # Lower because can be agricultural
            
            # Education
            'school': 0.7, 'university': 0.8, 'course': 0.6, 'degree': 0.7,
            'exam': 0.7, 'study': 0.5,
            
            # Fashion and lifestyle
            'fashion': 0.9, 'clothing': 0.8, 'shoes': 0.8, 'jewelry': 0.8,
            'beauty': 0.8, 'cosmetics': 0.8
        }
    
    def _load_product_database(self) -> Dict[str, Dict]:
        """Load agricultural product database"""
        return {
            'dormulin': {
                'type': 'rooting_agent',
                'crops': ['chilli', 'tomato', 'banana'],
                'confidence': 0.95
            },
            'zetol': {
                'type': 'growth_regulator',
                'crops': ['chilli', 'tomato'],
                'confidence': 0.95
            },
            'tracs': {
                'type': 'nutrient_supplement',
                'crops': ['chilli', 'tomato', 'banana'],
                'confidence': 0.95
            },
            'akre': {
                'type': 'fertilizer',
                'crops': ['chilli', 'tomato'],
                'confidence': 0.95
            },
            'trail': {
                'type': 'growth_enhancer',
                'crops': ['chilli', 'tomato', 'banana'],
                'confidence': 0.95
            },
            'actin': {
                'type': 'bio_stimulant',
                'crops': ['chilli', 'tomato', 'banana'],
                'confidence': 0.95
            }
        }
    
    def _load_crop_database(self) -> Dict[str, Dict]:
        """Load crop database with characteristics"""
        return {
            'chilli': {
                'scientific_name': 'Capsicum annuum',
                'category': 'vegetable',
                'confidence': 0.9
            },
            'tomato': {
                'scientific_name': 'Solanum lycopersicum',
                'category': 'vegetable',
                'confidence': 0.9
            },
            'banana': {
                'scientific_name': 'Musa acuminata',
                'category': 'fruit',
                'confidence': 0.9
            }
        }
    
    def _initialize_classification_rules(self) -> Dict:
        """Initialize classification rules and thresholds"""
        return {
            'agriculture_threshold': 0.6,
            'non_agriculture_threshold': 0.7,
            'context_availability_threshold': 0.5,
            'minimum_confidence': 0.3,
            'product_mention_boost': 0.3,
            'crop_mention_boost': 0.2
        }
    
    def classify_intent(self, query: str) -> ClassificationResult:
        """
        Classify the intent of a user query
        
        Args:
            query: User query string
            
        Returns:
            ClassificationResult with intent, confidence, and reasoning
        """
        # Preprocess query
        processed_query = self._preprocess_query(query)
        
        # Extract agricultural entities
        agricultural_entities = self._extract_agricultural_entities(processed_query)
        
        # Calculate agricultural confidence
        agricultural_confidence = self._calculate_agricultural_confidence(
            processed_query, agricultural_entities
        )
        
        # Calculate non-agricultural confidence
        non_agricultural_confidence = self._calculate_non_agricultural_confidence(processed_query)
        
        # Determine primary intent
        intent = self._determine_primary_intent(
            agricultural_confidence, non_agricultural_confidence
        )
        
        # Assess context availability for agricultural queries
        context_availability = False
        if intent in [IntentType.AGRICULTURE_WITH_CONTEXT, IntentType.AGRICULTURE_WITHOUT_CONTEXT]:
            context_availability = self._assess_context_availability(
                processed_query, agricultural_entities
            )
            
            # Refine agricultural intent based on context
            if intent != IntentType.NON_AGRICULTURE:
                intent = (IntentType.AGRICULTURE_WITH_CONTEXT if context_availability 
                         else IntentType.AGRICULTURE_WITHOUT_CONTEXT)
        
        # Generate reasoning
        reasoning = self._generate_reasoning(
            intent, agricultural_confidence, non_agricultural_confidence, 
            agricultural_entities, context_availability
        )
        
        # Calculate final confidence
        final_confidence = max(agricultural_confidence, non_agricultural_confidence)
        
        return ClassificationResult(
            intent=intent,
            confidence=final_confidence,
            reasoning=reasoning,
            agricultural_entities=agricultural_entities,
            context_availability=context_availability
        )
    
    def _preprocess_query(self, query: str) -> str:
        """Preprocess query for classification"""
        # Convert to lowercase
        processed = query.lower().strip()
        
        # Remove extra whitespace
        processed = re.sub(r'\s+', ' ', processed)
        
        # Remove punctuation for keyword matching
        processed = re.sub(r'[^\w\s]', ' ', processed)
        
        return processed
    
    def _extract_agricultural_entities(self, query: str) -> List[str]:
        """Extract agricultural entities from query"""
        entities = []
        
        # Extract product names
        for product in self.product_database.keys():
            if product.lower() in query:
                entities.append(f"product:{product}")
        
        # Extract crop names
        for crop in self.crop_database.keys():
            if crop.lower() in query:
                entities.append(f"crop:{crop}")
        
        # Extract agricultural keywords
        for keyword in self.agricultural_keywords.keys():
            if keyword in query:
                entities.append(f"keyword:{keyword}")
        
        return entities
    
    def _calculate_agricultural_confidence(self, query: str, entities: List[str]) -> float:
        """Calculate confidence that query is agricultural"""
        confidence = 0.0
        
        # Base confidence from agricultural keywords
        for keyword, weight in self.agricultural_keywords.items():
            if keyword in query:
                confidence += weight * 0.1  # Scale down individual contributions
        
        # Boost for product mentions
        product_mentions = [e for e in entities if e.startswith('product:')]
        confidence += len(product_mentions) * self.classification_rules['product_mention_boost']
        
        # Boost for crop mentions
        crop_mentions = [e for e in entities if e.startswith('crop:')]
        confidence += len(crop_mentions) * self.classification_rules['crop_mention_boost']
        
        # Normalize confidence to [0, 1]
        confidence = min(confidence, 1.0)
        
        return confidence
    
    def _calculate_non_agricultural_confidence(self, query: str) -> float:
        """Calculate confidence that query is non-agricultural"""
        confidence = 0.0
        
        # Base confidence from non-agricultural keywords
        for keyword, weight in self.non_agricultural_keywords.items():
            if keyword in query:
                confidence += weight * 0.15  # Slightly higher weight for non-ag detection
        
        # Normalize confidence to [0, 1]
        confidence = min(confidence, 1.0)
        
        return confidence
    
    def _determine_primary_intent(self, ag_confidence: float, non_ag_confidence: float) -> IntentType:
        """Determine primary intent based on confidence scores"""
        ag_threshold = self.classification_rules['agriculture_threshold']
        non_ag_threshold = self.classification_rules['non_agriculture_threshold']
        
        # Clear non-agricultural intent
        if non_ag_confidence >= non_ag_threshold and non_ag_confidence > ag_confidence:
            return IntentType.NON_AGRICULTURE
        
        # Clear agricultural intent
        if ag_confidence >= ag_threshold:
            return IntentType.AGRICULTURE_WITH_CONTEXT  # Will be refined later
        
        # Ambiguous case - use higher confidence
        if ag_confidence > non_ag_confidence:
            return IntentType.AGRICULTURE_WITH_CONTEXT
        else:
            return IntentType.NON_AGRICULTURE
    
    def _assess_context_availability(self, query: str, entities: List[str]) -> bool:
        """Assess if context is available in knowledge base for agricultural query"""
        # Simulate context availability check
        # In real implementation, this would query the actual knowledge base
        
        # High confidence if specific products are mentioned
        product_mentions = [e for e in entities if e.startswith('product:')]
        if product_mentions:
            return True  # Our knowledge base has product information
        
        # Check for specific crop + problem combinations
        crop_mentions = [e for e in entities if e.startswith('crop:')]
        problem_keywords = ['disease', 'pest', 'deficiency', 'control', 'treatment']
        
        has_crop = len(crop_mentions) > 0
        has_problem = any(keyword in query for keyword in problem_keywords)
        
        if has_crop and has_problem:
            return True  # Likely to have context for crop problems
        
        # Check for dosage/application queries
        dosage_keywords = ['dosage', 'application', 'rate', 'how much', 'quantity']
        if any(keyword in query for keyword in dosage_keywords):
            return len(product_mentions) > 0  # Context available if product mentioned
        
        # Default to no context for general agricultural queries
        return False
    
    def _generate_reasoning(self, intent: IntentType, ag_conf: float, non_ag_conf: float,
                          entities: List[str], context_available: bool) -> str:
        """Generate human-readable reasoning for classification"""
        if intent == IntentType.NON_AGRICULTURE:
            return f"Non-agricultural query detected (confidence: {non_ag_conf:.2f}). " \
                   f"Query appears to be about non-farming topics."
        
        elif intent == IntentType.AGRICULTURE_WITH_CONTEXT:
            entity_summary = f"Found {len(entities)} agricultural entities. " if entities else ""
            return f"Agricultural query with available context (confidence: {ag_conf:.2f}). " \
                   f"{entity_summary}Knowledge base contains relevant information."
        
        else:  # AGRICULTURE_WITHOUT_CONTEXT
            entity_summary = f"Found {len(entities)} agricultural entities. " if entities else ""
            return f"Agricultural query without sufficient context (confidence: {ag_conf:.2f}). " \
                   f"{entity_summary}Knowledge base lacks specific information for this query."
    
    def get_classification_stats(self) -> Dict:
        """Get classification system statistics"""
        return {
            'agricultural_keywords': len(self.agricultural_keywords),
            'non_agricultural_keywords': len(self.non_agricultural_keywords),
            'products_in_database': len(self.product_database),
            'crops_in_database': len(self.crop_database),
            'classification_rules': self.classification_rules
        }

# Example usage and testing
if __name__ == "__main__":
    classifier = IntentClassifier()
    print("🎯 Intent Classification Module - Agricultural RAG Pipeline")
    print("✅ Multi-stage classification pipeline ready")
    print("🌱 Agricultural domain expertise loaded")
    print("📊 Confidence scoring and reasoning enabled")
    print("🔍 Entity extraction and validation active")
    
    # Test classifications
    test_queries = [
        "How to apply Dormulin for chilli rooting?",
        "What is the best smartphone under 30k?",
        "How to grow purple basil commercially?"
    ]
    
    for query in test_queries:
        result = classifier.classify_intent(query)
        print(f"\nQuery: {query}")
        print(f"Intent: {result.intent.value}")
        print(f"Confidence: {result.confidence:.2f}")
        print(f"Entities: {result.agricultural_entities}")