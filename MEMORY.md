# MEMORY.md — Saito / Ito
### Beat #22 (06:38 JST) — Pipeline Healthy. Niches #41-42 Delivered
- infra_pulse: OK:9 WARN:1 FAIL:0 ✅
- Niches #41-42: GitHub Actions Runner Pool Saturation Forecaster + Zapier/Make Workflow Execution Latency Regression Detector

**Last Heartbeat:** 2026-04-28 06:38 JST — Beat #22
**Status:** ACTIVE — Hunter-Killer heartbeat running

---

## 📊 PIPELINE HEALTH
- **Workspace:** ito (~/workspace_ito) — minimal, healthy
- **infra_pulse.py:** ✅ FIXED — direct `python3 path/to/infra_pulse.py` (cron exec() caused `__file__` NameError)
- **infra_pulse location:** `/Users/jacksonhemopo/.openclaw/workspace_ito/intel/Telemetry/infra_pulse.py`
- **heartbeat_logs dir:** `/Users/jacksonhemopo/.openclaw/workspace_ito/heartbeat_logs/` (script writes to `~/workspace_ito/heartbeat_logs/infra_pulse_log.md`)
- **Cron:** b59d1431-e95f-4d6a-a6c3-c8850a96f793 · fires at :10 and :50 every hour
- **heartbeat_logs:** Active — direct python3 call now working ✅
- **Dashboard:** https://kaji-hemropo.github.io/telemetry/agents/saito/ (read-only)

---

## 🎯 ACTIVE MISSION
Per IDENTITY.md — Hunter-Killer mandate: identify **2 micro-SaaS niches per heartbeat**

---


## 🏹 NICHE #11: Terraform State File Corruption Early Warning System
**B2B Problem:** DevOps teams managing 20-200+ Terraform workspaces face state file drift, lock contention, and backend corruption (S3 versioned or not). When state goes out of sync with actual infrastructure, `terraform apply` destroys resources silently or fails catastrophically. No early detection — teams find out during incidents.

**Target Market:** Mid-large cloud-native companies with heavy Terraform adoption (eks/gke + multi-account AWS)

**Technical Architecture:**
- Go collector via Terraform Cloud/Enterprise API + direct backend polling (S3/GCS/Azure Blob)
- State diff engine: compares last known state hash vs current, detects drifted/missing resources
- Lock watchdog: alerts on stuck locks >30 min (auto-unlock risk)
- PostgreSQL, Docker, Slack alerts with workspace priority + estimated blast radius
- Dashboard: workspace health score, state drift timeline, lock status overview

**Why >$10k/mo:** 20 companies × $500-1500/mo. Prevents $50k-$500k in misconfigured infrastructure incidents.
**Capex:** ~$15k. Infra: ~$120/mo. **Effort:** <4 hrs/week.
**Competitors:** Terraform Cloud/Enterprise shows state but doesn't predict drift or correlate with actual infra.

---


## 🏹 NICHE #12: GitHub Actions Workflow Duration Regression Detector
**B2B Problem:** Engineering teams with 50-500+ GitHub Actions workflows get surprised by CI/CD regressions — a PR quietly adds 10 min to a critical path pipeline, blocking merges and inflating costs. No baseline tracking, no regression alerts, no root cause.
**Target Market:** Scale-up SaaS with complex CI/CD stacks (monorepo or polyrepo, 20+ engineers)

**Technical Architecture:**
- Go collector via GitHub Actions API + workflow run history scraping
- Duration regression engine: p50/p95 trend analysis, anomaly detection (>2σ vs 30-day baseline)
- Path impact analyzer: which workflow steps are the bottleneck, correlate with file changes
- PostgreSQL, Docker, Slack alerts with PR author + estimated cost impact
- Dashboard: workflow health scores, regression history, CI cost trends

**Why >$10k/mo:** 25 companies × $400-1000/mo. Saves 20-60 min/day per engineer on CI debugging.
**Capex:** ~$12k. Infra: ~$100/mo. **Effort:** <4 hrs/week.
**Competitors:** GitHub Actions metrics are raw — no regression detection or alerting built in.

---

**Why >$10k/mo:** 20 companies × $500-1500/mo. Prevents $100k+ incident costs.
**Capex:** ~$20k. Infra: ~$180/mo. **Effort:** <5 hrs/week.
**Competitors:** Datadog/Grafana show metrics but don't predict API latency cascades.

---

## 🏹 NICHE #8: Cross-Cloud Egress Spend Allocation Analyzer
**B2B Problem:** Finance teams at companies with workloads spanning AWS + GCP + Azure get blinded by total egress bills ($30k-$200k/mo). No per-team, per-service, or per-environment breakdown. Networking teams can't optimize without attribution data.

**Target Market:** Mid-market cloud-native companies ($5M-$50M ARR) with multi-cloud infrastructure

**Technical Architecture:**
- Go collector polling AWS/GCP/Azure billing APIs + CloudWatch/Custom metrics
- Cost allocation engine mapping egress to tags (team, service, env, project)
- PostgreSQL, scheduled job (daily), React dashboard with drill-down
- Anomaly detection: unexpected egress spikes by tag + estimated waste
- Slack alerts for budget threshold breaches

**Why >$10k/mo:** 25 companies × $400-1200/mo. Saves $20k-$100k/mo in wasted egress.
**Capex:** ~$15k. Infra: ~$120/mo. **Effort:** <4 hrs/week.
**Competitors:** CloudHealth/Densify — cost optimization, not egress attribution.

---

**Why >$10k/mo:** 25 companies × $400-1200/mo. Saves $20k-$100k/mo in wasted egress.
**Capex:** ~$15k. Infra: ~$120/mo. **Effort:** <4 hrs/week.
**Competitors:** CloudHealth/Densify — cost optimization, not egress attribution.

---

## 🏹 NICHE #9: Kubernetes API Response Time Anomaly Predictor
**B2B Problem:** SRE teams managing 50-500-node Kubernetes clusters get surprised by API server latency spikes that cascade into pod scheduling failures, ingress timeouts, and full-cluster instability. Reactive — not predictive.

**Target Market:** Mid-large SaaS with mission-critical Kubernetes clusters (eks/gke/openshift)

**Technical Architecture:**
- Go collector scraping kube-apiserver metrics via kube-state-metrics + Prometheus
- Time-series anomaly detection (>2σ in p95 latency, error rate, watch latency)
- Predictor: correlate with pending pod queue depth, etcd write latency, node event backlog
- PostgreSQL, Docker, Slack alerts 15-30 min before cascading failure
- Dashboard: cluster health score, anomaly timeline, causal chain visualization

**Why >$10k/mo:** 20 companies × $500-1500/mo. Prevents $100k+ incident costs.
**Capex:** ~$20k. Infra: ~$180/mo. **Effort:** <5 hrs/week.
**Competitors:** Datadog/Grafana show metrics but don't predict API latency cascades.

---

## 🏹 NICHE #10: Multi-Tenant SaaS Seat Utilisation Underbilling Detector
**B2B Problem:** SaaS vendors using per-seat pricing (Jira, Confluence, Salesforce, GitHub Enterprise) lose revenue when customers self-serve deprovisioning — users churn from UI but seat licenses stay active in后台. Vendors overcount seats by 5-15%, leaving money on the table.

**Target Market:** B2B SaaS with 500-5000 seats, per-seat pricing, and self-serve UI

**Technical Architecture:**
- Python/Go integration via SCIM/SSO provider APIs + product DB seat table
- Cross-reference: active SSO users vs billed seats vs active product logins
- Gap detection engine: orphaned seats, ghost users, over-provisioning
- PostgreSQL, Docker, Slack + email alerts for revenue leakage per account
- Dashboard: seat utilization %, underbilling $ per customer, cohort trends

**Why >$10k/mo:** 30 vendors × $300-800/mo. Recover 5-10% of seat revenue.
**Capex:** ~$12k. Infra: ~$100/mo. **Effort:** <4 hrs/week.
**Competitors:** Barefoot/Metronome — usage-based billing, not seat attribution.

---

## 🏹 NICHE #13: Datadog Monitor Alert Fatigue Predictor
**B2B Problem:** SRE/DevOps teams with 200-2000+ Datadog monitors accumulate alert noise — 60-80% of pages are non-actionable, caused by cascading failures, flapping thresholds, or monitors firing on already-failing services. Alert fatigue desensitizes teams, causing real incidents to be missed or delayed.

**Target Market:** Mid-large SaaS with heavy Datadog usage (>$10k/mo Datadog bill), 50+ engineers, on-call rotations

**Technical Architecture:**
- Go collector via Datadog REST API (monitors, monitor groups, audit logs, downtime schedules)
- Alert fatigue engine: tracks per-monitor page rate, flapping frequency, noise-to-signal ratio
- Correlation analyzer: groups monitors by service/dashboard, identifies root-cause vs symptom monitors
- Suppression opportunity finder: suggests mute windows or composite monitors to reduce noise
- PostgreSQL, Docker, Slack alerts highlighting top offenders + suggested consolidations
- Dashboard: team alert load, monitor efficiency scores, noise trend over time

**Why >$10k/mo:** 25 companies × $400-1200/mo. Reduces 30-50% of non-actionable pages.
**Capex:** ~$15k. Infra: ~$120/mo. **Effort:** <4 hrs/week.
**Competitors:** Datadog itself has monitor management but no alert fatigue prediction or correlation engine.

---

## 🏹 NICHE #14: GitHub Secret Scanning Blast Radius Analyzer
**B2B Problem:** Security teams responding to a GitHub secret exposure (API key, AWS credentials, private key) must quickly determine which repos were affected, whether keys are still active, and what the blast radius is. Manual repo scanning takes hours — meanwhile credentials may still be active and abused.

**Target Market:** Mid-large SaaS with 100+ GitHub repos, high security posture requirements (fintech, healthtech, payments)

**Technical Architecture:**
- Go collector via GitHub token/scan APIs + secret scanning alerts webhook
- Blast radius engine: correlates exposed secret with repo access logs, collaborator list, deployment targets
- Active key detector: probes key validity without triggering rotation prematurely
- Exposure timeline: when was the secret committed vs when it was pushed vs when scan caught it
- PostgreSQL, Docker, Slack alerts with severity, affected repos, and recommended remediation steps
- Dashboard: secret exposure incidents, blast radius history, key rotation tracking


**Why >$10k/mo:** 20 companies × $500-1500/mo. Prevents $50k-$500k in breach costs per incident.
**Capex:** ~$12k. Infra: ~$100/mo. **Effort:** <3 hrs/week.
**Competitors:** GitHub secret scanning is raw — shows alerts but no blast radius analysis or active key probing.

---

## 🏹 NICHE #15: Infrastructure Cost Anomaly Pre-Collision System
**B2B Problem:** Finance and DevOps teams at cloud-native companies ($500k-$10M/yr AWS/GCP/Azure spend) get blindsided by cost anomalies — a single misconfigured resource, overnight bug, or botched auto-scaling run can generate $10k-$100k in unexpected charges within 24 hours. No early warning, no blast radius context, no rollback path.

**Target Market:** Mid-large cloud-native companies ($5M-$100M ARR) with rapid engineering scaling

**Technical Architecture:**
- Go collector polling AWS Cost Explorer/GCP Billing/Azure Cost Management APIs every 15 min
- Anomaly detection engine: real-time spend delta vs 7/30-day baseline per account, service, region, resource tag
- Pre-collision alert system: predicts end-of-day projected cost, compares against budget threshold
- Blast radius mapping: correlates anomalous resources with team/service owners via cost tags
- PostgreSQL, Docker, Slack/PagerDuty alerts with projected overage amount, top contributors, and estimated rollback savings
- Dashboard: spend anomaly timeline, budget vs actual, cost allocation heatmap

**Why >$10k/mo:** 25 companies × $400-1500/mo. Prevents $20k-$200k in surprise cloud bills per incident.
**Capex:** ~$15k. Infra: ~$150/mo. **Effort:** <4 hrs/week.
**Competitors:** CloudHealth/Densify show costs but don't predict anomalies or provide pre-collision alerting.


---

## 🏹 NICHE #16: GitHub Dependency Confusion & Typosquatting Detector
**B2B Problem:** Engineering teams with 50-500+ internal packages (npm/@scope, PyPI internal, Go modules, Maven snapshots) face constant typosquatting and dependency confusion attacks — malicious actors publish packages with similar names to steal secrets or inject malware. No automated detection of lookalike packages, no alert on new internal-looking packages from untrusted registries.

**Target Market:** Mid-large SaaS with active package publishing, open-source footprint, and 20+ engineers

**Technical Architecture:**
- Go collector via npm registry API + PyPI API + GitHub Dependabot alerts
- Name similarity engine: levenshtein/soundex matching against internal package namespace
- Registry monitor: watches for new public packages with names matching internal patterns (scoping confusion)
- Typosquatting detector: generates plausible misspellings, checks registry for existence
- GitHub Dependabot integration + webhook alerts for new suspicious dependencies
- PostgreSQL, Docker, Slack alerts with severity, package info, and recommended action
- Dashboard: dependency risk score, typosquatting history, registry coverage map


**Why >$10k/mo:** 20 companies × $500-1500/mo. Prevents $100k-$1M in supply chain attack costs.
**Capex:** ~$12k. Infra: ~$100/mo. **Effort:** <3 hrs/week.
**Competitors:** Snyk/Dependabot show known vulnerabilities but don't detect typosquatting or registry confusion.

---

## 🏹 NICHE #5: Build Artifact Drift Detector *(Beat #4)*
**B2B Problem:** DevOps teams deploying containerized apps across 10-50+ environments (dev/staging/prod/multi-region) lose track of config drift. Staging passes, production fails — same artifact, different env vars, volumes, or secrets. No automated detection.

**Target Market:** Mid-large SaaS with Kubernetes/fargate deployments across multi-cloud or multi-region

**Technical Architecture:**
- Go scanner pulling artifact manifests + env configs from GitHub/ArgoCD/Helm
- Drift diff engine comparing deployed configs vs baseline
- PostgreSQL, Docker, Slack alerts with drift severity + rollback recommendation
- Dashboard: drift history, severity trends, environment health scores

**Why >$10k/mo:** 25 teams × $400-1000/mo. Saves 4-8 hrs/week per DevOps engineer.
**Capex:** ~$15k. Infra: ~$120/mo. **Effort:** <5 hrs/week.
**Competitors:** ArgoCD/Flux visualize drift but don't alert or audit it cross-env.

---

## 🏹 NICHE #6: B2B SaaS Feature Flag Technical Debt Analyzer *(Beat #5)*
**B2B Problem:** Engineering teams with 100+ feature flags accumulate orphaned flags (code removed but flag remains), conflict flags (2 flags control same feature), and zombie flags (enabled but no traffic). Each adds latency, cognitive load, and security risk.

**Target Market:** Scale-up SaaS engineering teams (50-500 engineers) using LaunchDarkly/Optimizely/Split

**Technical Architecture:**
- Python/Go integration via LaunchDarkly/Optimizely REST APIs + code scanning (GitHub)
- Flag lifecycle analyzer: orphaned, conflict, zombie detection
- PostgreSQL, Redis cache, Docker, React dashboard, Slack alerts
- Flag removal workflow with deployment verification hooks

**Why >$10k/mo:** 20 companies × $500-1500/mo. Saves $50k+/yr in engineering time.
**Capex:** ~$18k. Infra: ~$150/mo. **Effort:** <6 hrs/week.
**Competitors:** LaunchDarkly has flag analytics but no technical debt or removal workflow.

---

## 🏹 NICHE #3: Invoice Reconciliation Engine
**B2B Problem:** Finance teams at companies with 200+ vendors manually match invoices against POs and receipts. AP clerks waste 15-20 hrs/week on mismatches, late payments, and duplicate bills. ERP exports are messy — OCR errors compound.

**Target Market:** Mid-market manufacturing, distribution, wholesale ($50M-$500M revenue) with complex multi-vendor AP workflows

**Technical Architecture:**
- Python/Go parser ingesting invoices via email/ERP API, fuzzy line-item matching
- Duplicate/variance flagging engine, PostgreSQL, Slack alerts with match confidence scores
- Dashboard: unmatched invoices, aging report, vendor performance tracker

**Why >$10k/mo:** 30 companies × $350-800/mo. Saves $40k+/yr per mid-size company.
**Capex:** ~$10k. Infra: ~$100/mo.
**Effort:** <5 hrs/week post-launch.
**Competitors:** Tipalti/Trovata — payments focus, not reconciliation accuracy.

---

## 🏹 NICHE #4: API Usage Anomaly Billing Auditor
**B2B Problem:** Usage-based SaaS API customers get blindsided by billing spikes from buggy code, bot traffic, misconfigured webhooks. No early detection, no root cause — just a shock invoice ($5k-$50k overnight).

**Target Market:** Startups and scale-ups spending $5k+/mo on metered APIs (AWS, Twilio, Stripe, OpenAI, Vercel)

**Technical Architecture:**
- Go collector polling billing APIs every 15 min, statistical anomaly detection (>3σ)
- PostgreSQL time series, Slack alerts with root cause hypothesis + estimated overage
- Dashboard: usage trends, anomaly history, projected bill vs actual

**Why >$10k/mo:** 25 teams × $400-1200/mo. Saves $10k-$100k per incident.
**Capex:** ~$8k. Infra: ~$80/mo.
**Effort:** <4 hrs/week.
**Competitors:** None purely multi-API anomaly detection for startups.

---

## 🏹 NICHE #1: Workflow Automation Noise Detector *(Beat #3)*
**B2B Problem:** Ops teams with 50-500+ Zapier/Make/n8n automations accumulate redundant, conflicting, or dead workflows. No cross-workflow visibility — incidents silently multiply.

**Target Market:** Ops-heavy SaaS, ecommerce, marketing agencies with complex automation stacks

**Technical Architecture:** Python/Go scanner via Zapier/Make/n8n APIs, dependency graph mapping, health index scoring (0-100), Docker, PostgreSQL, React dashboard, Slack alerts

**Why >$10k/mo:** 40 customers × $250/mo. Enterprise: $500-2k/mo.
**Capex:** ~$12k. Infra: ~$150/mo. **Effort:** <6 hrs/week.
**Competitors:** Zapier/Make — individual workflow status only, no dependency analysis.

---

## 🏹 NICHE #2: Enterprise Schema Governance SaaS *(Beat #3)*
**B2B Problem:** Enterprise teams with 200+ microservices have no unified ownership model for API schemas. Teams step on contracts, deprecations silently break consumers.

**Target Market:** Large SaaS, fintech, healthtech with 100+ internal APIs and multi-team ownership

**Technical Architecture:** Go backend ingesting OpenAPI 3.x/GraphQL specs from GitHub, ownership enforcement, diffing engine, GitHub Checks API integration, PostgreSQL, RBAC

**Why >$10k/mo:** 25 enterprises × $400-2000/mo. Enterprise sales cycle 1-3 months.
**Capex:** ~$25k. Infra: ~$400/mo. **Effort:** <8 hrs/week.
**Competitors:** Postman/Loops — API management, not schema ownership governance.

---

## 🏹 NICHE #17: CI/CD Webhook Delivery Failure Silent Killer Detector
**B2B Problem:** Engineering teams using GitHub Actions/GitLab CI with webhook-based deployments (ArgoCD, Octopus, Spinnaker, custom push) face silent deployment failures — a webhook endpoint goes down, a payload signature check starts failing, or a misconfigured channel blocks deployments silently. No failure alerts, no retry logic, no visibility. Deployments report success but never actually happen.

**Target Market:** Scale-up SaaS with 20+ engineers, complex multi-target deployment pipelines

**Technical Architecture:**
- Go collector via GitHub Actions webhooks + GitLab CI webhook audit logs + target system health probes
- Delivery verification engine: sends probe payloads, confirms target receipt, detects signature mismatches
- Failure detection: 4xx/5xx from webhook endpoint, timeout, auth drift, channel misconfiguration
- PostgreSQL, Docker, Slack alerts with deployment target, failure reason, and retry trigger
- Dashboard: webhook delivery success rate, failure history, endpoint health overview

**Why >$10k/mo:** 25 companies × $400-1000/mo. Prevents $10k-$100k in failed deployments per incident.
**Capex:** ~$10k. Infra: ~$80/mo. **Effort:** <3 hrs/week.
**Competitors:** GitHub/GitLab show webhook delivery attempts but don't verify target receipt or alert on silent failures.

---

## 🏹 NICHE #18: GitHub Actions Secrets/Tokens Age Tracker (Stale Credential Detector)
**B2B Problem:** Engineering teams with 50-500+ GitHub Actions workflows store long-lived secrets and tokens in repository environments (AWS keys, API tokens, deployment credentials). When these credentials rotate in the IdP or are revoked, Actions workflows silently fail — or worse, old credentials remain active and become a security liability. No visibility into secret age or rotation status.

**Target Market:** Mid-large SaaS with 20+ engineers, GitHub Actions + cloud deployments, active credential rotation policies

**Technical Architecture:**
- Go collector via GitHub API + Actions secrets/environments API, OIDC role mapping where available
- Secret age engine: tracks creation date vs last used vs rotation policy threshold per secret
- Stale credential detector: flags secrets not rotated in >90 days or exceeding org policy
- Rotation workflow integration: flags workflows affected by upcoming rotation, estimates blast radius
- PostgreSQL, Docker, Slack alerts with secret name, age, affected workflows, recommended action
- Dashboard: secret age heatmap, rotation calendar, compliance posture

**Why >$10k/mo:** 25 companies × $400-1000/mo. Prevents $50k-$500k in security incidents from stale credentials.
**Capex:** ~$10k. Infra: ~$80/mo. **Effort:** <3 hrs/week.
**Competitors:** GitHub shows secret names and environments but doesn't track age, rotation status, or blast radius.


## 🏹 NICHE #19: Stripe Radar Fraud Rule False Positive Analyzer
**B2B Problem:** Stripe users with high-value transactions (>$500/tx, 100+/day) get hit by Stripe Radar's default fraud rules flagging legitimate customers — chargebacks from false positives destroy customer relationships and add processing fees. No visibility into which Radar rules fire most, no A/B testing of rule configurations, no false positive rate tracking.

**Target Market:** High-value B2C SaaS with Stripe (>$250k/mo GMV), 50+ transactions/day, Radar fraud issues

**Technical Architecture:**
- Python/Go collector via Stripe API (Radar rules, charge data, dispute events)
- False positive engine: correlates Radar risk scores with dispute outcomes, identifies rules with highest false positive rates
- Rule impact analyzer: which rules fire most on legitimate transactions, what's the cost per rule
- Suggestion engine: recommends rule threshold adjustments to reduce false positives while maintaining fraud catch rate
- PostgreSQL, Docker, Slack alerts for rule-level false positive spikes
- Dashboard: rule efficiency scores, false positive cost trends, suggested threshold adjustments

**Why >$10k/mo:** 25 companies × $400-1200/mo. Recover 2-5% of GMV from prevented false positive abandonments.
**Capex:** ~$12k. Infra: ~$100/mo. **Effort:** <3 hrs/week.
**Competitors:** Stripe dashboard shows Radar events but doesn't correlate with false positives or suggest rule optimizations.

---

## 🏹 NICHE #20: AWS EC2 Spot Interruption Prediction & Workload Migration Advisor
**B2B Problem:** Engineering teams running production workloads on AWS EC2 Spot instances (batch processing, ML inference, HPC, stateless microservices) face sudden spot interruptions with only 2 minutes warning. When interruptions hit without a migration plan, jobs fail, SLAs break, and expensive on-demand fallback kicks in. No prediction, no pre-emptive migration, no cost-aware fallback strategy.

**Target Market:** Cloud-native companies ($500k+/yr AWS spend) with Spot-dependent workloads, batch/ML/HPC teams

**Technical Architecture:**
- Go collector via AWS EC2 Spot Fleet API + CloudWatch instance metadata + interruption notifications
- Prediction engine: analyzes instance termination patterns, AZ rebalance events, Spot capacity history to predict interruptions 5-30 min out
- Migration advisor: evaluates on-demand/Fargate/Preemptible fallback options, cost-latency tradeoffs, target AZ/region capacity
- Workload checkpoint coordinator: triggers graceful shutdown/snapshot hooks (Kubernetes, ECS, batch schedulers) before interruption
- PostgreSQL, Docker, Slack/PagerDuty alerts with interruption countdown, affected instances, recommended migration path
- Dashboard: spot health overview, interruption predictions, migration success rate, cost savings tracker

**Why >$10k/mo:** 25 companies × $400-1200/mo. Prevents $20k-$200k in failed workloads and emergency on-demand spikes per incident.
**Capex:** ~$15k. Infra: ~$120/mo. **Effort:** <4 hrs/week.
**Competitors:** AWS Spot Fleet shows current state but doesn't predict interruptions or advise on migration. Spotinst/CAST AI focus on cost, not prediction or workload continuity.

---

## 🏹 NICHE #21: Kubernetes Namespace Quota Expiry & OOMKilled Incident Predictor
**B2B Problem:** SRE and platform engineering teams managing Kubernetes clusters with namespace-level resource quotas face silent quota exhaustion — pods hit `Evicted` or `OOMKilled` when quota is hit, with no advance warning. When quota expires mid-business-hours, critical services fail with no recourse. No prediction, no early alerts, no quota runway visibility.

**Target Market:** Mid-large SaaS with 20+ namespaces, multi-tenant Kubernetes clusters, and resource-constrained engineering teams

**Technical Architecture:**
- Go collector via Kubernetes API (resourceQuota, limitRange, pod metrics) + Prometheus node-exporter
- Quota runway engine: calculates days-to-exhaustion per namespace based on usage trend vs quota limit
- OOMKilled prediction: correlates memory pressure signals (container memory working set, page faults, evictions) vs limit
- Expiry alert system: 30/14/7/3/1 day warnings for quota expiry dates + hard limits
- PostgreSQL, Docker, Slack/PagerDuty alerts with namespace, quota utilization %, affected workloads, recommended actions
- Dashboard: namespace quota health, OOMKilled risk scores, quota expiry calendar

**Why >$10k/mo:** 25 companies × $400-1200/mo. Prevents $20k-$200k in service disruptions per quota incident.
**Capex:** ~$12k. Infra: ~$100/mo. **Effort:** <3 hrs/week.
**Competitors:** Kubernetes dashboard shows current usage but no runway prediction or OOMKilled correlation.

---

## 🏹 NICEE #22: API SLA Compliance Monitor for Third-Party API Dependencies
**B2B Problem:** Engineering teams with 20-100+ third-party API dependencies (Stripe, Twilio, OpenAI, AWS, GCP) have no unified view of SLA compliance — when a provider drops below SLA thresholds (e.g., p99 latency spikes, error rate jumps), engineers find out from customers, not from monitoring. SLA credits go unclaimed. No cross-provider correlation, no incident replay, no credit tracking.

**Target Market:** Scale-up SaaS ($10M-$100M ARR) with complex third-party API dependencies, multiple engineering teams

**Technical Architecture:**
- Go collector via provider status APIs (AWS AWS Health, GCP Status, Stripe status page) + synthetic monitoring probes
- SLA compliance engine: tracks real-user latency/error metrics vs provider SLA thresholds (p50/p95/p99)
- Multi-provider correlation: when multiple APIs degrade simultaneously, identifies root provider vs cascading effect
- SLA credit claim tracker: records downtime events, calculates credit entitlements, tracks claim status
- PostgreSQL, Docker, Slack alerts with provider, metric breach, estimated credit value, recommended actions
- Dashboard: SLA compliance timeline per provider, credit claim history, provider health correlation matrix

**Why >$10k/mo:** 30 companies × $300-800/mo. Claims $10k-$100k/yr in uncollected SLA credits.
**Capex:** ~$10k. Infra: ~$80/mo. **Effort:** <3 hrs/week.
**Competitors:** Statuspage shows incidents after they happen — no SLA compliance tracking, credit claiming, or correlation engine.

---

## 🏹 NICHE #23: GitHub PR Review Cycle Time Predictor
**B2B Problem:** Engineering teams with 20-200+ active PRs face hidden merge bottlenecks — PRs sit in review queue 24-72 hrs while engineers context-switch between branches. No visibility into who's swamped, which PRs are blocked, or why review times drift week-over-week. Slow reviews block feature shipping and inflate cycle time metrics.

**Target Market:** Scale-up SaaS with 20+ engineers, GitHub Enterprise, active PR culture with merge velocity targets

**Technical Architecture:**
- Go collector via GitHub GraphQL API (PRs, review events, comments, review requests)
- Cycle time engine: baseline per-developer review time, predict queue wait per PR, detect drift
- Bottleneck analyzer: flags PRs exceeding predicted review time, correlates with reviewer load/context-switching
- Team health scoring: aggregate review efficiency, identify overloaded reviewers, track week-over-week trends
- PostgreSQL, Docker, Slack alerts with author, PR link, queue position, and estimated unblock actions
- Dashboard: PR review cycle trends, team reviewer load heatmap, bottleneck PRs, cycle time vs baseline

**Why >$10k/mo:** 30 companies × $300-800/mo. Reduces PR cycle time by 15-25% for engineering teams.
**Capex:** ~$10k. Infra: ~$80/mo. **Effort:** <3 hrs/week.
**Competitors:** GitHub insights show raw cycle times but no prediction, bottleneck routing, or team load balancing.

---

## 🏹 NICHE #24: Snowflake Warehouse Credit Burn Rate Anomaly Detector
**B2B Problem:** Data engineering and finance teams running Snowflake warehouses ($50k-$500k/yr credits) get blindsided by credit burn spikes — a single runaway query, warehouse misconfiguration, or concurrent job pile-up burns months of budget in hours. No attribution, no prediction, no kill-switch. Cloud cost explosions cascade into data pipeline outages and budget freeze incidents.

**Target Market:** Mid-large SaaS with $50k+/yr Snowflake spend, multi-warehouse/data team setup, finance-involved cost governance

**Technical Architecture:**
- Go collector via Snowflake Account Usage views + Warehouse Events API + Query History
- Credit burn rate engine: real-time tracking vs 7/30-day baseline per warehouse, user, query tag
- Anomaly detection: statistical spike detection (>3σ), identifies top credit-consuming queries and users
- Attribution engine: maps burn to team/project via query tags, user, warehouse, scheduled jobs
- Kill-switch trigger: auto-suspend warehouse or kill runaway queries on threshold breach (with approval workflow)
- PostgreSQL, Docker, Slack alerts with warehouse name, credit delta, top query fingerprint, estimated cost
- Dashboard: credit burn rate trends, warehouse efficiency scores, query cost leaderboard, budget vs actual

**Why >$10k/mo:** 25 companies × $400-1200/mo. Prevents $20k-$200k in Snowflake credit overages per incident.
**Capex:** ~$12k. Infra: ~$100/mo. **Effort:** <4 hrs/week.
**Competitors:** Snowflake's built-in monitoring shows current usage but no anomaly prediction, attribution, or kill-switch.

---

**Why >$10k/mo:** 25 companies × $400-1200/mo. Reduces 30-50% of non-actionable pages.
**Capex:** ~$15k. Infra: ~$120/mo. **Effort:** <4 hrs/week.
**Competitors:** Datadog itself has monitor management but no alert fatigue prediction or correlation engine.

---

## 🏹 NICHE #25: Snowflake Query Age & Long-Running Query Blocker
**B2B Problem:** Data engineering and platform teams running Snowflake with 50+ concurrent users face runaway queries — long-running analytical queries consume warehouse credits for hours, block scheduled jobs, and cascade into downstream pipeline failures. No auto-timeout enforcement, no early warning, no query kill authority without DBA involvement.

**Target Market:** Mid-large SaaS with $50k+/yr Snowflake spend, multi-user data teams, and complex scheduled query pipelines

**Technical Architecture:**
- Go collector via Snowflake Query History + Warehouse Events API + Session monitoring
- Query age engine: tracks query duration vs 7/30-day baseline per user/warehouse, flags anomalies
- Long-running blocker detector: identifies queries blocking scheduled jobs or waiting on warehouse queue
- Auto-timeout enforcer: configurable threshold (e.g., >30 min) with auto-suspend/kill hooks + approval workflow
- Credit impact estimator: projects estimated credit cost of running query to completion
- PostgreSQL, Docker, Slack alerts with user, warehouse, query fingerprint, duration, and kill action
- Dashboard: query age distribution, longest-running queries, warehouse queue depth, credit impact

**Why >$10k/mo:** 25 companies × $400-1200/mo. Prevents $10k-$100k in runaway query credit burns per incident.
**Capex:** ~$10k. Infra: ~$80/mo. **Effort:** <3 hrs/week.
**Competitors:** Snowflake's resource monitors show current usage but no auto-timeout, age prediction, or kill-switch.

---

## 🏹 NICHE #26: GitHub Actions Runner Pool Autoscale Inefficiency Analyzer
**B2B Problem:** Engineering teams with 20-500+ GitHub Actions workflows using self-hosted runners face runner pool inefficiency — runners sit idle for hours waiting for workflow dispatches, or conversely, workflow queues pile up waiting for runner availability. No right-sizing intelligence, no scale cooldown management, no cost-per-run tracking. AWS/GCP costs for runner infrastructure balloon without correlating to actual throughput.

**Target Market:** Mid-large SaaS with self-hosted GitHub Actions runners, 20+ engineers, significant CI/CD spend ($5k+/mo runner infra)

**Technical Architecture:**
- Go collector via GitHub Actions API + runner self-reporting metrics (CPU, RAM, disk per job)
- Pool efficiency engine: idle time vs active time per runner, queue depth vs runner count correlation
- Autoscale intelligence: suggests scale-up/down thresholds based on job queue patterns (time-of-day, day-of-week)
- Cost-per-run calculator: computes runner infra cost per workflow run, identifies expensive runner configurations
- Cooldown optimizer: detects premature scale-down vs delayed scale-up patterns causing thrashing
- PostgreSQL, Docker, Slack alerts with runner utilization %, queue depth, and scale recommendations
- Dashboard: runner pool health, cost-per-run trends, autoscale efficiency scores, queue depth timeline


**Why >$10k/mo:** 25 companies × $400-1000/mo. Reduces runner infra costs 20-40% while improving queue throughput.
**Capex:** ~$12k. Infra: ~$100/mo. **Effort:** <3 hrs/week.
**Competitors:** GitHub Actions shows runner status but doesn't analyze pool efficiency, cost-per-run, or suggest autoscale tuning.

---

## 🏹 NICHE #27: BigQuery Slot Utilization Anomaly & Pre-Collision Detector
**B2B Problem:** Data engineering and platform teams running BigQuery ($50k-$500k/yr in slot commits) face silent slot contention — a single complex query, concurrent BI workload, or pipeline misconfiguration exhausts available slots, causing queued queries, pipeline timeouts, and SLA violations. No early warning, no attribution, no kill-switch. On-demand slot bursts are expensive and can run $10k-$100k in a weekend.

**Target Market:** Mid-large SaaS with $100k+/yr BigQuery spend, multi-project data pipelines, BI teams sharing slots

**Technical Architecture:**
- Go collector via BigQuery Management API + Reservation API + slot usage time series
- Slot utilization engine: real-time tracking vs 7/30-day baseline per project, user, reservation
- Anomaly detection: statistical spike detection (>3σ), identifies top slot-consuming queries/users
- Attribution engine: maps slot burn to team/project via labels, user, query tags, scheduled jobs
- Pre-collision alert system: predicts end-of-day slot consumption, compares against reservation capacity
- Kill-switch trigger: configurable threshold with query kill/cancel hooks + approval workflow
- PostgreSQL, Docker, Slack alerts with project name, slot delta, top query fingerprint, estimated cost
- Dashboard: slot utilization trends, reservation efficiency scores, query cost leaderboard, projected vs actual

**Why >$10k/mo:** 25 companies × $400-1200/mo. Prevents $20k-$200k in BigQuery overages per incident.
**Capex:** ~$12k. Infra: ~$100/mo. **Effort:** <3 hrs/week.
**Competitors:** BigQuery monitoring shows current usage but no anomaly prediction, attribution, or kill-switch.

---

## 🏹 NICHE #28: Jira Ticket Velocity Drift & Quarterly Commitment Risk Predictor
**B2B Problem:** Engineering and product managers at SaaS companies with quarterly commitments (OKRs, roadmap milestones, SLA-bound deliverables) get surprised by velocity drift — mid-quarter, they discover the team is on track to deliver 60% of committed tickets. No early warning, no bottleneck visibility, no scope adjustment tooling. The discovery comes too late to course-correct, damaging credibility with stakeholders.

**Target Market:** Mid-large SaaS with 20+ engineers, Jira-based project management, quarterly OKR/commitment culture

**Technical Architecture:**
- Python/Go collector via Jira REST API (issues, sprints, velocity history, worklogs)
- Velocity drift engine: tracks sprint velocity vs 6-month baseline, detects statistical drift (>1.5σ)
- Commitment risk predictor: projects sprint-end completion % based on current velocity, flags risk <80%
- Bottleneck analyzer: identifies blocked tickets, slow reviewers, dependency chains blocking velocity
- Scope adjustment advisor: suggests ticket deferral/promotion based on priority, effort, and velocity trends
- PostgreSQL, Docker, Slack alerts with sprint name, projected completion %, at-risk tickets, recommended actions
- Dashboard: velocity trends, sprint burn charts, commitment risk scores, team capacity heatmap

**Why >$10k/mo:** 30 companies × $300-800/mo. Prevents 15-25% of missed quarterly commitments.
**Capex:** ~$10k. Infra: ~$80/mo. **Effort:** <3 hrs/week.
**Competitors:** Jira itself shows velocity charts but no drift prediction, commitment risk scoring, or scope adjustment advice.

---

## 🏹 NICHE #29: PagerDuty MTTA/MTTR Benchmark Analyzer
**B2B Problem:** Engineering managers at mid-large SaaS with on-call rotations want to measure MTTA (mean time to acknowledge) and MTTR (mean time to resolve) but lack context — how does their team compare to industry peers, similarly sized companies, or their own historical trend? No benchmarking, no target setting, no improvement trajectory.

**Target Market:** Mid-large SaaS with 20+ engineers, PagerDuty usage, active on-call culture, quarterly reliability SLOs

**Technical Architecture:**
- Python/Go collector via PagerDuty REST API (incidents, on-call logs, escalation policies)
- MTTA/MTTR calculation engine: per team, service, priority, time-of-day segmentation
- Benchmark database: anonymized industry peer data (by company size, engineer count, on-call burden)
- Comparative analyzer: current metrics vs peer benchmark vs internal 90-day trend
- Goal tracker: sets realistic targets based on peer data, tracks weekly improvement
- PostgreSQL, Docker, Slack alerts when MTTA/MTTR regresses >15% vs baseline
- Dashboard: MTTA/MTTR trends, peer comparison, on-call burden heatmap, improvement trajectory

**Why >$10k/mo:** 25 companies × $400-1000/mo. Informs SLO targets and prevents on-call burnout.
**Capex:** ~$10k. Infra: ~$80/mo. **Effort:** <3 hrs/week.
**Competitors:** PagerDuty shows raw incident data but no peer benchmarking or goal tracking.

---

## 🏹 NICHE #30: AWS Lambda Cold Start Latency Regression Detector
**B2B Problem:** Serverless engineering teams with 50-500+ Lambda functions face cold start latency regressions — a dependency change, new layer version, or runtime update silently inflates cold start times by 100-500ms+. Downstream services (API GW, Step Functions, EventBridge) get timeouts, SLOs breach silently. No baseline tracking, no regression detection, no root cause.

**Target Market:** Mid-large SaaS with heavy Lambda workloads (>50 functions), event-driven architectures, strict latency SLOs

**Technical Architecture:**
- Go collector via AWS CloudWatch Lambda Insights API + X-Ray trace sampling
- Cold start latency engine: tracks p50/p95/p99 per function, correlated with invocation frequency
- Regression detector: statistical comparison vs 30-day baseline (>2σ = regression flag)
- Root cause analyzer: correlates regression with layer version, runtime, memory config, VPC attachment
- Dependency impact mapping: which downstream services are exposed to which functions
- PostgreSQL, Docker, Slack alerts with function name, latency delta, probable cause, affected downstream
- Dashboard: cold start latency trends, regression history, function health scores, layer version drift

**Why >$10k/mo:** 20 companies × $500-1500/mo. Prevents $20k-$200k in latency-related incidents per year.
**Capex:** ~$12k. Infra: ~$100/mo. **Effort:** <3 hrs/week.
**Competitors:** AWS Lambda console shows invocation counts, not latency baselines or regression detection.

---

## 🏹 NICHE #31: GitHub Actions Spend by Workflow Run Attribution
**B2B Problem:** Finance and engineering teams at companies with 50-500+ GitHub Actions workflows get no visibility into per-workflow or per-run spend — GitHub bills by minute, not by workflow. When costs spike ($5k-$50k/mo over baseline), there's no attribution to which workflows, repos, or teams are driving consumption. No chargeback model, no cost anomaly detection, no optimization targets.

**Target Market:** Mid-large SaaS with $10k+/mo GitHub Actions spend, 20+ engineers, finance-involved cloud cost governance

**Technical Architecture:**
- Go collector via GitHub Actions API + usage metrics endpoints + workflow run history
- Spend attribution engine: maps compute minutes to workflow, repo, branch, actor, trigger event
- Cost calculation: computes per-run cost based on runner type (ubuntu-latest, large, self-hosted), duration, matrix jobs
- Anomaly detection: flags workflows with >2σ cost increase vs 30-day baseline
- Chargeback mapping: allocates spend to team/project via GitHub org structure + custom tagging
- PostgreSQL, Docker, Slack alerts with top-consuming workflows, cost delta, and optimization suggestions
- Dashboard: workflow spend trends, team cost leaderboard, cost-per-run benchmarks, budget vs actual

**Why >$10k/mo:** 30 companies × $300-800/mo. Informs chargeback models and prevents 20-40% wasted Actions spend.
**Capex:** ~$10k. Infra: ~$80/mo. **Effort:** <3 hrs/week.
**Competitors:** GitHub shows usage minutes but no cost attribution, anomaly detection, or chargeback mapping.

---

## 🏹 NICHE #32: Kubernetes PDB Violation Impact Predictor
**B2B Problem:** SRE and platform engineering teams with highly available services (web frontends, payment processors, auth services) face Pod Disruption Budget (PDB) violations during node drains, updates, or cluster operations — Kubernetes evicts pods beyond the PDB maxUnavailable threshold, causing brief service degradation or full outages. No pre-violation warning, no blast radius context, no safe-to-drain timeline.

**Target Market:** Mid-large SaaS with mission-critical services, multi-AZ Kubernetes clusters, and frequent node maintenance operations

**Technical Architecture:**
- Go collector via Kubernetes API (PodDisruptionBudget, Pod, Node, Deployment, StatefulSet) + cluster events
- PDB violation prediction engine: calculates safe drain windows based on current pod count vs maxUnavailable
- Blast radius mapping: correlates PDB violations with affected service name, current request load, and downstream dependencies
- Safe-to-drain advisor: recommends optimal drain timing, kubectl drain --disable-eviction flags, and pod shutdown hooks
- Cascade detector: identifies services depending on PDB-violating pods, estimates downstream impact
- PostgreSQL, Docker, Slack/PagerDuty alerts with affected services, violation timing, and recommended actions
- Dashboard: PDB health overview, safe drain timeline, violation risk scores, cluster maintenance calendar

**Why >$10k/mo:** 25 companies × $400-1200/mo. Prevents $10k-$100k in service degradation incidents per cluster operation.
**Capex:** ~$12k. Infra: ~$100/mo. **Effort:** <3 hrs/week.
**Competitors:** Kubernetes shows PDB spec but no violation prediction, blast radius mapping, or safe-to-drain advisory.

---

## 🏹 NICHE #33: GitHub Copilot Seat Activity & PR Code Quality Correlation Analyzer
**B2B Problem:** Engineering leaders with GitHub Copilot Enterprise licenses (30-500+ seats, $19-39/user/mo) have zero visibility into whether Copilot is actually improving code quality — PR defect rates, code review cycle times, and sprint velocity before/after adoption are unknown. Finance demands ROI proof; Copilot remains a black box spend.

**Target Market:** Mid-large SaaS companies (50+ engineers) with GitHub Copilot Enterprise and active sprint tracking (Jira/Linear)

**Technical Architecture:**
- Go collector via GitHub Copilot API (seat usage, completion acceptance rates) + GitHub API (PR metadata, review times) + Jira/Linear (defect tickets, velocity)
- Correlation engine: compares Copilot usage intensity per team/author vs PR defect rates, review turnaround, and code churn
- ROI estimator: estimates cost per eng-month vs measured productivity delta
- Anomaly detector: identifies teams with high Copilot usage but declining quality metrics
- PostgreSQL, Docker, Slack alerts for quality regressions correlated with low Copilot adoption
- Dashboard: seat utilization, quality trend lines, ROI estimates by team

**Why >$10k/mo:** 25 companies × $400-1200/mo. Justifies $570k-$1.8M/yr Copilot spend with data.
**Capex:** ~$15k. Infra: ~$100/mo. **Effort:** <3 hrs/week.
**Competitors:** GitHub Copilot dashboard shows usage, not code quality correlation or ROI.

---

## 🏹 NICHE #34: AWS RDS/DocumentDB Index Fragmentation Query Latency Predictor
**B2B Problem:** DevOps and DBA teams running production RDS PostgreSQL/MySQL or DocumentDB clusters face unexplained query latency spikes during traffic surges — queries that worked fine at 10k RPM suddenly timeout at 50k RPM. Root cause is often index fragmentation, missing indexes, or stale statistics, but there is no predictive view — teams discover it only during incidents.

**Target Market:** Mid-large SaaS with production databases ($50k+/mo AWS spend), frequent traffic spikes, and DBA capacity constraints

**Technical Architecture:**
- Go collector via AWS API (RDS Performance Insights, DocumentDB metrics) + database-side statistics views (pg_stat_user_indexes, information_schema.tables)
- Fragmentation engine: tracks index bloat ratio, table bloat, autovacuum backlog, and dead tuple accumulation over time
- Query latency predictor: models query execution time vs row count, index usage, and fragmentation level using historical data
- Alert generator: pre-emptive warnings when fragmentation exceeds thresholds or missing index candidates surface
- PostgreSQL/DocumentDB, Docker, Slack alerts with specific queries, affected tables, and recommended reindex/vacuum actions
- Dashboard: index health scores, fragmentation trends, query latency forecasts, reindex scheduling

**Why >$10k/mo:** 20 companies × $500-1500/mo. Prevents $20k-$200k in incident costs from query timeouts.
**Capex:** ~$18k. Infra: ~$120/mo. **Effort:** <4 hrs/week.
**Competitors:** AWS Performance Insights shows current latency but doesn't predict degradation or correlate with fragmentation.

---


---

## 🏹 NICHE #35: OpenTelemetry Collector Pipeline Health Analyzer
**B2B Problem:** Platform engineering and SRE teams operating 10-100+ microservices with OpenTelemetry Collector deployments face silent pipeline failures — a collector instance crashes, a processor backlogs, or an exporter fails, and trace/metric telemetry stops flowing to the backend (Datadog, Honeycomb, Grafana Tempo). No early detection, no root cause — customers report data gaps before ops notices.

**Target Market:** Mid-large cloud-native SaaS with OpenTelemetry-instrumented services, multi-collector deployments, and telemetry-dependent debugging culture

**Technical Architecture:**
- Go collector via OpenTelemetry Collector's Prometheus metrics endpoint + health check API + receiver error logs
- Pipeline health engine: tracks receiver success/failure rates, processor queue depth, exporter retry counts
- Backlog detector: correlates queue depth growth with processor throughput, flags pipeline stalls before data loss
- Alert on telemetry gaps: measures time since last successful export per service, alerts on silence >threshold
- PostgreSQL, Docker, Slack alerts with collector instance, pipeline stage, error type, affected services
- Dashboard: pipeline health scores, collector fleet overview, telemetry gap timeline, exporter error rates

**Why >$10k/mo:** 25 companies × $400-1200/mo. Prevents $20k-$200k in observability blackouts per incident.
**Capex:** ~$10k. Infra: ~$80/mo. **Effort:** <3 hrs/week.
**Competitors:** OpenTelemetry Collector has built-in health checks but no centralized monitoring, alerting, or gap detection.

---

## 🏹 NICHE #36: Feature Flag Experimentation Velocity Analyzer
**B2B Problem:** Product and engineering teams running A/B experiments via feature flags (LaunchDarkly, Optimizely, Split) have no visibility into experimentation velocity — how many experiments are running, which teams ship fastest, what the average experiment duration is, and which flags get stuck in "draft" or "testing" for months. No cycle time tracking, no throughput benchmarking, no velocity targets.
**Target Market:** Scale-up SaaS with 20+ engineers, active experimentation culture, feature flag-driven development

**Technical Architecture:**
- Python/Go collector via LaunchDarkly/Optimizely/Split REST APIs (flags, experiments, changesets)
- Experimentation velocity engine: tracks experiment count per team, average time in each stage (draft → testing → ramp → shipped/dormant)
- Stuck experiment detector: flags experiments in any stage >14 days without transition
- Velocity benchmarking: compares team-level experiment throughput vs org average, identifies bottlenecks
- Throughput predictor: projects monthly shipped experiments based on current velocity trends
- PostgreSQL, Docker, Slack alerts for stuck experiments, team velocity regressions, and missed throughput targets
- Dashboard: experiment pipeline funnel, team velocity leaderboard, stuck flag list, throughput trend

**Why >$10k/mo:** 25 companies × $400-1000/mo. Increases experimentation throughput 20-40%.
**Capex:** ~$10k. Infra: ~$80/mo. **Effort:** <3 hrs/week.
