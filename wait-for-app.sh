#!/bin/sh

while ! curl -s http://app:8000/api/posts/health/ | grep "OK"; do
  echo "Waiting for app service for 10 seconds"
  sleep 10
done

echo "App service is ready."
