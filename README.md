 [ ![Download](https://api.bintray.com/packages/fbergmann/conan/copasi%3Afbergmann/images/download.svg) ](https://bintray.com/fbergmann/conan/copasi%3Afbergmann/_latestVersion)

## Conan package recipe for [*COPASI*](https://copasi.org)



## Issues
All conan specific issues should be tracked in [this project](https://github.com/fbergmann/conan-copasi/issues).

To report possible COPASI bugs or other issues:

* [COPASI issue tracker](https://http://tracker.copasi.org/)

## For Users

### Basic setup

    $ conan install copasi/4.26.213@fbergmann/stable

### Project setup

If you handle multiple dependencies in your project is better to add a *conanfile.txt*

    [requires]
    copasi/4.26.213@fbergmann/stable

    [generators]
    cmake

Complete the installation of requirements for your project running:

    $ mkdir build && cd build && conan install ..

Note: It is recommended that you run conan install from a build directory and not the root of the project directory.  This is because conan generates *conanbuildinfo* files specific to a single build configuration which by default comes from an autodetected default profile located in ~/.conan/profiles/default .  If you pass different build configuration options to conan install, it will generate different *conanbuildinfo* files.  Thus, they should not be added to the root of the project, nor committed to git.


## Build and package

The following command both runs all the steps of the conan file, and publishes the package to the local system cache.  This includes downloading dependencies from "build_requires" and "requires" , and then running the build() method.

    $ conan create . conan/stable


### Available Options

| Option        | Default | Possible Values  |
| ------------- |:----------------- |:------------:|
| shared      | False |  [True, False] |
| fPIC      | True |  [True, False] |
|copasi_se| False| [True, False] | 
              
## Add Remote

You might need to add the Conan Center repo before installing the package:

    $ conan remote add fbergmann "https://api.bintray.com/conan/fbergmann/conan"


## Conan Recipe License

Just as COPASI, the conan recipe uses the [Artistic License 2.0](https://opensource.org/licenses/Artistic-2.0).
