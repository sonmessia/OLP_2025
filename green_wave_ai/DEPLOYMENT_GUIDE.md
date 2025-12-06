# 🚀 Deployment Guide - Run Anywhere

This guide helps you deploy the Smart Traffic Control System on **any machine** with Docker.

---

## 📋 Prerequisites

### Required Software:
- **Docker** (version 20.10+)
- **Docker Compose** (version 2.0+)
- **Git**

### For machines with display (GUI):
- X11 server (Linux) or XQuartz (macOS) or VcXsrv (Windows)

---

## 🛠️ Quick Start (Any Machine)

### 1️⃣ Clone Repository
```bash
git clone https://github.com/sonmessia/OLP_2025.git
cd OLP_2025
git checkout feat/sumo-rl
```

### 2️⃣ Configure Environment
```bash
# Copy environment template
cp .env.example .env

# Edit .env file (optional, defaults work for most cases)
nano .env
```

**Default `.env` values:**
```env
# Database
# Database (CrateDB uses defaults: http://localhost:4200)
# No authentication by default in this dev setup

# SUMO Configuration
SUMO_SCENARIO=Nga4ThuDuc  # Options: Nga4ThuDuc, NguyenThaiSon, QuangTrung
DISPLAY=:0  # For GUI on Linux

# Backend
BACKEND_URL=http://backend:8000
ORION_URL=http://orion:1026
```

### 3️⃣ Start All Services
```bash
# Build and start all containers
docker-compose up -d --build

# View logs
docker-compose logs -f
```

### 4️⃣ Access Dashboard
Open browser: **http://localhost:3001/demo-dashboard.html**

---

## 🖥️ Platform-Specific Setup

### 🐧 Linux

**Everything works out-of-the-box!**

```bash
# Allow Docker to access X11 (for SUMO GUI)
xhost +local:docker

# Start services
docker-compose up -d
```

**To disable GUI (headless mode):**
```bash
# Edit docker-compose.yaml, remove --gui flag
# Or set environment variable:
SUMO_GUI=false docker-compose up -d
```

---

### 🍎 macOS

**Install XQuartz for GUI support:**

```bash
# 1. Install XQuartz
brew install --cask xquartz

# 2. Start XQuartz
open -a XQuartz

# 3. In XQuartz preferences:
#    - Go to "Security" tab
#    - Enable "Allow connections from network clients"

# 4. Get your IP address
IP=$(ifconfig en0 | grep inet | awk '$1=="inet" {print $2}')

# 5. Allow connections
xhost + $IP

# 6. Update .env file
echo "DISPLAY=$IP:0" >> .env

# 7. Start services
docker-compose up -d
```

---

### 🪟 Windows

**Option 1: WSL2 (Recommended)**

```bash
# 1. Install WSL2 with Ubuntu
wsl --install

# 2. Inside WSL2, follow Linux instructions
# 3. Install Docker Desktop with WSL2 backend
```

**Option 2: VcXsrv for GUI**

```powershell
# 1. Download and install VcXsrv
# https://sourceforge.net/projects/vcxsrv/

# 2. Start XLaunch with settings:
#    - Multiple windows
#    - Display number: 0
#    - Disable access control

# 3. Get Windows host IP
ipconfig

# 4. Update .env
DISPLAY=<YOUR_WINDOWS_IP>:0.0

# 5. Start services
docker-compose up -d
```

---

## 🎛️ Service Management

### Start/Stop Services
```bash
# Start all services
docker-compose up -d

# Stop all services
docker-compose down

# Restart specific service
docker-compose restart backend

# View logs
docker-compose logs -f sumo-simulation
```

### Change SUMO Scenario
```bash
# Method 1: Edit .env file
echo "SUMO_SCENARIO=NguyenThaiSon" >> .env
docker-compose up -d sumo-simulation

# Method 2: Environment variable
SUMO_SCENARIO=QuangTrung docker-compose up -d
```

### Switch Between GUI and Headless Mode

**Edit `docker-compose.yaml`:**

```yaml
# For GUI mode:
command: >
  bash -c "
    python3 /app/sumo_rl/agents/iot_agent.py --scenario ${SUMO_SCENARIO} --gui
  "

# For headless mode (no GUI, faster):
command: >
  bash -c "
    python3 /app/sumo_rl/agents/iot_agent.py --scenario ${SUMO_SCENARIO}
  "
```

---

## 🔧 Troubleshooting

### Issue 1: SUMO GUI doesn't appear

**Solution for Linux:**
```bash
xhost +local:docker
docker-compose restart sumo-simulation
```

**Solution for macOS:**
```bash
# Check XQuartz is running
ps aux | grep XQuartz

# Restart XQuartz
killall XQuartz
open -a XQuartz
xhost + $(ifconfig en0 | grep inet | awk '$1=="inet" {print $2}')
```

**Solution for Windows:**
```powershell
# Restart VcXsrv
# Make sure firewall allows connections
```

### Issue 2: Port already in use

```bash
# Check what's using the port
sudo lsof -i :8000  # Backend
sudo lsof -i :1026  # Orion
sudo lsof -i :8813  # SUMO

# Stop conflicting process or change port in docker-compose.yaml
```

### Issue 3: Database connection errors

```bash
# Reset databases
docker-compose down -v
docker-compose up -d
```

### Issue 4: SUMO TraCI connection timeout

```bash
# Check SUMO container logs
docker-compose logs sumo-simulation

# Restart SUMO container
docker-compose restart sumo-simulation

# Verify network connectivity
docker-compose exec backend ping sumo
```

---

## 🌐 Remote Server Deployment (No GUI)

For deployment on cloud servers (AWS, GCP, Azure) without GUI:

### 1️⃣ Update docker-compose.yaml

```yaml
# Comment out GUI-related volumes and DISPLAY
sumo-simulation:
  # ... other config ...
  # environment:
  #   DISPLAY: ${DISPLAY}  # ← Comment this out
  # volumes:
  #   - /tmp/.X11-unix:/tmp/.X11-unix:rw  # ← Comment this out
  command: >
    bash -c "
      python3 /app/sumo_rl/agents/iot_agent.py --scenario ${SUMO_SCENARIO}
    "
    # Remove --gui flag ↑
```

### 2️⃣ Deploy

```bash
# On remote server
git clone https://github.com/sonmessia/OLP_2025.git
cd OLP_2025
cp .env.example .env

# Start in headless mode
docker-compose up -d

# Monitor via dashboard
# Access via: http://<SERVER_IP>:3001/demo-dashboard.html
```

### 3️⃣ Set up Reverse Proxy (Optional)

**Nginx configuration:**
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:3001;
    }

    location /api/ {
        proxy_pass http://localhost:8000;
    }
}
```

---

## 📊 Health Checks

### Verify All Services Running
```bash
docker-compose ps

# Expected output:
# NAME                STATUS
# backend             Up
# fiware-orionld      Up (healthy)
# mongo-db            Up
# cratedb             Up (healthy)
# quantumleap         Up (healthy)
# sumo-simulation     Up
```

### API Health Check
```bash
# Backend API
curl http://localhost:8000/health

# Orion Context Broker
curl http://localhost:1026/version

# SUMO connection status
curl http://localhost:8000/sumo/status
```

---

## 🎯 Production Checklist

- [ ] Update `.env` with secure passwords
- [ ] Configure firewall rules
- [ ] Set up SSL/TLS certificates
- [ ] Enable Docker logging
- [ ] Configure automated backups for databases
- [ ] Set up monitoring (Prometheus + Grafana)
- [ ] Configure restart policies (`restart: always`)
- [ ] Set resource limits in docker-compose.yaml
- [ ] Use Docker secrets for sensitive data
- [ ] Set up CI/CD pipeline

---

## 📦 Build & Push Docker Images (CI/CD)

### Build Images Manually
```bash
# Backend
docker build -t your-registry/traffic-backend:latest ./src/backend

# SUMO Simulation
docker build -f ./src/backend/Dockerfile.sumo -t your-registry/traffic-sumo:latest ./src/backend

# Push to registry
docker push your-registry/traffic-backend:latest
docker push your-registry/traffic-sumo:latest
```

### Update docker-compose.yaml to use registry images
```yaml
backend:
  image: your-registry/traffic-backend:latest
  # build: ./src/backend  # ← Comment out

sumo-simulation:
  image: your-registry/traffic-sumo:latest
  # build: ...  # ← Comment out
```

---

## 🔐 Security Best Practices

1. **Use environment variables for secrets**
   ```bash
   # Don't commit .env file
   echo ".env" >> .gitignore
   ```

2. **Update default passwords**
   # Secure CrateDB if needed (refer to CrateDB docs)
   # CRATE_HOST=...

3. **Restrict network access**
   ```yaml
   networks:
     fiware_default:
       driver: bridge
       internal: true  # ← Prevent external access
   ```

4. **Use read-only volumes where possible**
   ```yaml
   volumes:
     - ./src/backend/app/sumo_rl/sumo_files:/app/sumo_files:ro
   ```

---

## 📚 Additional Resources

- [SUMO Documentation](https://sumo.dlr.de/docs/)
- [FIWARE Orion-LD](https://github.com/FIWARE/context.Orion-LD)
- [Docker Compose Reference](https://docs.docker.com/compose/)
- [Project README](./README.md)
- [AI Traffic Control Guide](./AI_TRAFFIC_CONTROL_GUIDE.md)

---

## 🆘 Support

If you encounter issues:
1. Check logs: `docker-compose logs -f`
2. Verify environment: `docker-compose config`
3. Open issue on GitHub: https://github.com/sonmessia/OLP_2025/issues

---

**🎉 Happy Deploying!**
