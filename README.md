# Mockingbard
Use Markov chains to generate real-ish looking gibberish from Campfire logs or any plain-text input.

## Requires
[pystache](https://github.com/defunkt/pystache)
[pinder](https://github.com/rhymes/pinder)

## Usage
    Usage: campfire.py [options]

    Options:
      -h, --help            show this help message and exit
      -t TOKEN, --token=TOKEN
                            Your Campfire API auth token
      -d DOMAIN, --domain=DOMAIN
                            Campfire subdomain to use
      -r ROOM, --room=ROOM  Name of room to use
      -n DAYS, --num_days=DAYS
                            Number of days to go back for source material.
      -o ORDER, --order=ORDER
                            Order of markov chain to use. Defaults to 2.
      -i IGNORE, --ignore=IGNORE
                            Comma separated names of users to ignore.
