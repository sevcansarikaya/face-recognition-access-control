# face-recognition-access-control


# Project Overview

This project is a Computer Engineering graduation thesis focused on developing a **real-time face recognition** desktop application to control authorized access to a physical area (room/lab). The system is designed to grant entry only to registered and authorized personnel, while simultaneously providing high security by instantly detecting and logging unauthorized entry attempts.

#Key Features

* **Live Face Verification:** Real-time image acquisition via webcam for high-precision identity verification.
* **Centralized Data Management:** Secure storage of authorized users' face encodings and personal data in a local database (SQLite).
* **Administrative Panel (GUI):** A professional desktop interface (PyQt5), protected by username and password, offering capabilities to add, delete authorized personnel, and view entry logs.
* **Security and Logging:** Instant visual/audible alarm trigger upon detection of an unknown face, with persistent logging of the captured image and the event's timestamp.
* **Role-Based Access:** User registration functionality restricted solely to operators with `Admin` privileges.
