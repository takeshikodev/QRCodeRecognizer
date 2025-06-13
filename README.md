# QRCodeRecognizer

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Technologies](#technologies)
- [Architecture](#architecture)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [License](#license)

## Overview

**QRCodeRecognizer** is a Python desktop application for detecting and decoding QR codes in images. It provides a user-friendly interface with advanced image processing capabilities to enhance QR code recognition even in challenging conditions.

The application uses computer vision techniques to detect QR codes and displays the decoded information in a clean, modern interface. It's designed for users who need to quickly extract data from QR codes in various image formats.

### Target Audience
- General users who need to scan QR codes from images
- Developers working with QR code data
- Businesses that process QR codes in batch operations

## Features

### QR Code Detection

- **Multi-stage Processing**: Uses various image processing techniques to improve detection
- **Enhanced Recognition**: Applies adaptive thresholding, CLAHE enhancement, and edge detection
- **Visual Feedback**: Highlights detected QR codes with green borders
- **Type Identification**: Shows the type of detected code

### User Interface

- **Modern Design**: Clean, intuitive interface with a modern aesthetic
- **Drag & Drop Support**: Easily load images via drag and drop
- **Image Preview**: See the processed image with marked QR codes
- **Results Panel**: View decoded QR code data in a separate panel
- **Save Results**: Save processed images with marked QR codes

## Technologies

### Development

- **Python**: Primary programming language
- **OpenCV**: Computer vision and image processing
- **NumPy**: Numerical operations for image processing
- **PyZbar**: QR code and barcode decoding
- **PyQt5**: GUI framework
- **Pillow**: Additional image processing capabilities

## Architecture

QRCodeRecognizer is built with a clean separation between the UI and detector components:

1. **Detector Module**: Core QR code detection logic
   - Image processing pipeline
   - QR code detection and decoding
   - Result processing

2. **UI Module**: User interface implementation
   - Main application window
   - Image display and interaction
   - Results presentation
   - Visual styling

## Installation

### Prerequisites

- Python 3.8+
- pip package manager

### Setup

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/takeshikodev/QRCodeRecognizer.git
   cd QRCodeRecognizer
   ```

2. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Application:**
   ```bash
   python main.py
   ```

## Usage

1. **Launch the application** by running `python main.py`
2. **Load an image** containing QR codes using one of these methods:
   - Click the "Select Image" button and choose a file
   - Drag and drop an image file onto the application window
3. **View results** in the right panel showing the decoded QR code data
4. **Save the processed image** with marked QR codes using the "Save Result" button

## Project Structure

```
QRCodeRecognizer/
├── detectors/           # QR code detection modules
│   └── qr_detector.py   # QR code detection implementation
├── ui/                  # User interface components
│   ├── app.py           # Main application window
│   └── styles.py        # UI styling definitions
├── requirements.txt     # Project dependencies
├── main.py              # Application entry point
└── README.md            # Project documentation
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details. 
