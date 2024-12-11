# Risk Allocator

Risk Allocator is a Python-based tool designed to help traders efficiently allocate risk across various tickers by weighing them based on sector exposure. The program simplifies portfolio management and ensures an optimized balance between exposure and risk.

---

## Features

- **Sector-Based Weighting**: Automatically calculates ticker weights based on their sector exposure.
- **Customizable Risk Parameters**: Tailor the logic to match your specific trading requirements.
- **User-Friendly Interface**: Accessible and easy to use for traders at all levels.
- **Single Executable**: Deployable as a standalone executable for non-Python users.

---

## Getting Started

### Prerequisites
- **Python 3.11+**
- Virtual Environment (recommended)
- **PyInstaller** (for creating standalone executables)

### Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/risk-allocator.git
    cd risk-allocator
    ```

2. Set up a virtual environment:
    ```bash
    python -m venv venv
    source venv/bin/activate # Linux/MacOS
    venv\Scripts\activate  # Windows
    ```

3. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

4. Run the program:
    ```bash
    python tradesorter.py
    ```

---

## Building the Executable

To distribute the program as a standalone executable:

1. Ensure **PyInstaller** is installed:
    ```bash
    pip install pyinstaller
    ```

2. Build the executable using the provided `.spec` file:
    ```bash
    pyinstaller --clean tradesorter.spec
    ```

3. The resulting executable will be in the `dist` folder.

---

## Project Structure

```
Risk Allocator/
├── input.txt               # TradingView watchlist import
├── output.txt              # Generated list of tickers with risk exposure percentages weighted by sector
├── requirements.txt        # Python dependencies
├── riskallocator.py        # Main logic of the program
├── settings.txt            # Settings file where user can define the max risk percentage assigned to each sector
├── README.md               # Project documentation
```
