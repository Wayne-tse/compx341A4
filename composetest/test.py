import unittest


target = __import__("app.py")

isprime = target.isPrime
sys.exit(1)
