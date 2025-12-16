"""
RAG (Retrieval-Augmented Generation) Pipeline Components

This module contains the core components for document processing,
embedding generation, and intelligent retrieval systems.
"""

from .ingestion import DocumentIngestion
from .chunking import SmartChunking
from .embedding import EmbeddingGenerator
from .indexing import VectorIndexing
from .intent_classifier import IntentClassifier

__version__ = "1.0.0"
__author__ = "Agricultural AI Team"

__all__ = [
    "DocumentIngestion",
    "SmartChunking", 
    "EmbeddingGenerator",
    "VectorIndexing",
    "IntentClassifier"
]