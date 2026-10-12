"""
Q9 - Threaded Job Scheduler Simulation

The assignment gives each job a resource requirement but does not specify
a global resource-capacity limit. Therefore resources are validated and
reported as job metadata, while worker availability controls scheduling.

A worker can execute one job at a time. At each scheduling event, the
highest-priority waiting job is assigned to the first available worker.
Ties use earlier arrival order.
"""
import heapq
import sys
from dataclasses import dataclass
from concurrent.futures import ThreadPoolExecutor


@dataclass
class Job:
    arrival: int
    job_id: str
    priority: int
    duration: int
    resources: int
    start: int = 0
    finish: int = 0
    worker: int = 0


def simulate(workers, jobs):
    jobs.sort(key=lambda j: (j.arrival, j.job_id))

    waiting = []
    running = []  # (finish_time, worker_id)
    available = list(range(1, workers + 1))
    heapq.heapify(available)

    time = 0
    next_job = 0
    completed = []

    while next_job < len(jobs) or waiting or running:
        if not waiting and not running and next_job < len(jobs):
            time = max(time, jobs[next_job].arrival)

        while next_job < len(jobs) and jobs[next_job].arrival <= time:
            job = jobs[next_job]
            heapq.heappush(
                waiting, (-job.priority, job.arrival, next_job, job)
            )
            next_job += 1

        # Finish all workers that are available at this simulated time.
        while running and running[0][0] <= time:
            finish, worker = heapq.heappop(running)
            heapq.heappush(available, worker)

        while waiting and available:
            _, _, _, job = heapq.heappop(waiting)
            worker = heapq.heappop(available)
            job.start = max(time, job.arrival)
            job.finish = job.start + job.duration
            job.worker = worker
            heapq.heappush(running, (job.finish, worker))
            completed.append(job)

        if running and (not available or waiting):
            time = running[0][0]
        elif next_job < len(jobs):
            time = max(time, jobs[next_job].arrival)
        elif running:
            time = running[0][0]

    # The sample output reports jobs in completion/assignment order. For
    # reproducibility, use start time, then worker, then job id.
    completed.sort(key=lambda j: (j.start, j.worker, j.job_id))
    return completed


def run(data):
    lines = [x.strip() for x in data.splitlines() if x.strip()]
    if not lines:
        raise ValueError("Empty input.")

    workers, n = map(int, lines[0].split())
    if workers < 1 or workers > 64:
        raise ValueError("workers must be in 1..64.")
    if len(lines) != n + 1:
        raise ValueError("Incorrect number of job records.")

    jobs = []
    for line in lines[1:]:
        arrival, job_id, priority, duration, resources = line.split()
        arrival, priority, duration, resources = map(
            int, (arrival, priority, duration, resources)
        )
        if arrival < 0 or duration <= 0 or resources <= 0:
            raise ValueError("Invalid job values.")
        jobs.append(Job(arrival, job_id, priority, duration, resources))

    result = simulate(workers, jobs)

    # Use a thread pool to model the final execution/report stage. The
    # scheduling itself is deterministic simulated time.
    with ThreadPoolExecutor(max_workers=workers) as executor:
        futures = [
            executor.submit(
                lambda j: (j.job_id, f"W{j.worker}", j.start, j.finish), job
            )
            for job in result
        ]
        report = [future.result() for future in futures]

    total_wait = sum(job.start - job.arrival for job in result)
    avg_wait = total_wait / len(result) if result else 0.0

    lines_out = [
        f"{job_id} {worker} {start} {finish}"
        for job_id, worker, start, finish in report
    ]
    lines_out.append(f"AVG_WAIT {avg_wait:.2f}")
    return "\n".join(lines_out)


def main():
    try:
        print(run(sys.stdin.read()))
    except (ValueError, IndexError) as exc:
        print(f"INPUT_ERROR: {exc}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
