# -*- coding: utf-8 -*-
# Copyright (c) 2003, Taro Ogawa.  All Rights Reserved.
# Copyright (c) 2013, Savoir-faire Linux inc.  All Rights Reserved.
# Copyright (c) 2020, Michael hansen  All Rights Reserved.

# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# Lesser General Public License for more details.
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
# MA 02110-1301 USA

import re
import unittest
from decimal import Decimal
from math import floor, log10

swOnes = [
    "",
    "moja",  # 1
    "mbili",  # 2
    "tatu",  # 3
    "nne",  # 4
    "tano",  # 5
    "sita",  # 6
    "saba",  # 7
    "nane",  # 8
    "tisa",  # 9
]

swTens = [
    "",
    "kumi",  # 10
    "ishirini",  # 20
    "thelathini",  # 30
    "arobaini",  # 40
    "hamsini",  # 50
    "sitini",  # 60
    "sabini",  # 70
    "themanini",  # 80
    "tisini",  # 90
]

swBig = [
    "",
    "",
    "mia",  # 1e2
    "elfu",  # 1e3
    "",
    "laki",  # 1e5
    "milioni",  # 1e6
    "",
    "",
    "bilioni",  # 1e9
]

swSeperator = " na "


class Num2Word_SW(object):
    errmsg_too_big = "Too large"
    max_num = 10 ** 36

    def __init__(self):
        self.number = 0

    def float2tuple(self, value):
        pre = int(value)

        # Simple way of finding decimal places to update the precision
        self.precision = abs(Decimal(str(value)).as_tuple().exponent)

        post = abs(value - pre) * 10 ** self.precision
        if abs(round(post) - post) < 0.01:
            # We generally floor all values beyond our precision (rather than
            # rounding), but in cases where we have something like 1.239999999,
            # which is probably due to python's handling of floats, we actually
            # want to consider it as 1.24 instead of 1.23
            post = int(round(post))
        else:
            post = int(math.floor(post))

        return pre, post, self.precision

    def cardinal3(self, number):
        if number < 10:
            return swOnes[number]

        if number < 100:
            x, y = divmod(number, 10)
            if y == 0:
                return swTens[x]

            return swTens[x] + swSeperator + swOnes[y]

        x = int(log10(number))
        y = number - pow(10, x)
        print(number, x, y)

        if y == 0:
            return swBig[x]

        return swBig[x] + " " + self.cardinal3(y)

    def cardinalPos(self, number):
        x = number
        res = ""
        for b in swBig:
            x, y = divmod(x, 1000)
            if y == 0:
                continue
            yx = self.cardinal3(y) + b
            if res == "":
                res = yx
            else:
                res = yx + swSeperator
        return res

    def fractional(self, number, l):
        if number == 5:
            return "نیم"
        x = self.cardinalPos(number)
        ld3, lm3 = divmod(l, 3)
        ltext = (farsiFrac[lm3] + " " + farsiFracBig[ld3]).strip()
        return x + " " + ltext

    def to_currency(self, value):
        return self.to_cardinal(value) + " shilingi"

    def to_ordinal(self, number):
        r = self.to_cardinal(number)
        raise NotImplementedError()

    def to_year(self, value):
        raise NotImplementedError()
        # return self.to_cardinal(value)

    def to_ordinal_num(self, value):
        raise NotImplementedError()

    def to_cardinal(self, number):
        if number < 0:
            raise NotImplementedError()

        if number == 0:
            return "sifuri"

        x, y, l = self.float2tuple(number)
        if y == 0:
            return self.cardinalPos(x)

        if x == 0:
            raise NotImplementedError()
            # return self.fractional(y, l)

        return self.cardinalPos(x) + swSeperator + self.fractional(y, l)


# -----------------------------------------------------------------------------


class SWTestCase(unittest.TestCase):
    def test_cardinal(self):
        test_cardinal = {
            21: "ishirini na moja",
            32: "thelathini na mbili",
            43: "arobaini na tatu",
            54: "hamsini na nne",
            65: "sitini na tano",
            76: "sabini na sita",
            87: "themanini na saba",
            98: "tisini na nane",
            200: "mia mbili",
            249: "mia mbili arobaini na tisa",
            300: "mia tatu",
            400: "mia nne",
            800: "mia nane",
            928: "mia tisa ishirini na nane",
            1_364: "elfu moja mia tatu sitini na nne",
            5_000: "elfu tano",
            8_723: "elfu nane mia saba ishirini na tatu",
            12_000: "elfu kumi na mbili",
            19_284: "elfu kumi na tisa mia mbili themanini na nne",
            53_981: "elfu hamsini na tatu, mia tisa themanini na moja",
            60_000: "elfu sitini",
            125_728: "laki moja elfu ishirini na tano mia saba ishirini na nane",
            400_000: "laki nne",
            500_200: "laki tano na mia mbili",
            7_000_000: "milioni saba",
        }

        conv = Num2Word_SW()

        for num, expected_words in test_cardinal.items():
            actual_words = conv.to_cardinal(num)
            self.assertEqual(actual_words, expected_words)


if __name__ == "__main__":
    unittest.main()
