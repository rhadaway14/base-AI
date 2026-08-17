from app_domain.events import RUN_EVENT_ADAPTER


def test_event_contract_is_discriminated_and_round_trips() -> None:
    event = RUN_EVENT_ADAPTER.validate_python(
        {"type": "run.started", "run_id": "r1", "sequence": 0, "objective": "prove the seam"}
    )
    assert event.type == "run.started"
    assert event.sequence == 0
