import time
from config import *
from core.git_operations import *
from core.utils.csv_exporter import *
from core.ml_operations.loader import *
from core.utils.code_files_loader import *
from core.analysis.sliding_window import sliding_window

if __name__ == "__main__":
    repo_path = "path/to/repo"  # Change this to the local path of the repository you want to analyze
    repo = get_repo(repo_path)
    contributions = extract_contributions(repo_path, commit_limit=10)

    if not os.path.exists(OUTPUT_FILES_BASE_PATH):
        os.mkdir(OUTPUT_FILES_BASE_PATH)

    if not contributions:
        print("No contributions found")
        exit(1)

    print("Contributions extracted. Now analyzing...")

    java_files = read_files_from_dict_list(contributions)
    models = load_models_from_directory(MODELS_BASE_PATH, MODELS_TO_LOAD)

    start_time = time.time()  # Start the timer

    results = sliding_window(java_files, 2, 12, 1, 1, models)

    end_time = time.time()  # Stop the timer
    elapsed_time = end_time - start_time
    print(f"\nTime taken to run sliding_window function: {elapsed_time:.4f} seconds")

    print("Exporting to CSV...")
    export_to_csv(java_files, os.path.join(OUTPUT_FILES_BASE_PATH, "output.csv"))  # This will overwrite the file if it already exists
    print("Done!")
