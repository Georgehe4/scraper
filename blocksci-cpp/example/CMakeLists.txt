file(GLOB EXAMPLE_HEADERS "*.hpp")
file(GLOB EXAMPLE_SOURCES "*.cpp")

add_executable(example ${EXAMPLE_SOURCES} ${EXAMPLE_HEADERS})

target_link_libraries( example cluster)

install(TARGETS example DESTINATION bin)
