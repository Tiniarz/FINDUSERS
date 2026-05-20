# FINDUSERS.py

![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)
![License](https://img.shields.io/badge/license-GPL%20v3-green.svg)
![Platform Count](https://img.shields.io/badge/platforms-140%20scanned-red.svg)

An asynchronous, high-speed OSINT command-line engine built to map and locate target usernames across 140 different websites and social networks simultaneously.

---

## Features

* **High-Concurrency Scanning:** Leverages asynchronous `asyncio` semaphores to scan 140 target networks rapidly without hitting local socket limitations.
* **Resilient Network Layer:** Intercepts drops, structural connection timeouts, and connection refusals to seamlessly switch to the next asset rather than throwing fatal script crashes.
* **Dynamic Color Tracking:** Utilizes automated ANSI visualization mappings via `colorama` to organize positive matches, empty hooks, and connection anomalies directly inside the terminal interface.

---

## Installation

```bash
git clone [https://github.com/yourusername/findusers.git](https://github.com/yourusername/findusers.git)
cd findusers
pip install -r requirements.txt


Initiate the terminal engine with the following control pattern:
python FINDUSERS.py
License
This architecture is completely open-source and structured under the GPL v3 License. Check out the LICENSE database files for foundational details.
