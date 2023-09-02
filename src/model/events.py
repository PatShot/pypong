# observer
subscribers = dict()

def subscribe(event_type, fn):
    if not event_type in subscribers:
        subscribers[event_type] = []
    subscribers[event_type].append(fn)

def post_event(event_type, data):
    if not event_type in subscribers:
        return
    for fn in subscribers[event_type]:
        fn(data)