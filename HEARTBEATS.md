---

### Beat #94 (01:45 JST) — Pipeline Healthy. Niches #177-178 Delivered
- **Last Heartbeat:** 2026-04-30 01:45 JST — Beat #94 | **Status:** ACTIVE — Hunter-Killer heartbeat running
- live_oracle: script unavailable (manual check — BTC ~$76,981 | ETH ~$2,309 | USD/JPY ~159.6 via last known)
- Gateway: ✅ Running (LaunchAgent pid 12459, state active)
- infra_pulse: script unavailable (manual check passed — Gateway OK)

## 🏹 NICHE #177: GCP Secret Manager Synchronized Rotation Drift Detector & Silent Auth Failure Forecaster

**B2B Problem:** SRE and DevOps teams managing microservices on GCP using Secret Manager for credential management face a silent credential staleness problem — when a secret is rotated in Secret Manager (automatically by policy or manually by an ops engineer), the new version propagates instantly to the vault but deployed application pods continue running with in-memory copies of the old secret version until they are restarted (which may take hours or days in a long-running deployment). A service that relies on a rotated secret immediately starts throwing authentication errors — but the team has no visibility into which pods have loaded which secret version, how long since rotation, or which services are about to hit auth failures. Secret Manager shows version history but doesn't track which running application instances have loaded which secret version, correlate secret rotation events with downstream authentication failure events, or forecast which services will fail when their cached secret expires. No tool continuously monitors secret version age per running application instance, detects when deployed services are running stale secret versions after rotation, or predicts auth failure windows based on secret TTL vs. application restart cycle.

**Target Market:** Mid-large SaaS companies on GCP GKE with Secret Manager for credential management, microservices architecture with long-running pods, automated secret rotation policies, and multi-team DevOps/SRE orgs where credential hygiene is a compliance requirement.

**Technical Architecture:**
- Python collector via GCP Secret Manager API (list secret versions, metadata, rotation events) + GKE Kubernetes API (pod spec, env var sources, mounted secrets, pod start timestamps) + Cloud Monitoring (secret version age metrics)
- Secret version age tracker: for each secret in Secret Manager, tracks current latest version and per-version creation timestamps, maps which Kubernetes pods have mounted which secret (via GKE VolumeMounts and envFrom), calculates how long each running pod has been using its current secret version vs. rotation policy
- Stale secret detector: for pods whose mounted secret version age exceeds configured TTL threshold (e.g., rotation policy is 24h but pod hasn't restarted in 48h), flags stale credential risk, calculates hours since rotation and estimated time until auth failure based on downstream service token TTLs
- Coordinated rotation gap analyzer: when a secret is rotated, identifies all services/pods that mount that secret, alerts if no rolling restart is scheduled to propagate new version, calculates blast radius (how many services will start failing auth with old cached version)
- Hardcoded secret detector: scans running pod specs for env vars or configmaps that contain raw credential strings instead of Secret Manager references, flags hardcoding violations that bypass Secret Manager rotation entirely
- GCP Secret Manager API + PostgreSQL + Grafana: secret version age per running pod heatmap, rotation event → stale credential gap timeline, auth failure forecast countdown, hardcoded secret violations table
- Alerting: Slack with "🚨 Secret `payment-gateway-api-key` rotated 6 hours ago. 14 GKE pods are still running with v3 (loaded 3 days ago). Services: `payment-service` (3 pods), `billing-worker` (2 pods), `subscription-api` (9 pods). These pods will start throwing `401 Unauthorized` when the downstream payment processor rejects the old key. Last rotation: v3 (2026-04-29 19:30 JST). Next rotation: v4 in 18 hours. Trigger a rolling restart of affected namespaces NOW, or pre-stage v4 in Secret Manager and add a startup probe to force reload. Affected downstream: Stripe webhook delivery will fail → revenue impact."

**Why >$10k/mo:** 13 companies × $800-1500/mo. Prevents auth failure cascades from secret rotation without pod restart, eliminates P0 incidents from credential staleness in production, reduces compliance violations from hardcoded secrets in pod specs.
**Capex:** ~$8k. **Infra:** ~$50/mo. **Effort:** <2 hrs/week.
**Competitors:** GCP Secret Manager console shows version history but doesn't track which running pods have loaded which version, correlate rotation events with downstream auth failures, or forecast auth failure windows based on pod restart cycles.

---

## 🏹 NICHE #178: GitHub Actions OIDC Role Trust Policy Drift Detector & Silent Workflow Failure Forecaster

**B2B Problem:** Platform engineering and DevOps teams using GitHub Actions with OpenID Connect to assume AWS IAM roles face a silent workflow breakage problem — when an AWS administrator modifies an IAM role's OIDC trust policy (adds a new GitHub org, repository, or branch condition) or adjusts the role's permission policies (attaches/detaches managed policies, updates inline policies), GitHub Actions workflows that rely on that role silently start failing with `403 Access Denied` errors. These failures are hard to diagnose: GitHub Actions shows the workflow run as failed but the error is in the `aws sts assume-role-with-web-identity` call or in subsequent AWS API calls, and the AWS console shows the role exists and has the right trust policy — but the workflow has changed and the trust policy is now overly restrictive (or was accidentally made too permissive, creating a compliance violation). AWS IAM and GitHub Actions provide no integration that would surface drift between the configured trust policy and the actual repositories/branches that workflows assume the role from, no alerts when trust policy changes would break existing workflows, and no detection of when a role's trust policy has drifted from its intended baseline.

**Target Market:** Platform engineering teams at mid-large companies with GitHub Actions CI/CD pipelines using OIDC to access AWS resources (S3, DynamoDB, ECS, Lambda deployments), multi-account AWS setups, and strict security/compliance requirements for least-privilege IAM.

**Technical Architecture:**
- Python/Go collector via AWS IAM API (get role, get role policy, get OpenID Connect provider attributes) + GitHub API (workflow files, workflow runs, OIDC token audience claims) + AWS CloudTrail (role assumption events, policy change events)
- OIDC trust policy baseline engine: for each IAM role with a GitHub OIDC trust policy, captures the baseline configuration (allowed GitHub orgs, repositories, branch patterns, audience claims), tracks trust policy revision history
- Trust policy drift detector: compares current trust policy against baseline, flags unauthorized changes (new org/repo/branch added or removed), distinguishes intentional safe changes from accidental breakage, calculates which GitHub workflows would break with the new policy
- Overly permissive trust policy analyzer: detects trust policies that grant access to `*` repos or `*` branches within an org (common after incident hotfixes), flags compliance violations, correlates with security findings from AWS Security Hub
- Workflow assumption audit trail: uses CloudTrail to track which repositories and workflow runs actually assumed each role over time, builds a usage fingerprint per role, alerts if a trust policy change would affect workflows that have been observed assuming that role
- GitHub + AWS CloudTrail + IAM API → PostgreSQL + Grafana: OIDC trust policy drift timeline per role, permissive policy violations heatmap, affected workflow count per trust policy change, compliance posture score
- Alerting: Slack with "⚠️ IAM Role `github-actions-deploy-prod` trust policy changed 4 hours ago by `jane@company.com`. Removed repo `acme/old-monorepo` from allowed list. Workflow `deploy-prod.yml` (acme/frontend#main, 47 runs/week) has been assuming this role and will now fail. 3 other workflows (`backend-deploy.yml`, `db-migrate.yml`, `infra-plan.yml`) also depend on this role — verify they are from allowed repos. Policy now allows: acme/frontend, acme/backend, acme/infra. Restore old repo or update workflow to use a dedicated role for old-monorepo deployments."

**Why >$10k/mo:** 12 companies × $800-1700/mo. Prevents silent production deployment failures from IAM trust policy drift, eliminates compliance audit findings from overly permissive OIDC trust policies, reduces mean-time-to-resolution for workflow auth failures from hours to minutes.
**Capex:** ~$8k. **Infra:** ~$50/mo. **Effort:** <2 hrs/week.
**Competitors:** AWS IAM console shows trust policy documents but doesn't detect drift from baseline, correlate trust policy changes with actual workflow usage from CloudTrail, or alert when a change would break existing GitHub Actions workflows. GitHub Actions shows job failures but doesn't surface the IAM configuration change that caused them.

