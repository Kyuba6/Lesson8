import pytest
from src.models import Parameters, ApartmentEvent
from src.manager import Manager


def test_load_additional_data_and_unsolved_events():
    manager = Manager(Parameters())
    assert manager.apartment_events == []

    manager.load_additional_data()
    assert len(manager.apartment_events) > 0
    assert all(isinstance(e, ApartmentEvent) for e in manager.apartment_events)

    unsolved = manager.generate_apartment_events_report("apart-polanka", only_unsolved=True)
    assert len(unsolved) > 0
    assert all(not e.solved for e in unsolved)

    all_events = manager.generate_apartment_events_report("apart-polanka", only_unsolved=False)
    assert len(all_events) >= len(unsolved)
    assert all(e.apartment == "apart-polanka" for e in all_events)


def test_generate_apartment_events_report_invalid_apartment():
    manager = Manager(Parameters())
    manager.load_additional_data()

    with pytest.raises(ValueError):
        manager.generate_apartment_events_report("non-existing-apartment")
