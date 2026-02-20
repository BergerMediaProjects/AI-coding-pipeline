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

# Sample data aligned with prompt template (Fortbildungsbeschreibung für Dozierende)
SAMPLE_DATA = [
    {
        "title": "Designing Effective Moodle Courses for Higher Education",
        "description": (
            "This professional development course supports higher education teachers in designing, "
            "structuring, and implementing pedagogically sound Moodle courses. Participants will learn "
            "how to translate didactic concepts into functional Moodle environments that support student "
            "engagement, self-regulated learning, and assessment.\n"
            "The course combines instructional design principles with hands-on practice in Moodle. "
            "Participants will explore core Moodle functionalities (e.g., activities, resources, "
            "assessments, feedback, and analytics) and learn how to align them with learning objectives, "
            "constructive alignment, and evidence-based teaching strategies.\n"
            "By the end of the course, participants will have developed a prototype Moodle course or a "
            "redesigned course unit that is ready for implementation in their own teaching context."
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
