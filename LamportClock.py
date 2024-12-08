"""
Author      : Trenton Hurd
Date        : 7 December 2024
Class       : CSCI-3601
"""

class LamportClock:
    def __init__(self):
        self.time = 0

    def increment(self):
        self.time += 1

    def update(self, received_time):
        self.time = max(self.time, received_time) + 1

    def get_time(self):
        return self.time
