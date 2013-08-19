#   File: utility.py

import math;

class Utility:

    # Function: locDist(loc1, loc2)
    # Returns the Euclidean distance between two points in 2D space.
    # Uses Pythagoras theorem to compute. If you do not *need* the
    # result square rooted, it is preferred that you use locDistSq
    # and square the comparator, as it is faster.
    @staticmethod
    def locDist(loc1, loc2):
        return math.sqrt( Utility.locDistSq(loc1, loc2) )

    @staticmethod
    def locDistSq(loc1, loc2):
        dx = loc1[0] - loc2[0]
        dy = loc1[1] - loc2[1]
        return ( (dx ** 2) + (dy ** 2) )

    #Returns the point on a line segment between p1 and p2 that is closest to
    #p3; if such a point exists, the distance to that point is also returned
    @staticmethod
    def getPointLineIntersect(p1, p2, p3):
        if(p1 != p2):
			# Simple geometry (best understood with a diagram):
			# - all points P3 on perpendicular passing through P1 satisfy: (P1P3).(P1P2) = 0
			# - all points P3 on perpendicular passing through P2 satisfy: (P1P3).(P1P2) = (P1P2).(P1P2)
			# - all points outside these perpendiculars satisfy: (P1P3).(P1P2) = (P1P2).(P1P2) + (P2P3).(P1P2) > (P1P2).(P1P2) (assumes (P2P3).(P1P2) > 0)
			# So for any point whose perpendicular to (P1P2) intersects inside segment [P1P2],
			# the scalar product (P1P3).(P1P2) divided by (P1P2)^2 is between 0 and 1
            u_top = ((p3[0] - p1[0])*(p2[0] - p1[0])) + ((p3[1] - p1[1])*(p2[1] - p1[1]))
            u_bot = Utility.locDistSq(p1, p2)
            u = (u_top * 1.0) / (u_bot * 1.0)
            if( 0 <= u <= 1 ):
                x = p1[0] + u*(p2[0] - p1[0])
                y = p1[1] + u*(p2[1] - p1[1])
                return ((x, y), Utility.locDist((x,y), p3))
            else:
                return (None, 0)
        else:
            return (None, 0)
