uphold-client
=============



The client for Uphold, a Windows administrative aid.

## Usage

Uphold is intended for deployment as two frozen Python executables. This one is a command-line program that gets tasks to be run from the Redis server every time it is run.

### Configuration

Uphold requires just information on where the Redis server is located. All other configuration is kept there.

That configuration information is currently supplied via a file in the working directory called `uphold.txt`. That file looks like this:

    redis:
        host: 192.168.1.35
        port: 6379

If this file is absent, Uphold will crash. `localhost` will be the default host and `6379` the default port if either or both or the `redis` block are missing.

### Recommended Setup

I setup Uphold so that each computer on my network runs Uphold once at midnight every night and also whenever the user locks the computer.

This makes it so that maintenance tasks are run at least once a day, but also means that if a user needs a fix right away it can be done sooner. Uphold is a small enough program that it is not a significant drain on resources when run every lock.

