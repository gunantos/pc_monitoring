from monitoring import Monitoring


def main():
    cls = Monitoring()
    cls.start()
    # or
    # await cls.run_async()


if __name__ == '__main__':
    main()
