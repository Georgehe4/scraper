file(GLOB EXAMPLE_HEADERS "*.hpp")
file(GLOB EXAMPLE_SOURCES "*.cpp")

add_executable(cluster_full ${EXAMPLE_SOURCES} ${EXAMPLE_HEADERS})

target_link_libraries( cluster_full cluster)

install(TARGETS cluster_full DESTINATION bin)
