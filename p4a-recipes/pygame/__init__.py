import os
from os.path import join

from pythonforandroid.recipes.pygame import Pygame2Recipe
from pythonforandroid.toolchain import current_directory


class Pygame261Recipe(Pygame2Recipe):
    version = "2.6.1"
    url = "https://github.com/pygame/pygame/archive/{version}.tar.gz"
    hostpython_prerequisites = ["setuptools", "cython==3.3.0"]

    def prebuild_arch(self, arch):
        # Let python-for-android generate its Android-specific Setup file first.
        super().prebuild_arch(arch)

        with current_directory(self.get_build_dir(arch.arch)):
            # pygame 2.6.1's optional Cython sprite accelerator fails with
            # Cython 3.3.0. pygame.sprite uses its pure-Python implementation.
            sprite_pyx = join("src_c", "cython", "pygame", "_sprite.pyx")
            if os.path.isfile(sprite_pyx):
                os.remove(sprite_pyx)

            # Fix the Android template and the generated Setup file. The
            # Android template must include the SIMD C sources referenced by
            # pygame.surface, otherwise the APK may build but fail at import.
            for setup_path in (
                join("buildconfig", "Setup.Android.SDL2.in"),
                "Setup",
            ):
                with open(setup_path, "r", encoding="utf-8") as file:
                    lines = file.read().splitlines()

                patched_lines = []
                found_surface = False
                for line in lines:
                    stripped = line.lstrip()

                    # _sprite is optional and not imported by pygame.sprite.
                    if stripped.startswith("_sprite "):
                        continue

                    if stripped.startswith("surface "):
                        found_surface = True
                        if "src_c/simd_blitters_sse2.c" not in line:
                            marker = "surface src_c/surface.c"
                            if marker not in line:
                                raise RuntimeError(
                                    f"Unexpected pygame surface setup in {setup_path}"
                                )
                            line = line.replace(
                                marker,
                                "surface src_c/simd_blitters_sse2.c "
                                "src_c/simd_blitters_avx2.c src_c/surface.c",
                                1,
                            )

                    patched_lines.append(line)

                if not found_surface:
                    raise RuntimeError(
                        f"Could not find pygame surface extension in {setup_path}"
                    )

                with open(setup_path, "w", encoding="utf-8") as file:
                    file.write("\n".join(patched_lines) + "\n")


recipe = Pygame261Recipe()
