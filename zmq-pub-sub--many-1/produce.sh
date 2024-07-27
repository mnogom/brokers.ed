#!/bin/bash

# source: https://stackoverflow.com/a/14203146
while [[ $# -gt 0 ]]; do
  case $1 in
    -n|--package-number)
      PACKAGE_NUMBER="$2"
      shift
      shift
      ;;
    -t|--timeout)
      TIMEOUT="$2"
      shift
      shift
      ;;
    -*|--*)
      echo "Unknown option $1"
      exit 1
      ;;
  esac
done

if [ -z "$PACKAGE_NUMBER" ]; then
  PACKAGE_NUMBER=1
fi
if [ -z "$TIMEOUT" ]; then
  TIMEOUT=0
fi

export EXEC_COMMAND="true"
for CONTAINER in $(docker compose ps "producer" -q) ; do
  EXEC_COMMAND="$EXEC_COMMAND & docker exec -i $CONTAINER produce -n $PACKAGE_NUMBER -t $TIMEOUT"
done
eval $EXEC_COMMAND
