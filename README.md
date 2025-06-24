# Smart Park-Vision: Real-Time Parking Monitoring System

[![Python](https://img.shields.io/badge/Python-3.9-blue.svg)](https://www.python.org/)
[![OpenCV](https://img.shields.io/badge/OpenCV-4.x-green.svg)](https://opencv.org/)
[![Flask](https://img.shields.io/badge/Flask-2.x-orange.svg)](https://flask.palletsprojects.com/)
[![HTML5](https://img.shields.io/badge/HTML-5-red.svg)](https://developer.mozilla.org/en-US/docs/Web/Guide/HTML/HTML5)
[![CSS3](https://img.shields.io/badge/CSS-3-purple.svg)](https://developer.mozilla.org/en-US/docs/Web/CSS)
[![JavaScript](https://img.shields.io/badge/JavaScript-ES6-yellow.svg)](https://developer.mozilla.org/en-US/docs/Web/JavaScript)

This project is a functional prototype of a smart parking system that uses computer vision to detect the availability of parking spots in real-time. The main goal is to create a fast, low-cost solution to monitor and manage parking spaces, providing users with a live map of vacant and occupied spots.

![Image](https://github.com/user-attachments/assets/2068d204-f16c-4f28-a087-13ca63ec4dc5)

## Core Features

*   **Computer Vision Engine:** A Python script using OpenCV to analyze a video feed from any webcam or IP camera. It identifies vacant vs. occupied spots based on visual changes, without requiring complex AI model training.
*   **Centralized Backend:** A lightweight Flask server that acts as the brain of the operation. It receives status updates from the vision engine and serves this data through a simple REST API.
*   **Live Web Frontend:** A responsive web interface built with plain HTML, CSS, and JavaScript. It polls the backend periodically to display a real-time, color-coded map of the parking lot, accessible from any browser.
*   **Simplified Workflow:** The system is designed for rapid prototyping, demonstrating a full end-to-end flow from physical detection to user-facing visualization.

## Tech Stack

*   **Vision & Backend:**
    *   [Python](https://www.python.org/)
    *   [OpenCV](https://opencv.org/)
    *   [Flask](https://flask.palletsprojects.com/)
*   **Frontend:**
    *   HTML5
    *   CSS3
    *   JavaScript (Fetch API)
*   **Environment:**
    *   Anaconda (or any Python virtual environment)

## How It Works

1.  **Calibration:** An initial setup script (`calibrador.py`) allows the user to define the exact coordinates of each parking spot on a static image or a live video feed. These coordinates are saved to a `posiciones.yml` file.
2.  **Detection:** The main script (`detector.py`) reads the video stream, resizes it for performance, and for each defined spot, it calculates the number of non-zero pixels after applying a threshold. If the pixel count exceeds a pre-defined `umbral_deteccion`, the spot is marked as "occupied".
3.  **Communication:** When a spot's status changes, `detector.py` sends a `POST` request to the Flask backend.
4.  **Backend Logic:** The `server.py` receives the update, stores the current status of all spots in a dictionary, and makes it available via a `GET` endpoint at `/api/status`.
5.  **Visualization:** The `index.html` page uses JavaScript to fetch data from the `/api/status` endpoint every few seconds, dynamically rendering the parking map and updating the colors of the spots accordingly.

## Getting Started

### Prerequisites

*   Python 3.7+
*   Anaconda or `venv`
*   A webcam or an IP camera stream URL

### Installation & Setup

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/your-username/your-repo-name.git
    cd your-repo-name
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    # Using Anaconda
    conda create --name park-vision-env python=3.9
    conda activate park-vision-env

    # Or using venv
    python -m venv venv
    source venv/bin/activate  # On Windows: .\venv\Scripts\activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    # Or install manually: pip install opencv-python numpy pyyaml flask flask-cors requests
    ```

4.  **Configure the system:**
    *   Edit the `config.yml` file.
    *   Add your IP camera URL or a video file path to `video_source`.
    *   Take a screenshot of your parking lot and save it in the project folder. Set its name in `imagen_calibracion`.
    *   Adjust `umbral_deteccion` if needed.

### Running the Prototype

1.  **Calibrate the parking spots:**
    *   Run the calibrator script. It will use the image specified in `config.yml`.
      ```bash
      python calibrador.py
      ```
    *   Follow the on-screen instructions: click two opposite corners of a spot and press `s` to save. Repeat for all spots. Press `q` to quit and save the `posiciones.yml` file.

2.  **Start the backend server:**
    *   Open a new terminal.
      ```bash
      python server.py
      ```
    *   Leave this terminal running.

3.  **Start the detection engine:**
    *   Open a third terminal.
      ```bash
      python detector.py
      ```
    *   A window will pop up showing the live detection.

4.  **View the web interface:**
    *   Navigate to the `frontend` directory.
    *   Open the `index.html` file in your web browser.
    *   You should see the live status of your parking lot!
