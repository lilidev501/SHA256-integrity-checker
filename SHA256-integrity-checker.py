import hashlib
import os
import json

BASELINE_FILE = "baseline.json"


def hash_file(filename):
    with open(filename, "rb") as f:
        data = f.read()
        return hashlib.sha256(data).hexdigest()


def create_baseline(folder):
    hashes = {}

    for file in os.listdir(folder):
        path = os.path.join(folder, file)
        if os.path.isfile(path):
            hashes[path] = hash_file(path)

    with open(BASELINE_FILE, "w") as f:
        json.dump(hashes, f, indent=4)

    print("Baseline created.")


def check_integrity(folder):
    with open(BASELINE_FILE, "r") as f:
        baseline = json.load(f)

    for file in os.listdir(folder):
        path = os.path.join(folder, file)
        if os.path.isfile(path):
            current = hash_file(path)
            if path not in baseline:
                print(f"[NEW] {file}")
            elif baseline[path] != current:
                print(f"[MODIFIED] {file}")
            else:
                print(f"[OK] {file}")

if __name__ == "__main__":
    folder = input("Enter folder path: ")
    action = input("Create baseline (c) or check integrity (i)? ")

    if action.lower() == "c":
        create_baseline(folder)
    elif action.lower() == "i":
        check_integrity(folder)
    else:
        print("Invalid choice.")
