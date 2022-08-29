import numpy as np

def Bezier(point_list, t):
    if len(point_list)==1:
        return point_list[0]
    else:
        P1=Bezier(point_list[0:-1], t)
        P2=Bezier(point_list[1:], t)
        nt = 1. - t
        return (nt * P1[0] + t * P2[0], nt * P1[1] + t * P2[1])

def Progression(point_list):
  return [PointsToAngle(point_list[i], point_list[i+1]) for i in range(len(point_list) - 1)]

def PointsToAngle(start, end):
  dy = end[1] - start[1]
  dx = end[0] - start[0]

  o = np.rad2deg(np.arctan(dy/dx))
  if o < 0: o += 360
  return o


if __name__ == "__main__":
  points = [
    (0,0),
    (0.2, 1),
    (1.3, -0.2),
    (1,1)
  ]
  path = [Bezier(points, i) for i in np.linspace(0, 1, 51)]
  angles = Progression(path)
  for i in path: print(round(i[0],2), round(i[1],2))

  for i in angles: print(round(i,2))