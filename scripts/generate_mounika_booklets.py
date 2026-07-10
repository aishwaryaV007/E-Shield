"""
Generate 10 Data-Science answer booklets in Mounika's handwriting style.

Uses the Caveat font (rounded, casual cursive — close to Mounika's writing),
blue ink on ruled notebook paper, multi-page output for 35 questions.

Output: dataset/raw_scripts/Mounika_Style/<Name>_DS_Answers_p<N>.png
"""

import os
import textwrap
from PIL import Image, ImageDraw, ImageFont

# ── paths ────────────────────────────────────────────────────────────────
BASE_DIR   = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FONT_PATH  = os.path.join(BASE_DIR, "fonts", "Caveat.ttf")
OUTPUT_DIR = os.path.join(BASE_DIR, "dataset", "raw_scripts", "Mounika_Style")
os.makedirs(OUTPUT_DIR, exist_ok=True)

if not os.path.exists(FONT_PATH):
    raise FileNotFoundError(
        f"Caveat font not found at {FONT_PATH}. "
        "Run the download step first (see implementation plan)."
    )

# ── page constants ───────────────────────────────────────────────────────
PAGE_W, PAGE_H = 1240, 1754          # A4 @ ~150 DPI
LINE_SPACING   = 60
MARGIN_LEFT    = 100
TEXT_X         = MARGIN_LEFT + 20
INK_COLOR      = (25, 25, 120)       # dark-blue ink matching Mounika
PAPER_COLOR    = (250, 247, 241)     # off-white notebook paper
RULE_COLOR     = (200, 210, 225)     # light-blue ruled lines
MARGIN_COLOR   = (255, 100, 100)     # red margin line
WRAP_WIDTH     = 50                  # chars per line

# ── student profiles ─────────────────────────────────────────────────────
# quality: "high" → near-perfect, "mid" → partial, "low" → weak/wrong

STUDENTS = [
    # ─── HIGH scorers (2-3) ───
    {
        "name": "Mounika Reddy",
        "roll": "DS-201",
        "quality": "high",
        "mcq": list("BCACBAAACACBCBCCBCBB"),   # all correct
        "short": {
            21: "Supervised learning is a type of machine learning where the model is trained on labeled data — data with known inputs and their corresponding correct outputs. The model learns a mapping function from inputs to outputs.",
            22: "The model is overfitting. It has memorized the training data patterns (99% accuracy) but completely fails to generalize to unseen test data (30% accuracy). The gap between training and testing performance is a classic sign of overfitting.",
            23: "Regression analysis is a statistical process for estimating the relationships between a dependent variable and one or more independent variables. It helps predict continuous outcomes based on input features.",
            24: "Two major challenges: 1) Data quality issues — missing values, noisy data, and inconsistent formats make it hard to train reliable models. 2) Overfitting — models memorize training data instead of learning general patterns, leading to poor performance on new data.",
            25: "1) Healthcare — predicting disease outcomes and drug effectiveness using patient records. 2) Finance — fraud detection systems that identify suspicious transactions in real-time using ML models.",
            26: "Structured data is highly organized in rows and columns (like SQL databases and Excel sheets). Semi-structured data has some organizational markers but doesn't fit into a rigid tabular format — examples include JSON, XML, and HTML documents.",
            27: "Detection methods: Z-score analysis, IQR method, box plots, and scatter plots. Handling methods: Trimming (removing outliers), Capping (replacing with boundary values), or Imputation (replacing with mean/median).",
            28: "Data pre-processing refers to the steps taken to clean, transform, and organize raw data into a format suitable for machine learning models. This includes handling missing values, normalization, encoding categorical variables, and removing noise.",
            29: "K-NN is a distance-based algorithm. If features have different scales (e.g., age 0-100 vs salary 10000-100000), features with larger scales will dominate the distance calculation, leading to biased predictions. Normalization ensures all features contribute equally.",
            30: "Continuous attributes are discretized by grouping values into bins or intervals. For example, ages 1-100 can be discretized into categories: 'Child' (0-12), 'Teenager' (13-19), 'Adult' (20-59), 'Senior' (60+).",
            31: "In K-Means clustering, 'K' represents the predefined number of clusters or groups that the data will be divided into. The algorithm partitions data points into exactly K clusters based on distance to cluster centroids.",
            32: "Three common hyperparameters: 1) Learning Rate — controls step size during gradient descent. 2) Number of Estimators/Trees — in ensemble methods like Random Forest. 3) Max Depth — controls how deep decision trees can grow.",
            33: "Gradient Descent is an iterative optimization algorithm used to minimize a cost/loss function. It works by computing the gradient (slope) of the cost function and moving the parameters in the direction of steepest descent until reaching a minimum.",
            34: "Comparing three SVM classifiers: A classifier with a large margin and correct boundary is ideal — it generalizes well. A narrow-margin classifier may overfit. A classifier with the maximum margin that correctly separates classes while keeping data points outside the margin (gutter) is optimal.",
            35: "The RBF (Radial Basis Function) kernel in SVM transforms data into a higher-dimensional space using a Gaussian function. This allows SVM to find non-linear decision boundaries. The kernel measures similarity between points — closer points have higher similarity values.",
        }
    },
    {
        "name": "Sravya Lakshmi",
        "roll": "DS-202",
        "quality": "high",
        "mcq": list("BCACBAAACACBCBCCBCBB"),   # all correct
        "short": {
            21: "Supervised Learning is a machine learning approach where the algorithm is trained using labeled data. The model receives input-output pairs and learns to map inputs to correct outputs so it can predict outcomes for new, unseen data.",
            22: "This model is suffering from overfitting. The 99% training accuracy means it memorized the training data, while the 30% test accuracy shows it cannot generalize. Solutions include regularization, cross-validation, or getting more training data.",
            23: "Regression analysis is a statistical method used to estimate relationships between variables. It predicts a continuous dependent variable based on one or more independent variables using mathematical equations.",
            24: "Challenge 1: Overfitting and underfitting — balancing model complexity to generalize well. Challenge 2: Data collection and quality — gathering sufficient, clean, representative data is often expensive and time-consuming.",
            25: "Application 1: E-commerce recommendation systems — platforms like Amazon use data science to recommend products. Application 2: Healthcare — predicting disease progression and optimizing treatment plans.",
            26: "Structured data: Organized into fixed rows and columns, easily stored in relational databases (Excel, SQL). Semi-structured: Contains tags or markers for organization but doesn't follow strict tabular format (JSON, XML, HTML).",
            27: "Detection: Use Z-score (values > 3 standard deviations), IQR method (below Q1-1.5*IQR or above Q3+1.5*IQR), and visual tools like box plots. Handling: Remove outliers, cap them at boundary values, or replace with mean/median.",
            28: "Data pre-processing is the process of cleaning and transforming raw data into a usable format. Steps include handling missing values, feature scaling, encoding categorical data, and removing duplicates or noise.",
            29: "K-NN relies on distance metrics like Euclidean distance. Without normalization, features with larger numerical ranges (e.g., income) overshadow features with smaller ranges (e.g., age), creating biased distance calculations and inaccurate predictions.",
            30: "Discretization converts continuous values into discrete categories. Example: Converting exact temperatures (23.5°C, 31.2°C, 15.8°C) into categories like 'Cold' (<20°C), 'Warm' (20-30°C), 'Hot' (>30°C).",
            31: "'K' in K-Means represents the number of clusters the algorithm will create. It is specified before running the algorithm. The algorithm assigns each data point to one of K clusters based on proximity to cluster centers.",
            32: "1) K in K-NN — the number of nearest neighbors to consider. 2) Learning Rate — how fast the model updates weights during training. 3) Number of Trees — in Random Forest, determines ensemble size.",
            33: "Gradient Descent is an optimization technique that minimizes a function by iteratively moving in the direction of steepest descent (negative gradient). Each step updates parameters by subtracting the gradient scaled by the learning rate.",
            34: "SVM classifiers differ by margins: Classifier 1 may have a wide margin (good generalization), Classifier 2 a narrow margin (potential overfitting), and Classifier 3 may misclassify some points for a wider margin. The optimal classifier maximizes margin while minimizing errors.",
            35: "The RBF kernel maps data to infinite-dimensional space using K(x,y) = exp(-gamma * ||x-y||^2). Points close together get high kernel values, far apart get low values. This enables SVM to create curved, non-linear decision boundaries in the original feature space.",
        }
    },
    {
        "name": "Haritha Devi",
        "roll": "DS-203",
        "quality": "high",
        "mcq": list("BCACBAAACACBCBBCBCBB"),   # Q15 wrong (A instead of C)
        "short": {
            21: "Supervised learning uses labeled datasets to train models. The training data has both input features and known output labels. The model learns patterns to predict outputs for new inputs.",
            22: "Overfitting is happening. The model learned the training data too well (99%) but fails on new data (30%). Need more data, regularization, or simpler model.",
            23: "Regression is a statistical technique that estimates relationships between a dependent variable and independent variables, predicting continuous numerical values.",
            24: "1) Data quality — messy, missing, or biased data leads to poor models. 2) Overfitting — model works great on training data but poorly on test data, failing to generalize.",
            25: "1) Healthcare — disease prediction from patient data. 2) Finance — fraud detection using transaction pattern analysis.",
            26: "Structured data has rigid format in rows and columns (databases, spreadsheets). Semi-structured has flexible tags/markers but no strict table format (JSON, XML).",
            27: "Detect using Z-score, IQR, box plots. Handle by removing, capping at boundaries, or replacing with central tendency measures.",
            28: "Pre-processing transforms raw data for ML: cleaning, handling missing values, normalization, feature engineering, encoding categorical variables.",
            29: "K-NN uses distance to classify. Without normalization, high-magnitude features dominate distance calculations, giving them unfair weight in predictions.",
            30: "Grouping continuous values into bins. Example: Income levels $0-30K='Low', $30-70K='Medium', $70K+='High'.",
            31: "K is the number of clusters to partition data into. User specifies K before running the algorithm.",
            32: "Learning rate, max depth of trees, and batch size are common hyperparameters.",
            33: "An optimization algorithm to minimize loss functions by computing gradients and updating parameters toward the minimum.",
            34: "The best SVM classifier has maximum margin between classes with all support vectors on the margin boundary. Narrow margins overfit, wide margins generalize better.",
            35: "RBF kernel transforms data to higher dimensions using Gaussian similarity. Allows non-linear separation by creating curved decision boundaries.",
        }
    },

    # ─── MID scorers (4) ───
    {
        "name": "Keerthi Priya",
        "roll": "DS-204",
        "quality": "mid",
        "mcq": list("BCACBAABCABCCBCCBCBA"),   # Q8 wrong (B→C), Q9 wrong (C→A), Q10 wrong (A→B), Q12 wrong (C→B), Q20 wrong (A→B)
        "short": {
            21: "Supervised learning is when we train a model using data that has labels. The model learns from examples where the answer is already known.",
            22: "The model is overfitting. It works well on training data but poorly on test data.",
            23: "Regression is used to predict continuous values based on input variables.",
            24: "Two challenges: 1) Getting enough good quality data. 2) Models can overfit to training data.",
            25: "Healthcare for disease prediction and finance for fraud detection.",
            26: "Structured data is in tables and columns. Semi-structured uses tags like JSON and XML.",
            27: "Outliers can be found using box plots and Z-scores. They can be removed or replaced.",
            28: "Pre-processing means cleaning the data before using it in a model.",
            29: "Normalization is needed because K-NN uses distances and features with bigger numbers would have more effect.",
            30: "Continuous values are grouped into categories. Like ages into Child, Adult, Senior.",
            31: "K is how many groups or clusters you want to make.",
            32: "Learning rate, number of trees, and K value.",
            33: "It is an algorithm that finds the minimum of a function by going downhill step by step.",
            34: "SVM classifiers have different margins. Bigger margins are better for classification.",
            35: "RBF kernel helps SVM handle non-linear data by transforming it to higher dimensions.",
        }
    },
    {
        "name": "Divya Sree",
        "roll": "DS-205",
        "quality": "mid",
        "mcq": list("BCAABABAACACBCBCBCBB"),   # Q5 wrong (A→B), Q6 wrong (B→A), Q7 wrong (B→A), Q8 wrong (A→C)
        "short": {
            21: "It is machine learning where we use labeled data with inputs and outputs for training the model.",
            22: "The model has overfitted to the training data. It memorized the data instead of learning patterns.",
            23: "Regression is a method for predicting numerical values from input data.",
            24: "1) Data might have missing values which affects model quality. 2) Overfitting makes the model useless on new data.",
            25: "Data science is used in healthcare to predict diseases and in online shopping for recommendations.",
            26: "Structured data is organized in tables. Semi-structured has some structure but not in rows and columns like JSON.",
            27: "Use IQR or Z-score to find outliers. Handle them by removing or capping them.",
            28: "Steps to clean raw data and make it ready for ML. Includes handling missing values and scaling.",
            29: "Features with different scales affect distance calculation in KNN. Normalization makes them equal.",
            30: "Converting continuous numbers into categories or bins. Example: temperature into Hot, Cold, Mild.",
            31: "K means the number of clusters we want the algorithm to create from the data.",
            32: "Learning rate, batch size, number of epochs.",
            33: "Gradient descent minimizes the cost function by taking steps in the direction of steepest descent.",
            34: "SVM uses margins to separate classes. A wider margin means better generalization.",
            35: "RBF kernel transforms data so that non-linearly separable data becomes linearly separable in higher dimensions.",
        }
    },
    {
        "name": "Manasa Rani",
        "roll": "DS-206",
        "quality": "mid",
        "mcq": list("BCBCBAABACACBCCCBCBB"),   # Q3 wrong (B→A), Q4 wrong (C→C), Q7 wrong (B→A), Q8 wrong (B→C), Q15 wrong (C→B)
        "short": {
            21: "Supervised learning trains models on data that already has correct answers provided.",
            22: "Overfitting has occurred. The model is too complex for the data.",
            23: "It predicts the relationship between dependent and independent variables. It gives continuous output.",
            24: "Challenges include handling missing or noisy data and preventing the model from overfitting.",
            25: "Used in medical diagnosis and financial fraud detection.",
            26: "Structured is organized tables. Semi-structured is partly organized like XML and JSON.",
            27: "Detect with box plots, handle by removal or replacement with median.",
            28: "Cleaning and organizing data before feeding it to ML algorithms. Includes normalization and encoding.",
            29: "KNN calculates distances between points. Without normalization, larger scale features dominate.",
            30: "Discretization bins continuous values. Age can be binned as Young, Middle-aged, Old.",
            31: "K is the number of groups the data is divided into by the algorithm.",
            32: "Learning rate, number of estimators, max depth.",
            33: "An algorithm that minimizes error by iteratively adjusting parameters downhill.",
            34: "Different SVMs have different margin widths. The best one maximizes the margin.",
            35: "RBF is a kernel function that maps data to higher space for non-linear classification.",
        }
    },
    {
        "name": "Anusha Goud",
        "roll": "DS-207",
        "quality": "mid",
        "mcq": list("ACACCAADCABBBCCCACBB"),   # several wrong
        "short": {
            21: "Supervised learning uses data with labels to train the model so it can predict correctly.",
            22: "The model overfitted. Training accuracy is high but test accuracy is very low.",
            23: "Regression predicts values. It shows the relationship between variables.",
            24: "Getting good quality data is hard. Also models can become too complex and overfit.",
            25: "Healthcare predictions and e-commerce recommendations use data science.",
            26: "Structured = tables and databases. Semi-structured = JSON, XML.",
            27: "Box plots and Z-scores detect outliers. Remove or replace them.",
            28: "Preparing raw data for use in machine learning by cleaning and transforming.",
            29: "Different scale features will have different impact on distance. Normalization fixes this.",
            30: "Putting numbers into groups or categories. Like marks into grades A, B, C.",
            31: "K is number of clusters.",
            32: "Learning rate, epochs, batch size.",
            33: "Optimization method that goes down the gradient to find minimum error.",
            34: "SVMs with larger margins work better. Support vectors define the boundary.",
            35: "RBF transforms data using Gaussian function for non-linear SVM classification.",
        }
    },

    # ─── LOW scorers (3) ───
    {
        "name": "Bhavani Sri",
        "roll": "DS-208",
        "quality": "low",
        "mcq": list("BADCAABDCBCACACCACBA"),   # many wrong
        "short": {
            21: "It uses labeled data for training.",
            22: "The model is not working well on test data.",
            23: "Regression predicts values.",
            24: "Data problems and overfitting.",
            25: "Healthcare and finance.",
            26: "Structured is tables. Semi-structured is JSON.",
            27: "Remove outliers from the data.",
            28: "Cleaning data.",
            29: "Normalization makes data equal.",
            30: "Putting values into groups.",
            31: "Number of clusters.",
            32: "Learning rate and batch size.",
            33: "It minimizes the cost function.",
            34: "SVM uses margins.",
            35: "RBF is a kernel.",
        }
    },
    {
        "name": "Thanuja Kumari",
        "roll": "DS-209",
        "quality": "low",
        "mcq": list("BBADAACDCACCBABBACAB"),   # many wrong
        "short": {
            21: "Learning with labels.",
            22: "Model is overfitting.",
            23: "Predicting continuous values.",
            24: "Bad data and complex models.",
            25: "Medicine and shopping websites.",
            26: "Structured has rows and columns.",
            27: "Use box plots to find outliers.",
            28: "Making data ready for models.",
            29: "Features need same scale.",
            30: "Grouping numbers.",
            31: "K is clusters.",
            32: "Learning rate.",
            33: "Finding minimum of function.",
            34: "Margins separate classes.",
            35: "Kernel for SVM.",
        }
    },
    {
        "name": "Swathi Naidu",
        "roll": "DS-210",
        "quality": "low",
        "mcq": list("CAABBDACCBAABCBCBCBA"),   # many wrong
        "short": {
            21: "Training models on data that has answers.",
            22: "Not generalizing to test data. Overfitting problem.",
            23: "Statistical method for prediction.",
            24: "1) Missing data. 2) Too much data.",
            25: "Hospitals and banks.",
            26: "Tables vs tags.",
            27: "Remove or replace bad values.",
            28: "Data cleaning steps.",
            29: "KNN needs normalized data for fair distance.",
            30: "Binning continuous data. Like age groups.",
            31: "How many groups to make.",
            32: "Learning rate, K value, depth.",
            33: "Goes downhill to minimize loss.",
            34: "SVM classifier with biggest margin is best.",
            35: "Gaussian kernel for non-linear problems.",
        }
    },
]


# ── rendering ────────────────────────────────────────────────────────────

def _new_page():
    """Create a blank ruled-notebook page."""
    img = Image.new("RGB", (PAGE_W, PAGE_H), PAPER_COLOR)
    draw = ImageDraw.Draw(img)
    # vertical margin
    draw.line([(MARGIN_LEFT, 0), (MARGIN_LEFT, PAGE_H)], fill=MARGIN_COLOR, width=2)
    # horizontal rules
    for y in range(LINE_SPACING, PAGE_H, LINE_SPACING):
        draw.line([(0, y), (PAGE_W, y)], fill=RULE_COLOR, width=2)
    return img, draw


def generate_booklet(student):
    """Render a full Data-Science answer booklet for one student."""
    name = student["name"]
    print(f"  Generating booklet for {name} ({student['quality']}) ...")

    try:
        font = ImageFont.truetype(FONT_PATH, 42)
    except IOError:
        print("    [WARN] Could not load Caveat font, falling back to default.")
        font = ImageFont.load_default()

    pages = []        # list of Image objects
    img, draw = _new_page()
    cur_y = LINE_SPACING + 10
    page_num = 1

    def _flush_page():
        nonlocal img, draw, cur_y, page_num
        pages.append((img, page_num))
        page_num += 1
        img, draw = _new_page()
        cur_y = LINE_SPACING + 10

    def _write(text):
        nonlocal cur_y
        wrapped = textwrap.wrap(text, width=WRAP_WIDTH)
        for line in wrapped:
            if cur_y > PAGE_H - LINE_SPACING * 2:
                _flush_page()
            draw.text((TEXT_X, cur_y), line, fill=INK_COLOR, font=font)
            cur_y += LINE_SPACING

    # ── header ──
    _write(f"Name: {name}")
    _write(f"Roll No: {student['roll']}")
    cur_y += LINE_SPACING  # blank line

    # ── Part I: MCQ answers ──
    _write("Part I: Multiple Choice Questions")
    cur_y += int(LINE_SPACING * 0.3)

    mcq_answers = student["mcq"]
    for i, ans in enumerate(mcq_answers, start=1):
        _write(f"{i}. {ans}")

    cur_y += LINE_SPACING  # gap before Part II

    # ── Part II: Short answers ──
    _write("Part II: Short Answer Questions")
    cur_y += int(LINE_SPACING * 0.3)

    for qnum in range(21, 36):
        ans_text = student["short"].get(qnum, "")
        _write(f"{qnum}. {ans_text}")
        cur_y += int(LINE_SPACING * 0.4)  # small gap between answers

    # flush last page
    pages.append((img, page_num))

    # ── save ──
    safe_name = name.replace(" ", "_")
    for page_img, pnum in pages:
        fname = os.path.join(OUTPUT_DIR, f"{safe_name}_DS_Answers_p{pnum}.png")
        page_img.save(fname)
    print(f"    [OK] Saved {len(pages)} page(s) for {name}")
    return len(pages)


# ── main ─────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("=" * 60)
    print("Generating Data-Science booklets in Mounika's style")
    print("=" * 60)
    total_pages = 0
    for s in STUDENTS:
        total_pages += generate_booklet(s)
    print(f"\nDone! {len(STUDENTS)} booklets, {total_pages} total pages.")
    print(f"Output: {OUTPUT_DIR}")
