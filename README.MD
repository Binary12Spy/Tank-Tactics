# TankTactics

---

### Install

Create and fill in .env file or supply environmnet vairables directly

```
python -m venv .venv
.\.venv\Scripts\activate.bat
pip install -r requirements.txt
```

### Run

```
python server.py
```

---

### Todo

#### API
- [x] Authentication REST endpoints
- [x] Account management REST endpoints
- [x] Game management REST endpoints
- [ ] Game websocket interface

#### UI
- [x] Authentication webpage
- [ ] Account management webpage
- [ ] Game management webpage

#### Phaser
- [ ] Websocket connection
- [ ] Display game background
- [ ] Display players
- [ ] Player interaction
- [ ] Handle game updates
- [ ] Animations (?)

#### Game rules engine
- [ ] Action validation
- [ ] Client notification