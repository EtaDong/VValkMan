# LLM Feature Demonstrations

This repository is a collection of minimal, runnable demonstrations for various Large Language Model (LLM) APIs and frameworks, designed for rapid testing and experimentation.

The project is managed using `uv` for high-speed dependency and environment management, and `pytest` for testing.

## Project Setup

### 1. Prerequisites
- Python 3.12+
- `git`

### 2. Installation & Environment Setup
Clone the repository, then use `uv` to set up the environment and install dependencies from `pyproject.toml`.

```bash
# Clone the repository
git clone <repository-url>
cd feature-llm

# Install uv if you don't have it
pip install uv

# Create the virtual environment and install all dependencies
uv sync
```

### 3. Configure API Keys
The demos require API keys to function.

1.  **Create a `.env` file** by copying the example:
    ```bash
    cp .env.example .env
    ```
2.  **Edit the `.env` file** to add your actual API keys.

## Running Tests
The test suite is managed by `pytest`. To run all tests, execute the following command from the project root:

```bash
uv run pytest -v
```
This command uses `uv` to execute `pytest` within the project's managed virtual environment, ensuring all dependencies are correctly loaded.

