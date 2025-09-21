from pathlib import Path
from base_app.core.job_runner import JobRunner
from base_app.core.logging_config import setup_json_logger

def test_thread_job_and_logs(tmp_path):
    logger, logpath = setup_json_logger('suite', log_dir=str(tmp_path/'logs'))
    jr = JobRunner(log_dir=tmp_path/'logs')
    def add(a,b):
        return a+b
    h = jr.submit_thread(add, 2, 3)
    h.wait(2.0)
    assert h.done and h.result == 5
    assert (tmp_path/'logs'/'jobs.jsonl').exists()
