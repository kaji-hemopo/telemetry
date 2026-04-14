# DASHBOARD QUICK REFERENCE
**For Saito's Memory - Updated: 2026-03-28**

## 🎯 CRITICAL TO REMEMBER

### **Centralized Telemetry System:**
```
📍 TRUE SOURCE DIRECTORY:
Primary: /Users/jacksonhemopo/.openclaw/workspace_saito/dashboard/dashboard
Symlink: /Users/jacksonhemopo/.openclaw/telemetry-repo → points to above

🌐 LIVE URL:
https://kaji-hemopo.github.io/telemetry/agents/saito/

📁 MY DIRECTORY:
/Users/jacksonhemopo/.openclaw/telemetry-repo/agents/saito/
```

### **🧱 NEW STRUCTURE (MANDATORY):**
```
telemetry-repo/
├── agents/ ← Each agent gets their own subdirectory
│   ├── makoto/ # Makoto's trading dashboards
│   ├── saito/  # Saito's development dashboards ← MY DIRECTORY
│   ├── ito/    # Ito's intelligence dashboards
│   ├── kaji/   # Kaji's coordination dashboards
│   └── jackson/ # Jackson's empire overview
├── [legacy root dashboards] # Existing ones stay
└── shared/ # Common resources
```

## 📜 GIT WORKFLOW (NON‑NEGOTIABLE)

### **Before Editing:**
```bash
cd /Users/jacksonhemopo/.openclaw/telemetry-repo
git pull origin main
```

### **While Editing:**
```bash
cd agents/saito/  # ONLY edit in my directory
# Edit my files
```

### **After Editing:**
```bash
cd /Users/jacksonhemopo/.openclaw/telemetry-repo
git add agents/saito/
git commit -m "[Saito] Brief description"
git push origin main
```

## 🚨 CRITICAL RULES (EMPHASIZE)

1. **ALWAYS pull before editing** – Prevents 99% of conflicts
2. **ONLY edit in my agent directory** – No touching others' files
3. **Commit with agent prefix** – `[Saito] ...`
4. **Test locally first** – `python3 -m http.server 8000`
5. **If conflict:** `git stash`, `git pull`, `git stash pop`, resolve

## 🌐 LIVE RIGHT NOW

- **My Dashboard:** https://kaji-hemopo.github.io/telemetry/agents/saito/
- **Empire Dashboard:** https://kaji-hemopo.github.io/telemetry/
- **Agent Directory:** https://kaji-hemopo.github.io/telemetry/agents/

## 🔧 FIRST‑TIME SETUP (ALREADY DONE)

```bash
# 1. Navigate to central repo
cd /Users/jacksonhemopo/.openclaw/telemetry-repo

# 2. Run setup script (already done)
./setup_agent_workspace.sh

# 3. Created:
#    - Symlink in workspace: workspace_saito/telemetry-repo
#    - Agent directory: agents/saito/
#    - Basic index.html dashboard
```

## 📊 MY DASHBOARD STRUCTURE

### **Main Pages:**
1. **index.html** - Main dashboard with urgent decisions
2. **decisions.html** - Complete decision protocol interface
3. **airbnb.html** - Airbnb project details & financial analysis
4. **README.md** - Documentation

### **Decision Protocol:**
```
1. 🚨 Issue identified (with impact analysis)
2. 🔢 Options presented (1, 2, 3 with clear descriptions)
3. 📱 Request: "Reply in Telegram with: 1, 2, or 3"
4. ✅ Immediate execution upon decision
```

## 💡 WHY THIS MATTERS

### **Jackson's Requirements:**
1. **"See your work when I am remote"** → Live dashboard accessible anywhere
2. **"No more dashboard problems"** → Centralized structure with proper git
3. **"Clear decisions"** → Numbered options, simple Telegram replies
4. **"No message overload"** → Details in dashboard, just decision needed

### **Problem Solved:**
- GitHub authentication issues fixed
- Git divergence resolved (72 commits synced)
- Central structure created
- Standard protocol established

## 🎯 IMMEDIATE USE

### **To Show Jackson My Work:**
1. **Update dashboard** with current status
2. **Push changes** using git workflow
3. **Share URL:** https://kaji-hemopo.github.io/telemetry/agents/saito/
4. **Request decision** via Telegram if needed

### **When Jackson Asks to See Something:**
1. **Add it to dashboard** in appropriate section
2. **Commit and push** immediately
3. **Share live URL** for viewing
4. **No need for screenshots** or long explanations

## ⚠️ COMMON PITFALLS TO AVOID

1. **Editing without pulling** → Causes conflicts
2. **Editing outside my directory** → Breaks structure
3. **Forgetting agent prefix** → Confuses commit history
4. **Not testing locally** → Might break live site
5. **Complex messages** → Use dashboard for details, Telegram for decisions

## ✅ SUCCESS METRICS

- **Dashboard always current** when Jackson checks
- **Decisions clear and simple** (1, 2, or 3)
- **No git conflicts** (always pull first)
- **Mobile-friendly** (Jackson views on phone)
- **Fast updates** (git push works reliably)

---

**MEMORIZE THIS:** 
- **My directory:** `agents/saito/` in telemetry-repo
- **Live URL:** https://kaji-hemopo.github.io/telemetry/agents/saito/
- **Git command:** `git pull` ALWAYS before editing
- **Decision format:** "Reply in Telegram with: 1, 2, or 3"

**This system ensures Jackson can always see my work when remote.**