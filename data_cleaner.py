
import csv
import re

INPUT_FILE = "students_raw.csv"
CLEAN_FILE = "cleaned_students.csv"
REJECT_FILE = "rejected_students.csv"

valid_records = []
rejected_records = []
seen_ids = set()

def validate_email(email):
    pattern = r"^[\w.-]+@[\w.-]+\.\w+$"
    return re.match(pattern, email) is not None

try:
    with open(INPUT_FILE, "r", newline="") as file:
        reader = csv.DictReader(file)

        for row in reader:
            student_id = row["ID"].strip()
            name = row["Name"].strip()
            email = row["Email"].strip()
            age = int(row["Age"])
            marks = float(row["Marks"])

            reason = ""

            if not student_id or not student_id.isdigit():
                reason = "Invalid ID"

            elif student_id in seen_ids:
                reason = "Duplicate ID"

            elif not name:
                reason = "Name missing"

            elif not validate_email(email):
                reason = "Invalid email"

            elif age < 16 or age > 100:
                reason = "Invalid age"

            elif marks < 0 or marks > 100:
                reason = "Invalid marks"

            if reason:
                row["Reason"] = reason
                rejected_records.append(row)
            else:
                seen_ids.add(student_id)
                valid_records.append(row)

    with open(CLEAN_FILE, "w", newline="") as file:
        fields = ["ID", "Name", "Email", "Age", "Marks"]
        writer = csv.DictWriter(file, fieldnames=fields)
        writer.writeheader()
        writer.writerows(valid_records)

    with open(REJECT_FILE, "w", newline="") as file:
        fields = [
            "ID", "Name", "Email",
            "Age", "Marks", "Reason"
        ]
        writer = csv.DictWriter(file, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rejected_records)

    print("\n===== DATA CLEANING REPORT =====")
    print("Total Records:", len(valid_records) + len(rejected_records))
    print("Valid Records:", len(valid_records))
    print("Rejected Records:", len(rejected_records))

    print("\n===== REJECTION DETAILS =====")

    for row in rejected_records:
        print(row["Name"], "->", row["Reason"])

    print("\nCleaned data saved successfully!")

except FileNotFoundError:
    print("Input CSV file not found!")

except (ValueError, KeyError) as error:
    print("Invalid CSV data:", error)
