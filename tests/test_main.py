from futura import logger1, log, warn


def test_testing():
    print('Running tests...')
    assert True


def test_logging(caplog):
    message = 'Info'
    log(message)
    assert message in caplog.text


def test_warning(caplog):
    message = 'Warning'
    warn(message)
    assert message in caplog.text
