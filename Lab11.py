import matplotlib.pyplot as plt
import os

# Helper functions
def parse_students(filepath):
    students = {}
    with (open(filepath, 'r') as file):
        for line in file:
            student_id = int(line[:3]) # first 3 characters are ID
            name = line[3:].strip()
            students[name] = student_id
    return students

def parse_assignments(filepath):
    assignments = {}
    with open(filepath, 'r') as file:
        lines = file.readlines()
        for i in range(0,len(lines),3):
            name = lines[i].strip()  # assignment name
            assignment_id = int(lines[i + 1].strip())  # assignment ID
            points = int(lines[i + 2].strip())  # points possible
            assignments[name] = (assignment_id, points)
    return assignments

def parse_submissions(folder_path):
    submissions = []
    # loop through all files in the submissions folder
    for filename in os.listdir(folder_path):
        if filename.endswith('.txt'):  # ensure we're only reading text files
            file_path = os.path.join(folder_path, filename)
            with open(file_path, 'r') as file:
                for line in file:
                    student_id, assignment_id, percent = line.strip().split('|')
                    submissions.append((int(student_id), int(assignment_id), float(percent)))
    return submissions


def calculate_student_grade(students, assignments, submissions, student_name):
    if student_name not in students:
        print("Student not found")
        return
    student_id = students[student_name]
    total_score = 0
    for student, assignment_id, percent in submissions:
        if student == student_id:
            assignment_points = next(points for aid, points in assignments.values() if aid == assignment_id)
            total_score += percent / 100 * assignment_points
    print(f"{round(total_score / 10)}%")

def assignment_statistics(assignments, submissions, assignment_name):
    if assignment_name not in assignments:
        print("Assignment not found")
        return
    assignment_id, _ = assignments[assignment_name]
    relevant_submissions = [submission for submission in submissions if submission[1] == assignment_id]
    scores = [submission[2] for submission in relevant_submissions]
    min_score = min(scores)
    avg_score = sum(scores) // len(scores)
    max_score = max(scores)
    print(f"Min: {min_score:.0f}%")
    print(f"Avg: {avg_score:.0f}%")
    print(f"Max: {max_score:.0f}%")

def display_assignment_graph(assignments, submissions, assignment_name):
    if assignment_name not in assignments:
        print("Assignment not found")
        return

    assignment_id, _ = assignments[assignment_name]
    relevant_submissions = [submission for submission in submissions if submission[1] == assignment_id]
    scores = [submission[2] for submission in relevant_submissions]
    plt.hist(scores, bins=[50,55, 60,65, 70,75, 80,85, 90,95, 100])
    plt.show()

# Main program
def main():
    students = parse_students('data/students.txt')
    assignments = parse_assignments('data/assignments.txt')
    submissions = parse_submissions('data/submissions')

    print("1. Student grade")
    print("2. Assignment statistics")
    print("3. Assignment graph")
    selection = input("\nEnter your selection: ")

    if selection == '1':
        student_name = input("What is the student's name: ")
        calculate_student_grade(students, assignments, submissions, student_name)
    elif selection == '2':
        assignment_name = input("What is the assignment name: ")
        assignment_statistics(assignments, submissions, assignment_name)
    elif selection == '3':
        assignment_name = input("What is the assignment name: ")
        display_assignment_graph(assignments, submissions, assignment_name)
    else:
        print("Invalid selection")

if __name__ == "__main__":
    main()
