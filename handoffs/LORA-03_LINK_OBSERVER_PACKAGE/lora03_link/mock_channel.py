from __future__ import annotations
from collections import deque
from typing import Deque, Iterable
class ScriptedMockChannel:
    def __init__(self): self._q:Deque[bytes]=deque()
    def send(self,packet:bytes)->None: self._q.append(bytes(packet))
    def drop(self,packet:bytes)->None: _=packet
    def duplicate(self,packet:bytes,count:int=2)->None:
        if count<1: raise ValueError('count')
        for _ in range(count): self._q.append(bytes(packet))
    def corrupt(self,packet:bytes,index:int=-3,mask:int=0x01)->None:
        b=bytearray(packet)
        if b: b[index]^=mask
        self._q.append(bytes(b))
    def reorder(self,packets:Iterable[bytes],order:Iterable[int])->None:
        p=[bytes(x) for x in packets]
        for i in order: self._q.append(p[i])
    def receive(self)->bytes|None: return self._q.popleft() if self._q else None
    def __len__(self)->int: return len(self._q)
