#!/usr/bin/python3
import matplotlib.pyplot as plt
from functools import total_ordering
import bisect as bs
from decimal import *

setcontext(ExtendedContext)

@total_ordering
class Point:
    def __init__(self, value1):
        if isinstance(value1, Point):
            self._x = Decimal(value1.x)
            self._y = Decimal(value1.y)
        elif isinstance(value1, (list, tuple)) and len(value1) == 2:
            self._x = Decimal(value1[0])
            self._y = Decimal(value1[1])
        else:
            raise ValueError('Enter a Point instance or a tuple or list of coordinates, x and y')

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, x1):
        self._x = Decimal(x1)

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, y1):
        self._y = Decimal(y1)

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
        self._line_y = Decimal(0)
        if isinstance(value1, Point) and isinstance(value2, Point):
            self._begin = Point(value1)
            self._end = Point(value2)
        elif isinstance(value1, (tuple, list)) and len(value1) == 4:
            self._begin = Point(value1[0:1])
            self._end = Point(value1[2:3])
        elif isinstance(value1, (tuple, list)) and len(value1) == 2 and isinstance(value2, (tuple, list)) and len(value2) == 2:
            self._begin = Point(value1)
            self._end = Point(value2)
        elif value1 is not None and value2 is not None and value3 is not None and value4 is not None :
            self._begin = Point((value1, value2))
            self._end = Point((value3, value4))
        else:
            raise ValueError("Enter the begin and end Point instances or four coordinates x1, y1, x2, y2")

        self.swap_check()


    def swap_check(self):
        if self.begin.x > self.end.x:
            print('SWAPPING')
            self.begin.x, self.end.x = self.end.x, self.begin.x
            self.begin.y, self.end.y = self.end.y, self.begin.y
        elif self.begin.x == self.end.x:
            if self.begin.y > self.end.y:
                print('SWAPPING')
                self.begin.x, self.end.x = self.end.x, self.begin.x
                self.begin.y, self.end.y = self.end.y, self.begin.y

    @property
    def begin(self):
        return self._begin

    @begin.setter
    def begin(self, value1):
        if isinstance(value1, Point):
            self._begin.x = Decimal(value1.x)
            self._begin.y = Decimal(value1.y)
        elif isinstance(value1, (tuple, list)) and len(value1) == 2:
            self._begin.x = Decimal(value1[0])
            self._begin.y = Decimal(value1[1])
        else:
            raise ValueError("Enter either a Point instance or an iterable with two coordinates, x and y")

        self.swap_check()

    @property
    def end(self):
        return self._end

    @end.setter
    def end(self, value1):
        if isinstance(value1, Point):
            self._end.x = Decimal(value1.x)
            self._end.y = Decimal(value1.y)
        elif isinstance(value1, (tuple, list)) and len(value1) == 2:
            self._end.x = Decimal(value1[0])
            self._end.y = Decimal(value1[1])
        else:
            raise ValueError("Enter either a Point instance or a list or tuple with two coordinates, x and y")

        self.swap_check()

    @property
    def begin_event(self):
        return Event(self.begin, 'B', self)

    @property
    def end_event(self):
        return Event(self.end, 'E', self)

    @property
    def line_y(self):
        return self._line_y

    # @line_y.setter
    # def line_y(self, value):
    #     a = (self.end.y - self.begin.y) / (self.end.x - self.begin.x)
    #     b = self.begin.y - a*self.begin.x
    #     self._line_y = a*value + b

    def set_line_y(self, value):
        if self.begin.x != self.end.x:
            a = (self.end.y - self.begin.y) / (self.end.x - self.begin.x)
            b = self.begin.y - a*self.begin.x
            self._line_y = a*Decimal(value) + b
        else:
            self._line_y = Decimal('Infinity')

    def __str__(self):
        return u"Segment %s -> %s" % (self._begin, self._end)

    def __repr__(self):
        return self.__str__()

    # ordering by y coordinate of line crossing
    def __eq__(self, other):
        #return self.begin.y == other.begin.y and self.begin.x == other.begin.x
        return self.line_y == other.line_y

    def __lt__(self, other):
        #return self.begin.y < other.begin.y or (self.begin.y == other.begin.y and self.begin.x < other.begin.x)
        return self.line_y < other.line_y


class Bott:
    def __init__(self):
        self.que = []   # event queue
        self.line = []  # segments which are crossed by the line
        self.segs = []  # list of segments
        self.cross_out = []  # list of crossections

        self.plot_line_ref = None
        self.min_y = None
        self.max_y = None
        self.min_x = None
        self.max_x = None

    def get_segments(self):
        with open('bentley_input') as f:
            lines = f.readlines()
            for line in lines:
                lin = line.strip()
                if lin.startswith('#') or len(lin) == 0:
                    continue
                numbers = lin.split()
                # print(numbers)
                self.segs.append(Segment(*numbers))

        w = [seg.begin.y for seg in self.segs] + [seg.end.y for seg in self.segs]
        h = [seg.begin.x for seg in self.segs] + [seg.end.x for seg in self.segs]
        self.min_y = min(w)
        self.max_y = max(w)
        self.max_x = max(h)
        self.min_x = min(h)

    def generate_segments(self):
        self.segs.append(Segment(1, 2, 4, 1))
        self.segs.append(Segment(2, 1, 9, 8))
        #self.segs.append(Segment(2, 1, 3, 3))
        self.segs.append(Segment(7, 0, 6, 5))
        #self.segs.append(Segment(4.5, 2.5, 7, 3))
        self.segs.append(Segment(2.5, 0.5, 7, 3))
        self.segs.append(Segment(2.5, 4, 7, 4))
        self.segs.append(Segment(7, 4, 9,8))
        self.segs.append(Segment(0.5, 4, 0.5, 6))
        self.segs.append(Segment(-1, 5, 2, 5))

        w = [seg.begin.y for seg in self.segs] + [seg.end.y for seg in self.segs]
        h = [seg.begin.x for seg in self.segs] + [seg.end.x for seg in self.segs]
        self.min_y = min(w)
        self.max_y = max(w)
        self.max_x = max(h)
        self.min_x = min(h)

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
            ix = Dx / D
            iy = Dy / D

            if min(seg1.begin.x, seg1.end.x) <= ix <= max(seg1.begin.x, seg1.end.x) and \
                min(seg1.begin.y, seg1.end.y) <= iy <= max(seg1.begin.y, seg1.end.y) and \
                min(seg2.begin.x, seg2.end.x) <= ix <= max(seg2.begin.x, seg2.end.x) and \
                min(seg2.begin.y, seg2.end.y) <= iy <= max(seg2.begin.y, seg2.end.y):
                ev = Event((ix, iy), 'C', seg1, seg2)
                print("Intersection: ", ev, seg1, seg2)
                return ev
        return None

    def get_right(self, seg):
        """
        finds a position after seg and returns the right neighbour of seg
        :param seg:
        :return:
        """
        i = bs.bisect(self.line, seg)
        if i != len(self.line):
            return self.line[i]
        else:
            return None

        # i = self.line.index(seg)
        # return self.line[i+1] if i+1 < len(self.line) else None
    def get_right_multiple(self, seg):
        i = bs.bisect(self.line, seg)
        if i != len(self.line):
            lr = [self.line[i], ]
            i += 1
            while i != len(self.line) and self.line[i].line_y == lr[0].line_y:
                lr.append(self.line[i])
                i += 1
            return lr
        return None

    def get_left(self, seg):
        """
        finds a position after seg and returns the left neighbour of seg
        :param seg:
        :return:
        """
        i = bs.bisect(self.line, seg)
        if i > 1:
            return self.line[i-2]
        else:
            return None

        # i = self.line.index(seg)
        # return self.line[i - 1] if i - 1 >= 0 else None

    def get_left_multiple(self, seg):
        i = bs.bisect(self.line, seg)
        if i > 1:
            lr = [self.line[i-2], ]
            i -= 1
            while i > 1 and self.line[i-2].line_y == lr[0].line_y:
                lr.append(self.line[i-2])
                i -= 1
            return lr
        return None


    def draw_seg(self, seg):
        plt.plot((seg.begin.x, seg.end.x), (seg.begin.y, seg.end.y))

    def draw_intersection(self, event):
        circle = plt.Circle((event.x, event.y), .5, color='k', clip_on=False, fill=False)
        plt.gcf().gca().add_artist(circle)

    def init_plot(self):
        plt.ion()
        plt.figure().add_subplot(1, 1, 1).set_aspect('equal')
        plt.ylim([float(self.min_y)-1, float(self.max_y)+1])
        plt.xlim([float(self.min_x)-1, float(self.max_x)+1])
        plt.show()
        for seg in self.segs:
            self.draw_seg(seg)
        plt.draw()

    def find_cross(self):
        self.init_plot()

        while len(self.que) > 0:
            e = self.que.pop(0)
            self.plot_line_ref, = plt.plot([e.x, e.x], [self.min_y-1, self.max_y+1], color='k')
            plt.draw()

            if e.ev_type == 'B':
                for seg in self.segs:
                    seg.set_line_y(e.x)
                self.line = sorted(self.line)

                segE = e.seg1
                bs.insort(self.line, segE)
                #segA = self.get_right(segE)
                #segB = self.get_left(segE)
                segA = self.get_right_multiple(segE)
                segB = self.get_left_multiple(segE)
                if segA:
                    for seg in segA:
                        int1 = self.intersection(segE, seg)
                        if int1:
                            bs.insort(self.que, int1)

                if segB:
                    for seg in segB:
                        int2 = self.intersection(segE, seg)
                        if int2:
                            bs.insort(self.que, int2)

            elif e.ev_type == 'E':
                for seg in self.segs:
                    seg.set_line_y(e.x)
                self.line = sorted(self.line)

                segE = e.seg1
                segA = self.get_right_multiple(segE)
                segB = self.get_left_multiple(segE)
                i = bs.bisect_left(self.line, segE)
                if not(i != len(self.line) and self.line[i]):
                    raise Exception("Nenaslo")
                #i = self.line.index(segE)
                print("NAJITI ", i, self.line)
                del self.line[i]
                if segA and segB:
                    for sA in segA:
                        for sB in segB:
                            int1 = self.intersection(sA, sB)
                            if int1:
                                i = bs.bisect_left(self.que, int1)
                                if i == len(self.que) or int1 != self.que[i]:
                                    bs.insort(self.que, int1)

            else:
                self.cross_out.append(e)
                self.draw_intersection(e)
                plt.draw()

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

                for seg in self.segs:
                    seg.set_line_y(e.x)
                self.line = sorted(self.line)


            plt.pause(2)
            self.plot_line_ref.remove()
            plt.draw()

        print(self.line)

        return self.cross_out


if __name__ == '__main__':
    bot = Bott()

    bot.get_segments()
    #bot.generate_segments()
    bot.init_que()
    print(bot.segs)
    print(bot.que)
    print ("VYSLEDEK", bot.find_cross())
    input("Press enter to exit")

