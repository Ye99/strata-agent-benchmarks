cd "$1" && grep -rlE '\bcalc\b' --include=*.py --include=*.md . | xargs sed -i -E 's/\bcalc\b/compute_total/g'
