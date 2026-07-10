import os
import sys

# Add backend directory to sys.path so we can import app modules
backend_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'backend'))
sys.path.insert(0, backend_dir)

from app.pipeline.grade_pipeline import grade_script

pdf_path = "dataset/Test Data/page-1.pdf"
answer_key_path = "dataset/Test Data/answer_key.txt"
question_path = "dataset/Test Data/question_paper.txt"

print(f"Running grade_script on:")
print(f"PDF: {pdf_path}")
print(f"Answer Key: {answer_key_path}")
print(f"Question Paper: {question_path}")

try:
    report = grade_script(pdf_path, answer_key_path, question_path)
    import json
    print("SUCCESS!")
    print(json.dumps(report, indent=2))
except Exception as e:
    import traceback
    print("FAILED!")
    traceback.print_exc()
