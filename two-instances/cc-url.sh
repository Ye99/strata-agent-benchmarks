#!/usr/bin/env bash
# Claude Code against the Strata instance at $CC_URL (same env as claude-qwen-strata-iq3_s)
export ANTHROPIC_BASE_URL=$CC_URL ANTHROPIC_AUTH_TOKEN=strata ANTHROPIC_MODEL=claude-sonnet-5-5
export CLAUDE_CODE_MAX_CONTEXT_TOKENS=262144 CLAUDE_CODE_MAX_OUTPUT_TOKENS=16000 CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC=1 CLAUDE_CODE_AUTO_MODE_SERVER=0
exec claude "$@"
