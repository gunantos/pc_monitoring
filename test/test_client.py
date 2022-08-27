from pc_monitoring.monitoring import Monitoring


def main():
    try:
        cls = Monitoring()
        cls.start()
    except KeyboardInterrupt:
        print('exit')
        exit()


if __name__ == '__main__':
    main()
