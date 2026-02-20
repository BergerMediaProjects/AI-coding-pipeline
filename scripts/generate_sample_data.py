#!/usr/bin/env python3
"""
Generate sample training data (Excel format) for researchers to try the pipeline.
Run from project root: python scripts/generate_sample_data.py
"""
import os
import sys

# Add project root to path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

try:
    import pandas as pd
except ImportError:
    print("Error: pandas is required. Run: pip install -r requirements.txt")
    sys.exit(1)

SAMPLE_DATA = [
    {
        "title": "Einführung in digitale Lehre",
        "description": (
            "In diesem Seminar lernen Sie die Grundlagen digitaler Lehrformate kennen. "
            "Themen: Lernplattformen, Videokonferenzen, digitale Prüfungsformate. "
            "Zielgruppe: Dozierende aller Fachrichtungen."
        ),
    },
    {
        "title": "Workshop: Aktivierende Methoden in der Hochschullehre",
        "description": (
            "Praktischer Workshop zu Methoden, die Studierende aktiv einbinden. "
            "Arbeit in Kleingruppen, Erprobung von Techniken. "
            "Angebot der Hochschuldidaktik."
        ),
    },
    {
        "title": "Coaching für neue Dozierende",
        "description": (
            "Individuelle Beratung und Begleitung für neue Lehrende. "
            "Reflexion der eigenen Lehrpraxis, kollegialer Austausch. "
            "Einzelcoaching oder Kleingruppen."
        ),
    },
]


def main():
    output_dir = os.path.join(project_root, "data")
    os.makedirs(output_dir, exist_ok=True)

    df = pd.DataFrame(SAMPLE_DATA)
    xlsx_path = os.path.join(output_dir, "training_data_sample.xlsx")
    df.to_excel(xlsx_path, index=False)
    print(f"Created {xlsx_path}")
    print("Copy to data/training_data.xlsx to use as default, or upload via the web interface.")


if __name__ == "__main__":
    main()
