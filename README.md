# Air Canvas

Built with the tools and technologies:  
![Python](https://img.shields.io/badge/Python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![OpenCV](https://img.shields.io/badge/OpenCV-27338e?style=for-the-badge&logo=opencv&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white)
![MediaPipe](https://img.shields.io/badge/MediaPipe-orange?style=for-the-badge&logo=google&logoColor=white)

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Usage](#usage)
- [Project Roadmap](#project-roadmap)
- [Contributing](#contributing)
- [License](#license)
- [Acknowledgments](#acknowledgments)

---


---

## Overview

**Air Canvas** is an interactive drawing application that uses **hand gestures** to draw on the screen. It provides a futuristic way to sketch and control the brush using your fingers — no mouse or stylus needed!

---

## Features

- ✋ **Hand Gesture Recognition** with MediaPipe
- 🖌️ **Dynamic Drawing Interface** with real-time color and thickness control
- 🌐 **Web App Powered by Flask**
- 🎨 Switch between brush colors and eraser with gestures
- 📏 Change brush thickness using finger positions

---

## Project Structure

```bash
Air-Canvas/
│
├── Air_canvas_images/
│   └──  1.png
├── static/
│   └── css/
       └── Style.css
    └── js/
       └── Script.js
├── templates/
    └── index.html
├── .gitignore
├── README.md
├── app.py
├── font.py
├── requirements.txt
└── README.md
```


## Getting Started

### Prerequisites

- **Programming Language:** Python 3.7 or higher
- **Required Libraries:** Flask, OpenCV, MediaPipe, NumPy, and other libraries listed in [requirements.txt](requirements.txt).

### Installation

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/yourusername/Air-Canvas.git
   ```

2. **Navigate to the Project Directory:**
   ```bash
   cd Air-Canvas
   ```
   
3. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
   
### Usage

To launch the Air Canvas application, use the following command:
   ```bash
   python app.py
   ```

This will start a local Flask server where you can:
- Access the web interface for hand gesture-based drawing.
- Use real-time drawing with customizable brush color and thickness.

---

## Project Roadmap

- [X] **Task 1:** Implement hand gesture recognition for drawing.
- [X] **Task 2:** Integrate color and thickness control.
- [X] **Task 3:** Improve user interface with Flask.
- [X] **Task 4:** Optimize for performance and latency.

---

## Contributing

- **💬 [Join the Discussions](https://LOCAL/GitHub/Air-Canvas/discussions):** Share insights, provide feedback, or ask questions.
- **🐛 [Report Issues](https://LOCAL/GitHub/Air-Canvas/issues):** Submit bugs or request features.
- **💡 [Submit Pull Requests](https://LOCAL/GitHub/Air-Canvas/blob/main/CONTRIBUTING.md):** Fork the repository, create a feature branch, and submit a PR.

<details>
<summary>Contributing Guidelines</summary>

1. **Fork the Repository:** Fork the project to your account.
2. **Clone Locally:** Clone your forked repository.
   ```bash
    git clone https://github.com/yourusername/Air-Canvas.git
   ```  
3. **Create a New Branch:**
   ```bash
   git checkout -b new-feature-x
   ```
4. **Make Your Changes:** Develop and test your changes locally.
5. **Commit Your Changes:**
   ```bash
   git commit -m "Implemented feature x."
   ```
6. **Push to Your Fork:**
   ```bash
   git push origin new-feature-x
   ```
7. **Submit a Pull Request:** Create a PR against the original repository with a clear description of your changes.
8. **Review:** Once reviewed and approved, your changes will be merged.

</details>

---

## License

This project is protected under the [MIT](https://choosealicense.com/licenses/mit/#) License. For more details, please refer to the [LICENSE](https://choosealicense.com/licenses/) site.

---

## Acknowledgments

- **Contributors:**
- **Sajal Dhuriya**  
 [LinkedIn](https://www.linkedin.com/in/sajal-dhuriya-b2056b272/) | [GitHub](https://github.com/sajaldhuriya)
- **Anshika Pragati**  
 [LinkedIn](https://www.linkedin.com/in/anshika-pragati-4418bb298/) | [GitHub]()
- **Khyati Jain**  
 [LinkedIn](https://www.linkedin.com/in/khyatij/) | [GitHub](https://github.com/kyati001)
- **Avinash Gupta**  
 [LinkedIn](https://www.linkedin.com/in/avinash-gupta-442469267?utm_source=share&utm_campaign=share_via&utm_content=profile&utm_medium=android_app ) | [GitHub]()
- **Ayush Kushwaha**  
 [LinkedIn](https://www.linkedin.com/in/ayush-kushwaha-693735225?utm_source=share&utm_campaign=share_via&utm_content=profile&utm_medium=android_app) | [GitHub](https://github.com/AYUS2307)

- **Inspiration & Contributions:** Thanks to the open-source community for providing robust libraries (such as MediaPipe, OpenCV, and Flask) that made this project possible.
- **Other Resources:** Special thanks to gesture recognition libraries like [MediaPipe](https://mediapipe.dev/) that enabled the hand gesture-based interface.







