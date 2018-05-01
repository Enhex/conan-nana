from conans import ConanFile, CMake, tools


class NanaConan(ConanFile):
	name = "nana"
	version = "hotfix-1.5.6"
	license = "Boost Software License - Version 1.0"
	url = "https://github.com/Enhex/conan-nana"
	description = "Nana is a cross-platform library for GUI programming in modern C++ style."
	settings = "os", "compiler", "build_type", "arch"
	options = {"shared": [True, False]}
	default_options = "shared=False"
	generators = "cmake"

	def source(self):
		self.run("git clone --depth=1 https://github.com/cnjinhao/nana.git .")
		# This small hack might be useful to guarantee proper /MT /MD linkage
		# in MSVC if the packaged project doesn't have variables to set it
		# properly
		tools.replace_in_file("CMakeLists.txt", "project(nana)",
							  '''project(nana)
include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()''')

	def build(self):
		cmake = CMake(self)
		cmake.definitions["MSVC_USE_STATIC_RUNTIME"] = False
		cmake.configure()
		cmake.build()

	def package(self):
		self.copy("*.h", dst="include", src="include")
		self.copy("*.hpp", dst="include", src="include")
		self.copy("*pop_ignore_diagnostic", dst="include", src="include")
		self.copy("*push_ignore_diagnostic", dst="include", src="include")
		self.copy("*nana.lib", dst="lib", keep_path=False)
		self.copy("*.dll", dst="bin", keep_path=False)
		self.copy("*.so", dst="lib", keep_path=False)
		self.copy("*.dylib", dst="lib", keep_path=False)
		self.copy("*.a", dst="lib", keep_path=False)

	def package_info(self):
		self.cpp_info.libs = ["nana"]

