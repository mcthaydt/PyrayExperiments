import unittest
from src.core.store import (
    Store,
    root_reducer,
    logger_middleware,
)


class TestRedux(unittest.TestCase):
    def setUp(self):
        self.store = Store(
            reducer=root_reducer,
            initial_state={"counter": 0},
            middleware=[logger_middleware],
        )

    def test_initial_state(self):
        self.assertEqual(self.store.get_state(), {"counter": 0})


if __name__ == "__main__":
    unittest.main()
