#!/usr/bin/python3
import matplotlib.pyplot as plt
from functools import total_ordering
import bisect as bs

# x = [1,2,3,4]
# y = [1,4,9,16]
# plt.plot(x, y)
# plt.plot([3,-1], [-2,-4])
# plt.show()


@total_ordering
class Point:
    def __init__(self, value1):
        if isinstance(value1, Point):
            self._x = value1.x
            self._y = value1.y
        elif isinstance(value1, (list, tuple)) and len(value1) == 2:
            self._x = value1[0]
            self._y = value1[1]
        else:
            raise ValueError('Enter a Point instance or a tuple or list of coordinates, x and y')

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, x1):
        self._x = x1

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, y1):
        self._y = y1

    def __str__(self):
        return u"<%s|%s>" % (self._x, self._y)

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __lt__(self, other):
        return self.x < other.x or (self.x == other.x and self.y < other.y)

@total_ordering
class Event(Point):
    def __init__(self, value, ev_type='B', segment1=None, segment2=None):
        if ev_type in ('B', 'E', 'C'):
            self.ev_type = ev_type
        else:
            raise ValueError("Unsupported event type. Use one of 'B', 'E', 'C'")
        self.seg1 = segment1
        self.seg2 = segment2
        super(Event, self).__init__(value)

    def __str__(self):
        return 'EV %s %s' % (super(Event, self).__str__(), self.ev_type)

    def __eq__(self, other):
        return self.x == other.x \
               and self.y == other.y \
               and self.ev_type == other.ev_type \
               and self.seg1 is other.seg1 \
               and self.seg2 is other.seg2

    def __lt__(self, other):
        #return self.x < other.x or (self.x == other.x and self.y < other.y)
        if self.x < other.x:
            return True
        if self.x == other.x:
            if self.y < other.y:
                return True

            if self.y == other.y:
                if self.ev_type == 'B' and other.ev_type == 'C':
                    return True
                if self.ev_type == 'B' and other.ev_type == 'E':
                    return True
                if self.ev_type == 'C' and other.ev_type == 'E':
                    return True

        return False


@total_ordering
class Segment:
    def __init__(self, value1, value2, value3=None, value4=None):
        if isinstance(value1, Point) and isinstance(value2, Point):
            self._begin = Point(value1)
            self._end = Point(value2)
        elif isinstance(value1, (tuple, list)) and len(value1) == 4:
            self._begin = Point(value1[0:1])
            self._end = Point(value1[2:3])
        elif isinstance(value1, (tuple, list)) and len(value1) == 2 and isinstance(value2, (tuple, list)) and len(value2) == 2:
            self._begin = Point(value1)
            self._end = Point(value2)
        elif value1 and value2 and value3 and value4:
            self._begin = Point((value1, value2))
            self._end = Point((value3, value4))
        else:
            raise ValueError("Enter the begin and end Point instances or four coordinates x1, y1, x2, y2")

    @property
    def begin(self):
        return self._begin

    @begin.setter
    def begin(self, value1):
        if isinstance(value1, Point):
            self._begin.x = value1.x
            self._begin.y = value1.y
        elif isinstance(value1, (tuple, list)) and len(value1) == 2:
            self._begin.x = value1[0]
            self._begin.y = value1[1]
        else:
            raise ValueError("Enter either a Point instance or an iterable with two coordinates, x and y")

    @property
    def end(self):
        return self._end

    @end.setter
    def end(self, value1):
        if isinstance(value1, Point):
            self._end.x = value1.x
            self._end.y = value1.y
        elif isinstance(value1, (tuple, list)) and len(value1) == 2:
            self._end.x = value1[0]
            self._end.y = value1[1]
        else:
            raise ValueError("Enter either a Point instance or a list or tuple with two coordinates, x and y")

    @property
    def begin_event(self):
        return Event(self.begin, 'B', self)

    @property
    def end_event(self):
        return Event(self.end, 'E', self)

    def __str__(self):
        return u"Segment %s -> %s" % (self._begin, self._end)

    def __repr__(self):
        return self.__str__()

    # ordering by y coordinate of the beginning
    def __eq__(self, other):
        return self.begin.y == other.begin.y and self.begin.x == other.begin.x

    def __lt__(self, other):
        return self.begin.y < other.begin.y or (self.begin.y == other.begin.y and self.begin.x < other.begin.x)


class Bott:
    def __init__(self):
        self.que = []   # event queue
        self.line = []  # segments which are crossed by the line
        self.segs = []  # list of segments
        self.cross_out = []  # list of crossections

    def get_segments(self):
        pass

    def generate_segments(self):
        self.segs.append(Segment(1, 2, 4, 1))
        self.segs.append(Segment(2, 1, 3, 3))

    def init_que(self):
        for seg in self.segs:
            bs.insort(self.que, seg.begin_event)
            bs.insort(self.que, seg.end_event)

    @staticmethod
    def line(seg):
        A = seg.begin.y - seg.end.y
        B = seg.end.x - seg.begin.x
        C = seg.end.x * seg.begin.y - seg.begin.x * seg.end.y
        return A, B, C

    @staticmethod
    def intersection(seg1, seg2):
        L1 = Bott.line(seg1)
        L2 = Bott.line(seg2)

        D  = L1[0] * L2[1] - L1[1] * L2[0]
        Dx = L1[2] * L2[1] - L1[1] * L2[2]
        Dy = L1[0] * L2[2] - L1[2] * L2[0]

        if D != 0:
            # float division, python 3 by default
            ev = Event((Dx / D, Dy / D), 'C', seg1, seg2)
            print("Intersection: ", ev)
            return ev
        else:
            return None

    def get_right(self, seg):
        """
        finds a position after seg and returns the right neighbour of seg
        :param seg:
        :return:
        """
        # i = bs.bisect(self.line, seg)
        # if i != len(self.line):
        #     return self.line[i]
        # else:
        #     return None

        i = self.line.index(seg)
        return self.line[i+1] if i+1 < len(self.line) else None

    def get_left(self, seg):
        """
        finds a position after seg and returns the left neighbour of seg
        :param seg:
        :return:
        """
        # i = bs.bisect(self.line, seg)
        # if i > 1:
        #     return self.line[i-2]
        # else:
        #     return None

        i = self.line.index(seg)
        return self.line[i - 1] if i - 1 >= 0 else None

    def find_cross(self):
        while len(self.que) > 0:
            e = self.que.pop(0)
            if e.ev_type == 'B':
                segE = e.seg1
                bs.insort(self.line, segE)
                segA = self.get_right(segE)
                segB = self.get_left(segE)
                if segA:
                    int1 = self.intersection(segE, segA)
                    if int1:
                        bs.insort(self.que, int1)
                if segB:
                    int2 = self.intersection(segE, segB)
                    if int2:
                        bs.insort(self.que, int2)

            elif e.ev_type == 'E':
                segE = e.seg1
                segA = self.get_right(segE)
                segB = self.get_left(segE)
                i = bs.bisect(self.line, segE)
                del self.line[i]
                int1 = self.intersection(segA, segB)
                if int1:
                    i = bs.bisect_left(self.que, int1)
                    if i == len(self.que) or int1 != self.que[i]:
                        bs.insort(self.que, int1)

            else:
                self.cross_out.append(e)
                if e.seg2 < e.seg1:
                    segE1 = e.seg1
                    segE2 = e.seg2
                else:
                    segE2 = e.seg1
                    segE1 = e.seg2
                i1 = bs.bisect_left(self.line, segE1)
                i2 = bs.bisect_left(self.line, segE2)
                if i1 == i2 == len(self.line):
                    raise Exception("Segments not found")
                self.line[i1], self.line[i2] = self.line[i2], self.line[i1]
                segA = self.line[i1+1] if len(self.line) < i1 - 2 else None
                segB = self.line[i2 - 1] if i2 > 0 else None
                if segA:
                    int1 = self.intersection(segA, segE2)
                    if int1:
                        i = bs.bisect_left(self.que, int1)
                        if i == len(self.que) or int1 != self.que[i]:
                            bs.insort(self.que, int1)
                if segB:
                    int2 = self.intersection(segB, segE1)
                    if int2:
                        i = bs.bisect_left(self.que, int2)
                        if i == len(self.que) or int2 != self.que[i]:
                            bs.insort(self.que, int2)
        print(self.line)
        return self.cross_out



if __name__ == '__main__':
    bot = Bott()

    bot.generate_segments()
    bot.init_que()
    print(bot.segs)
    print(bot.que)
    bot.find_cross()