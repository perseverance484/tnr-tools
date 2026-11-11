"""One activity per file. Each registers itself with player.registry.REGISTRY when it is imported; the brain only
runs what is registered, and no activity reads another's private state (the world model is the shared store)."""
