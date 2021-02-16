Useful links:   
* [Connan Getting Started](https://docs.conan.io/en/latest/getting_started.html)   
* [Redis C++ Library * recomended*](https://github.com/sewenew/redis-plus-plus)   
* [Redis client libraries](https://redis.io/clients)   
* [Redis docker images](https://hub.docker.com/_/redis/)

*** Make sure you have CMake installed. 3.12+ ***

Let's create a directory for our project,   
and install conan if not installed already:
```bash
mkdir redisTest && cd redisTest
pip install conan
#let's look for redis-plus-plus c++ library in conan
conan search redis-plus-plus --remote=all 
```

create conanfile.txt:

```
[requires]
redis-plus-plus/1.2.1

[generators]
cmake
```

create CMakeLists.txt file:
```cmake
cmake_minimum_required(VERSION 3.12)
project(redistTest)

add_definitions("-std=c++11")

include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()

add_executable(redisTest main.cpp)
target_link_libraries(redisTest ${CONAN_LIBS})
set_property(TARGET redisTest PROPERTY CXX_STANDARD 17)
add_compile_definitions(_CRT_SECURE_NO_WARNINGS WIN32_LEAN_AND_MEAN)
```

create main.cpp:
```c++
#include <iostream>
#include <sw/redis++/redis++.h>

using namespace sw::redis;

int main() {
  try {
    auto redis = Redis("tcp://127.0.0.1:6379");
    redis.set("name", "Marina");
    auto val = redis.get("name");
    if (val) {
      std::cout << "My name is:" << *val << "\n";
    }
  } catch (const Error &e) {
    std::cerr << "Error:" << e.what() << "\n";
  }
  return 0;
}
```

```bash
mkdir build && cd build
conan install -s build_type=Debug ..
cmake -Ax64
cmake --build .
```
Start redis localy or change source code to point to redis in the cloud.

Create in Azure Portal: "Azure Cache for Redis" Enable non ssl port for easier access.
To connect to azure cache, modify the code as follows:
```c++
#include <iostream>
#include <sw/redis++/redis++.h>

using namespace sw::redis;

int main() {
  try {
    ConnectionOptions connection_options;
    connection_options.host = "test_marina.redis.cache.windows.net";
    connection_options.port = 6379; //6380 for secure port
    connection_options.password ="Your AZURE PASSWORD";
    auto redis = Redis(connection_options);
    redis.set("name", "Marina");
    auto val = redis.get("name");
    if (val) {
      std::cout << "My name is:" << *val << "\n";
    }
  } catch (const Error &e) {
    std::cerr << "Error:" << e.what() << "\n";
  }
  return 0;
}
```

Start redis locally (This will not persist data, ALL DATA WILL BE REMOVED ON RESTART)
```bash
 docker run --name redis -p6379:6379 -d redis
 ```

 Start redis with persistant storage:
 ```bash
docker run  --name redis -p6379:6379 -d -v C:\dev\marina\redis_db:/data redis --appendonly yes  
 ```

