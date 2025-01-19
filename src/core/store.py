# src/core/store.py


class Store:
    def __init__(self, reducer, initial_state, middleware=None):
        self.reducer = reducer
        self.state = initial_state
        self.middleware = middleware if middleware else []

    def get_state(self):
        return self.state

    def dispatch(self, action):
        # Let each middleware process the action
        for mw in self.middleware:
            mw(self, action)

        # Then reduce
        new_state = self.reducer(self.state, action)
        self.state = new_state
        return action


def logger_middleware(store, action):
    print(f"[LOGGER] Dispatching: {action}")
