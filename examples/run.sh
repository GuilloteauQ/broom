start_time=$(date +%s.%N)
sleep $1
echo $start_time, $1 >> plop.log

echo "hello"

