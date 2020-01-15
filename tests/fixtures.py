import pytest
@pytest.fixture(autouse=True)
def no_log_errors(caplog):
    yield  # Run in teardown
    errors = [record for record in caplog.records if record.levelno >= logging.ERROR]
    assert not errors
