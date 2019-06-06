import time

import redis
from flask import Flask
from itertools import islice

app = Flask(__name__)
cache = redis.Redis(host='redis', port=6379)


def get_hit_count():
    retries = 5
    while True:
        try:
            return cache.incr('hits')
        except redis.exceptions.ConnectionError as exc:
            if retries == 0:
                raise exc
            retries -= 1
            time.sleep(0.5)

#prime test function returns true if argument is prime, returns false if argument is not prime using AKS
def PrimeTest(n):
    if n == 2:
        return True
    if n == 3:
        return True
    if n % 2 == 0:
        return False
    if n % 3 == 0:
        return False
    i = 5
    w = 2
    while i*i <= n:
        if n % i == 0:
            return False
        i += w
        w = 6 - w
    return True

@app.route('/')
def hello():
    count = get_hit_count()
    return 'Hello World! I have been seen {} times.\n'.format(count), 200

@app.route('/isPrime/<int:prime>')
def isPrime(prime):
    if PrimeTest(prime):
        cache.sadd('primes',prime)
        return "{} is prime\n".format(prime), 200
    else:
        return "{} is not prime\n".format(prime), 200


@app.route('/primesStored')
def PrimeStored():
    dbPrimes = cache.smembers('primes')
    string = ""
    if len(dbPrimes) == 0:
        return "Database is empty\n"
    for var in dbPrimes:
        string += var.decode("utf-8")
        string += '\n'

    return string, 200


@app.route('/clear')
def Clear():
    cache.flushdb()
    return "Cleared database\n", 200