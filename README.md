# Broom

A simple, local parameter sweep runner

## Usage


```yaml
script_path: PATH_TO_YOUR_SCRIPT
max_concurrent_expe: NUMBER_OF_JOBS_RUNNING_CONCURRENTLY
sleep_time: TIME_IN_SECS_BETWEEN_TERMINATION_CHECKS
params:
  - PARAMS1
  - ...
  - PARAMSN
```

It will call `PATH_TO_YOUR_SCRIPT` with `PARAMSI`.

`broom` will go through all the parameters in a queue fashion, if one fails, it is pushed at the end of the queue.

It will not stop until all the jobs are executed.

