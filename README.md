# AI Pipeline for Course Description Analysis

This pipeline analyzes course descriptions using AI to classify them according to specific digital competence categories.

## Quick Start (for Researchers)

**Easiest way to get started:** Use the web interface. No command line required.

1. **Install Python** (3.8 or newer) — [python.org](https://www.python.org/downloads/)
2. **Open a terminal** in this project folder and run:
   ```bash
   pip install -r requirements.txt
   cp .env.example .env
   ```
3. **Edit `.env`** and add your OpenAI API key: `OPENAI_API_KEY=sk-your-key-here`
4. **Start the web interface:**
   ```bash
   python web_interface/app.py
   ```
5. **Open http://127.0.0.1:5001** in your browser
6. **Upload your files** (or use the sample data in `data/training_data_sample.xlsx` to try it first)
7. **Select categories** and click "Run Pipeline"

> **Tip:** The web interface automatically uses `data/training_data_sample.xlsx` if no data file exists. You can also upload your own Excel file.

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
```bash
bash scripts/setup.sh
```
This creates a virtual environment, installs dependencies, and generates sample data.

**Option B — Manual setup:**
1. Clone the repository
2. Install dependencies:
```bash
pip install -r requirements.txt
```
3. Set up your OpenAI API key. Either:
   - **Option A (recommended):** Copy `.env.example` to `.env` and add your key:
     ```bash
     cp .env.example .env
     # Edit .env and set: OPENAI_API_KEY=your-api-key-here
     ```
   - **Option B:** Export as an environment variable:
     ```bash
     export OPENAI_API_KEY='your-api-key-here'
     ```

## File Structure

```
.
├── README.md
├── requirements.txt
├── .env.example             # Template for environment variables
├── run_pipeline.py     # Main pipeline script
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
│   ├── setup.sh             # Quick setup for researchers
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
python web_interface/app.py
```

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

1. **"Data file not found"**
   - Use the sample: copy `data/training_data_sample.xlsx` to `data/training_data.xlsx`
   - Or upload your file via the web interface
   - Ensure your Excel/CSV has `title` and `description` columns

2. **File Not Found Errors**
   - Check if all required directories exist
   - Ensure input files are in the correct locations
   - Verify file permissions

3. **YAML Validation Errors**
   - Run the YAML validator
   - Check for proper indentation
   - Verify all required fields are present

4. **Classification Issues**
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
