from pc_monitoring.monitoring import Monitoring
import unittest
import sys
import os
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../src")


class TestServer(unittest.TestCase):
    def test_run(self):
        cls = Monitoring()
        cls.run()


if __name__ == '__main__':
    unittest.main()
