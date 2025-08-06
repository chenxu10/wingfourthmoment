#!/usr/bin/env python3
"""
Comprehensive Options Strategy Analyzer
Supports all 84 strategies from the Options Strategy Bagua Analysis

This is now a thin wrapper around the modular implementation in src/option_analyzer/
"""

import sys
import os

# Add the src directory to Python path so we can import our modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from option_analyzer import main

if __name__ == "__main__":
    main() 