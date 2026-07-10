import os
import glob
import re

docs_dir = "/Users/gaurav/Desktop/MyProjects/E-Shield/docs"

todos = {
    "API_CONTRACT.md": ["[ ] Implement FastAPI endpoints for submission", "[ ] Implement FastAPI endpoints for retrieval"],
    "API_SECURITY.md": ["[ ] Implement JWT authentication", "[ ] Add rate limiting and DDoS protection"],
    "ARCHITECTURE.md": ["[ ] Finalize component architecture diagrams", "[ ] Review system boundaries"],
    "BACKEND_SECURITY.md": ["[ ] Setup secure environment variables", "[ ] Implement input sanitization middleware"],
    "BACKUP_RESTORE.md": ["[ ] Create automated SQLite backup scripts", "[ ] Test database restore procedure"],
    "DASHBOARD_PLAN.md": ["[ ] Scaffold Next.js dashboard UI", "[ ] Implement reporting and analytics views"],
    "DATABASE_DESIGN.md": ["[x] Implement SQLite schema", "[x] Implement CRUD operations in db.py"],
    "DATA_FLOW.md": ["[x] Implement ingestion data flow", "[ ] Implement evaluation data flow"],
    "DATA_PRIVACY.md": ["[ ] Add data anonymization for students", "[ ] Implement data retention and deletion policies"],
    "DBMS_CONCEPTS.md": ["[x] Map relational concepts to SQLite schema", "[x] Apply foreign key constraints"],
    "DEVOPS_PLAN.md": ["[ ] Setup GitHub Actions CI/CD pipeline", "[ ] Create Dockerfiles for deployment"],
    "DISASTER_RECOVERY.md": ["[ ] Define failover strategies", "[ ] Test disaster recovery plan locally"],
    "ENGINES_PLAN.md": ["[x] Build Ingestion & OCR Engines", "[ ] Build Evaluation & Scoring Engine"],
    "EXAM_INTEGRITY.md": ["[ ] Implement anomaly detection in grading", "[ ] Add audit logging for score changes"],
    "EXAM_LIFECYCLE.md": ["[ ] Implement exam creation workflow", "[ ] Implement end-to-end exam grading workflow"],
    "ExamShield_Workflow.md": ["[x] Document initial processing workflow", "[ ] Complete end-to-end integration"],
    "FAQ.md": ["[ ] Review and update questions based on implementation progress"],
    "FEATURES.md": ["[x] Implement Core OCR and Storage features", "[ ] Implement Frontend and Analytics features"],
    "FUTURE_IMPLEMENTATION_TASKS.md": ["[ ] Prioritize backlog items", "[ ] Assign remaining tasks to milestones"],
    "HOW_TO_RUN.md": ["[x] Document backend local setup", "[ ] Document frontend local setup"],
    "MONITORING.md": ["[ ] Setup logging infrastructure", "[ ] Configure alerting for failed pipelines"],
    "OCR_PLAN.md": ["[x] Integrate local TrOCR model", "[x] Implement confidence scoring module"],
    "PIPELINE_PLAN.md": ["[x] Build PDF Rasterization pipeline", "[x] Build Image Preprocessing & Segmentation pipelines"],
    "PROBLEM_STATEMENT.md": ["[x] Define problem scope clearly", "[x] Identify target audience and use cases"],
    "PROGRESS.md": ["[x] Update phase 1 ingestion progress", "[ ] Track phase 2 evaluation progress"],
    "PROJECT_ANALYSIS.md": ["[x] Complete initial feasibility analysis", "[ ] Review system requirements"],
    "ROADMAP.md": ["[x] Define initial milestones", "[ ] Update roadmap based on current progress"],
    "SCALABILITY.md": ["[ ] Implement caching layer for model predictions", "[ ] Design for horizontal scaling of OCR tasks"],
    "SECRETS.md": ["[ ] Setup .env templates", "[ ] Configure local secrets manager integration"],
    "SECURE_DEVELOPMENT.md": ["[ ] Add SAST scanning to pipeline", "[ ] Review dependencies for known vulnerabilities"],
    "SYSTEM_DESIGN.md": ["[x] Draft initial system architecture", "[ ] Refine API gateways and load balancers"],
    "TECH_STACK.md": ["[x] Document Python backend stack", "[ ] Document Next.js frontend stack"],
    "TESTING_PLAN.md": ["[x] Write ingestion and storage unit tests", "[ ] Write end-to-end integration tests"],
    "USER_ROLES.md": ["[ ] Define RBAC (Role-Based Access Control) models", "[ ] Implement Role-checking middleware"],
    "context.md": ["[x] Establish baseline project context", "[ ] Update context with implementation details"],
    "implementation_plan.md": ["[x] Execute database implementation plan", "[ ] Draft evaluation engine implementation plan"],
    "plan.md": ["[x] Complete initial planning phase", "[ ] Complete execution phase"],
}

standard_items = [
    "[ ] Review document for technical accuracy against current implementation.",
    "[ ] Ensure all referenced internal links are valid and working.",
    "[ ] Add architectural or workflow diagrams where applicable.",
    "[ ] Proofread for grammar, consistency, and tone.",
    "[ ] Cross-reference with SYSTEM_DESIGN.md for alignment.",
    "[ ] Verify that security considerations are documented if relevant.",
    "[ ] Add examples or code snippets to clarify complex sections.",
    "[ ] Check formatting (headers, bolding, lists) for readability.",
    "[ ] Schedule a final review with project stakeholders.",
    "[ ] Update the 'Last Modified' timestamp once finalized."
]

for filepath in glob.glob(os.path.join(docs_dir, "*.md")):
    filename = os.path.basename(filepath)
    if filename in todos:
        specific_items = todos[filename]
        
        # We need at least 10 items
        needed = 10 - len(specific_items)
        full_list = specific_items + standard_items[:needed]
        
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # If the file already has a To-Do list, we replace it
        if "## To-Do List" in content:
            # Strip everything after and including "## To-Do List"
            content = content.split("## To-Do List")[0].rstrip()
            
        print(f"Updating 10-item To-Do list in {filename}")
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
            f.write("\n\n## To-Do List\n\n")
            for item in full_list:
                f.write(f"- {item}\n")

print("Done updating To-Do lists to 10 items each.")
