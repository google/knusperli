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

import os
import sys
import subprocess

cjpeg_dirs = ('cjpeg_30', 'cjpeg_70', 'cjpeg_78', 'cjpeg_90', 'cjpeg_95')


def iterate_pngs(directory):
  for root, dirs, files in os.walk(directory, followlinks=True):
    for f in files:
      if f.endswith('.png'):
        yield os.path.join(root, f)


def create_output_dirs(directory):
  for cdir in cjpeg_dirs:
    try:
      os.makedirs(os.path.join(directory, cdir))
    except:
      pass


def compress(cjpeg, src_file, dst_file, quality):
  cmdline = [cjpeg, '-quality', str(quality), src_file]
  jpeg_data = subprocess.check_output([x.encode('utf-8') for x in cmdline])

  with open(dst_file, 'wb') as f:
    f.write(jpeg_data)


def decompress(knusperli, src_file, dst_file):
  cmdline = [knusperli, src_file, dst_file]
  return subprocess.Popen(
      [x.encode('utf-8') for x in cmdline], stdout=subprocess.DEVNULL)


def compare(butteraugli, orig_file, compressed_file):
  """Runs Butteraugli to compare the original and compressed file."""
  cmdline = [butteraugli, orig_file, compressed_file, compressed_file + '.ppm']
  return subprocess.Popen(
      [x.encode('utf-8') for x in cmdline], stdout=subprocess.PIPE)


def print_stats(label, values):
  values = sorted(values)
  median = (
      values[int(len(values) / 2)] + values[int(len(values) / 2) - 1]) / 2.0
  print('{} min: {:.3}, median: {:.3}, max: {:.3}'.format(
      label, min(values), median, max(values)))


def main():
  """Usage: ./compare.py input_directory output_directory

  The program expects the following programs to exist on the PATH:

      cjpeg
      knusperli
      butteraugli

  All of these can be overridden with the environment variables CJPEG,
  KNUSPERLI, and BUTTERAUGLI.
  """

  if len(sys.argv) != 3:
    sys.exit(main.__doc__)

  input_dir = sys.argv[1]
  output_dir = sys.argv[2]
  cjpeg = os.getenv('CJPEG', 'cjpeg')
  knusperli = os.getenv('KNUSPERLI', 'knusperli')
  butteraugli = os.getenv('BUTTERAUGLI', 'butteraugli')

  create_output_dirs(output_dir)

  # Run all the decompress and compare programs concurrently, and store the
  # process handle (Popen) in a list so we can wait for all to complete.
  procs_jpeg = []
  procs_knus = []

  for input_png in iterate_pngs(input_dir):
    print(input_png)
    input_png_basename = os.path.basename(input_png)
    fnames = [
        os.path.join(output_dir, dirname, input_png_basename)
        for dirname in cjpeg_dirs
    ]
    jpg_fnames = [os.path.splitext(fname)[0] + '.jpg' for fname in fnames]
    # Note: for a quality of 80, mozjpeg produces an RGB file (rather than a
    # YCbCr file), which Knusperli does not handle, so pick 78 instead.
    for i, quality in enumerate((30, 70, 78, 90, 95)):
      compress(cjpeg, input_png, jpg_fnames[i], quality)

    for i in range(len(fnames)):
      proc_decompress = decompress(knusperli, jpg_fnames[i], fnames[i])
      procs_jpeg.append(compare(butteraugli, input_png, jpg_fnames[i]))
      # Wait untill decompression is complete before we can compare its output.
      proc_decompress.wait()
      procs_knus.append(compare(butteraugli, input_png, fnames[i]))

  # Wait for all processes to complete and collect the Butteraugli scores.
  scores_jpeg = []
  scores_knus = []

  for proc in procs_jpeg:
    proc.wait()
    scores_jpeg.append(float(proc.stdout.read()))

  for proc in procs_knus:
    proc.wait()
    scores_knus.append(float(proc.stdout.read()))

  scores_diff = [jpeg - knus for jpeg, knus in zip(scores_jpeg, scores_knus)]

  print_stats('Jpeg scores:      ', scores_jpeg)
  print_stats('Knusperli scores: ', scores_knus)
  print_stats('Jpeg - Knusperli: ', scores_diff)


if __name__ == '__main__':
  main()
