---
title: "Glossary"
---

### Application package

A package that is not intended to be used as a library. Application packages may
have [dependencies](#dependency) on other packages, but are never depended on
themselves. They are usually meant to be run directly, either on the command
line or in a browser. The opposite of an application package is a [library
package](#library-package).

Application packages should check their [lockfiles](#lockfile) into source
control, so that everyone working on the application and every location the
application is deployed has a consistent set of dependencies. Because their
dependencies are constrained by the lockfile, application packages usually
specify `any` for their dependencies' [version
constraints](#version-constraint).

### Asset

<div class="learn-more">
  <a href="/doc/assets-and-transformers.html">
    Learn more about assets &rarr;
  </a>
</div>

A resource&mdash;Dart, HTML, JavaScript, CSS, image, or anything
else&mdash;intended to be part of a deployed package. The package can be a web
app, a package used by a web app, or any other package that benefits from a
build step. Tools such as [`pub serve`](pub-serve.html) and [`pub build`](pub-
build.html) take _source_ assets (such as an HTML file, a CSS file, and
several Dart files) and produce _generated_ assets (such as the same HTML and
CSS files, plus a single JavaScript file).


### Dependency

Another package that your package relies on. If your package wants to import
code from some other package, that package must be a dependency. Dependencies
are specified in your package's [pubspec](pubspec.html) and described
[here](dependencies.html).

### Entrypoint

"Entrypoint" is used to mean two things. In the general context of Dart, it is
a Dart library that is directly invoked by a Dart implementation. When you
reference a Dart library in a `<script>` tag or pass it as a command line
argument to the standalone Dart VM, that library is the entrypoint. In other
words, it's usually the `.dart` file that contains `main()`.

In the context of Tavern, an "entrypoint package" or "root package" is the root
of a dependency graph. It will usually be an application. When you run your app,
it's the entrypoint package. Every other package it depends on will not be an
entrypoint in that context.

A package can be an entrypoint in some contexts and not in others. Lets say your
app uses a library package A. When you run your app, A is not the entrypoint
package. However, if you go over to A and execute its unit tests, in that
context, it *is* the entrypoint since your app isn't involved.

### Entrypoint directory

A directory inside your package that is allowed to contain
[Dart entrypoints](#entrypoint). Tavern will ensure all of these directories get
a "packages" directory, which is needed for "package:" imports to work.

Tavern has a whitelist of these directories: `benchmark`, `bin`, `example`,
`test`, `tool`, and `web`. Any subdirectories of those (except `bin`) may also
contain entrypoints.

### Immediate dependency

A [dependency](#dependency) that your package directly uses itself. The
dependencies you list in your pubspec are your package's immediate dependencies.
All other dependencies are [transitive dependencies](#transitive-dependency).

### Library package

A package that other packages will depend on. Library packages may have
[dependencies](#dependency) on other packages *and* may be dependencies
themselves. They may also include scripts that will be run directly. The
opposite of a library package is an [application package](#application-package).

Library packages should not check their [lockfile](#lockfile) into source
control, since they should support a range of dependency versions. Their
[immediate dependencies](#immediate-dependency)' [version
constraints](#version-constraints) should be as wide as possible while still
ensuring that the dependencies will be compatible with the versions that were
tested against.

Since [semantic versioning](http://semver.org) requires that libraries increment
their major version numbers for any backwards incompatible changes, library
packages will usually require their dependencies' versions to be greater than or
equal to the versions that were tested and less than the next major version. So
if your library depended on the (fictional) `transmogrify` package and you
tested it at version 1.2.1, your version constraint would be `">=1.2.1 <2.0.0"`.

### Lockfile

A file named `pubspec.lock` that specifies the concrete versions and other
identifying information for every immediate and transitive dependency a package
relies on.

Unlike the pubspec, which only lists immediate dependencies and allows version
ranges, the lock file comprehensively pins down the entire dependency graph to
specific versions of packages. A lockfile ensures that you can recreate the
exact configuration of packages used by an application.

The lockfile is generated automatically for you when you run Tavern. If your
package is an application package, you will typically check this into source
control. For library packages, you usually won't.

<!-- ### SDK constraint

The declared versions of the Dart SDK itself that a package declares that it
supports. An SDK constraint is specified using normal
[version constraint](#version-constraint) syntax, but in a special "environment"
section [in the pubspec](pubspec.html#sdk-constraints).
 -->

### System cache

When Tavern gets a remote package, it downloads it into a single "system cache"
directory maintained by Tavern.

This means you only have to download a given version of a package once and can
then reuse it in as many packages as you would like. It also means you can
delete and regenerate your "packages" directory without having to access the
network.

### Transitive dependency

A dependency that your package indirectly uses because one of its dependencies
requires it. If your package depends on A, which in turn depends on B which
depends on C, then A is an [immediate dependency](#immediate-dependency) and B
and C are transitive ones.

### Uploader

An uploader of a package is someone who has administrative permissions
for that package. They can not only upload new versions of a package,
but also [add and remove other uploaders](pub-uploader.html) for that
package. The uploader of a package is often, but not necessarily, the
same as the [author](pubspec.html#authorauthors) of a package.

Anyone uploading a new package automatically becomes an uploader for
that package. Otherwise, to become an uploader, you need to contact an
existing uploader and ask them to add you as another uploader.

### Version constraint

<div class="learn-more">
  <a href="/doc/dependencies.html#version-constraints">
    Learn more about version constaints &rarr;
  </a>
</div>

A constraint placed on each [dependency](#dependency) of a package that
specifies which versions of that dependency the package is expected to work
with. This can be a single version (e.g. `0.3.0`), a range of versions (e.g.
`">=1.2.1 <2.0.0"`), or `any` (or just empty) to specify that any version is
allowed.

<div class="learn-more">
  <a href="/doc/versioning.html">
    Learn about Tavern's versioning philosophy &rarr;
  </a>
</div>

[Library packages](#library-package) should always specify version constraints
for all of their dependencies, but [application packages](#application-package)
should usually allow any version of their dependencies, since they use the
[lockfile](#lockfile) to manage their dependency versions.
