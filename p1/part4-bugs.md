# Dockerfile Bugs

The Dockerfile in Part 4 has the following bugs:

1. It uses `apt` instead of `apt-get`.  Although `apt` often works, it
   is designed for interactive use and may behave unexpectedly in
   scripts and Dockerfiles.

2. It splits `apt-get update` and `apt-get install` into separate
   `RUN` commands.  This is problematic because Docker caches each
   layer separately.  If the package index changes after the image is
   built, a rebuild might use the cached (stale) update layer with a
   fresh install, causing package installation to fail.

3. It is missing the `-y` flag for `apt-get install`, which will cause
   the build to hang waiting for user confirmation.
