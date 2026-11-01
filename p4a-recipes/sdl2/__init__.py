from os.path import exists, join

from pythonforandroid.recipe import BootstrapNDKRecipe
from pythonforandroid.toolchain import current_directory, shprint
import sh


class LibSDL2Recipe(BootstrapNDKRecipe):
    # Newer stable SDL2 than the 2.30.11 version bundled by the pinned p4a
    # revision. Refreshes the Android Java/native bootstrap sources as well.
    version = "2.32.10"
    url = "https://github.com/libsdl-org/SDL/releases/download/release-{version}/SDL2-{version}.tar.gz"
    md5sum = "7b234751c91737168d88c83041ca5aa9"

    conflicts = ["sdl3"]
    dir_name = "SDL"
    depends = ["sdl2_image", "sdl2_mixer", "sdl2_ttf"]

    def get_recipe_env(self, arch=None, with_flags_in_cc=True, with_python=True):
        env = super().get_recipe_env(
            arch=arch,
            with_flags_in_cc=with_flags_in_cc,
            with_python=with_python,
        )
        env["APP_ALLOW_MISSING_DEPS"] = "true"
        return env

    def should_build(self, arch):
        libdir = join(self.get_build_dir(arch.arch), "../..", "libs", arch.arch)
        libs = [
            "libmain.so",
            "libSDL2.so",
            "libSDL2_image.so",
            "libSDL2_mixer.so",
            "libSDL2_ttf.so",
        ]
        return not all(exists(join(libdir, name)) for name in libs)

    def build_arch(self, arch):
        env = self.get_recipe_env(arch)
        with current_directory(self.get_jni_dir()):
            shprint(
                sh.Command(join(self.ctx.ndk_dir, "ndk-build")),
                "V=1",
                "NDK_DEBUG=" + ("1" if self.ctx.build_as_debuggable else "0"),
                _env=env,
            )


recipe = LibSDL2Recipe()
