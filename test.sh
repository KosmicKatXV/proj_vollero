#rm *.db
konsole -e python3 auth_server.py &
konsole -e python3 master.py &
for i in {0..3}
do
   let j=4000+i
   konsole -e python3 slave.py -p $j -d "slave$i.db" &
done
sleep 10
konsole -e python3 endpoint.py &