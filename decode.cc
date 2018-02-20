// Copyright 2018 Google LLC
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//      http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

#include <cassert>
#include <fstream>
#include <sstream>

#include "lodepng.h"
#include "jpeg_data.h"
#include "jpeg_data_decoder.h"
#include "jpeg_data_reader.h"

using knusperli::DecodeJpegToRGB;
using knusperli::JPEGData;
using knusperli::JPEG_READ_ALL;
using knusperli::ReadJpeg;

int main(int argc, char** argv) {
  if (argc != 3) {
    printf("Usage: knusperli <input.jpg> <output.png>\n");
    return 1;
  }

  std::ifstream in_file(argv[1]);
  if (!in_file.good()) {
    printf("Failed to open input file.\n");
    return 1;
  }
  std::stringstream in_data;
  in_data << in_file.rdbuf();

  JPEGData jpg;
  std::vector<uint8_t> rgb;

  bool read_ok = ReadJpeg(in_data.str(), JPEG_READ_ALL, &jpg);
  if (!read_ok) {
    printf("Error reading jpeg data from input file.\n");
    return 1;
  }
  rgb = DecodeJpegToRGB(jpg);
  if (rgb.empty()) {
    printf("Failed to decode.\n");
    return 1;
  }

  unsigned int write_error =
      lodepng_encode24_file(argv[2], &rgb[0], jpg.width, jpg.height);
  if (write_error != 0) {
    printf("Failed to write png.\n");
    return 1;
  }
}
