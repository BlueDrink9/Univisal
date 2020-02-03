## Testing

Download [`pytest`](https://docs.pytest.org/en/latest/getting-started.html) using `pip install pytest`.

Run from the root repo dir using `python3 setup.py test`

## windows pipes

Currently is working, but very slow. Look at optimising opening and closing of pipes.
Also univisal occasionally gets stuck waiting for AHK to read pipe. Does AHK wait for something to be readable? No!

## Writing adapters

See [Writing adapters](docs/adapters.md) for more on adding and editing adapters.
