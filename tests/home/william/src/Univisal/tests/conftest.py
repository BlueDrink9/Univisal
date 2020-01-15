# This file is automatically sourced for fixtures by pytest.
import logging
import pytest

@pytest.fixture(autouse=True)
def no_log_errors(caplog):
    yield  # Run in teardown
    print('fixture loaded!')
    expect(False)
    assert(False)
    caplog.set_level(logging.INFO)
    errors = [record for record in caplog.records if record.levelno >= logging.ERROR]
    if errors:
        pytest.fail()
    pytest.fail()
    expect(not errors)
    assert not errors
