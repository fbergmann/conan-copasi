from conans import ConanFile, CMake
import os

class CopasiTestConan(ConanFile):
    settings = "os", "compiler", "arch", "build_type"
    generators = "cmake"

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    #def imports(self):
    #    self.copy("*.dll", src="bin", dst="bin")
    #    self.copy("*.dylib*", src="lib", dst="bin")
    #    self.copy("*.so*", src="lib", dst="bin")

    def test(self):
        self.run(os.path.join("bin", "CopasiSE") + ' ../../brusselator.cps', run_environment=True)
