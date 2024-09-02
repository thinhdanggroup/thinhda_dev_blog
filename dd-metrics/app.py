from datadog import initialize, statsd
import time

from datadog import initialize, statsd


def main():
    options = {"statsd_host": "127.0.0.1", "statsd_port": 8125}

    initialize(**options)
    statsd.enable_background_sender()

    while 1:
        statsd.increment("example_metric.increment", tags=["environment:dev"])
        statsd.decrement("example_metric.decrement", tags=["environment:dev"])
        statsd.set("example_metric.set", 100, tags=["environment:dev"])

        print("Sent metrics")
        statsd.flush()
        time.sleep(1)


if __name__ == "__main__":
    main()
