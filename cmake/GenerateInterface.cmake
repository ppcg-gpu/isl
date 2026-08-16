# Assemble a generated interface file.
#
# Optionally runs a generator and concatenates its output with a number of
# fixed fragments.  The result is written atomically, so an interrupted or
# failing run never leaves a half written file behind.
#
# Everything is driven by -D options rather than by a shell pipeline, because
# add_custom_command() escapes redirections and the generated sources are too
# large to pass through CMake strings safely.
#
#   OUTPUT          file to create
#   PREPEND         '|' separated files to place before the generator output
#   APPEND          '|' separated files to place after the generator output
#   GENERATOR       program to run; may be empty for plain concatenation
#   GENERATOR_ARGS  '|' separated arguments for the generator
#   WORKDIR         working directory for the generator

if(NOT OUTPUT)
  message(FATAL_ERROR "GenerateInterface: OUTPUT is required")
endif()

set(fragments "")

if(PREPEND)
  string(REPLACE "|" ";" prepend_list "${PREPEND}")
  list(APPEND fragments ${prepend_list})
endif()

if(GENERATOR)
  string(REPLACE "|" ";" generator_args "${GENERATOR_ARGS}")
  set(body "${OUTPUT}.body")
  execute_process(
    COMMAND ${GENERATOR} ${generator_args}
    WORKING_DIRECTORY "${WORKDIR}"
    OUTPUT_FILE "${body}"
    RESULT_VARIABLE generator_result
  )
  if(NOT generator_result EQUAL 0)
    file(REMOVE "${body}")
    message(FATAL_ERROR "${GENERATOR} failed with ${generator_result}")
  endif()
  list(APPEND fragments "${body}")
endif()

if(APPEND)
  string(REPLACE "|" ";" append_list "${APPEND}")
  list(APPEND fragments ${append_list})
endif()

execute_process(
  COMMAND ${CMAKE_COMMAND} -E cat ${fragments}
  OUTPUT_FILE "${OUTPUT}.tmp"
  RESULT_VARIABLE cat_result
)
if(NOT cat_result EQUAL 0)
  file(REMOVE "${OUTPUT}.tmp")
  message(FATAL_ERROR "Concatenating ${fragments} failed with ${cat_result}")
endif()

file(RENAME "${OUTPUT}.tmp" "${OUTPUT}")
if(GENERATOR)
  file(REMOVE "${OUTPUT}.body")
endif()
