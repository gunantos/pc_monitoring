from src.socket_monitoring.monitoring import Monitoring


def main():
    cls = Monitoring()
    cls.run()
    # or
    # await cls.run_async()


if __name__ == '__main__':
    main()
