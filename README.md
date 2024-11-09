# OpenCV-Based Face Recognition Attendance System

A real-time face recognition-based attendance system using OpenCV, face_recognition, and Firebase as a cloud backend. This application detects faces through a webcam, matches them against a pre-generated encoding, and logs attendance data to Firebase. 

## Table of Contents

- [Project Overview](#project-overview)
- [Features](#features)
- [System Architecture](#system-architecture)
- [Technologies Used](#technologies-used)
- [Setup and Installation](#setup-and-installation)
- [File Descriptions](#file-descriptions)
- [Usage](#usage)
- [Future Improvements](#future-improvements)
- [Contributing](#contributing)
- [License](#license)

## Project Overview

This project leverages face recognition technology to automate attendance tracking. It uses a real-time webcam feed to recognize and identify individuals based on pre-stored images, logs the attendance data in a Firebase real-time database, and updates attendance only once per day per individual.

### Key Objectives
- Automate attendance logging using face recognition.
- Ensure secure and real-time data storage.
- Efficiently manage attendance records with minimal user intervention.

## Features

- **Real-Time Face Detection**: Uses OpenCV and face_recognition to detect faces via webcam.
- **Student Data Retrieval**: Fetches student details like ID, Major, Year, and last attendance time from Firebase.
- **Attendance Logging**: Records attendance in real-time and updates only once per day.
- **Cloud-Based Storage**: Firebase stores attendance data and images securely.
- **Adaptive User Interface**: Displays attendance status and individual details dynamically.
- **Optimized Data Access**: Implements data caching for faster data retrieval.

## System Architecture

The architecture consists of three primary modules:
1. **Face Recognition**: Detects and encodes faces in real-time from webcam feed.
2. **Database Integration**: Communicates with Firebase to retrieve and update attendance data.
3. **User Interface**: Displays information such as student data, attendance status, and real-time updates.

## Technologies Used

- **Python**: Core language for development.
- **OpenCV**: For real-time face detection and display.
- **face_recognition**: Face encoding and matching.
- **Firebase**: Real-time database and cloud storage.
- **cvzone**: Interface enhancement for display elements.

## Setup and Installation

### Prerequisites

- Python 3.7 or later
- Firebase account with Firebase Realtime Database and Storage set up

### Installation Steps

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/your-username/OpenCV-Based-Face-Recognition-Attendance-System.git
   ```
   
2. **Navigate to the Project Directory**:
   ```bash
   cd OpenCV-Based-Face-Recognition-Attendance-System
   ```

3. **Install Required Packages**:
   ```bash
   pip install -r requirements.txt
   ```
   
4. **Firebase Setup**:
   - Obtain a `serviceAccounts.json` file from Firebase and place it in the `src/` directory.
   - Update the Firebase configuration in the code with your `databaseURL` and `storageBucket`.

5. **Generate Encodings**:
   - Run `encodegeneration.py` to generate face encodings for students and save them as `encode.p`.

## File Descriptions

- **main.py**: Main code for running the real-time face recognition attendance system.
- **adddatatodb.py**: Script to initialize Firebase and add sample student data to the database.
- **encodegeneration.py**: Generates face encodings from images and saves them in a pickle file for recognition.
- **serviceAccounts.json**: Firebase service account credentials (keep this file secure).
- **Resources/**: Contains background images and mode overlays for UI enhancements.

## Usage

1. **Run the Face Recognition Attendance System**:
   ```bash
   python main.py
   ```

2. **Adding Students**:
   - Use `adddatatodb.py` to initialize student data with relevant details such as name, major, and starting year.

3. **Viewing Attendance Records**:
   - Log into your Firebase console to view attendance data stored in the Realtime Database.

## Future Improvements

- **Enhanced Security**: Add encryption for stored data to protect sensitive information.
- **Advanced Face Recognition**: Integrate a more sophisticated model for faster and more accurate recognition.
- **Data Analytics Dashboard**: Visualize attendance data through Firebase’s data visualization tools.
- **Scalability**: Optimize the code and database queries to handle large datasets more efficiently.

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the project.
2. Create your feature branch (`git checkout -b feature/AmazingFeature`).
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`).
4. Push to the branch (`git push origin feature/AmazingFeature`).
5. Open a pull request.
