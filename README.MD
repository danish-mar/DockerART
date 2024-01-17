🌈 **Flask-Docker-Management Kawaii Dashboard** 🌈

This repository is a super cute Flask web application designed for managing Docker containers and providing system information 🎀✨

### Features: 🚀

1. **Dashboard:**
   - Accessible at the root (`/`) and `/docker`.
   - Provides a delightful and informative user interface 💖

2. **Docker Information:**
   - `/api/docker-info` endpoint delivers essential Docker details:
     - Running containers count 🏃‍♂️
     - Current installed images 🖼️
     - Total containers 📦

3. **Server Information:**
   - `/api/server-info` endpoint offers real-time server information:
     - CPU usage 💻
     - RAM usage 🧠

4. **Docker Container Management:**
   - `/api/docker-manage/list` endpoint lists all Docker containers. 📋
   - `/api/docker-manage/startcontainer` starts a specified container. 🚀
   - `/api/docker-manage/stopcontainer` stops a specified container. ⛔
   - `/api/docker-manage/createcontainer` creates a new Docker container. 🌈
   - `/api/docker-manage/deletecontainer` deletes a specified Docker container. 🗑️
   - `/api/docker-manage/createNetwork` creates a Docker network. 🌐
   - `/api/docker-manage/searchImage` searches Docker Hub for images. 🔍
   - `/api/docker-manage/pullImage` pulls a Docker image. 🚚
   - `/api/docker-manage/installedImages/list` lists installed Docker images. 📸
   - `/api/docker-manage/network/getNetworks` lists Docker networks. 🌐

5. **Miscellaneous:**
   - `/api/misc/random-name` endpoint generates a random kawaii name. 💕

### Dependencies: 🛠️
- Flask: Lightweight web framework.
- Docker-Py: Python API for Docker.
- Psutil: Cross-platform library for system monitoring.
- Requests: HTTP library for sending requests.

### How to Run: 🚀
1. Clone the repository. 🌍
2. Install dependencies: `pip install -r requirements.txt` 🛠️
3. Run the Flask app: `python app.py` 🚀

Feel free to explore, contribute

### Contributors:

- Keqing (Denizuh)
