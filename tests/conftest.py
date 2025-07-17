"""
Shared test configuration and fixtures for spool-coder tests
"""
import pytest
import sys
import os

# Add src directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))