# Batched rollout inference

`BatchedInferenceServer` is a local `torch.multiprocessing` process.  It is the
only rollout-side process that owns policy models and CUDA memory.

Each rollout worker sends `InferenceRequest(state, mask, config_path,
restore_step)` through one shared request queue and waits on its own response
queue.  The server gathers requests for `max_wait_ms` or until
`max_batch_size`, groups requests with the same model checkpoint, and executes
one batched forward pass per group.

The learner continues to receive completed trajectories through the existing
`Info_Communication.data_queue`.  After each learner update it sends a
`PolicyUpdate` control message; the server reloads that checkpoint before
serving later requests.

The service caches up to `max_cached_policies` model checkpoints.  This lets
multiple opponent snapshots share one GPU model without creating one model per
environment.
