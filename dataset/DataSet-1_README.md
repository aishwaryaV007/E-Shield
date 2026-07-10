Title: A Dataset of Digitized Student Examination Papers, Answer Keys, and Manual Evaluations for Automated Grading Research

Authors: [Dinesh K P email: kp.dinesh@yahoo.com]


Abstract
The automation of subjective and objective academic grading is an ongoing challenge in Educational Data Mining and Natural Language Processing (NLP). This dataset provides a comprehensive collection of university-level examination records for 50 students in a Data Science course. The exam comprises 20 Multiple Choice Questions (MCQs) carrying 1 mark each, and 15 Short Answer Questions carrying 2 marks each (Maximum Total: 50 marks). The dataset includes the original questionnaire, the authoritative answer key, raw digitized student answer sheets (PDFs), annotated/corrected student answer sheets (PDFs), and comma-separated values (CSV) files detailing item-level manual evaluation scores. This dataset serves as a valuable benchmark for researchers developing Optical Character Recognition (OCR) systems, Automated Essay Scoring (AES) models, and automated student evaluation pipelines.

Background & Summary
Manual grading of examinations is a time-consuming process prone to subjective inconsistencies. While automated grading of MCQs is highly standardized, the automated scoring of short descriptive answers remains a complex NLP task. To train and evaluate machine learning models for this purpose, researchers require paired datasets containing raw handwritten responses, ground-truth answer keys, and teacher-assigned marks.

This dataset fulfills that need by providing a transparent, end-to-end view of the examination process for 50 students. By providing both the uncorrected and corrected variations of the handwritten examination PDFs, alongside a meticulously recorded CSV of item-level marks, this dataset provides the necessary ground truth for training computer vision and machine learning models in the educational technology space.

Methods
Examination Structure
The examination evaluates students on the subject of Data Science. The question paper consists of two parts:

Part I: 20 Multiple Choice Questions (1 mark each).

Part II: 15 Short Answer Questions (2 marks each).

Total: 50 marks.

Data Collection & Digitization
Students submitted their handwritten answers on physical paper, which were subsequently digitized via a scanner into Portable Document Format (PDF) files. These represent the raw input data (Student_Pdf).

Manual Evaluation Process
An expert teacher evaluated the physical or digitized copies, applying standard grading rubrics aligned with the provided answer key. Marks for each of the 35 questions were documented. Corrections, ticks, and marks were directly annotated onto the PDFs, generating the ground-truth corrected records (Corrected_PDF). Final itemized scores were transcribed into digital CSV format for tabular data analysis.

Data Records
The dataset is organized into a hierarchical file structure containing raw texts, PDFs, and CSV files. All data is stored in the root directory Dataset/.

1. Root Directory Files
Question.txt: A text file containing the exact examination questions (Q1 to Q35) and instructions.

answerkey.txt: The definitive ground-truth reference containing the correct MCQ options and rubric/expected key points for the short answers.

Teacher_manual_marks.csv: The primary tabular dataset containing the itemized marks awarded by the teacher to each student.

Student_MCQ.csv: Tabular data specifically capturing the extracted MCQ responses of the students.

file.txt: Auxiliary metadata/log file.

2. Sub-directories
/Student_Pdf/: Contains 50 raw, uncorrected PDF files. Each file is named corresponding to the student's unique identification number (e.g., 1101901019.pdf). These are the raw inputs for OCR and grading models.

/Corrected_PDF/: Contains 50 manually graded PDF files. These files feature the teacher's annotations, visual corrections, and final tally marks, matching the filenames in the uncorrected folder.

Data Dictionary and Variables
The Teacher_manual_marks.csv file contains the following structure:

Student_ID: The unique numeric identifier of the student (corresponds to PDF filenames).

Student_Name: The name of the respective student.

MCQ_mark: The aggregated score for Q1–Q20 (Maximum 20).

2_marks: The aggregated score for the short answers Q21–Q35 (Maximum 30).

Total: The total examination score (Maximum 50).

Q1 to Q20: The student's chosen option for the MCQs (e.g., A, B, C, D).

Q21 to Q35: The specific numerical mark awarded for each short answer question (ranging from 0.0 to 2.0).

Special Value Encoding
NC: Stands for "No mark awarded, not corrected". This tag is used in the dataset to denote instances where a student left a question entirely blank, or a question was skipped and explicitly received no correction/marks from the evaluator.

Technical Validation
To ensure data integrity, the tabular data in Teacher_manual_marks.csv was cross-verified against the manual annotations present in the Corrected_PDF files. The sum of itemized columns (Q1-Q20 and Q21-Q35) strictly equals the values in the MCQ_mark, 2_marks, and Total columns respectively. To comply with standard ethical guidelines and protect student privacy, all Personally Identifiable Information (PII) has been strictly anonymized. Student names and institutional IDs have been replaced with sequential identifiers (e.g., Student_1, Student_2).

Usage Notes
This dataset is specifically designed for researchers in Artificial Intelligence and Educational Technology. Recommended use cases include:

Optical Character Recognition (OCR): Using Student_Pdf to test handwriting-to-text algorithms.

Automated Short Answer Scoring: Feeding extracted text into NLP models (like BERT or GPT architectures) to predict the score based on answerkey.txt and evaluating the model's accuracy against the itemized scores in Teacher_manual_marks.csv.

Computer Vision: Detecting teacher annotations (checkmarks, crosses) by calculating the pixel-wise differences between Student_Pdf and Corrected_PDF.
