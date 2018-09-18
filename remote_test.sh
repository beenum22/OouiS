echo "Deleting old tarball"
rm -rf remote_test.tar.xz
echo "Creating new tarball"
tar -cvJf remote_test.tar.xz Orion/ > /dev/null
echo "Transfering tarball to remote host"
scp remote_test.tar.xz cntl0:/home/heat-admin/ > /dev/null
ssh cntl0 "sudo tar xf /home/heat-admin/remote_test.tar.xz"
echo "Executing the program"
echo "=========================================="
ssh cntl0 "sudo /home/heat-admin/Orion/main.py --ip '127.0.0.1' --port '6640'"
