#!/bin/bash

DIRNAME="supercop/crypto_kem/"

mkdir -p $DIRNAME/ntruhrss701/neon
rsync --archive --copy-links --recursive neon-hrss701/ $DIRNAME/ntruhrss701/neon

mkdir -p $DIRNAME/ntruhps2048509/neon
rsync --archive --copy-links --recursive neon-hps2048509/ $DIRNAME/ntruhps2048509/neon

mkdir -p $DIRNAME/ntruhps2048677/neon
rsync --archive --copy-links --recursive neon-hps2048677/ $DIRNAME/ntruhps2048677/neon

mkdir -p $DIRNAME/ntruhps4096821/neon
rsync --archive --copy-links --recursive neon-hps4096821/ $DIRNAME/ntruhps4096821/neon



tar czf supercop-ntru-$(date +"%Y%m%d").tar.gz DIRNAME