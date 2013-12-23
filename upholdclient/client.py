__version__ = "1.1"

import platform
import json
import argparse
import datetime

import redis
import yaml

from upholdclient import msi, putfile


def log_success(r, task, started):
    success = {
        "computer": platform.node(),
        "task": task,
        "started": started,
        "finished": datetime.datetime.utcnow().isoformat()
    }
    r.rpush("tasklog", json.dumps(success))


def log_failure(r, task, started):
    failure = {
        "computer": platform.node(),
        "task": task,
        "started": started,
        "finished": datetime.datetime.utcnow().isoformat(),
        "error": True
    }
    r.rpush("tasklog", json.dumps(failure))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', action='version', version='uphold-client v'+__version__)
    parser.parse_args()

    modules = [msi, putfile]
    
    try:
        with open("uphold.txt") as config_file:
            config = yaml.load(config_file)
    except IOError:
        print "No uphold.txt file: exiting."
        return
    except yaml.YAMLError:
        print "uphold.txt not valid YAML: exiting."
        return

    redis_config = config.get("redis", {"host":"localhost", "port":6379})
    
    r = redis.StrictRedis(
        host=redis_config.get("host", "localhost"),
        port=redis_config.get("port", 6379))

    r.sadd("subscriptions", platform.node())

    task_json = r.lpop("tasks:"+platform.node())
    while task_json:
        task = json.loads(task_json)
        
        #execute task
        for module in modules:
            if module.validate(task):
                started = datetime.datetime.utcnow().isoformat()
                if module.call(task):
                    log_success(r, task, started)
                else:
                    log_failure(r, task, started)
                break

        #get next task
        task_json = r.lpop("tasks:"+platform.node())


