from flask import Flask, render_template, request, redirect, url_for
import os
import cv2
import face_recognition
import pandas as pd
from datetime import datetime

app = Flask(__name__)

# Directories and files
known_faces_dir = "known_faces"
student_info_file = 'students_info.xlsx'
attendance_file = 'attendance.xlsx'

# Ensure directories exist
if not os.path.exists(known_faces_dir):
    os.makedirs(known_faces_dir)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        user_name = request.form['name']
        enrollment = request.form['enrollment']
        semester = request.form['semester']

        image_path = capture_image(user_name)
        if image_path:
            store_student_info(user_name, enrollment, semester, image_path)
            return redirect(url_for('home'))
    return render_template('register.html')

@app.route('/attendance', methods=['GET', 'POST'])
def attendance():
    if request.method == 'POST':
        student_df = load_student_info()
        if student_df is not None:
            known_faces, known_names = load_known_faces(student_df)  # This will work now
            image = capture_image_for_attendance()
            if image is not None:
                recognized_data = recognize_face(image, known_faces, student_df)
                if recognized_data:
                    student_name, enrollment, semester = recognized_data
                    mark_attendance(student_name, enrollment, semester)
                    return render_template('success.html', name=student_name)
                else:
                    return render_template('failure.html', message="Student not recognized!")
    return render_template('attendance.html')

@app.route('/view', methods=['GET', 'POST'])
def view_attendance():
    if request.method == 'POST':
        student_name = request.form['name'].strip().lower()
        semester = request.form['semester'].strip()

        df = pd.read_excel(attendance_file)
        df['Name'] = df['Name'].str.strip().str.lower()
        df['Semester'] = df['Semester'].astype(str).str.strip()

        filtered_df = df[(df['Name'] == student_name) & (df['Semester'] == semester)]
        if filtered_df.empty:
            return render_template('view.html', result=None)
        else:
            return render_template('view.html', result=filtered_df.to_dict(orient='records'))
    return render_template('view.html', result=None)

# Helper functions (similar to your Python code)
def capture_image(user_name):
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    if ret:
        image_path = os.path.join(known_faces_dir, f"{user_name}.png")
        cv2.imwrite(image_path, frame)
        cap.release()
        return image_path
    return None

def store_student_info(user_name, enrollment, semester, image_path):
    student_data = {'Name': [user_name], 'Enrollment': [enrollment], 'Semester': [semester], 'ImagePath': [image_path]}
    df = pd.DataFrame(student_data)
    if os.path.exists(student_info_file):
        existing_df = pd.read_excel(student_info_file)
        df = pd.concat([existing_df, df], ignore_index=True)
    df.to_excel(student_info_file, index=False)

def load_student_info():
    if os.path.exists(student_info_file):
        return pd.read_excel(student_info_file)
    return None

def load_known_faces(student_df):
    known_faces = []
    known_names = []
    
    for index, row in student_df.iterrows():
        image_path = row['ImagePath']
        if os.path.exists(image_path):
            image = face_recognition.load_image_file(image_path)
            encodings = face_recognition.face_encodings(image)
            if encodings:  # Ensure there's at least one encoding
                known_faces.append(encodings[0])  # Only take the first encoding
                known_names.append(row['Name'])  # Add the corresponding name

    # Return only two lists: faces and names
    return known_faces, known_names

def capture_image_for_attendance():
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    cap.release()
    return frame if ret else None

def recognize_face(captured_image, known_faces, student_df):
    face_encodings = face_recognition.face_encodings(captured_image)
    if len(face_encodings) == 0:
        return None
    captured_encoding = face_encodings[0]
    matches = face_recognition.compare_faces(known_faces, captured_encoding)
    if True in matches:
        first_match_index = matches.index(True)
        student_name = student_df.iloc[first_match_index]['Name']
        enrollment = student_df.iloc[first_match_index]['Enrollment']
        semester = student_df.iloc[first_match_index]['Semester']
        return student_name, enrollment, semester
    return None

def mark_attendance(student_name, enrollment, semester, file='attendance.xlsx'):
    now = datetime.now()
    current_date = now.strftime("%Y-%m-%d")
    current_time = now.strftime("%H:%M:%S") 
    
    try:
        df = pd.read_excel(file)
    except FileNotFoundError:
        df = pd.DataFrame(columns=["Enrollment", "Name", "Semester", "Date", "Time"])

    # New record to be added
    new_record_df = pd.DataFrame({
        "Enrollment": [enrollment], 
        "Name": [student_name], 
        "Semester": [semester], 
        "Date": [current_date], 
        "Time": [current_time]
    })
    
    # Append using pd.concat instead of df.append()
    df = pd.concat([df, new_record_df], ignore_index=True)
    
    # Save the updated DataFrame back to the Excel file
    df.to_excel(file, index=False)
    
    print(f"Attendance marked for {student_name} (Enrollment: {enrollment}, Semester: {semester})")

if __name__ == "__main__":
    app.run(debug=True)
