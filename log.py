
log_file = None


def log_open(name: str) -> None:
    global log_file
    log_file = open(name, 'wt')
    log('START log')


def log_close() -> None:
    global log_file
    if log_file:
        log('END log')
        log_file.close()
        log_file = None
    else:
        assert False


def log(s: str) -> None:
    global log_file
    if log_file:
        print(s, file=log_file)
