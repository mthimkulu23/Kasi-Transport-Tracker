# Kasi Transport Tracker 🚐

## 📋 Project Overview

The **Kasi Transport Tracker** is a Python + PostgreSQL mini-project designed to help South African township taxi associations manage their operations digitally. The system tracks **drivers**, **routes**, and **trips**, and generates **daily reports** for better financial transparency.

---

## ⚙️ Features

* 🧍‍♂️ **Add Driver** – Register a driver with a name, password, and taxi number.
* 🛣️ **Add Route** – Record taxi routes with origin, destination, and fare.
* 🧾 **Record Trip** – Log daily trips, including number of passengers and total fare collected.
* 📊 **Daily Report** – View each driver’s total earnings for the current day and export the results to a CSV file.

---

## 🧠 Technologies Used

* **Python** – Backend logic
* **PostgreSQL** – Database management
* **Psycopg2** – PostgreSQL database adapter for Python
* **CSV Module** – Report export functionality
* **Git** – Version control

---



## 💻 How to Run the Project

1. Clone the repository:

   ```bash
   git clone https://github.com/mthimkulu23/Kasi-Transport-Tracker
   ```
2. Navigate to the project directory:

   ```bash
   cd Kasi-Transport-Tracker
   ```
3. Run the main program:

   ```bash
   python transport_app.py
   ```

---

## 🏁 Recent Updates

* Added emojis to the main menu for better UX.
* Fixed SQL insert errors in `record_trip`.
* Enhanced **daily_report()** to include driver names, taxi numbers, and route details.
* Implemented CSV export for daily reports.

---

## 👨‍💻 Contributors

* **Thabang Mthimkulu** – Data Science || Developer || & Cybersecurity Analyst Intern

---

## 📅 Future Enhancements

* Add admin authentication.
* Generate weekly and monthly reports.
* Include a graphical dashboard.
* Integrate with a web-based version using Flask.

---

> 🚀 *Digitizing township transport operations, one trip at a time!*
