# 📸 Photon Client Gallery

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/)
[![Django Version](https://img.shields.io/badge/django-4.2%2B-green)](https://www.djangoproject.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**Photon Client Gallery** is a professional-grade web platform designed for photographers to streamline the process of delivering high-quality images to clients. It bridges the gap between raw file management and a polished, mobile-responsive user experience.



## 🌟 Key Features

* **Bulk Administrative Upload:** Integrated drag-and-drop functionality for uploading entire photoshoots simultaneously via the Django Admin.
* **Modern Viewing Experience:** Powered by **Fancybox**, providing high-performance zooming, full-screen modes, and touch-gestures for mobile users.
* **Fully Responsive Architecture:** Custom-engineered CSS Media Queries ensure a seamless experience across desktops, tablets, and smartphones.
* **Optimized Image Processing:** Backend integration with **Pillow** for automatic image handling and metadata management.
* **Client-Centric Design:** Clean, distraction-free interface focused on visual storytelling.

---

## 🛠️ Tech Stack

* **Backend:** [Django](https://www.djangoproject.com/) (Python Web Framework)
* **Database:** SQLite (Development) / PostgreSQL (Production ready)
* **Image Processing:** [Pillow](https://python-pillow.org/)
* **Frontend Enhancements:** [Fancybox v5](https://fancyapps.com/fancybox/)
* **Admin Extensions:** `django-multiupload-admin`

---

## 🚀 Getting Started

### Prerequisites

* Python 3.10+
* Pip (Python Package Manager)

### Installation

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/your-username/photon-client-gallery.git](https://github.com/your-username/photon-client-gallery.git)
    cd photon-client-gallery
    ```

2.  **Install dependencies:**
    ```bash
    python -m pip install django pillow django-multiupload-admin django-storages
    ```

3.  **Run Migrations:**
    ```bash
    python manage.py migrate
    ```

4.  **Create a Superuser (Admin):**
    ```bash
    python manage.py createsuperuser
    ```

5.  **Start the Development Server:**
    ```bash
    python manage.py runserver
    ```

Visit `http://127.0.0.1:8000/admin` to begin creating galleries and uploading photos.

---

## 📂 Project Structure

```text
├── galleries/
│   ├── static/          # Custom CSS and UI optimization
│   ├── templates/       # Professional HTML5 templates
│   ├── models.py        # Gallery and Photo relational schema
│   ├── admin.py         # Multi-upload configuration
│   └── views.py         # High-level logic for gallery rendering
├── media/               # User-uploaded content (Images)
└── photon_gallery/      # Core project settings
