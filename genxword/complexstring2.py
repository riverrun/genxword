# -*- coding: utf-8 -*-
from __future__ import unicode_literals

class ComplexString(unicode):
    accents = [768, 769, 770, 771, 772, 773, 774, 775, 776, 777, 778, 779, 780, 781,
            782, 783, 784, 785, 786, 787, 788, 789, 790, 791, 792, 793, 794, 795,
            796, 797, 798, 799, 800, 801, 802, 803, 804, 805, 806, 807, 808, 809,
            810, 811, 812, 813, 814, 815, 816, 817, 818, 819, 820, 821, 822, 823,
            824, 825, 826, 827, 828, 829, 830, 831, 832, 833, 834, 835, 836, 837,
            838, 839, 840, 841, 842, 843, 844, 845, 846, 847, 848, 849, 850, 851,
            852, 853, 854, 855, 856, 857, 858, 859, 860, 861, 862, 863, 864, 865,
            866, 867, 868, 869, 870, 871, 872, 873, 874, 875, 876, 877, 878, 879,
            2306, 2366, 2367, 2368, 2369, 2370, 2371, 2372, 2375, 2376, 2379,
            2380, 2402, 2403, 2433, 2492, 2494, 2495, 2496, 2497, 2498, 2499,
            2500, 2503, 2504, 2507, 2508, 2519, 2530, 2531, 3006, 3007, 3008,
            3009, 3010, 3014, 3015, 3016, 3018, 3019, 3020, 3021, 3031, 3633,
            3636, 3637, 3638, 3639, 3640, 3641, 3655, 3656, 3657, 3658, 3659,
            3660, 3661, 3662, 4139, 4140, 4141, 4142, 4143, 4144, 4145, 4146,
            4150, 4151, 4152, 4154, 4155, 4156, 4157, 4158, 4182, 4185]

    @staticmethod
    def format_word(word):
        chars = {unichr(n) for n in ComplexString.accents}
        formatted = []
        for letter in word:
            if letter in chars:
                formatted[-1] += letter
                continue
            formatted.append(letter)
        return formatted

    def __new__(cls, content):
        cs = super(ComplexString, cls).__new__(cls, content)
        cs.blocks = cls.format_word(content)
        return cs

    def __iter__(self):
        for block in self.blocks:
            yield block

    def __len__(self):
        return len(self.blocks)
