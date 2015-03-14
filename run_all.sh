# Run daemon
python get_twit_daemon.py &
# Run server
python server.py deploy >/dev/null 2>/dev/null
