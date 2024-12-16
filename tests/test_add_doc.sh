echo "Heartbeat:"
curl -f "http://ec2-107-21-213-1318.compute-1.amazonaws.com:8000/heartbeat"
echo ""

echo "testing add document"
curl -X POST "http://ec2-107-21-213-131.compute-1.amazonaws.com:8000/add_document" -H "Content-Type: application/json" -d @topology_event.json
echo ""