#!/usr/bin/env python3
"""
Spool-Coder Application Entry Point

This is the main entry point for the Spool-Coder application.
"""

import sys
import os

# Add the src directory to the Python path
src_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'src')
sys.path.insert(0, src_dir)

def main():
    """Main entry point for the application"""
    try:
        # Import the main function from the core module
        from core.main import main as core_main
        
        # Call the core main function
        core_main()
        
    except ImportError as e:
        print(f"Error importing core module: {e}")
        print("Make sure all dependencies are installed and you're in the correct directory.")
        sys.exit(1)
    except Exception as e:
        print(f"Error starting application: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
