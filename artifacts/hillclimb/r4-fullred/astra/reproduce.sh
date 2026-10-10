#!/bin/sh
# Run only the newly written independent verifiers, from this directory.
set -eu
python3 -I live_audit.py small > live_small.out
python3 -I live_audit.py literal > live_literal.out
python3 -I live_audit.py extended > live_extended.out
python3 -I live_audit.py random > live_random.out
python3 -I lp_audit_exact.py > lp_audit_exact.out
python3 -I lp_audit_general.py > lp_audit_general.out
python3 -I triangle_audit_exact.py > triangle_audit_exact.out
python3 -I triangle_audit_additional.py > triangle_audit_additional.out
python3 -I triangle_audit_fans.py > triangle_audit_fans.out
python3 -I triangle_audit_padding.py > triangle_audit_padding.out
python3 -I fourcycle_check.py dual > fourcycle_dual.out
python3 -I fourcycle_check.py small random arcs grid > fourcycle_tests.out
python3 -I fourcycle_extra.py > fourcycle_extra.out
python3 -I engine_audit.py > engine_audit.out
python3 -I engine_review_exact.py > engine_review_exact.out
