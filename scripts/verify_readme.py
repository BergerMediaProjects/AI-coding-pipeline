#!/usr/bin/env python3
"""
Verify README accuracy by checking:
1. File structure matches documented layout
2. Scripts run without errors (dry-run where possible)
3. Paths referenced in README exist or are created correctly

Run from project root. Requires: pip install -r requirements.txt (or use a venv).
"""
import os
import subprocess
import sys

# Project root
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)

def check(name: str, condition: bool, detail: str = "") -> bool:
    status = "✓" if condition else "✗"
    print(f"  {status} {name}" + (f" — {detail}" if detail else ""))
    return condition

def main():
    print("=== README Verification ===\n")
    passed = 0
    total = 0

    # 1. File structure
    print("1. File structure")
    files = [
        ("README.md", True),
        ("requirements.txt", True),
        ("run_pipeline.py", True),
        ("data/training_data_sample.xlsx", True),
        ("utils/validate_yaml.py", True),
        ("utils/fix_yaml_format.py", True),
        ("utils/yaml_generator.py", True),
        ("data/prompt.txt", True),
        ("data/DOC_coding_scheme/coding_scheme_imported.yml", True),
        ("data/training_data.xlsx", False),  # Optional - may not exist
        ("data/coding_scheme.yml", False),   # Created by workflow
        ("data/DOC_coding_scheme/doc_cs.docx", False),  # User provides
    ]
    for path, required in files:
        exists = os.path.exists(path)
        total += 1
        if check(path, exists or not required, 
                "missing" if not exists and required else ("optional" if not required else "")):
            passed += 1
    print()

    # 2. Script invocations (no API calls)
    print("2. Script invocations")
    
    # fix_yaml_format - can run if coding_scheme_imported.yml exists
    if os.path.exists("data/DOC_coding_scheme/coding_scheme_imported.yml"):
        result = subprocess.run(
            [sys.executable, "utils/fix_yaml_format.py"],
            capture_output=True, text=True, cwd=ROOT, timeout=10
        )
        total += 1
        ok = result.returncode == 0 and os.path.exists("coding_scheme.yml")
        if check("fix_yaml_format.py", ok, result.stderr[:80] if result.stderr else ""):
            passed += 1
    else:
        print("  - fix_yaml_format.py (skipped: no coding_scheme_imported.yml)")

    # validate_yaml - needs coding_scheme.yml (root or data/)
    for path in ["coding_scheme.yml", "data/coding_scheme.yml"]:
        if os.path.exists(path):
            result = subprocess.run(
                [sys.executable, "utils/validate_yaml.py", path],
                capture_output=True, text=True, cwd=ROOT, timeout=10
            )
            total += 1
            ok = result.returncode == 0
            if check(f"validate_yaml.py {path}", ok, result.stderr[:80] if result.stderr else ""):
                passed += 1
            break
    else:
        print("  - validate_yaml.py (skipped: no coding_scheme.yml)")

    # 3. README vs actual behavior
    print("\n3. README vs implementation")
    total += 1
    has_dotenv = os.path.exists(".env.example")
    if check(".env support documented", has_dotenv, 
             "README only mentions export; project uses .env"):
        passed += 1

    print(f"\n=== Result: {passed}/{total} checks passed ===")
    return 0 if passed == total else 1

if __name__ == "__main__":
    sys.exit(main())
