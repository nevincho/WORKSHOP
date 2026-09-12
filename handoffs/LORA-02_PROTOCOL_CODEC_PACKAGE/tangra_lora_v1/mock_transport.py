from collections import deque
class MockByteTransport:
    def __init__(self): self._q=deque()
    def send(self, packet: bytes): self._q.append(bytes(packet))
    def receive(self): return self._q.popleft() if self._q else None
    def __len__(self): return len(self._q)
