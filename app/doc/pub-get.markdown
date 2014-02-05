---
title: "Downloading packages from Tavern"
---

The most common use case is to download all the dependencies listed in the
[`pubspec.yaml`](pubspec.html) file in the current working directory, as well as
their [transitive dependencies](glossary.html#transitive-dependency), and place
them in a `packages` directory located next to the pubspec.

Once the dependencies are acquired, they may be referenced in Dart code. For
example, if a Chrome App depends on `git`:

{% highlight dart %}
import "package:git/git.dart;
{% endhighlight %}

The dependencies could be used in any aspect of Chrome App development like in
the HTML. A common example is a Chrome App that depends on `jquery`:

{% highlight html %}
    <script src="packages/jquery/jquery.js"></script>
{% endhighlight %}

When Tavern gets new dependencies, it writes a
[lockfile](glossary.html#lockfile) to ensure that future gets will use the
same versions of those dependencies. Application packages should check in the
lockfile to source control; this ensures the application will use the exact same
versions of all dependencies for all developers and when deployed to production.
Library packages should not check in the lockfile, though, since they're
expected to work with a range of dependency versions.

If a lockfile already exists, Tavern uses the versions of dependencies
locked in it if possible. If a dependency isn't locked, Tavern will get the
latest version of that dependency that satisfies all the [version
constraints](glossary.html#version-constraint).

## Getting a new dependency

If a dependency is added to the pubspec and then Tavern is run, it will
get the new dependency and any of its transitive dependencies and place them in
the `packages` directory. However, it won't change the versions of any
already-acquired dependencies unless that's necessary to get the new
dependency.

## Removing a dependency

If a dependency is removed from the pubspec and then Tavern is run, it will
remove the dependency from the `packages` directory, thus making it
unavailable for importing. Any transitive dependencies of the removed dependency
will also be removed, as long as no remaining immediate dependencies also depend
on them. Removing a dependency will never change the versions of any
already-acquired dependencies.

## Linked `packages` directories

Every [entrypoint](glossary.html#entrypoint) in a package needs to be next to a
`packages` directory in order for it to import packages acquired by Tavern.
However, it's not convenient to put every entrypoint at the top level of the
package alongside the main `packages` directory. You may have example scripts or
tests that you want to be able to run from subdirectories.

Tavern solves this issue by creating additional `packages` directories
that link to the main `packages` directory at the root of your package. It
assumes your package is laid out according to the [package layout
guide](package-layout.html), and creates a linked `packages` directory in
`bin/`, `test/`, and `example/`, as well as their subdirectories.

## The system package cache

Dependencies are downloaded over the internet from [tavern.org]
(http://tavern.org) are stored in a system-wide cache and linked to from the
`packages` directory. This means that if multiple packages use the same version
of the same dependency, it will only need to bedownloaded and stored locally
once. It also means that it's safe to delete the `packages` directory without
worrying about re-downloading packages. By default, the system package cache is
located inside tavern's HTML5 sandboxed
filesystem.

## Getting while offline

If you don't have network access, you can still run Tavern. Since Tavern
downloads packages to a central cache shared by all packages on your system, it
can often find previous-downloaded packages there without needing to hit the
network.

However, by default, Tavern will always try to go online when you get if you
have any hosted dependencies so that it can see if newer versions of them are
available.