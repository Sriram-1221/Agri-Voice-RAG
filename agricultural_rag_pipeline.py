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
            'deficiency', 'potash', 'zinc', 'iron', 'boron', 'phosphorus', 'nitrogen',
            'nutrient', 'absorption', 'uptake', 'synthesis', 'assimilation',
            'interveinal', 'internodes', 'dormancy',
            
            # 🚜 FARMING PRACTICES
            'dosage', 'application', 'foliar', 'spray', 'soil', 'acre', 'treatment',
            'control', 'drenching', 'fertigation', 'irrigation', 'ploughing',
            'basal', 'fertilizers', 'organic', 'material', 'preparation', 'rotation',
            'summer', 'ploughing', 'transplant', 'shock', 'stress', 'tolerance',
            
            # 📏 MEASUREMENTS & RATIOS
            'kg', 'gram', 'ml', 'litre', 'ratio', 'grade', 'granules', 'powder',
            'concentration', 'frequency', 'interval', 'coating', 'uniform',
            
            # 🎯 AGRICULTURAL GOALS
            'yield', 'quality', 'firmness', 'shelf', 'life', 'taste', 'sugar',
            'weight', 'size', 'shape', 'colour', 'shine', 'retention', 'drop',
            'setting', 'hands', 'fingers', 'market', 'price', 'vigorous',
            
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
        """Ultra-fast intent classification using pattern matching"""
        query_lower = query.lower()
        
        # 🚨 PRIORITY: Check for agricultural products first (CRITICAL FIX)
        agricultural_products = ['dormulin', 'zetol', 'tracs', 'akre', 'trail', 'actin']
        for product in agricultural_products:
            if product in query_lower:
                return "AGRICULTURE"  # FORCE agriculture for product queries
        
        # Check other agriculture keywords
        for keyword in self.agri_patterns:
            if keyword in query_lower:
                return "AGRICULTURE"
        
        # Check non-agriculture (only after agriculture check)
        for keyword in self.non_agri_patterns:
            if keyword in query_lower:
                return "NON_AGRICULTURE"
        
        # Fallback: Use OpenAI for ambiguous queries (natural classification)
        return self._classify_with_openai(query)
    
    def _classify_with_openai(self, query: str) -> str:
        """Fallback OpenAI classification for edge cases"""
        try:
            client = self._get_client()
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": f"Classify as AGRICULTURE or NON_AGRICULTURE: {query}"}],
                temperature=0.0,
                max_tokens=5
            )
            result = response.choices[0].message.content.strip().upper()
            return "AGRICULTURE" if "AGRICULTURE" in result else "NON_AGRICULTURE"
        except:
            return "NON_AGRICULTURE"  # Conservative fallback
    
    def retrieve_ultra_fast(self, query: str, top_k: int = 3) -> List[Dict]:
        """Ultra-fast retrieval with minimal overhead"""
        if not self.index:
            return []
        
        # Get query embedding
        client = self._get_client()
        response = client.embeddings.create(
            model="text-embedding-ada-002",
            input=[query]
        )
        query_embedding = np.array([response.data[0].embedding], dtype=np.float32)
        
        # Normalize and search
        faiss.normalize_L2(query_embedding)
        scores, indices = self.index.search(query_embedding, top_k)
        
        # Build results with minimal processing
        results = []
        for score, idx in zip(scores[0], indices[0]):
            results.append({
                'content': self.chunks[idx]['content'],
                'metadata': self.chunks[idx]['metadata'],
                'score': float(score),
                'original_score': float(score)  # No keyword boosting for speed
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
        
        # Generate answer with minimal context (top 1 chunk for speed)
        context = relevant_chunks[0]['content']
        
        # 🎯 CRITICAL FIX: Extract exact keywords from query to avoid confusion
        query_lower = query.lower()
        
        # Identify specific disease/pest/product in query
        specific_terms = []
        key_terms = ['late blight', 'early blight', 'bacterial wilt', 'powdery mildew', 'root rot', 
                    'fusarium wilt', 'thrips', 'aphids', 'whiteflies', 'dormulin', 'zetol', 'tracs']
        
        for term in key_terms:
            if term in query_lower:
                specific_terms.append(term)
        
        if specific_terms:
            # Enhanced prompt with specific focus
            prompt = f"""Based on this context, answer ONLY about {specific_terms[0].upper()}. Ignore other diseases/pests mentioned.

Context: {context}

Question: {query}

Answer about {specific_terms[0].upper()} only:"""
        else:
            # Fallback prompt
            prompt = f"Answer based ONLY on this context:\n{context}\n\nQ: {query}\nA:"
        
        client = self._get_client()
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.0,
            max_tokens=150  # Reduced for speed
        )
        
        return response.choices[0].message.content.strip(), "AGRICULTURE_WITH_CONTEXT"
    
    def query_agricultural_knowledge(self, question: str) -> Dict:
        """Complete agricultural knowledge retrieval pipeline"""
        start_time = time.time()
        
        # Step 1: Ultra-fast intent classification
        intent_start = time.time()
        intent = self.classify_intent_ultra_fast(question)
        intent_time = time.time() - intent_start
        
        # Step 2: Ultra-fast retrieval (only if agriculture)
        retrieval_start = time.time()
        if intent == "AGRICULTURE":
            retrieved = self.retrieve_ultra_fast(question, top_k=2)  # Reduced for speed
        else:
            retrieved = []
        retrieval_time = time.time() - retrieval_start
        
        # Step 3: Ultra-fast generation
        generation_start = time.time()
        answer, response_type = self.generate_ultra_fast_answer(question, intent, retrieved)
        generation_time = time.time() - generation_start
        
        total_time = time.time() - start_time
        
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