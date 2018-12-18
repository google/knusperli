package(
    default_visibility = ["//visibility:public"],
)

cc_binary(
    name = "knusperli",
    srcs = [
        "decode.cc",
    ],
    deps = [
        ":jpeg_data",
        ":jpeg_data_decoder",
        ":jpeg_data_reader",
        ":output_image",
        "@lodepng",
    ],
)

cc_library(
    name = "jpeg_data_reader",
    srcs = [
        "jpeg_data_reader.cc",
        "jpeg_huffman_decode.cc",
        "jpeg_huffman_decode.h",
    ],
    hdrs = ["jpeg_data_reader.h"],
    deps = [
        ":jpeg_data",
    ],
)

cc_library(
    name = "jpeg_data_decoder",
    srcs = ["jpeg_data_decoder.cc"],
    hdrs = ["jpeg_data_decoder.h"],
    deps = [
        ":jpeg_data",
        ":output_image",
    ],
)

cc_library(
    name = "jpeg_data",
    srcs = ["jpeg_data.cc"],
    hdrs = [
        "jpeg_data.h",
        "jpeg_error.h",
    ],
)

cc_library(
    name = "output_image",
    srcs = ["output_image.cc"],
    hdrs = ["output_image.h"],
    deps = [
        ":color_transform",
        ":dct_double",
        ":gamma_correct",
        ":idct",
        ":jpeg_data",
        ":preprocess_downsample",
        ":quantize",
    ],
)

cc_library(
    name = "color_transform",
    textual_hdrs = ["color_transform.h"],
)

cc_library(
    name = "dct_double",
    srcs = ["dct_double.cc"],
    hdrs = ["dct_double.h"],
    copts = ["-ffast-math"],
)

cc_library(
    name = "gamma_correct",
    srcs = ["gamma_correct.cc"],
    hdrs = ["gamma_correct.h"],
)

cc_library(
    name = "idct",
    srcs = ["idct.cc"],
    hdrs = ["idct.h"],
    deps = [":jpeg_data"],
)

cc_library(
    name = "preprocess_downsample",
    srcs = ["preprocess_downsample.cc"],
    hdrs = ["preprocess_downsample.h"],
)

cc_library(
    name = "quantize",
    srcs = ["quantize.cc"],
    hdrs = ["quantize.h"],
    deps = [":jpeg_data"],
)
