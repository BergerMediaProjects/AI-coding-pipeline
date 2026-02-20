# AI Pipeline for Course Description Analysis

This pipeline analyzes course descriptions using AI to classify them according to specific digital competence categories.

## Quick Start (for Researchers)

**Easiest ways to get started — minimal or no command line:**

### Option 1: Docker (one command, no Python install)
If you have [Docker Desktop](https://www.docker.com/products/docker-desktop/):
```bash
docker-compose up
```
Then open **http://127.0.0.1:5001**. Enter your OpenAI API key in the web form — no file editing needed.

### Option 2: Double-click to start (after one-time setup)
1. Run setup once:
   - **Windows:** Double-click `scripts\setup.bat` (or run it from a terminal)
   - **Mac/Linux:** Open a terminal, `cd` to this folder, run `bash scripts/setup.sh`
2. After that, just **double-click**:
   - **Windows:** `start.bat`
   - **Mac:** `start.command`
3. Enter your API key in the web form when prompted.

### Option 3: Traditional setup
1. Run `bash scripts/setup.sh` (or install Python + dependencies manually)
2. Run `bash scripts/run_web.sh` (or `python web_interface/app.py`)
3. Open http://127.0.0.1:5001
4. **Enter your OpenAI API key in the web form** — no need to edit `.env` files.

> **Tip:** You can paste your API key directly in the web interface. The sample data is used automatically if you don't upload files.

## What Can You Do With This Pipeline?

This pipeline helps researchers and educators analyze course descriptions to identify digital competencies. Here's what you can do:

1. **Automated Course Analysis**
   - Analyze large numbers of course descriptions automatically
   - Classify courses according to digital competence categories
   - Get consistent and objective classifications
   - Save time compared to manual coding

2. **Flexible Category System**
   - Use predefined digital competence categories
   - Create your own categories using the YAML generator
   - Modify existing categories easily
   - Activate/deactivate categories as needed

3. **Quality Control**
   - Get confidence scores for each classification
   - Review AI reasoning for each decision
   - Validate YAML structure automatically
   - Cross-check results with manual coding

## Setup

**Option A — Quick setup (recommended for researchers):**
- **Windows:** Double-click `scripts\setup.bat` or run it from a terminal
- **Mac/Linux:** Run `bash scripts/setup.sh`

This creates a virtual environment, installs dependencies, and generates sample data.

**Option B — Manual setup:**
1. Clone the repository
2. Create a virtual environment and install dependencies (required on Linux — system pip is restricted):
```bash
python3 -m venv .venv
source .venv/bin/activate   # Linux/Mac; on Windows: .venv\Scripts\activate
pip install -r requirements.txt
```
3. Set up your OpenAI API key. Either:
   - **Option A (recommended):** Enter it in the web interface when you run the pipeline — no file editing needed.
   - **Option B:** Copy `.env.example` to `.env` and add your key (useful if you prefer not to type it each time).

## File Structure

```
.
├── README.md
├── requirements.txt
├── Dockerfile               # For Docker deployment
├── docker-compose.yml       # One-command run: docker-compose up
├── start.bat                # Double-click launcher (Windows)
├── start.command            # Double-click launcher (Mac)
├── .env.example             # Template for environment variables
├── run_pipeline.py          # Main pipeline script
├── wsgi.py                  # WSGI entry point for production
├── gunicorn_config.py       # Gunicorn configuration
├── web_interface/           # Web UI
│   ├── app.py               # Flask application
│   └── templates/
│       └── index.html
├── data/
│   ├── training_data.xlsx   # Course descriptions
│   ├── training_data_sample.xlsx  # Sample data (try this first)
│   ├── human_codes.xlsx     # Optional human-coded data
│   ├── coding_scheme.yml    # Active coding scheme (used by pipeline)
│   ├── prompt.txt           # GPT prompt template
│   ├── DOC_coding_scheme/   # Directory for coding scheme documents
│   │   ├── doc_cs.docx      # Word document with coding scheme (user-provided)
│   │   └── coding_scheme_imported.yml  # Generated YAML scheme
│   ├── log/                 # Log files directory
│   └── results/             # Results will be saved here
│       └── ai_coded_results_*.xlsx   # Timestamped results
├── scripts/
│   ├── setup.sh             # Quick setup (Mac/Linux)
│   ├── setup.bat            # Quick setup (Windows)
│   ├── run_web.sh           # Start web interface (activates venv)
│   ├── generate_sample_data.py  # Create sample Excel
│   └── verify_readme.py     # Verify README accuracy
└── utils/
    ├── validate_yaml.py     # YAML validation script
    ├── yaml_generator.py   # Converts Word docs to YAML
    └── fix_yaml_format.py  # Cleans up YAML format
```

**Note:** `training_data.xlsx` and `doc_cs.docx` are not included by default. Use `data/training_data_sample.xlsx` to try the pipeline, or provide your own files. Run `python scripts/generate_sample_data.py` to create the sample Excel if needed.

## Workflow

1. **Generate YAML from Word document**
   ```bash
   python utils/yaml_generator.py
   ```
   This creates `data/DOC_coding_scheme/coding_scheme_imported.yml` (requires `doc_cs.docx` in that folder)

2. **Fix YAML formatting**
   ```bash
   python utils/fix_yaml_format.py
   ```
   This creates `coding_scheme.yml` in the project root. Copy it to `data/coding_scheme.yml` for the pipeline.

3. **Validate YAML structure**
   ```bash
   python utils/validate_yaml.py data/coding_scheme.yml
   ```
   Validates the coding scheme used by the pipeline

4. **Run the pipeline**
   ```bash
   python run_pipeline.py
   ```
   This uses `data/coding_scheme.yml`

## Web Interface

You can run the pipeline through a web UI instead of the command line.

**Start the web server:**
```bash
bash scripts/run_web.sh
```
(Or `source .venv/bin/activate` then `python web_interface/app.py`)

Then open **http://127.0.0.1:5001** in your browser.

**Features:**
- Upload coding scheme (YAML), prompt template, and input data (Excel)
- Run the pipeline with live progress updates
- Cancel a running pipeline
- Download results

**Production (optional):** For a production deployment, use Gunicorn:
```bash
gunicorn -c gunicorn_config.py wsgi:app
```
This serves the app on http://127.0.0.1:8000.

## Available Scripts

### 1. YAML Generator (`utils/yaml_generator.py`)

Converts the Word document coding scheme to YAML format.

**Usage:**
```bash
python utils/yaml_generator.py
```

**Input:**
- Reads from: `DOC_coding_scheme/doc_cs.docx`
- Expects a table with columns for:
  - Category names
  - Values (including conditions)
  - Criteria descriptions
  - Examples

**Output:**
- Creates: `DOC_coding_scheme/coding_scheme_imported.yml`
- Copy this file to `data/coding_scheme.yml` to use it in the pipeline

### 2. YAML Format Fixer (`utils/fix_yaml_format.py`)

Cleans and standardizes the YAML format after generation.

**Usage:**
```bash
python utils/fix_yaml_format.py
```

**Features:**
- Simplifies category names by removing numbering patterns
- Standardizes formatting of criteria, examples, and values
- Fixes quote consistency and special characters
- Ensures UTF-8 encoding

**Input:**
- Reads from: `data/DOC_coding_scheme/coding_scheme_imported.yml`

**Output:**
- Creates: `coding_scheme.yml` in the root directory
- Performs these transformations:
  - Removes numbering (e.g., "2.1.1 Category" → "Category")
  - Standardizes quotes and line breaks
  - Fixes bullet points in examples
  - Ensures consistent value formats

**Example Transformations:**
```yaml
# Before:
2.0 a Vorkommen Medienkompetenz:
  criteria: "Kriterium: Some text"
  examples:
    - "• Example 1"
    - "· Example 2"
  values: 'Ja (1), Nein (0)'

# After:
Vorkommen Medienkompetenz:
  criteria: "Some text"
  examples:
    - "Example 1"
    - "Example 2"
  values: "Ja (1), Nein (0)"
```

### 3. YAML Validator (`utils/validate_yaml.py`)

Validates the coding scheme structure.

**Usage:**
```bash
python utils/validate_yaml.py [path]
```

**Paths:**
- Pass a path to validate: `python utils/validate_yaml.py data/coding_scheme.yml`
- If no path is provided, it looks for `coding_scheme.yml` in the current directory

### 4. Main Pipeline (`run_pipeline.py`)

The primary script for analyzing course descriptions.

**Usage:**
```bash
python run_pipeline.py
```

**Input Requirements:**
- Excel files in `data/` directory:
  - `data/training_data.xlsx`: Course descriptions (title and description columns)
  - `data/human_codes.xlsx`: Optional human-coded data
- Valid `data/coding_scheme.yml`
- OpenAI API key in environment

**Configuration:**
- Edit `SELECTED_CATEGORIES` in the script to choose which categories to analyze
- Categories can be activated/deactivated by uncommenting/commenting them

**Output:**
- Creates Excel files in the `data/results/` directory
- Files are timestamped (format: `ai_coded_results_YYYYMMDD_HHMMSS.xlsx`)
- Results include:
  - Original course titles and descriptions
  - AI classifications (1/0 for binary categories)
  - Confidence scores
  - AI reasoning for each classification

## Value Transformations

The pipeline automatically transforms certain values in the output:
- "Ja", "Ja (1)", "(1)" → "1"
- "Nein", "Nein (0)", "(0)" → "0"

## Input Data Format

Your course data file (Excel or CSV) must have these columns:

| Column       | Required | Description                          |
|--------------|----------|--------------------------------------|
| `title`      | Yes      | Course title                         |
| `description`| Yes      | Full course description text         |

**Example** (see `data/training_data_sample.xlsx`):
| title | description |
|-------|-------------|
| Einführung in digitale Lehre | In diesem Seminar lernen Sie... |

## Best Practices

1. **Input Data**
   - Ensure clean, consistent formatting in input files
   - Remove any special characters from titles/descriptions
   - Use UTF-8 encoding for all files

2. **Category Selection**
   - Start with a few categories for testing
   - Gradually add more categories as needed
   - Check confidence scores to validate results

3. **Output Validation**
   - Review AI reasoning for unexpected classifications
   - Monitor confidence scores for reliability
   - Cross-validate results with manual coding if possible

## Troubleshooting

Common issues and solutions:

1. **"externally-managed-environment" or "pip install" fails**
   - Linux restricts system-wide pip. Use a virtual environment:
     ```bash
     python3 -m venv .venv
     source .venv/bin/activate
     pip install -r requirements.txt
     ```
   - Or run `bash scripts/setup.sh` which does this automatically.

2. **"ModuleNotFoundError: No module named 'flask'"**
   - You're using system Python instead of the venv. Run `bash scripts/run_web.sh` (which activates the venv automatically), or:
     ```bash
     source .venv/bin/activate
     python web_interface/app.py
     ```

3. **"Data file not found"**
   - Use the sample: copy `data/training_data_sample.xlsx` to `data/training_data.xlsx`
   - Or upload your file via the web interface
   - Ensure your Excel/CSV has `title` and `description` columns

4. **File Not Found Errors**
   - Check if all required directories exist
   - Ensure input files are in the correct locations
   - Verify file permissions

5. **"Apple could not verify start.command is free of malware" (Mac)**
   - Run setup again: `bash scripts/setup.sh` (it removes the quarantine flag)
   - Or manually: `xattr -d com.apple.quarantine start.command`
   - Then right-click start.command → Open, or double-click again

6. **YAML Validation Errors**
   - Run the YAML validator
   - Check for proper indentation
   - Verify all required fields are present

7. **Classification Issues**
   - Review the prompt.txt file
   - Adjust category criteria if needed
   - Add more specific examples to the coding scheme

## Updates and Maintenance

To update the pipeline:
1. Pull latest changes from repository
2. Check for new dependencies in requirements.txt
3. Review any changes to the coding scheme
4. Test with a small sample before full analysis

## Contact

For support or questions, please contact sonja.berger@lmu.de.
