from ev3dev2.sound import Sound
from typing import List, Tuple

class SoundModule:
  def __init__(self, Simulator = False, debug = False):
    self.simulator = Simulator
    # Default to off if simulator is active
    self.active = not Simulator
    self.sound: Sound = None

    if not self.simulator:
      self.sound = Sound()

    self.Patterns = dict()

  def Enable(self):
    self.active = True

  def Disable(self):
    self.active = False

  def NewPattern(self, name: str, pattern: List[Tuple[str, str]], tempo = 120, delay = 0.05):
    self.Patterns[name] = (pattern, tempo, delay)

  def PlaySound(self, name: str, reverse=False):
    if self.active:
      song = self.Patterns[name]
      pattern = song[0]
      if reverse: pattern = reversed(pattern)
      self.sound.play_song(pattern, song[1], song[2])