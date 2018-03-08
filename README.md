# Knusperli

The goal of Knusperli is to reduce blocking artifacts in decoded JPEG images, by
interpreting quantized DCT coefficients in the image data as an interval, rather
than a fixed value, and choosing the value from that interval that minimizes
discontinuities at block boundaries.

Left: a traditional JPEG decoder (Imagemagick 6.9.7-4). Right: Knusperli.

![Lena JPEG, zoomed][lena-jpeg-crop] ![Lena Knusperli, zoomed][lena-knus-crop]

![Lena JPEG][lena-jpeg] ![Lena Knusperli][lena-knus]

## Building

Knusperli builds with [Bazel][bazel]:

    CC=gcc bazel build :knusperli
    bazel-bin/knusperli input.jpg output.png

## Details

A JPEG encoder quantizes DCT coefficients by rounding coefficients to the
nearest multiple of the elements of the quantization matrix. For every
coefficient, there is an interval of values that would round to the same
multiple. A traditional decoder uses the center of this interval to reconstruct
the image. Knusperli instead chooses the value in the interval that reduces
discontinuities at block boundaries. The coefficients that Knusperli uses, would
have rounded to the same values that are stored in the JPEG image.

## Disclaimer

This is not an officially supported Google product.

[bazel]: https://bazel.build/
[lena-jpeg-crop]: doc/img/lena.q50.jpeg.crop.png
[lena-knus-crop]: doc/img/lena.q50.knusperli.crop.png
[lena-jpeg]: doc/img/lena.q50.jpeg.png
[lena-knus]: doc/img/lena.q50.knusperli.png
