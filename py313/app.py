import concurrent.futures
import datetime
import sys
import logging
import multiprocessing

logging.basicConfig(format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

cpus = multiprocessing.cpu_count()
pool_executor = (
    concurrent.futures.ProcessPoolExecutor
    if len(sys.argv) > 1 and sys.argv[1] == "1"
    else concurrent.futures.ThreadPoolExecutor
)
python_version_str = (
    f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
)
logger.info(
    f"Executor={pool_executor.__name__}, python={python_version_str}, cpus={cpus}"
)


def is_prime(n: int) -> bool:
    if n <= 1:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True


def count_primes(limit: int) -> int:
    return sum(1 for i in range(limit) if is_prime(i))


start = datetime.datetime.now()
with pool_executor(8) as executor:
    futures = [executor.submit(count_primes, 100000) for _ in range(8)]
    for future in concurrent.futures.as_completed(futures):
        future.result()
end = datetime.datetime.now()
elapsed = end - start
logger.info(f"Elapsed: {elapsed.total_seconds():.2f} seconds")
