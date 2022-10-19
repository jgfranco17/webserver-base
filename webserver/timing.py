import time
from pydantic import BaseModel, validator

class TimeInterval(BaseModel):
    seconds: int
    minutes: int
    hours: int

    @validator("seconds")
    def seconds_validation(cls, s):
        if s < 0 or s > 59:
            raise ValueError("Seconds value must be between 0 and 59.")
        return s

    @validator("minutes")
    def minutes_validation(cls, m):
        if m < 0 or m > 59:
            raise ValueError("Minutes value must be between 0 and 59.")
        return m

    def __repr__(self):
        props = [
            f'seconds={self.seconds}',
            f'minutes={self.minutes}',
            f'hours={self.hours}'
        ]
        return f'<TimeInterval: {", ".join(props)}>'

    def __len__(self):
        return (self.hours*3600) + (self.minutes*60) + self.seconds

    def __str__(self):
        time_elapsed = []
        if self.hours:
            time_elapsed.append(f'{self.hours}h')
        if self.minutes:
            time_elapsed.append(f'{self.minutes}m')
        if self.seconds:
            time_elapsed.append(f'{self.seconds}s')

        return str(' '.join(time_elapsed))

    def __eq__(self, other):
        return len(self) == len(other)

    @classmethod
    def from_time_diff(cls, duration):
        d_hours = int(duration // 3600)
        d_minutes = int((duration - (d_hours * 3600)) // 60)
        d_seconds = int(round(duration - (d_hours * 3600) - (d_minutes * 60)))

        return cls(seconds=d_seconds, minutes=d_minutes, hours=d_hours)

