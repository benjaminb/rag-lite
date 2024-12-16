echo "Heartbeat:"
curl -f "http://ec2-107-21-213-131.compute-1.amazonaws.com:8000/heartbeat"
echo ""

# echo "testing ask"
# curl -X POST "http://ec2-107-21-213-131.compute-1.amazonaws.com:8000/ask_question" \
#      -H "Content-Type: application/json" \
#      -d '{"body": "Does topology have any real-world applications?", "headers": {}}'
# echo ""

echo "testing ask"
curl -X POST "http://ec2-107-21-213-131.compute-1.amazonaws.com:8000/ask_question" \
     -H "Content-Type: application/json" \
     -d "$(jq -n --arg body "$(cat topology_prompt.txt)" '{"body": $body, "headers": {}}')"
echo ""