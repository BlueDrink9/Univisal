# This file is automatically sourced for fixtures by pytest.
import logging
import pytest
import univisal

@pytest.fixture(autouse=True)
def no_log_errors(caplog):
    yield  # Run in teardown
    print(caplog.records)
    caplog.set_level(logging.INFO)
    errors = [record for record in caplog.records if record.levelno >= logging.ERROR]
    assert not errors

@pytest.fixture(scope="function", autouse=True)
def clear_state():
    univisal.model.init_model()
