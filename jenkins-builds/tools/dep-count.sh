#!/bin/bash
: ${1?"Usage: $0 jenkins-build-file"}
rm -rf deps.out
while read eb; do
      eb -D $eb | grep module | cut -f2 -d: | cut -f1 -d/ >> deps.out
  done <$1
cat deps.out | sort | uniq -c | sort -n
