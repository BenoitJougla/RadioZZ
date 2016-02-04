INCLUDE(FindPkgConfig)
PKG_CHECK_MODULES(PC_RADIOZZ RadioZZ)

FIND_PATH(
    RADIOZZ_INCLUDE_DIRS
    NAMES RadioZZ/api.h
    HINTS $ENV{RADIOZZ_DIR}/include
        ${PC_RADIOZZ_INCLUDEDIR}
    PATHS ${CMAKE_INSTALL_PREFIX}/include
          /usr/local/include
          /usr/include
)

FIND_LIBRARY(
    RADIOZZ_LIBRARIES
    NAMES gnuradio-RadioZZ
    HINTS $ENV{RADIOZZ_DIR}/lib
        ${PC_RADIOZZ_LIBDIR}
    PATHS ${CMAKE_INSTALL_PREFIX}/lib
          ${CMAKE_INSTALL_PREFIX}/lib64
          /usr/local/lib
          /usr/local/lib64
          /usr/lib
          /usr/lib64
)

INCLUDE(FindPackageHandleStandardArgs)
FIND_PACKAGE_HANDLE_STANDARD_ARGS(RADIOZZ DEFAULT_MSG RADIOZZ_LIBRARIES RADIOZZ_INCLUDE_DIRS)
MARK_AS_ADVANCED(RADIOZZ_LIBRARIES RADIOZZ_INCLUDE_DIRS)

