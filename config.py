
from typing import Dict


def load_config(fname: str) -> Dict[str, int]:
    "Return a dict representing config file 'fname'."
    d = {}
    with open(fname, 'rt') as cfg:
        for line in cfg:
            # Ignore comments and blank lines
            if line.startswith('#') or len(line) == 1:
                continue
            # Each ine should look like: NAME = VALUE
            flds = line.split('=')
            name = flds[0].strip()
            value = int(flds[1].strip())
            d[name] = value
    return d


# Just for testing

def main() -> None:
    d = load_config('tmp/config')
    for key in d:
        print(f'{key} = {d[key]}')


if __name__ == '__main__':
    main()
