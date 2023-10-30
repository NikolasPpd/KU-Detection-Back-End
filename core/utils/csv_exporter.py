import csv
from config.settings import MODELS_TO_LOAD


def export_to_csv(files, csv_filename):
    # Assume the process names are like P1, P2, ... etc.
    # Extract and sort process names from the first CodeFile object for simplicity.
    # This assumes that each CodeFile object has results from all processes.
    # process_names = sorted(files[0].process_results.keys())
    # kus = sorted(files[0].ku_results.keys(), key=lambda x: int(x[1:]))
    kus = MODELS_TO_LOAD

    headers = ['filename', 'author', 'timestamp'] + kus

    with open(csv_filename, 'w', newline='', encoding='utf-8-sig') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(headers)

        for code_file in files.values():
            row = [
                      code_file.filename,
                      code_file.author,
                      code_file.timestamp
                  ] + [1 if code_file.ku_results[ku] else 0 for ku in kus]
            writer.writerow(row)
