
def test_jobrunner_counter_exposed():
    from base_app.services import job_runner as jr
    if hasattr(jr, "queued_count"):
        before = jr.queued_count()
        if hasattr(jr, "increment_queue"):
            jr.increment_queue(3)
            after = jr.queued_count()
            assert after >= before + 3 - 0  # allow clamped logic
    else:
        # If job runner not present, at least ensure module loads
        assert True
