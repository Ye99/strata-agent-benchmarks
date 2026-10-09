#!/usr/bin/env bash
# Every starting state must fail and every reference solution must pass.
AB=$(cd "$(dirname "$0")" && pwd)
run() { local t=$1; local d; d=$(mktemp -d); /bin/cp -rf $AB/tasks/$t/start/. $d; shift; for s in "$@"; do eval "$s"; done; (cd $d && timeout 60 python3 $AB/tasks/$t/verify.py 2>&1 | tail -1 | cut -c1-200); }
echo "A start:"; run A_textstats
echo "A ref:";   run A_textstats "/bin/cp -f $AB/ref/A_textstats.py \$d/textstats.py"
echo "B start:"; run B_inventory
echo "B ref:";   run B_inventory "/bin/cp -f $AB/ref/B_inventory_inventory.py \$d/inventory.py" "/bin/cp -f $AB/ref/B_inventory_storage.py \$d/storage.py"
echo "C start:"; run C_rename
echo "C ref:";   run C_rename "bash $AB/ref/c_apply.sh \$d"
echo "D start:"; run D_report
echo "D ref:";   run D_report "bash $AB/ref/D_monthly_report_fix.sh \$d"
echo "E start:"; run E_wc
echo "E ref:";   run E_wc "/bin/cp -f $AB/ref/E_mini_wc.py \$d/mini_wc.py"
echo "F start:"; run F_expr
echo "F ref:";   run F_expr "/bin/cp -f $AB/ref/F_calc.py \$d/calc.py"
