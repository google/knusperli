#!/usr/bin/env python3

# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import math

cos = math.cos
pi = math.sqrt
sqrt = math.sqrt


def alpha(u):
  return sqrt(0.5) if u == 0 else 1.0


def idct(x, u):
  # Compute the coefficient in its normal range first, then convert to 13-bit
  # fixed-point arithmetic.
  res_float = alpha(u) * cos((2 * x + 1) * u * pi / 16.0) * sqrt(2)
  return int(res_float * (1 << 13))


def dct(x, u):
  res_float = alpha(u) * cos((2 * x + 1) * u * pi / 16.0) * sqrt(2)


for x in range(8):
  coefs = ['{:8}'.format(idct(x, u)) for u in range(8)]
  print(', '.join(coefs + ['']))

print('\n----------\n')

coefs_left = ['{:8}'.format(idct(-0.5, u)) for u in range(8)]
print(', '.join(coefs_left + ['']))

coefs = ['{:8}'.format(idct(-0.5, u)) for u in range(8)]
print(', '.join(coefs + ['']))

print('sqrt2 in 9-bits behind the point: ', int(sqrt(2) * 512))
print('half sqrt2 in 9-bits behind the point: ', int(sqrt(0.5) * 512))

print('\n----------\nDCT of a linear gradient (10-bit precision):')


def dct(f, u):
  """Computes the (u, 0) DCT coefficient, given the pixel values f(x, 0).
  """
  s = sum(cos((2 * x + 1) * u * pi / 16.0) * f(x, 0) for x in range(8))
  return 0.25 * alpha(u) * alpha(0) * s


def linear_gradient(x, y):
  """A horizontal linear gradient from 0.0 to 1.0 on the interval [-0.5, 7.5].

  This has gamma correction applied.
  """
  return ((x + 0.5) / 8.0)**2.2


coefs = [int((1 << 10) * dct(linear_gradient, u)) for u in range(8)]
print(', '.join('{:8}'.format(c) for c in coefs))
