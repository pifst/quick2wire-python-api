
from contextlib import closing
from itertools import islice
from quick2wire.selector import Selector, INPUT, OUTPUT, ERROR, Semaphore


def test_selector_is_a_convenient_api_to_epoll():
    with closing(Semaphore(blocking=False)) as ev1, \
         closing(Selector()) as selector:
        
        selector.add(ev1, INPUT)
        
        ev1.signal()
        
        selector.wait()
        assert selector.ready == ev1
        assert selector.has_input == True
        assert selector.has_output == False
        assert selector.has_error == False
        assert selector.has_hangup == False
        assert selector.has_priority_input == False

        
def test_selecting_from_multiple_event_sources():
    with closing(Semaphore(blocking=False)) as ev1, \
         closing(Semaphore(blocking=False)) as ev2, \
         closing(Selector()) as selector:
        
        selector.add(ev1, INPUT)
        selector.add(ev2, INPUT)
        
        ev1.signal()
        ev2.signal()
        
        selector.wait()
        first = selector.ready
        first.receive()
        
        selector.wait()
        second = selector.ready
        second.receive()
        
        assert first in (ev1, ev2)
        assert second in (ev1, ev2)
        assert first is not second
        
        
def test_can_use_a_different_value_to_identify_the_event_source():
    with closing(Semaphore(blocking=False)) as ev1, \
         closing(Selector()) as selector:
        
        selector.add(ev1, INPUT, identifier=999)
        
        ev1.signal()
        
        selector.wait()
        assert selector.ready == 999

        
def test_can_wait_with_a_timeout():
    with closing(Semaphore(blocking=False)) as ev1, \
         closing(Selector()) as selector:
        
        selector.add(ev1, INPUT, identifier=999)
        
        selector.wait(timeout=0)
        assert selector.ready == None


def test_can_remove_source_from_selector():
    with closing(Semaphore(blocking=False)) as ev1, \
         closing(Selector()) as selector:
        
        selector.add(ev1, INPUT)
        
        ev1.signal()
        
        selector.wait(timeout=0)
        assert selector.ready == ev1
        
        selector.remove(ev1)
        
        selector.wait(timeout=0)
        assert selector.ready == None