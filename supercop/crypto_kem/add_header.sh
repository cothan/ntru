#!/bin/bash 

SUB='neon_'

for file in ntruhps2048509/neon/*; do
    [ -e "$file" ] || continue
    if ! grep -q "neon_" <<< $file; then 
        echo -e "$(cat header)\n\n$(cat $file)" > $file
    fi
done 

for file in ntruhps2048677/neon/*; do
    [ -e "$file" ] || continue
    if ! grep -q "neon_" <<< $file; then 
        echo -e "$(cat header)\n\n$(cat $file)" > $file
    fi
done 

for file in ntruhps4096821/neon/*; do
    [ -e "$file" ] || continue
    if ! grep -q "neon_" <<< $file; then 
        echo -e "$(cat header)\n\n$(cat $file)" > $file
    fi
done 

for file in ntruhrss701//neon/*; do
    [ -e "$file" ] || continue
    if ! grep -q "neon_" <<< $file; then 
        echo -e "$(cat header)\n\n$(cat $file)" > $file
    fi
done 


echo -e "Duc Tri Nguyen (CERG George Mason University)" > ntruhps2048509/neon/implementors
echo -e "Duc Tri Nguyen (CERG George Mason University)" > ntruhps2048677/neon/implementors
echo -e "Duc Tri Nguyen (CERG George Mason University)" > ntruhps4096821/neon/implementors
echo -e "Duc Tri Nguyen (CERG George Mason University)" > ntruhrss701/neon/implementors

echo -e "aarch64\narmeabi\narm" > ntruhps2048509/neon/architectures
echo -e "aarch64\narmeabi\narm" > ntruhps2048677/neon/architectures
echo -e "aarch64\narmeabi\narm" > ntruhps4096821/neon/architectures
echo -e "aarch64\narmeabi\narm" > ntruhrss701/neon/architectures