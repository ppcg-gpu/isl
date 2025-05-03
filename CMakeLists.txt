cmake_minimum_required(VERSION 3.10)
project(isl LANGUAGES C CXX)

option(SMALL_INT_OPT "Enable small integer optimization for IMATH" OFF)
option(HAVE_PYTHON "Enable Python interface and tests" OFF)

# Set C standard
set(CMAKE_C_STANDARD 99)
set(CMAKE_C_STANDARD_REQUIRED ON)

# Add imath as a subdirectory and link against its target
add_subdirectory(ThirdParty/imath)

# Ensure ISL_IMATH is defined for all isl sources
add_definitions(-DISL_IMATH)

# Use imath for multiprecision
set(MP_SRC
    isl_imath.c
    isl_imath.h
    isl_int_imath.h
    imath_wrap/gmp_compat.h
    imath_wrap/imath.h
    imath_wrap/imrat.h
    imath_wrap/wrap.h
    imath_wrap/gmp_compat.c
    imath_wrap/imath.c
    imath_wrap/imrat.c
    isl_val_imath.c
)

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
add_library(isl SHARED ${ISL_SOURCES} ${MP_SRC})
target_include_directories(isl PRIVATE
    ${CMAKE_CURRENT_SOURCE_DIR}
    ${CMAKE_CURRENT_SOURCE_DIR}/imath_wrap
)
target_link_libraries(isl PRIVATE imath)

target_include_directories(isl PUBLIC
    $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
    $<INSTALL_INTERFACE:include>
)

# Add test_imath executable
add_executable(isl_test_imath isl_test_imath.c)
target_link_libraries(isl_test_imath isl imath)

# Option for Python support
option(HAVE_PYTHON "Enable Python interface and tests" OFF)

if(HAVE_PYTHON)
    find_package(Python3 COMPONENTS Interpreter REQUIRED)
endif()

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

# Dummy library for header dependencies
add_library(dep STATIC dep.c)

# Build the extract_interface tool
add_executable(extract_interface interface/extract_interface.cc)
target_include_directories(extract_interface PRIVATE interface)

# Custom commands for generated headers and Python interface
set(GEN_DIR ${CMAKE_CURRENT_BINARY_DIR}/.gen)
file(MAKE_DIRECTORY ${GEN_DIR})

add_custom_command(
    OUTPUT ${GEN_DIR}/isl.py.core
    COMMAND extract_interface --language=python -I. -I${CMAKE_CURRENT_SOURCE_DIR} -I${CMAKE_CURRENT_SOURCE_DIR}/include -Iinclude ${CMAKE_CURRENT_SOURCE_DIR}/all.h > ${GEN_DIR}/isl.py.core
    DEPENDS extract_interface all.h dep
    WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}
    COMMENT "Generating .gen/isl.py.core"
)

add_custom_target(gen_isl_py_core DEPENDS ${GEN_DIR}/isl.py.core)

# Example for C++ header generation (cpp.h)
add_custom_command(
    OUTPUT ${GEN_DIR}/cpp.h
    COMMAND bash -c "cat cpp/cpp.h.top all.h && extract_interface --language=cpp -I. -I${CMAKE_CURRENT_SOURCE_DIR} -I${CMAKE_CURRENT_SOURCE_DIR}/include -Iinclude ${CMAKE_CURRENT_SOURCE_DIR}/all.h && cat cpp/cpp.h.bot > ${GEN_DIR}/cpp.h"
    DEPENDS extract_interface all.h dep cpp/cpp.h.top cpp/cpp.h.bot
    WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}
    COMMENT "Generating .gen/cpp.h"
)
add_custom_target(gen_cpp_h DEPENDS ${GEN_DIR}/cpp.h)

# C++ checked header generation (cpp-checked.h)
add_custom_command(
    OUTPUT ${GEN_DIR}/cpp-checked.h
    COMMAND bash -c "cat cpp/cpp-checked.h.top all.h && extract_interface --language=cpp-checked -I. -I${CMAKE_CURRENT_SOURCE_DIR} -I${CMAKE_CURRENT_SOURCE_DIR}/include -Iinclude ${CMAKE_CURRENT_SOURCE_DIR}/all.h && cat cpp/cpp-checked.h.bot > ${GEN_DIR}/cpp-checked.h"
    DEPENDS extract_interface all.h dep cpp/cpp-checked.h.top cpp/cpp-checked.h.bot
    WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}
    COMMENT "Generating .gen/cpp-checked.h"
)
add_custom_target(gen_cpp_checked_h DEPENDS ${GEN_DIR}/cpp-checked.h)

# C++ checked conversion header generation (cpp-checked-conversion.h)
add_custom_command(
    OUTPUT ${GEN_DIR}/cpp-checked-conversion.h
    COMMAND bash -c "cat cpp/cpp-checked-conversion.h.top && extract_interface --language=cpp-checked-conversion -I. -I${CMAKE_CURRENT_SOURCE_DIR} -I${CMAKE_CURRENT_SOURCE_DIR}/include -Iinclude ${CMAKE_CURRENT_SOURCE_DIR}/all.h && cat cpp/cpp-checked-conversion.h.bot > ${GEN_DIR}/cpp-checked-conversion.h"
    DEPENDS extract_interface all.h dep cpp/cpp-checked-conversion.h.top cpp/cpp-checked-conversion.h.bot
    WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}
    COMMENT "Generating .gen/cpp-checked-conversion.h"
)
add_custom_target(gen_cpp_checked_conversion_h DEPENDS ${GEN_DIR}/cpp-checked-conversion.h)

# Typed C++ header generation (typed_cpp.h)
add_custom_command(
    OUTPUT ${GEN_DIR}/typed_cpp.h
    COMMAND bash -c "cat cpp/typed_cpp.h.top && extract_interface --language=template-cpp -I. -I${CMAKE_CURRENT_SOURCE_DIR} -I${CMAKE_CURRENT_SOURCE_DIR}/include -Iinclude ${CMAKE_CURRENT_SOURCE_DIR}/all.h && cat cpp/typed_cpp.h.bot > ${GEN_DIR}/typed_cpp.h"
    DEPENDS extract_interface all.h dep cpp/typed_cpp.h.top cpp/typed_cpp.h.bot
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

# Generate a minimal isl_config.h if missing, and define ISL_IMATH for imath backend
set(ISL_CONFIG_H ${CMAKE_CURRENT_SOURCE_DIR}/isl_config.h)
if(NOT EXISTS ${ISL_CONFIG_H})
    file(WRITE ${ISL_CONFIG_H} "#pragma once\n#define ISL_IMATH 1\n/* Minimal isl_config.h for CMake build */\n")
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

if(HAVE_PYTHON AND Python3_Interpreter_FOUND)
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
endif()

# Configure test scripts from .sh.in to .sh
set(TEST_SCRIPTS
    bound_test.sh
    pip_test.sh
    codegen_test.sh
    schedule_test.sh
    flow_test.sh
)
foreach(script IN LISTS TEST_SCRIPTS)
    configure_file(${script}.in ${CMAKE_CURRENT_BINARY_DIR}/${script} @ONLY)
    file(COPY ${CMAKE_CURRENT_BINARY_DIR}/${script} DESTINATION ${CMAKE_CURRENT_SOURCE_DIR})
endforeach()

# Add tests
enable_testing()

foreach(script IN LISTS TEST_SCRIPTS)
    add_test(NAME ${script}
        COMMAND bash ${CMAKE_CURRENT_SOURCE_DIR}/${script}
    )
    set_tests_properties(${script} PROPERTIES
        ENVIRONMENT "PYTHONPATH=${CMAKE_CURRENT_SOURCE_DIR}/interface;ISL_DYLD_LIBRARY_PATH=${CMAKE_CURRENT_SOURCE_DIR}/.libs;LD_LIBRARY_PATH=${CMAKE_CURRENT_SOURCE_DIR}/.libs:$ENV{LD_LIBRARY_PATH}"
    )
endforeach()

# Python test integration
if(HAVE_PYTHON AND Python3_Interpreter_FOUND)
    add_test(NAME isl_test_python.py
        COMMAND ${Python3_EXECUTABLE} ${CMAKE_CURRENT_SOURCE_DIR}/isl_test_python.py
    )
    set_tests_properties(isl_test_python.py PROPERTIES
        ENVIRONMENT "PYTHONPATH=${CMAKE_CURRENT_SOURCE_DIR}/interface;ISL_DYLD_LIBRARY_PATH=${CMAKE_CURRENT_SOURCE_DIR}/.libs;LD_LIBRARY_PATH=${CMAKE_CURRENT_SOURCE_DIR}/.libs:$ENV{LD_LIBRARY_PATH}"
    )
endif()

# Install generated C++ interface headers and Python interface if present
install(FILES
    ${CMAKE_CURRENT_SOURCE_DIR}/include/isl/cpp.h
    ${CMAKE_CURRENT_SOURCE_DIR}/include/isl/cpp-checked.h
    ${CMAKE_CURRENT_SOURCE_DIR}/include/isl/cpp-checked-conversion.h
    ${CMAKE_CURRENT_SOURCE_DIR}/include/isl/typed_cpp.h
    DESTINATION include/isl
)
if(HAVE_PYTHON AND Python3_Interpreter_FOUND)
    install(FILES ${CMAKE_CURRENT_SOURCE_DIR}/interface/isl.py DESTINATION interface)
endif()
