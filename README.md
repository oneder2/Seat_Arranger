# 🎲 Random Seat Arranger

A simple desktop application built with PyQt5 that generates randomized seating charts from a student list. Users can load `.txt` or `.csv` files, specify the number of columns, and the app will automatically display a well-formatted seating table that can be exported to a CSV file.

## ✨ Features

- Load student lists from `.txt` or `.csv` files
- Generate random seating arrangements based on custom column count
- Intuitive graphical interface (GUI)
- Export seating charts to `.csv`
- Automatically fills incomplete rows with empty seats for even layout

## 🖼️ UI Preview

> 📸 You can insert screenshots of the application interface here for visual presentation.

## 🛠️ Getting Started

### 1. Install Dependencies

Make sure you have Python 3 installed, then run:

```bash
pip install pyqt5 pandas prompt_toolkit
```

### 2. Run the Application

```bash
python driver.py
```

### 3. How to Use

1. Click **"Select File"** to import a student list (`.txt` or `.csv`)
   - `.txt`: One student name per line
   - `.csv`: Must include a `name` column
2. Enter the number of **columns**
3. Click **"Start Sorting"** to generate the seating chart
4. Use the **"Save"** option from the File menu to export the chart

## 📂 Project Structure

```
.
├── driver.py           # Entry point for the application
├── main_window.py      # GUI implementation using PyQt5
├── seat_arranger.py    # Core logic for loading, shuffling, and saving data
└── README.md           # Project description (this file)
```

## 📥 Input Format Examples

### TXT format:

```
Alice
Bob
Charlie
```

### CSV format:

```csv
name
Alice
Bob
Charlie
```

## 💡 Highlights

- Uses `QTableWidget` with auto-resize and centered text
- Flexible file input format
- Clear error messages and warnings
- Clean layout, ideal for classrooms, exams, or workshops

## 📄 License

This project is licensed under the MIT License. Feel free to use, modify, and distribute it.

---

👨‍💻 Developer: **Oneder2**  
📫 Contact: gellar@tutanota.com
🌱 Motivation: A fun practice project for learning PyQt5 and building useful automation tools
