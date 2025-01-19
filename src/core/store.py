class Store:
    def __init__(self, reducer, initial_state=None, middleware=None):
        self.state = initial_state or {}
        self.reducer = reducer
        self.middleware = middleware or []
        self.subscribers = []

    def dispatch(self, action):
        # Pass the action through middleware
        for mw in self.middleware:
            action = mw(self.state, action, self.dispatch)

        # Update the state using the reducer
        self.state = self.reducer(self.state, action)

        # Notify subscribers
        for subscriber in self.subscribers:
            subscriber(self.state)

    def get_state(self):
        return self.state

    def subscribe(self, callback):
        self.subscribers.append(callback)


# Reducer function
def root_reducer(state, action):
    state = state or {"player_position": [400, 300]}
    if action["type"] == "UPDATE_PLAYER_POSITION":
        return {**state, "player_position": action["position"]}
    return state


# Middleware functions
def logger_middleware(state, action, dispatch):
    print(f"Dispatching action: {action}")
    print(f"Current state: {state}")
    return action
