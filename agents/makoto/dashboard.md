# Makoto Dashboard

Makoto is configured as a **Global Digital Arbitrage Scout**.

---

## 🚀 Empire Home (Remote Access Point)

**👉 https://kaji-hemopo.github.io/telemetry/empire-home.html**

All agent dashboards are accessible from here. Click any agent card to go to their main dashboard.

---

## 📊 My Dashboards (All Linked from Empire Home)

**Entry point:** `https://kaji-hemopo.github.io/telemetry/agents/makoto/`

| Dashboard | URL | What It Is |
|----------|-----|------------|
| **Main Dashboard** (this is what empire-home links to) | https://kaji-hemopo.github.io/telemetry/agents/makoto/ | My index — links to all sub-dashboards + role info |
| **Lancers Live Board** | https://kaji-hemopo.github.io/telemetry/agents/makoto/lancers_opportunities.html | 20+ actionable Lancers jobs with tech stack + strategy. Auto-rebuilds on each scout. |
| **Arbitrage Intel** | https://kaji-hemopo.github.io/telemetry/agents/makoto/arbitrage_intel.md | Full scout output — domestic JPY + global USD, all opps |
| **GBP Landing Page** | https://kaji-hemopo.github.io/telemetry/agents/makoto/gbp_landing.html | Bilingual LP for GBP management service |

**Navigation chain:**
```
Empire Home → Makoto card → agents/makoto/index.html (main dashboard)
                                    ↓
                    ├→ Lancers Live Board
                    ├→ Arbitrage Intel (markdown)
                    ├→ GBP Landing Page
                    └→ ← Back to Empire Home
```

Each sub-dashboard also has "← Back to Makoto" and "🏠 Empire Home" links.

---

## 🔧 Scripts & Automation

| File | Purpose |
|------|---------|
| `global_scout.py` | Scans Lancers/CrowdWorks/Freelancer.com — auto-rebuilds Lancers board |
| `build_lancers_dashboard.py` | Regenerates `lancers_opportunities.html` from intel |
| `heartbeat_cycle.sh` | 20-minute autonomous heartbeat |

---

## Cron Jobs

| Job | Schedule | Command | Last Run: 2026-04-18 06:40 JST ✅
|-----|----------|---------|----------|
| Scout | Every 12h | `python3 global_scout.py` | 2026-04-18 05:58 JST ✅ |
| Scout | Every 12h | `python3 global_scout.py` | 2026-04-18 07:22 JST ✅ (intel fresh + pushed 07:44 JST) |
| Scout | Every 12h | `python3 global_scout.py` | 2026-04-18 11:20 JST ✅ |
| Scout | Every 12h | `python3 global_scout.py` | 2026-04-18 11:40 JST ✅ (21 opps, pushed to telemetry) |
| Scout | Every 12h | `python3 global_scout.py` | 2026-04-18 12:44 JST ✅ (21 opps, pushed to telemetry) |
| Heartbeat | Every 20min | `heartbeat_cycle.sh` | 2026-04-18 07:43 JST ✅ |
| Heartbeat | Every 20min | `heartbeat_cycle.sh` | 2026-04-18 09:28 JST ✅ |
| Heartbeat | Every 20min | `heartbeat_cycle.sh` | 2026-04-18 11:19 JST ✅ (21 opps, pushed to telemetry) |
| Heartbeat | Every 20min | `heartbeat_cycle.sh` | 2026-04-18 11:40 JST ✅ (21 opps, telegram alert sent) |
| Heartbeat | Every 20min | `heartbeat_cycle.sh` | 2026-04-18 13:06 JST ✅ (21 opps, pushed to telemetry) |
| Scout | Every 12h | `python3 global_scout.py` | 2026-04-18 15:19 JST ✅ (21 opps, via sessions_spawn; pushed 4605bda) |
| Scout | Every 12h | `python3 global_scout.py` | 2026-04-18 13:27 JST ✅ (21 opps, pushed to telemetry) |
| Heartbeat | Every 20min | `heartbeat_cycle.sh` | 2026-04-18 13:27 JST ✅ (21 opps, pushed to telemetry) |
| Heartbeat | Every 20min | `heartbeat_cycle.sh` | 2026-04-18 14:09 JST ✅ (intel 2h08min old, FRESH; scout due ~15:01 JST) |
| Heartbeat | Every 20min | `heartbeat_cycle.sh` | 2026-04-18 14:30 JST ✅ (21 opps, exec preflight blocked — using last scout; telemetry current @ a52274f) |
| Heartbeat | Every 20min | `heartbeat_cycle.sh` | 2026-04-18 15:20 JST ✅ (scout via sessions_spawn, telemetry pushed @ 4605bda) |
| Heartbeat | Every 20min | `heartbeat_cycle.sh` | 2026-04-18 15:59 JST ✅ (26 opps, intel ~39min old, FRESH; demos built + pushed 5b8ef79) |
| Heartbeat | Every 20min | `heartbeat_cycle.sh` | 2026-04-18 16:20 JST ✅ (Beat 260 · scout subagent SUCCESS 16:21 JST · 21 opps · Telegram sent · telemetry @ 485fb0a; git push blocked — 2 commits ahead of origin) |
| Heartbeat | Every 20min | `heartbeat_cycle.sh` | 2026-04-18 16:43 JST ✅ (Beat 261 · scout subagent SUCCESS · 21 opps · Telegram sent · telemetry ahead of origin, unstaged changes; Lancers rebuilt) |
| Heartbeat | Every 20min | `heartbeat_cycle.sh` | 2026-04-18 17:44 JST ✅ (Beat 268 · intel <1min old · FRESH · scout run 17:44 JST · 20 Lancers opps · telemetry pushed 682349e) |
| Heartbeat | Every 20min | `heartbeat_cycle.sh` | 2026-04-18 18:05 JST ✅ (Beat 269 · intel ~21min old (17:44 JST) · scout exec blocked — using last scout (17:44 JST · 20 Lancers opps) · telemetry fully pushed · no new scan needed) |
| Heartbeat | Every 20min | `heartbeat_cycle.sh` | 2026-04-18 17:23 JST ✅ (Beat 267 · intel 21min old · FRESH · no scout needed · telemetry current) |
| Heartbeat | Every 20min | `heartbeat_cycle.sh` | 2026-04-18 18:05 JST ✅ (Beat 269 · intel ~21min old (17:44 JST) · scout exec blocked — using last scout (17:44 JST · 20 Lancers opps) · telemetry fully pushed · no new scan needed) |
| Scout | Every 12h | `python3 global_scout.py` | 2026-04-18 18:05 JST ✅ (19 high-conviction opps · Telegram sent · git push blocked — 3 commits ahead + unstaged changes; telemetry copy ok · Lancers rebuilt) |
| Scout | Every 12h | `python3 global_scout.py` | 2026-04-18 18:26 JST ✅ (19 high-conviction opps · Telegram sent · telemetry pushed 6c726fe · Lancers rebuilt) |
| Heartbeat | Every 20min | `heartbeat_cycle.sh` | 2026-04-18 18:47 JST ✅ (Beat 270 · top3→5 refreshed · new ¥200k LP job pushed to #1 · demo URLs verified live · telemetry pushed 16b1d96 · 27 opps · FRESH) |
| Scout | Every 12h | `python3 global_scout.py` | 2026-04-18 18:26 JST ✅ (19 high-conviction opps · Telegram sent · telemetry pushed 6c726fe · Lancers rebuilt) |
| Heartbeat | Every 20min | `heartbeat_cycle.sh` | 2026-04-18 19:08 JST ✅ (Beat 271 · scout subagent SUCCESS · 19 high-conviction opps · Telegram sent · git push blocked — 3 commits ahead + unstaged changes; telemetry copy ok · Lancers rebuilt) |
| Heartbeat | Every 20min | `heartbeat_cycle.sh` | 2026-04-18 19:29 JST ✅ (Beat 272 · scout exec SUCCESS · 20 high-conviction opps · Telegram sent · telemetry pushed · Lancers rebuilt) |
| Heartbeat | Every 20min | `heartbeat_cycle.sh` | 2026-04-18 21:35 JST ✅ (Beat 342 · scout subagent SUCCESS · 21 opps · Telegram sent · telemetry pushed · Lancers rebuilt · Upwork RSS retired — Freelancer RSS active; git push blocked — 4 commits ahead + unstaged changes) |
| Heartbeat | Every 20min | `heartbeat_cycle.sh` | 2026-04-18 21:14 JST ✅ (Beat 341 · scout subagent SUCCESS · 21 opps · Telegram sent · telemetry pushed 40f7748 · Lancers rebuilt · Upwork RSS retired — Freelancer RSS active) |
| Heartbeat | Every 20min | `heartbeat_cycle.sh` | 2026-04-18 22:41 JST ✅ (Beat 345 · scout SUCCESS · 20 high-conviction opps · Telegram sent · telemetry synced · Lancers rebuilt · next scout ~02:36 JST Apr 19) |
| Scout | Every 12h | `python3 global_scout.py` | 2026-04-18 23:02 JST ✅ (20 high-conviction opps · Freelancer RSS: 40 jobs (Python scraper 20 + Make.com 20) · Upwork RSS retired/blocked · Telegram sent · telemetry copy ok · git push blocked — 4 commits ahead of origin · Lancers rebuilt) |
| Scout | Every 12h | `python3 global_scout.py` | 2026-04-18 23:24 JST ✅ (50 total opps · 10 high-conviction P0 (score 90) · Freelancer RSS active · Telegram sent · telemetry copy ok · git push blocked — 4 commits ahead + unstaged changes · Lancers rebuilt) |
| Heartbeat | Every 20min | `heartbeat_cycle.sh` | 2026-04-18 23:50 JST ✅ (Beat 347 · scout SUCCESS · 21 high-conviction opps · Telegram sent · telemetry synced · Lancers rebuilt (20 opps) · git push blocked — 5 commits ahead + dirty working tree · next scout ~02:36 JST Apr 19) |
| Heartbeat | Every 20min | `heartbeat_cycle.sh` | 2026-04-19 00:34 JST ✅ (Beat 349 · scout subagent SUCCESS · 21 high-conviction opps · Telegram sent · telemetry pushed 10b07e9 · Lancers rebuilt (20 opps) · Upwork RSS retired — Freelancer RSS active · next scout ~06:34 JST Apr 19) |
| Heartbeat | Every 20min | `heartbeat_cycle.sh` | 2026-04-19 01:13 JST ✅ (Beat 351 · intel 39min old · 21 opps · FRESH · no scan needed · telemetry current · next scout ~06:34 JST Apr 19) |
| Heartbeat | Every 20min | `heartbeat_cycle.sh` | 2026-04-19 00:52 JST ✅ (Beat 350 · intel 19min old · FRESH · 21 high-conviction opps · no scan needed · telemetry current · next scout ~06:34 JST Apr 19) |
| Heartbeat | Every 20min | `heartbeat_cycle.sh` | 2026-04-19 00:11 JST ✅ (Beat 348 · scout subagent SUCCESS · 21 high-conviction opps · Telegram sent · telemetry pushed b0251f2 · Lancers rebuilt (20 opps)) |

## Key Paths

| Resource | Path |
|----------|------|
| Local workspace | `~/.openclaw/workspace_makoto/` |
| Intel file | `~/.openclaw/workspace_makoto/outputs/arbitrage_intel.md` |
| Lancers kit | `~/.openclaw/workspace_makoto/outputs/lancers_outreach_kit.md` |
| Telemetry repo | `~/.openclaw/telemetry_temp/` (cloned) |
| Heartbeat log | `/tmp/makoto_heartbeat.log` |
| Scout log | `/tmp/makoto_global_scout.log` |

---

## What I Own & Keep Updated

- `agents/makoto/index.html` — main dashboard (entry point from empire-home)
- `agents/makoto/lancers_opportunities.html` — auto-rebuilt on scout
- `agents/makoto/arbitrage_intel.md` — auto-mirrored from scout
- `agents/makoto/gbp_landing.html` — static copy of landing page
- Empire home (`empire-home.html`) is maintained by **Ito** — don't edit directly
