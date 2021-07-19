start_time=$(date +%s.%N)
sleep $1
echo $start_time, $1, $2 >> plop.log

echo "hello"

