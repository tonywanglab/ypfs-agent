import threading

from harness import tasks


def test_claim_returns_none_on_empty_queue(pg):
    assert tasks.claim("worker-1") is None


def test_claim_orders_fifo_by_created_at(pg):
    first = tasks.enqueue(tasks.KIND_EXPERIMENT, {"query": "a"})
    second = tasks.enqueue(tasks.KIND_EXPERIMENT, {"query": "b"})
    claimed_first = tasks.claim("worker-1")
    claimed_second = tasks.claim("worker-1")
    assert claimed_first["task_id"] == first["task_id"]
    assert claimed_second["task_id"] == second["task_id"]
    assert tasks.claim("worker-1") is None


def test_claim_marks_running_and_bumps_attempts(pg):
    enqueued = tasks.enqueue(tasks.KIND_PROMPT_DRAFT, {"base_id": "prompt_v1"})
    claimed = tasks.claim("worker-1")
    assert claimed["task_id"] == enqueued["task_id"]
    assert claimed["status"] == "running"
    assert claimed["attempts"] == 1


def test_no_double_claim_under_concurrent_workers(pg):
    # The pg fixture's own get_thread_conn replacement already hands each
    # thread its own real connection (a closure-scoped threading.local), so
    # spawning plain threads here exercises real concurrent claiming safely.
    n_tasks = 20
    for i in range(n_tasks):
        tasks.enqueue(tasks.KIND_EXPERIMENT, {"query": f"q{i}"})

    claimed_ids = []
    lock = threading.Lock()

    def worker(name):
        while True:
            task = tasks.claim(name)
            if task is None:
                return
            with lock:
                claimed_ids.append(task["task_id"])

    threads = [threading.Thread(target=worker, args=(f"worker-{i}",)) for i in range(4)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    assert len(claimed_ids) == n_tasks
    assert len(set(claimed_ids)) == n_tasks


def test_heartbeat_and_set_progress_merge_fields(pg):
    enqueued = tasks.enqueue(tasks.KIND_EXPERIMENT, {"query": "q"})
    task_id = enqueued["task_id"]
    tasks.claim("worker-1")
    tasks.set_progress(task_id, phase="agent", current_sample=1, completed_samples=0, message="Running agent…")
    loaded = tasks.load(task_id)
    assert loaded["progress"] == {
        "phase": "agent",
        "current_sample": 1,
        "completed_samples": 0,
        "message": "Running agent…",
    }
    tasks.set_progress(task_id, phase="checks")
    loaded = tasks.load(task_id)
    assert loaded["progress"]["phase"] == "checks"
    assert loaded["progress"]["message"] == "Running agent…"


def test_set_run_and_finish(pg, make_run):
    run_id = make_run()
    enqueued = tasks.enqueue(tasks.KIND_EXPERIMENT, {"query": "q"})
    task_id = enqueued["task_id"]
    tasks.claim("worker-1")
    tasks.set_run(task_id, run_id)
    tasks.finish(task_id, result={"run_id": run_id})
    loaded = tasks.load(task_id)
    assert loaded["status"] == "finished"
    assert loaded["run_id"] == run_id
    assert loaded["result"] == {"run_id": run_id}
    assert loaded["error"] is None


def test_fail_sets_error_and_status(pg):
    enqueued = tasks.enqueue(tasks.KIND_PROMPT_DRAFT, {"base_id": "prompt_v1"})
    task_id = enqueued["task_id"]
    tasks.claim("worker-1")
    tasks.fail(task_id, "OPENROUTER_API_KEY is not set.")
    loaded = tasks.load(task_id)
    assert loaded["status"] == "failed"
    assert loaded["error"] == "OPENROUTER_API_KEY is not set."
    assert loaded["finished_at"] is not None


def test_load_missing_task_raises(pg):
    import pytest
    with pytest.raises(FileNotFoundError):
        tasks.load("task_000000000000")


def test_list_active_excludes_finished_and_failed(pg):
    # claim() is strictly oldest-first, so enqueue the one that should stay
    # "queued" last — otherwise it would always be the one claimed first.
    running_task = tasks.enqueue(tasks.KIND_EXPERIMENT, {"query": "running"})
    finished_task = tasks.enqueue(tasks.KIND_EXPERIMENT, {"query": "finished"})
    failed_task = tasks.enqueue(tasks.KIND_EXPERIMENT, {"query": "failed"})
    queued = tasks.enqueue(tasks.KIND_EXPERIMENT, {"query": "queued"})

    claimed_running = tasks.claim("worker-1")
    claimed_finished = tasks.claim("worker-1")
    claimed_failed = tasks.claim("worker-1")
    assert claimed_running["task_id"] == running_task["task_id"]
    assert claimed_finished["task_id"] == finished_task["task_id"]
    assert claimed_failed["task_id"] == failed_task["task_id"]

    tasks.finish(finished_task["task_id"], result={})
    tasks.fail(failed_task["task_id"], "boom")

    active_ids = {t["task_id"] for t in tasks.list_active()}
    assert active_ids == {queued["task_id"], running_task["task_id"]}


def test_requeue_stale_returns_to_queue_under_max_attempts(pg):
    enqueued = tasks.enqueue(tasks.KIND_EXPERIMENT, {"query": "q"})
    task_id = enqueued["task_id"]
    tasks.claim("worker-1")
    from harness import dbio
    dbio.execute(
        "UPDATE tasks SET heartbeat_at = now() - interval '1000 seconds' WHERE task_id = %s",
        (task_id,),
    )
    requeued = tasks.requeue_stale(timeout_s=120, max_attempts=3)
    assert requeued == 1
    loaded = tasks.load(task_id)
    assert loaded["status"] == "queued"
    assert loaded["attempts"] == 1


def test_requeue_stale_fails_past_max_attempts(pg):
    enqueued = tasks.enqueue(tasks.KIND_EXPERIMENT, {"query": "q"})
    task_id = enqueued["task_id"]
    from harness import dbio

    for _ in range(3):
        tasks.claim("worker-1")
        dbio.execute(
            "UPDATE tasks SET heartbeat_at = now() - interval '1000 seconds' WHERE task_id = %s",
            (task_id,),
        )
        tasks.requeue_stale(timeout_s=120, max_attempts=3)

    loaded = tasks.load(task_id)
    assert loaded["status"] == "failed"
    assert loaded["attempts"] == 3
    assert "heartbeat timeout" in loaded["error"]
    assert loaded["finished_at"] is not None


def test_requeue_stale_leaves_healthy_running_tasks_alone(pg):
    enqueued = tasks.enqueue(tasks.KIND_EXPERIMENT, {"query": "q"})
    task_id = enqueued["task_id"]
    tasks.claim("worker-1")
    assert tasks.requeue_stale(timeout_s=120, max_attempts=3) == 0
    assert tasks.load(task_id)["status"] == "running"
