# spool-coder
Analyze and reprogram bambulab filament spools

## Quick Start

### Running the Application
```bash
python main.py
```

### Building Executable
```bash
python build.py
```

## Environment Setup

For production use, you need to set the `BAMBU_XOR_KEY` environment variable with the correct XOR key used for decoding and encoding NFC tags.

```bash
# Example (Windows PowerShell)
$env:BAMBU_XOR_KEY="your_actual_key_here"

# Example (Windows Command Prompt)
set BAMBU_XOR_KEY=your_actual_key_here

# Example (Linux/macOS)
export BAMBU_XOR_KEY="your_actual_key_here"
```

For development purposes, a default key is provided, but it should not be used in production.
