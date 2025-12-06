# 🔄 How to Switch SUMO Scenarios

## Quick Steps

### 1. Stop Current Scenario
```bash
# Kill SUMO process
lsof -ti :8813 | xargs kill -9 2>/dev/null

# Restart backend to clear TraCI connection
docker restart backend
sleep 5
```

### 2. Start New Scenario

#### For Nga4ThuDuc:
```bash
python3 scripts/auto_start_sumo.py Nga4ThuDuc
```

#### For NguyenThaiSon:
```bash
python3 scripts/auto_start_sumo.py NguyenThaiSon
```

#### For QuangTrung:
```bash
python3 scripts/auto_start_sumo.py QuangTrung
```

### 3. Connect from Dashboard
1. Open dashboard: http://localhost:3001/demo-dashboard.html
2. Select scenario from dropdown (MUST match SUMO running)
3. Click **"Start SUMO"** button
4. Wait for "Connected ✓" status
5. Click **"Start Simulation"**

## One-Line Switch Commands

### Switch to Nga4ThuDuc:
```bash
lsof -ti :8813 | xargs kill -9 2>/dev/null && \
docker restart backend && sleep 5 && \
python3 scripts/auto_start_sumo.py Nga4ThuDuc &
```

### Switch to NguyenThaiSon:
```bash
lsof -ti :8813 | xargs kill -9 2>/dev/null && \
docker restart backend && sleep 5 && \
python3 scripts/auto_start_sumo.py NguyenThaiSon &
```

### Switch to QuangTrung:
```bash
lsof -ti :8813 | xargs kill -9 2>/dev/null && \
docker restart backend && sleep 5 && \
python3 scripts/auto_start_sumo.py QuangTrung &
```

## Troubleshooting

**Dashboard shows "Failed to connect":**
- Verify SUMO is running: `lsof -i :8813`
- Check backend status: `curl http://localhost:8000/sumo/status`
- Ensure scenario dropdown matches SUMO running

**Port 8813 already in use:**
```bash
lsof -ti :8813 | xargs kill -9
```

**Backend shows "Connection 'default' is already active":**
```bash
docker restart backend
```

**SUMO exits immediately:**
- Check if scenario has vehicles (trips.xml, routes.rou.xml)
- View SUMO log: `cat /tmp/sumo_*.log`

## Why Backend Restart is Needed?

TraCI maintains a persistent connection labeled "default". When you switch scenarios, the old connection must be closed before creating a new one. Currently, the easiest way is to restart the backend container, which clears all TraCI connections.

## Future Improvement

We can add a `/sumo/restart` endpoint that:
1. Closes existing TraCI connection
2. Clears internal state
3. Ready for new connection

This would eliminate the need for manual backend restart.
