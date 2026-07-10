import os
import pandas as pd
import numpy as np

def clean_and_verify():
    print("==================================================")
    print("            CLEANING & NORMALIZING DATA            ")
    print("==================================================")
    
    dataset_dir = "/Users/gaurav/Desktop/MyProjects/E-Shield/dataset"
    teacher_csv_path = os.path.join(dataset_dir, "training_csv/Teacher_manual_marks_Anonymized.csv")
    student_mcq_path = os.path.join(dataset_dir, "training_csv/Student_MCQ.csv")
    
    # Load raw data
    df_teacher = pd.read_csv(teacher_csv_path)
    df_mcq = pd.read_csv(student_mcq_path)
    
    # Rename columns in student_mcq for consistency
    df_mcq.columns = ['Numeric_ID', 'Student_Name'] + list(df_mcq.columns[2:])
    
    # 1. Clean MCQ Responses (1-20) in both datasets
    # Normalize '-' and empty cells to NaN
    mcq_cols = [str(i) for i in range(1, 21)]
    
    for col in mcq_cols:
        # In Teacher marks
        df_teacher[col] = df_teacher[col].astype(str).str.strip()
        df_teacher[col] = df_teacher[col].replace({'-': np.nan, 'nan': np.nan, 'NC': np.nan})
        # Map 'TRUE' to 'T' or similar if necessary (the answer key says B, so it is just an incorrect answer anyway)
        df_teacher[col] = df_teacher[col].replace({'TRUE': 'T'})
        
        # In Student MCQ
        df_mcq[col] = df_mcq[col].astype(str).str.strip()
        df_mcq[col] = df_mcq[col].replace({'-': np.nan, 'nan': np.nan, 'NC': np.nan, 'TRUE': 'T'})
        
    print("✓ MCQ response columns normalized (missing/skipped responses represented as NaN).")

    # 2. Clean Short Answer marks (21-35) in Teacher CSV
    sa_cols = [str(i) for i in range(21, 36)]
    
    for col in sa_cols:
        # Convert values to string, strip, then map non-numeric flags
        df_teacher[col] = df_teacher[col].astype(str).str.strip()
        # 'NC' (Not Corrected/Blank) and 'NM' (Not Marked) should be 0.0 marks awarded
        df_teacher[col] = df_teacher[col].replace({'NC': '0.0', 'NM': '0.0', 'nan': '0.0'})
        # Convert to float
        df_teacher[col] = pd.to_numeric(df_teacher[col], errors='coerce').fillna(0.0)
        
    print("✓ Short Answer mark columns normalized (converted to float, 'NC'/'NM' mapped to 0.0).")
    
    # 3. Verify total marks calculation
    print("\n--- Verification of Total Marks ---")
    
    # Re-calculate MCQ marks
    # Read answer key
    answer_key_path = os.path.join(dataset_dir, "answer_keys/answerkey.txt")
    df_key = pd.read_csv(answer_key_path)
    mcq_key = df_key[df_key['Type'] == 'MCQ'].set_index('Question_Number')['Correct_Answer'].to_dict()
    
    recalc_mcqs = []
    recalc_sas = []
    recalc_totals = []
    mismatch_details = []
    
    for idx in range(len(df_teacher)):
        row = df_teacher.iloc[idx]
        student_id = row['Student_ID']
        
        # Recalculate MCQ mark
        mcq_score = 0.0
        for q in range(1, 21):
            ans = row[str(q)]
            correct_ans = mcq_key.get(q)
            if ans == correct_ans:
                mcq_score += 1.0
        recalc_mcqs.append(mcq_score)
        
        # Recalculate Short Answer score
        sa_score = sum(row[str(q)] for q in range(21, 36))
        recalc_sas.append(sa_score)
        
        total_score = mcq_score + sa_score
        recalc_totals.append(total_score)
        
        # Verify against recorded values
        recorded_mcq = float(row['MCQ mark'])
        recorded_sa = float(row['2 marks'])
        recorded_total = float(row['total'])
        
        if abs(mcq_score - recorded_mcq) > 0.01 or abs(sa_score - recorded_sa) > 0.01 or abs(total_score - recorded_total) > 0.01:
            mismatch_details.append({
                'Student_ID': student_id,
                'Recorded_MCQ': recorded_mcq, 'Recalc_MCQ': mcq_score,
                'Recorded_SA': recorded_sa, 'Recalc_SA': sa_score,
                'Recorded_Total': recorded_total, 'Recalc_Total': total_score
            })
            
    print(f"Calculated MCQ marks matching recorded MCQ marks: {len(df_teacher) - len([m for m in mismatch_details if m['Recorded_MCQ'] != m['Recalc_MCQ']])} / {len(df_teacher)}")
    print(f"Calculated SA marks matching recorded SA marks: {len(df_teacher) - len([m for m in mismatch_details if m['Recorded_SA'] != m['Recalc_SA']])} / {len(df_teacher)}")
    print(f"Calculated Total marks matching recorded Total marks: {len(df_teacher) - len([m for m in mismatch_details if m['Recorded_Total'] != m['Recalc_Total']])} / {len(df_teacher)}")
    
    if mismatch_details:
        print("\nDetails of Mismatches (if any):")
        for m in mismatch_details:
            print(f"  - {m['Student_ID']}:")
            print(f"    * MCQ: Recorded={m['Recorded_MCQ']}, Calculated={m['Recalc_MCQ']}")
            print(f"    * SA: Recorded={m['Recorded_SA']}, Calculated={m['Recalc_SA']}")
            print(f"    * Total: Recorded={m['Recorded_Total']}, Calculated={m['Recalc_Total']}")
            
    # 4. Map Anonymous and Numeric IDs and save Cleaned CSV files
    # Create clean mapping
    mapping_list = []
    for idx in range(len(df_teacher)):
        t_row = df_teacher.iloc[idx]
        t_id = t_row['Student_ID']
        
        # Find matching row in df_mcq by matching non-null MCQ answers
        match_idx = None
        for jdx in range(len(df_mcq)):
            m_row = df_mcq.iloc[jdx]
            match = True
            for q in range(1, 21):
                t_ans = t_row[str(q)]
                m_ans = m_row[str(q)]
                # If one is NaN, the other should be NaN or 'nan'
                if pd.isna(t_ans) and pd.isna(m_ans):
                    continue
                if t_ans != m_ans:
                    match = False
                    break
            if match:
                match_idx = jdx
                break
                
        if match_idx is not None:
            m_row = df_mcq.iloc[match_idx]
            mapping_list.append({
                'Student_ID': t_id,
                'Numeric_ID': m_row['Numeric_ID'],
                'Student_Name': m_row['Student_Name']
            })
            
    df_map = pd.DataFrame(mapping_list)
    mapping_path = os.path.join(dataset_dir, "training_csv/student_id_mapping.csv")
    df_map.to_csv(mapping_path, index=False)
    print(f"\n✓ Saved student ID mapping to {mapping_path}")
    
    # Save cleaned CSV files
    cleaned_teacher_path = os.path.join(dataset_dir, "training_csv/cleaned_Teacher_manual_marks.csv")
    cleaned_mcq_path = os.path.join(dataset_dir, "training_csv/cleaned_Student_MCQ.csv")
    
    df_teacher.to_csv(cleaned_teacher_path, index=False)
    df_mcq.to_csv(cleaned_mcq_path, index=False)
    
    print(f"✓ Saved cleaned Teacher marks to {cleaned_teacher_path}")
    print(f"✓ Saved cleaned Student MCQ to {cleaned_mcq_path}")

if __name__ == "__main__":
    clean_and_verify()
