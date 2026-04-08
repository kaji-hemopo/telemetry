#!/bin/bash
# Titan Fit Research Agent Launcher
# Run this to spawn research agents for each phase

echo "=== TITAN FIT RESEARCH AGENT LAUNCHER ==="
echo "Business: Premium Western-sized basics for Japan"
echo "Timeline: 6-week deep research"
echo ""

# Phase 1: Market Validation
echo "Spawning Phase 1 Agent: Market Validation..."
openclaw sessions spawn \
  --runtime subagent \
  --agentId main \
  --label "TitanFit-Phase1-MarketValidation" \
  --task "Execute Phase 1 research from TITAN_FIT_RESEARCH_BLUEPRINT.md:
1. Web search analysis for 'big and tall Japan' trends
2. Competitor mapping (10+ websites)
3. Online community analysis (r/japanlife, expat forums)
4. Social media listening for clothing size issues
5. Market size estimation from Japanese government data
Deliver: Compiled data report by end of Week 2" \
  --mode run \
  --timeoutSeconds 604800  # 7 days

echo ""
echo "Phase 1 agent launched. Check sessions list for progress."
echo ""
echo "To launch Phase 2 (after Phase 1 completes):"
echo "openclaw sessions spawn --runtime subagent --agentId main --label 'TitanFit-Phase2-SolutionValidation' --task 'Execute Phase 2 research...' --mode run --timeoutSeconds 604800"
echo ""
echo "To monitor all research agents:"
echo "openclaw sessions list --kinds agent"