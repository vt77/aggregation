#!/bin/bash

nowtime=$(date +%s)


send_request(){
  payload="{\"timestamp\":$1,\"example1.com\":$2,\"example2.com\":$3,\"example3\":$4}"
  echo "Send : $payload"
  curl -X POST "http://127.0.0.1:5000/domains" -H "accept: application/json" -H "Content-Type: application/json" -d "$payload"
}


send_request $nowtime 10 30 44
let nowtime="$nowtime + 10"
send_request $nowtime 80 5 12

