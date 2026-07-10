import os
import glob
from PIL import Image

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def create_pdf_from_images(image_paths, output_pdf_path):
    if not image_paths:
        return
        
    print(f"Creating {output_pdf_path} from {len(image_paths)} pages...")
    images = []
    first_image = None
    
    for filepath in image_paths:
        img = Image.open(filepath).convert("RGB")
        if first_image is None:
            first_image = img
        else:
            images.append(img)
            
    # Save as PDF
    first_image.save(
        output_pdf_path,
        "PDF",
        resolution=100.0,
        save_all=True,
        append_images=images
    )

def sort_by_page(filepath):
    # Extracts the page number for sorting
    # e.g., ..._p1.png -> 1
    basename = os.path.basename(filepath)
    parts = basename.split('_p')
    if len(parts) == 2:
        try:
            return int(parts[1].split('.')[0])
        except:
            pass
    return 0

def process_student_booklets():
    input_dir = os.path.join(BASE_DIR, "dataset", "raw_scripts", "Mounika_Style")
    output_dir = os.path.join(BASE_DIR, "dataset", "raw_scripts", "Student_Pdf")
    os.makedirs(output_dir, exist_ok=True)
    
    # Get all PNGs
    all_pngs = glob.glob(os.path.join(input_dir, "*.png"))
    
    # Group by student prefix
    students = {}
    for filepath in all_pngs:
        basename = os.path.basename(filepath)
        # e.g., Anusha_Goud_DS_Answers_p1.png -> prefix: Anusha_Goud_DS_Answers
        prefix = basename.split('_p')[0]
        if prefix not in students:
            students[prefix] = []
        students[prefix].append(filepath)
        
    for student_prefix, filepaths in students.items():
        # Sort files by page number
        filepaths.sort(key=sort_by_page)
        
        output_pdf = os.path.join(output_dir, f"{student_prefix}.pdf")
        create_pdf_from_images(filepaths, output_pdf)

def process_rendered_keys():
    input_dir = os.path.join(BASE_DIR, "dataset", "answer_keys", "rendered")
    
    # Question Paper
    q_pngs = glob.glob(os.path.join(input_dir, "Question_Paper_p*.png"))
    q_pngs.sort(key=sort_by_page)
    if q_pngs:
        create_pdf_from_images(q_pngs, os.path.join(input_dir, "Question_Paper.pdf"))
        
    # Answer Key
    a_pngs = glob.glob(os.path.join(input_dir, "Answer_Key_p*.png"))
    a_pngs.sort(key=sort_by_page)
    if a_pngs:
        create_pdf_from_images(a_pngs, os.path.join(input_dir, "Answer_Key.pdf"))

if __name__ == "__main__":
    print("Generating individual student PDFs...")
    process_student_booklets()
    
    print("\nGenerating Question Paper and Answer Key PDFs...")
    process_rendered_keys()
    
    print("\nDone!")
