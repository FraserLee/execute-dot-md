# print the first few prime numbers separated by dashes
for ((i=2; i<37; i++)); do
    for ((j=2; j<i; j++)); do
        if (($i % $j == 0)); then break; fi
    done
    if (($i == $j)); then echo -n $i"-"; fi
done

# then finish off a few more with awk
awk 'BEGIN { RS = " "; ORS = "|" } {
    for (i=2; i<$1; i++) {
        if ($1 % i == 0) break
        if ($1 == i+1) print $1
    }
} END { ORS = "\n"; print "" }' <<< $(seq 37 100)