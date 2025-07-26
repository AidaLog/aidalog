
# 🌿 AidaLog — Aided Logbook Entry Helper

**AidaLog** is an open-source web application designed to simplify and enhance the logbook experience for students undergoing **practical training**. Originally built for students at the **University of Dar es Salaam**, it helps reduce the burden of manual entry and lets students focus on learning, not formatting.

Whether you're tracking engineering projects, documenting lab work, or organizing weekly progress, AidaLog provides a structured, intuitive, and beautiful interface to help you **log your learning** — efficiently and meaningfully.

---

## 📚 Table of Contents

* [Features](#features)
* [Installation](#installation)
* [Usage](#usage)
* [Configuration](#configuration)
* [Project Structure](#project-structure)
* [Contributing](#contributing)
* [License](#license)
* [Contact](#contact)

---

## ✨ Features

* **🚀 One-Click Weekly Log Entries**
  Automatically generate structured entries for each week — then customize as needed.

* **📐 Diagram Uploads**
  Visualize your work by attaching supporting diagrams or charts.

* **🔐 Secure Authentication**
  Full user system with login, registration, and password reset flows.

* **📱 Mobile-Responsive & Aesthetic UI**
  Minimalist design with subtle animations and a clean student-first layout.

* **🌊 Parallax Animations**
  Soft visual effects (like wave patterns) make the experience more engaging.

* **🎓 Built for Students, by a Student**
  Lightweight, intuitive, and focused on reducing effort — not adding friction.

* **🌍 Open Source**
  Licensed under MIT. Anyone can use, remix, and improve.

---

## ⚙️ Installation

### Prerequisites

* Python 3.10+
* Git
* Django 4.x
* Virtual environment (recommended)
* Modern browser (Chrome, Firefox, Safari)

### Setup Steps

1. **Clone the repository**

   ```bash
   git clone https://github.com/AidaLog/aidalog.git
   cd aidalog
   ```

2. **Create a virtual environment**

   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Apply database migrations**

   ```bash
   python manage.py migrate
   ```

5. **Collect static files**

   ```bash
   python manage.py collectstatic
   ```

6. **Run the server**

   ```bash
   python manage.py runserver
   ```

Visit `http://localhost:8000` in your browser to get started.

---

## 🧭 Usage

### 🔓 Logging In

Visit `/login` to sign in using your email or username and password.

### 📝 Registering

Navigate to `/signup` to create a new account with:

* Username
* Email (e.g., `student@udsm.ac.tz`)
* Password (confirmed twice)

### 🔑 Forgot Password

Go to `/reset` and enter your email to reset your password securely.

---

### 📔 Creating a Logbook

After signing in:

1. Navigate to the **"My Logbooks"** section.
2. Click **"Create New"** and enter:

   * Week number
   * Starting date (Monday)
3. Click **"Generate Entries"** to pre-fill all 5 weekdays.
4. Click **"Operations"** to customize daily tasks and content.
5. Upload diagrams as needed.
6. Click **"Export / Print"** for submission-ready output.

---

## 🛠 Configuration

In `main/settings.py`:

### Static files

```python
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"
```

### Media files

```python
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / "media"
```

### Development mode

```python
DEBUG = True  # Set to False in production
```

Ensure you configure production settings with care, including static/media serving and secret keys.

---

## 🗂️ Project Structure

```
aidalog/
├── README.md
├── manage.py
├── main/                  # Django config
│   ├── settings.py
│   ├── urls.py
├── home/                  # Homepage and auth views
│   ├── templates/home/
│   ├── static/home/
├── logbook/               # Logbook feature logic
│   ├── templates/logbook/
│   ├── migrations/
├── static/                # Project-wide static files
├── media/                 # Uploaded diagrams
├── staticfiles/           # Production-ready static files
└── requirements.txt
```

### Key Files

* `static/home/assets/styles.css`: Core frontend styles
* `static/home/assets/js/script.js`: UI animations (Anime.js, form handling)
* `templates/home/index.html`: Landing page
* `templates/logbook/logbook_detail.html`: Weekly log interface
* `media/aidaLog.png`: Brand asset

---

## 🤝 Contributing

All contributions are welcome — whether you're fixing typos, adding new features, or improving the documentation.

### Quick Start

1. **Fork** the repo
   [https://github.com/AidaLog/aidalog](https://github.com/AidaLog/aidalog)

2. **Clone your fork**

   ```bash
   git clone https://github.com/YOUR_USERNAME/aidalog.git
   ```

3. **Create a feature branch**

   ```bash
   git checkout -b feature/your-feature-name
   ```

4. **Make your changes**
   Follow PEP8 and existing code style. Place new static assets in `/static/home/assets/`.

5. **Test locally**

   ```bash
   python manage.py runserver
   ```

6. **Commit & Push**

   ```bash
   git commit -m "Add: [short description]"
   git push origin feature/your-feature-name
   ```

7. **Open a Pull Request**
   Submit a PR with a clear explanation of what you’ve done.

### Guidelines

* Keep pull requests focused and concise
* Update docs or tests if applicable
* Respect the minimalist design aesthetic
* Check existing issues or open a new one to propose features

---

## 🪪 License

AidaLog is licensed under the **MIT License**.
You’re free to use, modify, and share — just retain the license notice.

---

## 👨‍🎓 Contact

* **GitHub**: [AidaLog/aidalog](https://github.com/AidaLog/aidalog)
* **Contact**: Open an issue or submit feedback via GitHub Discussions
* **Creator**: Built by a UDSM student to support peers in their training journey

---

## 💭 Final Note

> *“The best logs are lived, not typed.”*
> Begin your practical training with focus, not friction.