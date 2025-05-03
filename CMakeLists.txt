cmake_minimum_required(VERSION 3.10)
project(isl VERSION 0.27 LANGUAGES C CXX)

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
    isl_list_private.h
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
    isl_union_set_private.h
    isl_val.c
    isl_vec.c
    isl_version.c
    isl_vertices.c
)

# Add the main library
add_library(isl SHARED ${ISL_SOURCES})
target_include_directories(isl PRIVATE
    ${CMAKE_CURRENT_SOURCE_DIR}
)

target_include_directories(isl PUBLIC
    $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
    $<INSTALL_INTERFACE:include>
)

target_compile_definitions(isl PUBLIC USE_IMATH_FOR_MP)

target_link_libraries(isl PUBLIC imath)

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
set_source_files_properties(isl_test_cpp.cc PROPERTIES COMPILE_OPTIONS "-UCOMPILE_ERROR")

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

add_custom_command(
    OUTPUT ${GEN_DIR}/isl.py.core
    COMMAND $<TARGET_FILE:extract_interface> --language=python -I. -I${CMAKE_CURRENT_SOURCE_DIR} -I${CMAKE_CURRENT_SOURCE_DIR}/include -Iinclude ${CMAKE_CURRENT_SOURCE_DIR}/all.h > ${GEN_DIR}/isl.py.core
    DEPENDS extract_interface all.h
    WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}
    COMMENT "Generating .gen/isl.py.core"
)

add_custom_target(gen_isl_py_core DEPENDS ${GEN_DIR}/isl.py.core)

# Example for C++ header generation (cpp.h)
add_custom_command(
    OUTPUT ${GEN_DIR}/cpp.h
    COMMAND bash -c "cat cpp/cpp.h.top all.h && $<TARGET_FILE:extract_interface> --language=cpp -I. -I${CMAKE_CURRENT_SOURCE_DIR} -I${CMAKE_CURRENT_SOURCE_DIR}/include -Iinclude ${CMAKE_CURRENT_SOURCE_DIR}/all.h && cat cpp/cpp.h.bot > ${GEN_DIR}/cpp.h"
    DEPENDS extract_interface all.h cpp/cpp.h.top cpp/cpp.h.bot
    WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}
    COMMENT "Generating .gen/cpp.h"
)
add_custom_target(gen_cpp_h DEPENDS ${GEN_DIR}/cpp.h)

# C++ checked header generation (cpp-checked.h)
add_custom_command(
    OUTPUT ${GEN_DIR}/cpp-checked.h
    COMMAND bash -c "cat cpp/cpp-checked.h.top all.h && $<TARGET_FILE:extract_interface> --language=cpp-checked -I. -I${CMAKE_CURRENT_SOURCE_DIR} -I${CMAKE_CURRENT_SOURCE_DIR}/include -Iinclude ${CMAKE_CURRENT_SOURCE_DIR}/all.h && cat cpp/cpp-checked.h.bot > ${GEN_DIR}/cpp-checked.h"
    DEPENDS extract_interface all.h cpp/cpp-checked.h.top cpp/cpp-checked.h.bot
    WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}
    COMMENT "Generating .gen/cpp-checked.h"
)
add_custom_target(gen_cpp_checked_h DEPENDS ${GEN_DIR}/cpp-checked.h)

# C++ checked conversion header generation (cpp-checked-conversion.h)
add_custom_command(
    OUTPUT ${GEN_DIR}/cpp-checked-conversion.h
    COMMAND bash -c "cat cpp/cpp-checked-conversion.h.top && $<TARGET_FILE:extract_interface> --language=cpp-checked-conversion -I. -I${CMAKE_CURRENT_SOURCE_DIR} -I${CMAKE_CURRENT_SOURCE_DIR}/include -Iinclude ${CMAKE_CURRENT_SOURCE_DIR}/all.h && cat cpp/cpp-checked-conversion.h.bot > ${GEN_DIR}/cpp-checked-conversion.h"
    DEPENDS extract_interface all.h cpp/cpp-checked-conversion.h.top cpp/cpp-checked-conversion.h.bot
    WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}
    COMMENT "Generating .gen/cpp-checked-conversion.h"
)
add_custom_target(gen_cpp_checked_conversion_h DEPENDS ${GEN_DIR}/cpp-checked-conversion.h)

# Typed C++ header generation (typed_cpp.h)
add_custom_command(
    OUTPUT ${GEN_DIR}/typed_cpp.h
    COMMAND bash -c "cat cpp/typed_cpp.h.top && $<TARGET_FILE:extract_interface> --language=template-cpp -I. -I${CMAKE_CURRENT_SOURCE_DIR} -I${CMAKE_CURRENT_SOURCE_DIR}/include -Iinclude ${CMAKE_CURRENT_SOURCE_DIR}/all.h && cat cpp/typed_cpp.h.bot > ${GEN_DIR}/typed_cpp.h"
    DEPENDS extract_interface all.h cpp/typed_cpp.h.top cpp/typed_cpp.h.bot
    WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}
    COMMENT "Generating .gen/typed_cpp.h"
)
add_custom_target(gen_typed_cpp_h DEPENDS ${GEN_DIR}/typed_cpp.h)

# Optionally, copy generated headers to include/isl/
add_custom_command(
    TARGET gen_cpp_h POST_BUILD
    COMMAND ${CMAKE_COMMAND} -E copy ${GEN_DIR}/cpp.h ${CMAKE_CURRENT_SOURCE_DIR}/include/isl/cpp.h
)
add_custom_command(
    TARGET gen_cpp_checked_h POST_BUILD
    COMMAND ${CMAKE_COMMAND} -E copy ${GEN_DIR}/cpp-checked.h ${CMAKE_CURRENT_SOURCE_DIR}/include/isl/cpp-checked.h
)
add_custom_command(
    TARGET gen_cpp_checked_conversion_h POST_BUILD
    COMMAND ${CMAKE_COMMAND} -E copy ${GEN_DIR}/cpp-checked-conversion.h ${CMAKE_CURRENT_SOURCE_DIR}/include/isl/cpp-checked-conversion.h
)
add_custom_command(
    TARGET gen_typed_cpp_h POST_BUILD
    COMMAND ${CMAKE_COMMAND} -E copy ${GEN_DIR}/typed_cpp.h ${CMAKE_CURRENT_SOURCE_DIR}/include/isl/typed_cpp.h
)

# Install headers
install(DIRECTORY include/isl/ DESTINATION include/isl FILES_MATCHING PATTERN "*.h")

# Generate include/isl/stdint.h if missing (mimic AX_CREATE_STDINT_H)
include(CheckIncludeFile)
include(CheckTypeSize)

set(ISL_STDINT_H ${CMAKE_CURRENT_SOURCE_DIR}/include/isl/stdint.h)
if(NOT EXISTS ${ISL_STDINT_H})
    file(WRITE ${ISL_STDINT_H} "#pragma once\n#include <stdint.h>\n")
endif()

include_directories(${CMAKE_CURRENT_SOURCE_DIR})

# Generate gitversion.h if missing
set(GITVERSION_H ${CMAKE_CURRENT_SOURCE_DIR}/gitversion.h)
if(NOT EXISTS ${GITVERSION_H})
    file(WRITE ${GITVERSION_H} "#define GIT_HEAD_ID \"unknown\"\n")
endif()

# Generate isl_srcdir.c if missing
set(ISL_SRCDIR_C ${CMAKE_CURRENT_SOURCE_DIR}/isl_srcdir.c)
if(NOT EXISTS ${ISL_SRCDIR_C})
    file(WRITE ${ISL_SRCDIR_C} "const char *isl_srcdir = \".\";\n")
endif()

set(INTERFACE_DIR ${CMAKE_CURRENT_SOURCE_DIR}/interface)
file(MAKE_DIRECTORY ${INTERFACE_DIR})
add_custom_command(
    OUTPUT ${INTERFACE_DIR}/isl.py
    COMMAND ${CMAKE_COMMAND} -E make_directory ${INTERFACE_DIR}
    COMMAND bash -c "cat python/isl.py.top ${GEN_DIR}/isl.py.core > ${INTERFACE_DIR}/isl.py"
    DEPENDS python/isl.py.top ${GEN_DIR}/isl.py.core
    WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}
    COMMENT "Generating interface/isl.py"
)
add_custom_target(gen_isl_py DEPENDS ${INTERFACE_DIR}/isl.py)

enable_testing()

# Python tests for ISL
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

add_test(NAME codegen_test
    COMMAND ${Python3_EXECUTABLE} ${CMAKE_CURRENT_SOURCE_DIR}/codegen_test.py
        --srcdir=${CMAKE_CURRENT_SOURCE_DIR}
        --isl-codegen=$<TARGET_FILE:isl_codegen>
        --diff="${CMAKE_COMMAND} -E compare_files"
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
    bound_test pip_test codegen_test schedule_test flow_test
    PROPERTIES ENVIRONMENT "${TEST_ENV_VARS}"
)

# Python test integration
add_test(NAME isl_test_python.py
    COMMAND ${Python3_EXECUTABLE} ${CMAKE_CURRENT_SOURCE_DIR}/isl_test_python.py
)
set_tests_properties(isl_test_python.py PROPERTIES
    ENVIRONMENT "PYTHONPATH=${CMAKE_CURRENT_SOURCE_DIR}/interface;ISL_DYLD_LIBRARY_PATH=${CMAKE_CURRENT_SOURCE_DIR}/.libs;LD_LIBRARY_PATH=${CMAKE_CURRENT_SOURCE_DIR}/.libs:$ENV{LD_LIBRARY_PATH}"
)

# Install generated C++ interface headers and Python interface if present
install(FILES
    ${CMAKE_CURRENT_SOURCE_DIR}/include/isl/cpp.h
    ${CMAKE_CURRENT_SOURCE_DIR}/include/isl/cpp-checked.h
    ${CMAKE_CURRENT_SOURCE_DIR}/include/isl/cpp-checked-conversion.h
    ${CMAKE_CURRENT_SOURCE_DIR}/include/isl/typed_cpp.h
    DESTINATION include/isl
)
