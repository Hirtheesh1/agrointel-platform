import subprocess
import sys
import os

def run_command(command, cwd=None):
    """Runs a shell command and returns the exit code."""
    print(f"\n==========================================")
    print(f"Running: {command}")
    print(f"==========================================")
    
    # Use powershell if on windows, otherwise bash
    shell_cmd = ["powershell", "-Command", command] if os.name == 'nt' else command
    
    result = subprocess.run(
        shell_cmd,
        cwd=cwd,
        shell=(os.name != 'nt'),
        text=True
    )
    return result.returncode

def main():
    print("starting AgroIntel Platform Validation Suite...")
    
    # Paths
    backend_dir = os.path.join(os.path.dirname(__file__), "..")
    frontend_dir = os.path.join(os.path.dirname(__file__), "../../frontend")
    
    # 1. Run Backend Tests
    print("\n[Phase 1-3] Backend Infrastructure, Pipeline, and AI Models")
    # For windows, use the venv
    pytest_cmd = ".\\venv\\Scripts\\pytest tests -q --disable-warnings" if os.name == 'nt' else "./venv/bin/pytest tests -q --disable-warnings"
    backend_status = run_command(pytest_cmd, cwd=backend_dir)
    
    if backend_status != 0:
        print("\n[ERROR] Backend validation failed. See above for details.")
        sys.exit(1)
        
    print("\n[SUCCESS] Backend validation passed!")
    
    # 2. Run Frontend Tests
    print("\n[Phase 4] Frontend Validation")
    frontend_status = run_command("npm run test", cwd=frontend_dir)
    
    if frontend_status != 0:
        print("\n[ERROR] Frontend validation failed. See above for details.")
        sys.exit(1)
        
    print("\n[SUCCESS] Frontend validation passed!")
    
    # 3. Generate Report
    print("\n[Phase 5] Validation Report generation")
    report_path = os.path.join(backend_dir, "validation_report.md")
    with open(report_path, "w", encoding="utf-8") as f:
        f.write("# AgroIntel Platform Validation Report\n\n")
        f.write("## Status: PASS\n\n")
        f.write("- **Backend Architecture**: Validated\n")
        f.write("- **Data Pipelines**: Validated\n")
        f.write("- **AI Forecasting Engine**: Validated\n")
        f.write("- **Frontend UI**: Validated\n")
        
    print(f"\n[SUCCESS] All systems go. Validation report written to {report_path}.")

if __name__ == "__main__":
    main()
