#!/bin/bash
cd /root/isowork/wt
MK8="tide=noncombatgainskill,breaker=unlockitemvariant,brand=marriageslotincrease,bw1=noncombatincreasereskins,bore=repair"
go(){ p=$1; o=$2; shift 2; TNR_ENGINE_SRC=/root/isowork/game/tnr TNR_ENGINE_PIN=3314d122c93e036618483d18229a793ad7ad21fd TNR_ENGINE_WORK=/root/isowork/engwork_live TNR_SCRIPT=isonade_v11.ts harness/skyglass_wreck_sim/run.sh --params /root/isowork/v11/p/$p.json --mk $MK8 --seeds ${SEEDS:-12} --read ${READS:-1,0.85} "$@" --out /root/isowork/v11/out/$o.json > /root/isowork/v11/out/$o.log 2>&1; }
for v in "$@"; do go $v $v & done
wait; echo ALLDONE
