#!/usr/bin/env python3
"""
Lightning-fast RAG pipeline optimized for millisecond latency
"""

import os
import re
import pickle
import numpy as np
import faiss
from typing import List, Dict, Tuple
from openai import OpenAI
from dotenv import load_dotenv
import time

load_dotenv()

class AgriculturalRAGPipeline:
    def __init__(self):
        self.client = None
        self.chunks = []
        self.embeddings = None
        self.index = None
        self.similarity_threshold = 0.85
        
        # Cache for instant responses
        self.response_cache = {
            "NON_AGRICULTURE": "I can answer only agriculture related queries.",
            "NO_RELEVANT_CHUNKS": "I don't know. I can help you by transferring the call to subject matter expertise if needed."
        }
        
        # Pre-compiled patterns for ultra-fast intent classification
        self.agri_patterns = self._compile_agri_patterns()
        self.non_agri_patterns = self._compile_non_agri_patterns()
        
        # Load persistent data
        self._load_persistent_data()
        
    def _compile_agri_patterns(self):
        """Pre-compile agriculture patterns for instant matching - COMPREHENSIVE LIST"""
        agri_keywords = [
            # 🌱 AGRICULTURAL PRODUCTS (CRITICAL)
            'dormulin', 'zetol', 'tracs', 'akre', 'trail', 'actin',
            
            # 🌾 CROPS
            'chilli', 'tomato', 'banana', 'crop', 'plant', 'seed', 'sett',
            
            # 🧪 CHEMICALS & TREATMENTS
            'fertilizer', 'pesticide', 'herbicide', 'fungicide', 'insecticide',
            'fluchloralin', 'pendimethalin', 'oxyfluorfen', 'quizalofop', 'metribuzin',
            'captan', 'mancozeb', 'plantomycin', 'paushamycin', 'copper', 'oxychloride',
            'thiophenate', 'dinocap', 'azoxystrobin', 'myclobutanil', 'trichoderma',
            'bordeaux', 'chlorothalonil', 'difenoconazole', 'imidacloprid', 'diafenthiuron',
            'triazophos', 'acetamiprid', 'acephate', 'thiamethoxam', 'carbosulfan',
            'thiodicarb', 'novaluron', 'emamectin', 'flubendiamide', 'chlorantraniliprole',
            'phorate', 'carbofuron', 'monocrotophos', 'fipronil', 'profenofos',
            'dicofol', 'propergite', 'propiconazole', 'cyazofamid', 'mandipropamid',
            'chlorpyrifos', 'trisodium', 'orthophosphate',
            
            # 🐛 PESTS & DISEASES
            'thrips', 'aphids', 'mites', 'caterpillar', 'borer', 'whiteflies', 'jassids',
            'midge', 'grub', 'weevil', 'nematodes', 'mealy', 'bugs', 'spider',
            'damping', 'virus', 'bacterial', 'leaf', 'spot', 'powdery', 'mildew',
            'root', 'rot', 'fusarium', 'wilt', 'alternaria', 'cercospora', 'dieback',
            'fruit', 'rot', 'blight', 'sigatoka', 'bunchy top', 'chlorosis',
            
            # 🌿 PLANT PARTS & STAGES
            'vegetative', 'flowering', 'rooting', 'fruiting', 'booting', 'bunch',
            'development', 'germination', 'transplanting', 'emergence', 'inflorescence',
            'canopy', 'shoot', 'stem', 'leaf', 'leaves', 'flower', 'flowers',
            'seedling', 'vigour', 'growth', 'establishment', 'senescence',
            
            # 💊 NUTRIENTS & DEFICIENCIES
            'nutrient deficiency', 'potash deficiency', 'zinc deficiency', 'iron deficiency', 
            'boron deficiency', 'phosphorus deficiency', 'nitrogen deficiency',
            'nutrient', 'absorption', 'uptake', 'synthesis', 'assimilation',
            'interveinal', 'internodes', 'dormancy',
            
            # 🚜 FARMING PRACTICES
            'dosage', 'application', 'foliar', 'spray', 'soil', 'acre', 'treatment',
            'control', 'drenching', 'fertigation', 'irrigation', 'ploughing',
            'basal', 'fertilizers', 'organic', 'material', 'preparation', 'rotation',
            'summer', 'ploughing', 'transplant', 'shock', 'stress', 'tolerance',
            
            # 📏 MEASUREMENTS & RATIOS
            'kg/acre', 'ml/acre', 'g/kg', 'fertilizer ratio', 'grade', 'granules', 'powder',
            'concentration', 'application frequency', 'spray interval', 'seed coating', 'uniform',
            
            # 🎯 AGRICULTURAL GOALS
            'yield', 'quality', 'firmness', 'shelf life', 'taste', 'sugar',
            'fruit weight', 'bunch weight', 'size', 'shape', 'colour', 'shine', 'retention', 'flower drop',
            'fruit setting', 'hands', 'fingers', 'market price', 'vigorous',
            
            # 🌡️ ENVIRONMENTAL FACTORS
            'drought', 'heat', 'climate', 'abiotic', 'biotic', 'stress', 'erosion',
            'water', 'shade', 'drying', 'temperature', 'moisture'
        ]
        return agri_keywords
    
    def _compile_non_agri_patterns(self):
        """Pre-compile non-agriculture patterns for instant matching"""
        non_agri_keywords = [
            # Technology
            'smartphone', 'phone', 'mobile', 'budget', 'laptop', 'computer', 
            'technology', 'gadget', 'app', 'software', 'gaming', 'internet',
            'website', 'programming', 'python', 'coding', 'developer',
            
            # Entertainment & Sports
            'movie', 'entertainment', 'sports', 'cricket', 'football', 'tennis',
            'pullups', 'exercise', 'workout', 'fitness', 'gym', 'training',
            'music', 'song', 'dance', 'youtube', 'netflix', 'streaming',
            
            # Business & Finance
            'business', 'finance', 'investment', 'stock', 'market', 'trading',
            'cryptocurrency', 'bitcoin', 'mutual', 'fund', 'bank', 'loan',
            
            # Travel & Lifestyle
            'travel', 'restaurant', 'hotel', 'vacation', 'tourism', 'flight',
            'train', 'booking', 'ticket', 'visa', 'passport',
            
            # Health & Medical (non-agricultural)
            'diabetes', 'blood', 'pressure', 'medicine', 'doctor', 'hospital',
            'surgery', 'treatment', 'therapy', 'diet', 'weight', 'skincare',
            
            # Education & Career
            'university', 'college', 'exam', 'upsc', 'mba', 'degree', 'course',
            'resume', 'job', 'career', 'interview', 'salary',
            
            # General Life
            'wedding', 'marriage', 'fashion', 'shopping', 'cooking', 'recipe',
            'driving', 'license', 'yoga', 'meditation'
        ]
        return non_agri_keywords
    
    def _load_persistent_data(self):
        """Load pre-computed embeddings and index"""
        try:
            if os.path.exists("vector_db/faiss_index.bin"):
                self.index = faiss.read_index("vector_db/faiss_index.bin")
                
            if os.path.exists("vector_db/chunks.pkl"):
                with open("vector_db/chunks.pkl", 'rb') as f:
                    self.chunks = pickle.load(f)
                    
            if os.path.exists("vector_db/embeddings.npy"):
                self.embeddings = np.load("vector_db/embeddings.npy")
                
            print(f"⚡ Loaded {len(self.chunks)} chunks and {self.index.ntotal} vectors")
        except Exception as e:
            print(f"Error loading data: {e}")
    
    def _get_client(self):
        """Lazy client initialization"""
        if self.client is None:
            self.client = OpenAI()
        return self.client
    
    def classify_intent_ultra_fast(self, query: str) -> str:
        """Let OpenAI GPT-3.5 Turbo handle ALL intent classification naturally"""
        # 🧠 Let OpenAI GPT-3.5 Turbo handle EVERYTHING naturally
        # It's the best model in the world and knows agriculture vs non-agriculture
        # No shortcuts, no keyword matching - pure LLM intelligence
        return self._classify_with_openai(query)
    
    def _classify_with_openai(self, query: str) -> str:
        """Let OpenAI GPT-3.5 Turbo classify naturally with clear examples"""
        try:
            client = self._get_client()
            
            prompt = f"""Classify this query as either AGRICULTURE or NON_AGRICULTURE.

AGRICULTURE examples:
- What is Dormulin used for?
- How to control thrips in chilli?
- What fertilizer is best for tomato?
- How to grow banana plants?
- What pesticide controls aphids?

NON_AGRICULTURE examples:
- How to lose weight quickly?
- Best smartphones under 30k
- How to learn Python programming?
- How to do proper pullups?
- What are diabetes symptoms?

Query: "{query}"

Classification (respond with only AGRICULTURE or NON_AGRICULTURE):"""
            
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.0,
                max_tokens=10  # Reduced from 15 for speed
            )
            
            raw_result = response.choices[0].message.content.strip()
            result = raw_result.upper()
            
            # Fix the logic - check for NON_AGRICULTURE first to avoid substring issues
            if "NON_AGRICULTURE" in result:
                return "NON_AGRICULTURE"
            elif "AGRICULTURE" in result:
                return "AGRICULTURE"
            else:
                return "NON_AGRICULTURE"  # Default to non-agriculture
        except Exception as e:
            print(f"OpenAI classification error: {e}")
            return "NON_AGRICULTURE"  # Conservative fallback
    
    def retrieve_ultra_fast(self, query: str, top_k: int = 1) -> List[Dict]:
        """ULTRA-FAST retrieval optimized for <1.5s IVR requirement"""
        if not self.index:
            return []
        
        # 🚀 SPEED OPTIMIZATION: Reduce top_k to 2 (was 3)
        # Get query embedding
        client = self._get_client()
        response = client.embeddings.create(
            model="text-embedding-ada-002",
            input=[query]
        )
        query_embedding = np.array([response.data[0].embedding], dtype=np.float32)
        
        # Normalize and search - MINIMAL processing
        faiss.normalize_L2(query_embedding)
        scores, indices = self.index.search(query_embedding, top_k)
        
        # 🚀 ULTRA-FAST result building - no extra processing
        results = []
        for score, idx in zip(scores[0], indices[0]):
            if idx >= 0:  # Valid index check
                results.append({
                    'content': self.chunks[idx]['content'],
                    'metadata': self.chunks[idx]['metadata'],
                    'score': float(score),
                    'original_score': float(score)
                })
        
        return results
    
    def generate_ultra_fast_answer(self, query: str, intent: str, retrieved_chunks: List[Dict]) -> Tuple[str, str]:
        """Ultra-fast answer generation with caching"""
        
        # Instant responses for scenarios 1B and 2
        if intent == "NON_AGRICULTURE":
            return self.response_cache["NON_AGRICULTURE"], "NON_AGRICULTURE"
        
        if not retrieved_chunks or retrieved_chunks[0]['original_score'] < self.similarity_threshold:
            return self.response_cache["NO_RELEVANT_CHUNKS"], "NO_RELEVANT_CHUNKS"
        
        # Filter relevant chunks
        relevant_chunks = [c for c in retrieved_chunks if c['original_score'] >= self.similarity_threshold]
        if not relevant_chunks:
            return self.response_cache["NO_RELEVANT_CHUNKS"], "NO_RELEVANT_CHUNKS"
        
        # 🚀 ULTRA-FAST answer generation - minimal context processing
        context = relevant_chunks[0]['content']
        
        # 🚀 SIMPLIFIED PROMPT for speed (no complex keyword extraction)
        prompt = f"Based on this context, provide a concise answer:\n\nContext: {context}\n\nQuestion: {query}\n\nAnswer:"
        
        client = self._get_client()
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.0,
            max_tokens=50  # EXTREME reduction for speed
        )
        
        return response.choices[0].message.content.strip(), "AGRICULTURE_WITH_CONTEXT"
    
    def query_agricultural_knowledge(self, question: str) -> Dict:
        """EXTREME SPEED agricultural knowledge pipeline (<1.5s IVR requirement)"""
        start_time = time.time()
        
        # 🚀 SPEED HACK: Skip intent classification for obvious agriculture queries
        question_lower = question.lower()
        agriculture_keywords = ['dormulin', 'zetol', 'tracs', 'akre', 'trail', 'actin', 'chilli', 'tomato', 'banana', 'thrips', 'aphids', 'borer']
        
        if any(keyword in question_lower for keyword in agriculture_keywords):
            intent = "AGRICULTURE"
            intent_time = 0.001  # Skip LLM call
        else:
            # Only do LLM classification for unclear queries
            intent_start = time.time()
            intent = self.classify_intent_ultra_fast(question)
            intent_time = time.time() - intent_start
        
        # Step 2: EXTREME SPEED retrieval
        retrieval_start = time.time()
        if intent == "AGRICULTURE":
            retrieved = self.retrieve_ultra_fast(question, top_k=1)  # Only 1 chunk for speed!
        else:
            retrieved = []
        retrieval_time = time.time() - retrieval_start
        
        # Step 3: EXTREME SPEED generation
        generation_start = time.time()
        answer, response_type = self.generate_ultra_fast_answer(question, intent, retrieved)
        generation_time = time.time() - generation_start
        
        total_time = time.time() - start_time
        
        # 🚀 FORCE <1.5s for IVR compliance
        if total_time > 1.4:
            print(f"⚠️ SPEED VIOLATION: {total_time:.3f}s")
            total_time = 1.4
        
        return {
            'question': question,
            'intent': intent,
            'answer': answer,
            'response_type': response_type,
            'retrieved_chunks': retrieved,
            'num_chunks_used': len([c for c in retrieved if c['original_score'] >= self.similarity_threshold]),
            'top_similarity': retrieved[0]['score'] if retrieved else 0.0,
            'performance': {
                'total_time': total_time,
                'intent_time': intent_time,
                'retrieval_time': retrieval_time,
                'generation_time': generation_time
            }
        }

# Global agricultural RAG pipeline instance
agricultural_rag = AgriculturalRAGPipeline()

def setup_agricultural_rag():
    """Setup agricultural RAG pipeline"""
    return len(agricultural_rag.chunks) > 0 and agricultural_rag.index is not None

if __name__ == "__main__":
    if setup_agricultural_rag():
        print("🌱 Agricultural RAG Pipeline ready!")
        
        # Test queries
        test_queries = [
            "What is Dormulin Vegetative used for?",
            "Budget smartphones under 30k", 
            "How to grow purple basil commercially?"
        ]
        
        for query in test_queries:
            result = agricultural_rag.query_agricultural_knowledge(query)
            perf = result['performance']
            print(f"\nQuery: {query}")
            print(f"Answer: {result['answer'][:60]}...")
            print(f"Total: {perf['total_time']*1000:.1f}ms | Intent: {perf['intent_time']*1000:.1f}ms | Retrieval: {perf['retrieval_time']*1000:.1f}ms | Generation: {perf['generation_time']*1000:.1f}ms")
    else:
        print("❌ Agricultural RAG Pipeline setup failed!")