/*
 * Copyright 2016 Google Inc.
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 * http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

#include "quantize.h"

namespace knusperli {

bool QuantizeBlock(coeff_t block[kDCTBlockSize],
                   const int q[kDCTBlockSize]) {
  bool changed = false;
  for (int k = 0; k < kDCTBlockSize; ++k) {
    coeff_t coeff = Quantize(block[k], q[k]);
    changed = changed || (coeff != block[k]);
    block[k] = coeff;
  }
  return changed;
}

}  // namespace knusperli
