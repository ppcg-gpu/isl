cmake_minimum_required(VERSION 3.18)
project(isl VERSION 0.27 LANGUAGES C CXX)

include(GNUInstallDirs)

# The installed programs and libraries have to find each other inside the
# installation prefix rather than picking up whatever the system provides.
if(NOT DEFINED CMAKE_INSTALL_RPATH)
    set(CMAKE_INSTALL_RPATH "$ORIGIN;$ORIGIN/../${CMAKE_INSTALL_LIBDIR}")
endif()

# Include required CMake modules for configuration checks
include(CheckIncludeFile)
include(CheckTypeSize)
include(CheckSymbolExists)
include(CheckCSourceCompiles)
include(CMakePushCheckState)

# Options that match configure.ac options
option(SMALL_INT_OPT "Enable small integer optimization for IMATH" OFF)

# Set C standard
set(CMAKE_C_STANDARD 99)
set(CMAKE_C_STANDARD_REQUIRED ON)

# Add imath as a subdirectory and link against its target
add_subdirectory(ThirdParty/imath)

# Add extract_interface - a utility to create ISL language bindings
add_subdirectory(ThirdParty/extract_interface)

include_directories(${CMAKE_CURRENT_BINARY_DIR})

# Configuration checks for isl_config.h similar to configure.ac
# Check for declarations of functions with proper header files

# Check for ffs declaration in strings.h
check_c_source_compiles("
    #include <strings.h>
    int main() {
        (void)ffs;
        return 0;
    }
" HAVE_DECL_FFS)

# Check for __builtin_ffs declaration (no specific header needed)
check_c_source_compiles("
    int main() {
        (void)__builtin_ffs;
        return 0;
    }
" HAVE_DECL___BUILTIN_FFS)

# Check for _BitScanForward declaration in intrin.h
check_c_source_compiles("
    #include <intrin.h>
    int main() {
        (void)_BitScanForward;
        return 0;
    }
" HAVE_DECL__BITSCANFORWARD)

# Check for strcasecmp and strncasecmp declarations in strings.h
check_c_source_compiles("
    #include <strings.h>
    int main() {
        (void)strcasecmp;
        (void)strncasecmp;
        return 0;
    }
" HAVE_DECL_STRCASECMP_STRNCASECMP)

if(HAVE_DECL_STRCASECMP_STRNCASECMP)
  set(HAVE_DECL_STRCASECMP 1)
  set(HAVE_DECL_STRNCASECMP 1)
else()
  # Check them individually if the combined check failed
  check_c_source_compiles("
      #include <strings.h>
      int main() {
          (void)strcasecmp;
          return 0;
      }
  " HAVE_DECL_STRCASECMP)

  check_c_source_compiles("
      #include <strings.h>
      int main() {
          (void)strncasecmp;
          return 0;
      }
  " HAVE_DECL_STRNCASECMP)
endif()

# Check for _stricmp and _strnicmp declarations in string.h
check_c_source_compiles("
    #include <string.h>
    int main() {
        (void)_stricmp;
        (void)_strnicmp;
        return 0;
    }
" HAVE_DECL_STRICMP_STRNICMP)

if(HAVE_DECL_STRICMP_STRNICMP)
  set(HAVE_DECL__STRICMP 1)
  set(HAVE_DECL__STRNICMP 1)
else()
  # Check them individually if the combined check failed
  check_c_source_compiles("
      #include <string.h>
      int main() {
          (void)_stricmp;
          return 0;
      }
  " HAVE_DECL__STRICMP)

  check_c_source_compiles("
      #include <string.h>
      int main() {
          (void)_strnicmp;
          return 0;
      }
  " HAVE_DECL__STRNICMP)
endif()

# Check for snprintf and _snprintf declarations in stdio.h
check_c_source_compiles("
    #include <stdio.h>
    int main() {
        (void)snprintf;
        return 0;
    }
" HAVE_DECL_SNPRINTF)

check_c_source_compiles("
    #include <stdio.h>
    int main() {
        (void)_snprintf;
        return 0;
    }
" HAVE_DECL__SNPRINTF)

# Check for __attribute__ support
check_c_source_compiles("
    void foo(int) __attribute__((unused));
    int main() { return 0; }
    " HAVE___ATTRIBUTE__)

# Check for __attribute__((warn_unused_result)) support
if(HAVE___ATTRIBUTE__)
  check_c_source_compiles("
      int foo(void) __attribute__((warn_unused_result));
      int main() { return 0; }
      " HAVE_WARN_UNUSED_RESULT)

  if(HAVE_WARN_UNUSED_RESULT)
    set(GCC_WARN_UNUSED_RESULT "__attribute__((warn_unused_result))")
  endif()
endif()

# Check if any of the functions are missing (error out like in configure.ac)
if(NOT HAVE_DECL_FFS AND NOT HAVE_DECL___BUILTIN_FFS AND NOT HAVE_DECL__BITSCANFORWARD)
  message(FATAL_ERROR "No ffs implementation found")
endif()

if(NOT HAVE_DECL_STRCASECMP AND NOT HAVE_DECL__STRICMP)
  message(FATAL_ERROR "No strcasecmp implementation found")
endif()

if(NOT HAVE_DECL_STRNCASECMP AND NOT HAVE_DECL__STRNICMP)
  message(FATAL_ERROR "No strncasecmp implementation found")
endif()

if(NOT HAVE_DECL_SNPRINTF AND NOT HAVE_DECL__SNPRINTF)
  message(FATAL_ERROR "No snprintf implementation found")
endif()

# Configure isl_config.h
if(SMALL_INT_OPT)
  set(USE_SMALL_INT_OPT 1)
endif()

# Generate the configured isl_config.h file
configure_file(
  ${CMAKE_CURRENT_SOURCE_DIR}/isl_config.h.in
  ${CMAKE_CURRENT_BINARY_DIR}/isl_config.h
)

# Rest of the CMakeLists.txt content
set(ISL_SOURCES
    isl_aff.c
    isl_aff_map.c
    isl_affine_hull.c
    isl_arg.c
    isl_ast.c
    isl_ast_build.c
    isl_ast_build_expr.c
    isl_ast_codegen.c
    isl_ast_graft.c
    basis_reduction_tab.c
    isl_bernstein.c
    isl_blk.c
    isl_bound.c
    isl_box.c
    isl_coalesce.c
    isl_constraint.c
    isl_convex_hull.c
    isl_ctx.c
    isl_deprecated.c
    isl_dim_map.c
    isl_equalities.c
    isl_factorization.c
    isl_farkas.c
    isl_ffs.c
    isl_flow.c
    isl_fold.c
    isl_hash.c
    isl_id_to_ast_expr.c
    isl_id_to_id.c
    isl_id_to_pw_aff.c
    isl_ilp.c
    isl_imath.c
    isl_input.c
    isl_local.c
    isl_local_space.c
    isl_lp.c
    isl_map.c
    isl_map_list.c
    isl_map_simplify.c
    isl_map_subtract.c
    isl_map_to_basic_set.c
    isl_mat.c
    isl_morph.c
    isl_id.c
    isl_obj.c
    isl_options.c
    isl_output.c
    isl_point.c
    isl_polynomial.c
    isl_printer.c
    print.c
    isl_range.c
    isl_reordering.c
    isl_sample.c
    isl_scan.c
    isl_schedule.c
    isl_schedule_band.c
    isl_schedule_node.c
    isl_schedule_read.c
    isl_schedule_tree.c
    isl_schedule_constraints.c
    isl_scheduler.c
    isl_scheduler_clustering.c
    isl_scheduler_scc.c
    isl_set_list.c
    isl_sort.c
    isl_space.c
    isl_stream.c
    isl_seq.c
    isl_set_to_ast_graft_list.c
    isl_stride.c
    isl_tab.c
    isl_tab_pip.c
    isl_tarjan.c
    isl_transitive_closure.c
    isl_union_map.c
    isl_val.c
    isl_vec.c
    isl_version.c
    isl_vertices.c
)

# The multiple precision backend.  isl is built against imath here, either
# through the plain interface or through the small integer optimisation.
if(SMALL_INT_OPT)
    list(APPEND ISL_SOURCES isl_int_sioimath.c isl_val_sioimath.c)
else()
    list(APPEND ISL_SOURCES isl_val_imath.c)
endif()

# Add the main library
add_library(isl SHARED ${ISL_SOURCES})
target_include_directories(isl PRIVATE
    ${CMAKE_CURRENT_SOURCE_DIR}
)

target_include_directories(isl PUBLIC
    $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
    $<INSTALL_INTERFACE:include>
)

# The autotools build passed "-version-info 27:0:4" to libtool.  Libtool does
# not use current:revision:age as a version triple: the soname number is
# current - age (23) and the file it points at is named
# libisl.so.<current-age>.<age>.<revision>, i.e. libisl.so.23.4.0.  Anything
# else here would silently break every binary already linked against isl.
set_target_properties(isl PROPERTIES
    VERSION 23.4.0
    SOVERSION 23
)

target_compile_definitions(isl PUBLIC USE_IMATH_FOR_MP)

target_link_libraries(isl PUBLIC imath)

# A missing source file would otherwise only show up when some program
# happens to use one of the symbols it defines.
if(NOT APPLE AND NOT WIN32)
    target_link_options(isl PRIVATE "LINKER:--no-undefined")
endif()

# Add test_imath executable
add_executable(isl_test_imath isl_test_imath.c)
target_link_libraries(isl_test_imath isl imath)

find_package(Python3 COMPONENTS Interpreter REQUIRED)

# Always build C++ test executables
add_executable(isl_test2 isl_test2.cc include/isl/cpp.h)
target_link_libraries(isl_test2 isl)
set_target_properties(isl_test2 PROPERTIES CXX_STANDARD 11)

add_executable(isl_test_cpp isl_test_cpp.cc include/isl/cpp.h)
target_link_libraries(isl_test_cpp isl)
set_target_properties(isl_test_cpp PROPERTIES CXX_STANDARD 11)

add_executable(isl_test_cpp_checked isl_test_cpp-checked.cc include/isl/cpp-checked.h)
target_link_libraries(isl_test_cpp_checked isl)
set_target_properties(isl_test_cpp_checked PROPERTIES CXX_STANDARD 11)

add_executable(isl_test_cpp_checked_conversion isl_test_cpp-checked-conversion.cc include/isl/cpp-checked-conversion.h)
target_link_libraries(isl_test_cpp_checked_conversion isl)
set_target_properties(isl_test_cpp_checked_conversion PROPERTIES CXX_STANDARD 11)

add_executable(isl_test_cpp17 isl_test_cpp17.cc include/isl/cpp.h)
target_link_libraries(isl_test_cpp17 isl)
set_target_properties(isl_test_cpp17 PROPERTIES CXX_STANDARD 17)

add_executable(isl_test_cpp17_checked isl_test_cpp17-checked.cc include/isl/cpp.h)
target_link_libraries(isl_test_cpp17_checked isl)
set_target_properties(isl_test_cpp17_checked PROPERTIES CXX_STANDARD 17)

# Add executables and link them to the isl library
add_executable(isl_test isl_test.c)
target_link_libraries(isl_test isl)

add_executable(isl_polyhedron_sample polyhedron_sample.c)
target_link_libraries(isl_polyhedron_sample isl)

add_executable(isl_pip pip.c)
target_link_libraries(isl_pip isl)

add_executable(isl_polyhedron_minimize polyhedron_minimize.c)
target_link_libraries(isl_polyhedron_minimize isl)

add_executable(isl_polytope_scan polytope_scan.c)
target_link_libraries(isl_polytope_scan isl)

add_executable(isl_polyhedron_detect_equalities polyhedron_detect_equalities.c)
target_link_libraries(isl_polyhedron_detect_equalities isl)

add_executable(isl_polyhedron_remove_redundant_equalities polyhedron_remove_redundant_equalities.c)
target_link_libraries(isl_polyhedron_remove_redundant_equalities isl)

add_executable(isl_cat cat.c)
target_link_libraries(isl_cat isl)

add_executable(isl_closure closure.c)
target_link_libraries(isl_closure isl)

add_executable(isl_bound bound.c)
target_link_libraries(isl_bound isl)

add_executable(isl_schedule schedule.c)
target_link_libraries(isl_schedule isl)

add_executable(isl_codegen codegen.c)
target_link_libraries(isl_codegen isl)

add_executable(isl_test_int isl_test_int.c)
target_link_libraries(isl_test_int isl)

add_executable(isl_flow flow.c)
target_link_libraries(isl_flow isl)

add_executable(isl_flow_cmp flow_cmp.c)
target_link_libraries(isl_flow_cmp isl)

add_executable(isl_schedule_cmp schedule_cmp.c)
target_link_libraries(isl_schedule_cmp isl)

# Custom commands for generated headers and Python interface
set(GEN_DIR ${CMAKE_CURRENT_BINARY_DIR}/.gen)
file(MAKE_DIRECTORY ${GEN_DIR})

set(GENERATE_INTERFACE ${CMAKE_CURRENT_SOURCE_DIR}/cmake/GenerateInterface.cmake)

# extract_interface parses all.h, which pulls in the public headers from both
# the source and the build tree.
set(INTERFACE_INCLUDES
    -I${CMAKE_CURRENT_SOURCE_DIR}
    -I${CMAKE_CURRENT_SOURCE_DIR}/include
    -I${CMAKE_CURRENT_BINARY_DIR}
    -I${CMAKE_CURRENT_BINARY_DIR}/include
)
list(JOIN INTERFACE_INCLUDES "|" INTERFACE_INCLUDES_ARG)

# Assemble one of the generated interface files.
#
#   name     base name of the generated file in .gen
#   language value passed to extract_interface --language
#   prepend  files placed before the generated body
#   append   files placed after the generated body
function(add_interface_target name language prepend append)
    list(JOIN prepend "|" prepend_arg)
    list(JOIN append "|" append_arg)
    add_custom_command(
        OUTPUT ${GEN_DIR}/${name}
        COMMAND ${CMAKE_COMMAND}
            -DOUTPUT=${GEN_DIR}/${name}
            -DPREPEND=${prepend_arg}
            -DAPPEND=${append_arg}
            -DGENERATOR=$<TARGET_FILE:extract_interface>
            "-DGENERATOR_ARGS=--language=${language}|${INTERFACE_INCLUDES_ARG}|${CMAKE_CURRENT_SOURCE_DIR}/all.h"
            -DWORKDIR=${CMAKE_CURRENT_SOURCE_DIR}
            -P ${GENERATE_INTERFACE}
        DEPENDS extract_interface all.h ${prepend} ${append} ${GENERATE_INTERFACE}
        COMMENT "Generating .gen/${name}"
        VERBATIM
    )
endfunction()

add_interface_target(isl.py.core python "" "")

# The C++ interface headers under include/isl are kept under version control,
# but they are pure generator output.  Building them here and comparing them
# against the checked-in copies (see the *_up_to_date tests below) is what
# keeps the cpp, cpp-checked, cpp-checked-conversion and template-cpp backends
# of extract_interface exercised at all; without it they are dead code.  The
# targets are in ALL because ctest cannot depend on a build step.
add_interface_target(cpp.h cpp
    "${CMAKE_CURRENT_SOURCE_DIR}/cpp/cpp.h.top;${CMAKE_CURRENT_SOURCE_DIR}/all.h"
    "${CMAKE_CURRENT_SOURCE_DIR}/cpp/cpp.h.bot")
add_custom_target(gen_cpp_h ALL DEPENDS ${GEN_DIR}/cpp.h)

add_interface_target(cpp-checked.h cpp-checked
    "${CMAKE_CURRENT_SOURCE_DIR}/cpp/cpp-checked.h.top;${CMAKE_CURRENT_SOURCE_DIR}/all.h"
    "${CMAKE_CURRENT_SOURCE_DIR}/cpp/cpp-checked.h.bot")
add_custom_target(gen_cpp_checked_h ALL DEPENDS ${GEN_DIR}/cpp-checked.h)

add_interface_target(cpp-checked-conversion.h cpp-checked-conversion
    "${CMAKE_CURRENT_SOURCE_DIR}/cpp/cpp-checked-conversion.h.top"
    "${CMAKE_CURRENT_SOURCE_DIR}/cpp/cpp-checked-conversion.h.bot")
add_custom_target(gen_cpp_checked_conversion_h ALL
    DEPENDS ${GEN_DIR}/cpp-checked-conversion.h)

add_interface_target(typed_cpp.h template-cpp
    "${CMAKE_CURRENT_SOURCE_DIR}/cpp/typed_cpp.h.top"
    "${CMAKE_CURRENT_SOURCE_DIR}/cpp/typed_cpp.h.bot")
add_custom_target(gen_typed_cpp_h ALL DEPENDS ${GEN_DIR}/typed_cpp.h)

# The C++ interface headers are kept under version control, so refreshing them
# is an explicit maintainer action.  The build itself never writes into the
# source tree.
add_custom_target(update_cpp_headers
    COMMAND ${CMAKE_COMMAND} -E copy_if_different
        ${GEN_DIR}/cpp.h ${CMAKE_CURRENT_SOURCE_DIR}/include/isl/cpp.h
    COMMAND ${CMAKE_COMMAND} -E copy_if_different
        ${GEN_DIR}/cpp-checked.h ${CMAKE_CURRENT_SOURCE_DIR}/include/isl/cpp-checked.h
    COMMAND ${CMAKE_COMMAND} -E copy_if_different
        ${GEN_DIR}/cpp-checked-conversion.h
        ${CMAKE_CURRENT_SOURCE_DIR}/include/isl/cpp-checked-conversion.h
    COMMAND ${CMAKE_COMMAND} -E copy_if_different
        ${GEN_DIR}/typed_cpp.h ${CMAKE_CURRENT_SOURCE_DIR}/include/isl/typed_cpp.h
    DEPENDS ${GEN_DIR}/cpp.h ${GEN_DIR}/cpp-checked.h
            ${GEN_DIR}/cpp-checked-conversion.h ${GEN_DIR}/typed_cpp.h
    COMMENT "Refreshing the checked-in C++ interface headers"
)

# Install headers.  include/isl/hmap_templ.c is a header in all but name: the
# generated hash map headers include it textually, so a consumer that includes
# isl/id_to_ast_expr.h needs it.  include/isl/val_gmp.h on the other hand
# declares the GMP conversion functions, which do not exist in a build against
# imath, so installing it would advertise an interface that is not there.
install(DIRECTORY include/isl/ DESTINATION ${CMAKE_INSTALL_INCLUDEDIR}/isl
    FILES_MATCHING
        PATTERN "val_gmp.h" EXCLUDE
        PATTERN "*.h"
        PATTERN "hmap_templ.c")

install(TARGETS isl
    LIBRARY DESTINATION ${CMAKE_INSTALL_LIBDIR}
    ARCHIVE DESTINATION ${CMAKE_INSTALL_LIBDIR}
    RUNTIME DESTINATION ${CMAKE_INSTALL_BINDIR}
)

# pkg-config metadata, the replacement for AX_CREATE_PKGCONFIG_INFO.  The
# fields reproduce what that macro emitted: the imath backend contributes no
# extra libraries or include paths, so Libs and Cflags only mention isl itself.
configure_file(
    ${CMAKE_CURRENT_SOURCE_DIR}/isl.pc.in
    ${CMAKE_CURRENT_BINARY_DIR}/isl.pc
    @ONLY
)
install(FILES ${CMAKE_CURRENT_BINARY_DIR}/isl.pc
    DESTINATION ${CMAKE_INSTALL_LIBDIR}/pkgconfig)

# The GDB pretty printer is auto-loaded from a file named after the object
# file GDB actually maps, so it has to carry the full versioned library name.
install(FILES ${CMAKE_CURRENT_SOURCE_DIR}/libisl-gdb.py
    DESTINATION ${CMAKE_INSTALL_LIBDIR}
    RENAME $<TARGET_FILE_NAME:isl>-gdb.py)

# Files that the autotools build used to create in the source tree are
# generated into the build tree instead.  They are picked up ahead of any
# leftovers because the build directory comes first on the include path.
set(GEN_INCLUDE_DIR ${CMAKE_CURRENT_BINARY_DIR}/include/isl)

# include/isl/stdint.h, the replacement for AX_CREATE_STDINT_H
file(GENERATE
    OUTPUT ${GEN_INCLUDE_DIR}/stdint.h
    CONTENT "#pragma once\n#include <stdint.h>\n"
)
install(FILES ${GEN_INCLUDE_DIR}/stdint.h DESTINATION ${CMAKE_INSTALL_INCLUDEDIR}/isl)

target_include_directories(isl PUBLIC
    $<BUILD_INTERFACE:${CMAKE_CURRENT_BINARY_DIR}/include>
)

# isl_srcdir.c, textually included by isl_test to locate its input files
file(GENERATE
    OUTPUT ${CMAKE_CURRENT_BINARY_DIR}/isl_srcdir.c
    CONTENT "const char *isl_srcdir = \"${CMAKE_CURRENT_SOURCE_DIR}\";\n"
)

# gitversion.h, reported by isl_version()
execute_process(
    COMMAND git describe --always --dirty
    WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}
    OUTPUT_VARIABLE GIT_HEAD_VERSION
    OUTPUT_STRIP_TRAILING_WHITESPACE
    ERROR_QUIET
    RESULT_VARIABLE GIT_DESCRIBE_RESULT
)
if(NOT GIT_DESCRIBE_RESULT EQUAL 0 OR NOT GIT_HEAD_VERSION)
    set(GIT_HEAD_VERSION "isl-${PROJECT_VERSION}")
endif()
file(GENERATE
    OUTPUT ${CMAKE_CURRENT_BINARY_DIR}/gitversion.h
    CONTENT "#define GIT_HEAD_ID \"${GIT_HEAD_VERSION}\"\n"
)

include_directories(${CMAKE_CURRENT_SOURCE_DIR})

# Python interface
set(INTERFACE_DIR ${CMAKE_CURRENT_BINARY_DIR}/interface)
file(MAKE_DIRECTORY ${INTERFACE_DIR})

file(GENERATE
    OUTPUT ${INTERFACE_DIR}/isldlname.py
    CONTENT "isl_dlname = \"$<TARGET_FILE_NAME:isl>\"\n"
)

add_custom_command(
    OUTPUT ${INTERFACE_DIR}/isl.py
    COMMAND ${CMAKE_COMMAND}
        -DOUTPUT=${INTERFACE_DIR}/isl.py
        "-DPREPEND=${INTERFACE_DIR}/isldlname.py|${CMAKE_CURRENT_SOURCE_DIR}/python/isl.py.top|${GEN_DIR}/isl.py.core"
        -P ${GENERATE_INTERFACE}
    DEPENDS ${CMAKE_CURRENT_SOURCE_DIR}/python/isl.py.top
            ${GEN_DIR}/isl.py.core
            ${INTERFACE_DIR}/isldlname.py
            ${GENERATE_INTERFACE}
    COMMENT "Generating interface/isl.py"
    VERBATIM
)
add_custom_target(gen_isl_py ALL DEPENDS ${INTERFACE_DIR}/isl.py)

enable_testing()

# Test programs that check the library itself
add_test(NAME isl_test COMMAND $<TARGET_FILE:isl_test>)
add_test(NAME isl_test2 COMMAND $<TARGET_FILE:isl_test2>)
add_test(NAME isl_test_int COMMAND $<TARGET_FILE:isl_test_int>)
add_test(NAME isl_test_imath COMMAND $<TARGET_FILE:isl_test_imath>)
add_test(NAME isl_test_cpp COMMAND $<TARGET_FILE:isl_test_cpp>)
add_test(NAME isl_test_cpp_checked COMMAND $<TARGET_FILE:isl_test_cpp_checked>)
add_test(NAME isl_test_cpp_checked_conversion
    COMMAND $<TARGET_FILE:isl_test_cpp_checked_conversion>)
add_test(NAME isl_test_cpp17 COMMAND $<TARGET_FILE:isl_test_cpp17>)
add_test(NAME isl_test_cpp17_checked COMMAND $<TARGET_FILE:isl_test_cpp17_checked>)

# isl_test_cpp.cc is expected to fail to compile with COMPILE_ERROR defined.
# The include path is taken from the isl target itself and written to a
# response file, so it cannot go stale: a hand written -I list would sooner or
# later make this test "pass" because a header is missing rather than because
# of the intended intersect_range error.  Only that one translation unit is
# compiled, so an unrelated build failure cannot make the test pass either;
# isl_test_cpp above is the positive control that the same file does compile
# without the macro.  The empty element comes from $<INSTALL_INTERFACE:include>,
# which is not part of the build tree include path.
set(CPP_FAILED_RSP ${CMAKE_CURRENT_BINARY_DIR}/isl_test_cpp_failed.rsp)
file(GENERATE
    OUTPUT ${CPP_FAILED_RSP}
    CONTENT "$<JOIN:$<LIST:TRANSFORM,$<LIST:FILTER,$<TARGET_PROPERTY:isl,INCLUDE_DIRECTORIES>,EXCLUDE,^$>,PREPEND,-I>,\n>\n"
)

add_test(NAME isl_test_cpp_failed
    COMMAND ${CMAKE_CXX_COMPILER}
        -std=c++11
        -DCOMPILE_ERROR
        @${CPP_FAILED_RSP}
        -c ${CMAKE_CURRENT_SOURCE_DIR}/isl_test_cpp.cc
        -o ${CMAKE_CURRENT_BINARY_DIR}/isl_test_cpp_failed.o
)
set_tests_properties(isl_test_cpp_failed PROPERTIES WILL_FAIL TRUE)

# The checked-in C++ interface headers must stay identical to what
# extract_interface produces, and running the comparison is what exercises the
# generator backends in the first place.  The generated files are built by ALL,
# so they are always present by the time ctest runs.
foreach(generated IN ITEMS cpp.h cpp-checked.h cpp-checked-conversion.h typed_cpp.h)
    string(REPLACE "." "_" test_suffix ${generated})
    string(REPLACE "-" "_" test_suffix ${test_suffix})
    add_test(NAME interface_${test_suffix}_up_to_date
        COMMAND ${CMAKE_COMMAND} -E compare_files
            ${GEN_DIR}/${generated}
            ${CMAKE_CURRENT_SOURCE_DIR}/include/isl/${generated}
    )
endforeach()

# Python driven tests around the command line tools
add_test(NAME bound_test
    COMMAND ${Python3_EXECUTABLE} ${CMAKE_CURRENT_SOURCE_DIR}/bound_test.py
        --srcdir=${CMAKE_CURRENT_SOURCE_DIR}
        --isl-bound=$<TARGET_FILE:isl_bound>
)

add_test(NAME pip_test
    COMMAND ${Python3_EXECUTABLE} ${CMAKE_CURRENT_SOURCE_DIR}/pip_test.py
        --srcdir=${CMAKE_CURRENT_SOURCE_DIR}
        --isl-pip=$<TARGET_FILE:isl_pip>
)

# The reference outputs under test_inputs/codegen differ from the generated
# ones in indentation, so the comparison has to be whitespace insensitive, as
# it was in the autotools codegen_test.sh ("diff $DIFF_OPTIONS -w").  The
# context option is probed the way ISL_DETECT_DIFF_OPTIONS used to probe it,
# so that a failure prints the offending hunk instead of nothing at all.
find_program(DIFF_EXECUTABLE diff REQUIRED)
foreach(option -u -c)
    execute_process(
        COMMAND ${DIFF_EXECUTABLE} ${option} /dev/null /dev/null
        RESULT_VARIABLE diff_option_result
        OUTPUT_QUIET
        ERROR_QUIET
    )
    if(diff_option_result EQUAL 0)
        set(DIFF_CONTEXT_OPTION ${option})
        break()
    endif()
endforeach()

add_test(NAME codegen_test
    COMMAND ${Python3_EXECUTABLE} ${CMAKE_CURRENT_SOURCE_DIR}/codegen_test.py
        --srcdir=${CMAKE_CURRENT_SOURCE_DIR}
        --isl-codegen=$<TARGET_FILE:isl_codegen>
        # codegen_test.py splits this with shlex, so quote the path.
        "--diff='${DIFF_EXECUTABLE}' ${DIFF_CONTEXT_OPTION} -w"
)

add_test(NAME schedule_test
    COMMAND ${Python3_EXECUTABLE} ${CMAKE_CURRENT_SOURCE_DIR}/schedule_test.py
        --srcdir=${CMAKE_CURRENT_SOURCE_DIR}
        --isl-schedule=$<TARGET_FILE:isl_schedule>
        --isl-schedule-cmp=$<TARGET_FILE:isl_schedule_cmp>
)

add_test(NAME flow_test
    COMMAND ${Python3_EXECUTABLE} ${CMAKE_CURRENT_SOURCE_DIR}/flow_test.py
        --srcdir=${CMAKE_CURRENT_SOURCE_DIR}
        --isl-flow=$<TARGET_FILE:isl_flow>
        --isl-flow-cmp=$<TARGET_FILE:isl_flow_cmp>
)

# Set environment variables for all tests
set(TEST_ENV_VARS "LD_LIBRARY_PATH=$<TARGET_FILE_DIR:isl>:$ENV{LD_LIBRARY_PATH}")
if(APPLE)
    list(APPEND TEST_ENV_VARS "DYLD_LIBRARY_PATH=$<TARGET_FILE_DIR:isl>")
endif()

# Apply environment variables to all tests
set_tests_properties(
    isl_test isl_test2 isl_test_int isl_test_imath
    isl_test_cpp isl_test_cpp_checked isl_test_cpp_checked_conversion
    isl_test_cpp17 isl_test_cpp17_checked
    bound_test pip_test codegen_test schedule_test flow_test
    PROPERTIES ENVIRONMENT "${TEST_ENV_VARS}"
)

# Python test integration
add_test(NAME isl_test_python.py
    COMMAND ${Python3_EXECUTABLE} ${CMAKE_CURRENT_SOURCE_DIR}/isl_test_python.py
)
set_tests_properties(isl_test_python.py PROPERTIES
    ENVIRONMENT "PYTHONPATH=${INTERFACE_DIR};ISL_DYLD_LIBRARY_PATH=$<TARGET_FILE_DIR:isl>;LD_LIBRARY_PATH=$<TARGET_FILE_DIR:isl>:$ENV{LD_LIBRARY_PATH}"
)
