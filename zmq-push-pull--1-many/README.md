# ZMQ Push/Pull

In this case we start 1 producer and 10 consumers in one network. They will make connection with ZMQ
over TCP protocol on port `5556` (setup in .env)

# Usage
```bash
# Build and run docker compose. Lookup for logs
make run
```
```bash
# Send 1000 random messages without timeout from 10 producers
make produce
```

```bash
# Custom produce usage
#  -n - pacakge number [default 1]
#  -t - timeout between messages [default 0]
./produce.sh -n 100 -t 1
```
