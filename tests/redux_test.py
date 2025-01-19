import unittest
from modules.redux import (
    Store,
    root_reducer,
    logger_middleware,
    transform_increment_middleware,
    get_counter,
)


class TestRedux(unittest.TestCase):
    def setUp(self):
        self.store = Store(
            reducer=root_reducer,
            initial_state={"counter": 0},
            middleware=[logger_middleware, transform_increment_middleware],
        )

    def test_initial_state(self):
        self.assertEqual(self.store.get_state(), {"counter": 0})

    def test_increment(self):
        self.store.dispatch({"type": "INCREMENT"})
        self.assertEqual(self.store.get_state()["counter"], 1)

    def test_decrement(self):
        self.store.dispatch({"type": "DECREMENT"})
        self.assertEqual(self.store.get_state()["counter"], -1)

    def test_reset(self):
        self.store.dispatch({"type": "RESET"})
        self.assertEqual(self.store.get_state()["counter"], 0)

    def test_transform_increment_middleware(self):
        self.store.dispatch({"type": "TRANSFORM_INCREMENT"})
        self.assertEqual(self.store.get_state()["counter"], 1)

    def test_subscriber(self):
        changes = []
        self.store.subscribe(lambda state: changes.append(state))
        self.store.dispatch({"type": "INCREMENT"})
        self.assertEqual(changes[-1], {"counter": 1})

    def test_selector(self):
        self.store.dispatch({"type": "INCREMENT"})
        self.store.dispatch({"type": "INCREMENT"})
        self.assertEqual(get_counter(self.store.get_state()), 2)


if __name__ == "__main__":
    unittest.main()
