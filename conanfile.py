#!/usr/bin/env python
# -*- coding: utf-8 -*-
from conans import ConanFile, tools, CMake
from shutil import copyfile

class CopasiConan(ConanFile):

    name = "copasi"
    version = "4.26.213"
    url = "http://github.com/fbergmann/conan-copasi"
    homepage = "https://copasi.org"
    author = "Frank Bergmann"
    license = "BSD"

    description = ("COPASI is a software tool for editing, simulating, and analyzing models of biochemical reaction networks. COPASI is available for all major platforms (Linux, Windows, OS X), easy to install COPASI is free and open source software.")

    settings = "os", "arch", "compiler", "build_type"

    options = {
        "shared": [True, False],
        "fPIC": [True, False],
        "copasi_se": [True, False]
        #"copasi_ui": [True, False]
    }

    default_options = (
        "shared=False",
        "fPIC=True",
        "copasi_se=True"
        #"copasi_ui=True"
    )

    generators = "cmake"
    
    exports_sources = ["CopasiVersion.h", "copasi.patch"]

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC

        self.requires("Expat/2.2.7@pix4d/stable")
        self.options['Expat'].shared = self.options.shared

        self.requires("crossguid/0.2.2@fbergmann/stable")
        
        self.requires("libcombine/0.2.3@fbergmann/stable")
        self.options['libcombine'].shared = self.options.shared
        
        self.requires("libsedml/0.4.5@fbergmann/stable")
        self.options['libsedml'].shared = self.options.shared

        self.requires("libsbml/5.18.1@fbergmann/stable")
        self.options['libsbml'].shared = self.options.shared
        
        self.requires("raptor/1.4.19@fbergmann/stable")

        self.requires("zipper/0.9.1@fbergmann/stable")
        self.options['zipper'].shared = self.options.shared

        #self.requires("lapack/3.7.1@conan/stable")
        #self.options['lapack'].shared = self.options.shared
        #if self.settings.os == "Windows": 
        #    self.options['lapack'].visual_studio=True
        #    self.options['lapack'].shared = True
        
        if not self.settings.os == "Macos":
          self.requires("clapack/3.2.1@fbergmann/stable")
          
        #if self.options.copasi_ui:
        #  self.requires("bzip2/1.0.8@conan/stable")
        #  self.requires("qt/5.13.0@bincrafters/stable")
        #  self.options['qt'].qtcharts = True
        #  self.options['qt'].qtdatavis3d = True
        #  self.options['qt'].qtgraphicaleffects = True
        #  self.options['qt'].with_mysql = False
        #  self.options['qt'].with_odbc = False


    def source(self):
        git = tools.Git("src")
        git.clone("https://github.com/copasi/COPASI/", branch="release/Version-4.27")
        copyfile('CopasiVersion.h', 'src/copasi/CopasiVersion.h')
        tools.replace_in_file('src/CMakeLists.txt', 'project (COPASI VERSION "${COPASI_VERSION_MAJOR}.${COPASI_VERSION_MINOR}.${COPASI_VERSION_BUILD}")', '''project (COPASI VERSION "${COPASI_VERSION_MAJOR}.${COPASI_VERSION_MINOR}.${COPASI_VERSION_BUILD}")

include(${CMAKE_BINARY_DIR}/../conanbuildinfo.cmake)
conan_basic_setup()''')

    def _configure(self, cmake):
        args = ['-DCOPASI_INSTALL_C_API=ON', 
        '-DDISABLE_CORE_OBJECT_LIBRARY=ON',
        '-DBUILD_GUI=OFF']
        if self.options.copasi_se: 
            args.append('-DBUILD_SE=ON')
        else:
            args.append('-DBUILD_SE=OFF')
        if self.settings.compiler == 'Visual Studio' and 'MT' in self.settings.compiler.runtime:
            args.append('-DWITH_STATIC_RUNTIME=ON')
        if self.options.shared:
            args.append('-DENABLE_LIBCOPASISE_SHARED=ON')

        cmake.configure(build_folder="build", args=args, source_folder="src")

    def build(self):
        cmake = CMake(self)
        self._configure(cmake)
        cmake.build()

    def package(self):
        cmake = CMake(self)
        self._configure(cmake)
        cmake.install()
        self.copy("*.lib", dst="lib", keep_path=False)
        if self.settings.os == "Windows":
            self.copy("*.dll", dst="bin", keep_path=False)
        self.copy("*.so", dst="lib", keep_path=False)
        self.copy("*.dylib", dst="lib", keep_path=False)
        self.copy("*.a", dst="lib", keep_path=False)

        if self.options.copasi_se: 
            self.copy("CopasiSE*", dst="bin", keep_path=False)            

        
    def deploy(self):
        self.copy("*", dst="bin", src="bin")

    def package_info(self):

        libfile = "COPASISE"

        if not self.settings.os == "Windows":
            if self.options.shared:
                if self.settings.os == "Linux":
                    libfile += ".so"
                if self.settings.os == "Macos":
                    libfile += ".dylib"
            else:
                libfile += ".a"
        else:
            if self.options.shared:
                libfile += ".dll"
            else:
                libfile += ".lib"

        self.cpp_info.libs = [libfile]
        if self.settings.os == "Macos":
            self.cpp_info.exelinkflags.append("-framework CoreFoundation")
            self.cpp_info.exelinkflags.append("-framework Accelerate")
        if not self.settings.os == "Windows":
          self.cpp_info.cxxflags = ["-std=c++11"]
