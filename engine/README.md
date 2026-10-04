# engine/ · the LLM layer the agents run on

- `claude.py`: the Claude provider behind the `Model` interface.
- `failover.py`: switches to a backup model when the primary is slow or fails (the duelist's 8 s budget).
