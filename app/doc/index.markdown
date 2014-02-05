---
title: "Getting Started"
---

1. [Installing and configuring tavern](#installing-and-configuring-pub)
1. [Creating a package](#creating-a-package)
1. [Adding a dependency](#adding-a-dependency)
1. [Getting dependencies](#getting-dependencies)
1. [Importing code from a dependency](#importing-code-from-a-dependency)
1. [Upgrading a dependency](#upgrading-a-dependency)
1. [Publishing a package](#publishing-a-package)
{:.toc}

*Tavern* is a package manager for Chrome Apps. It helps you reuse existing code
and bundle your apps and libraries so that you can reuse and share them
with other people. Tavern handles versioning and dependency management so that
you can ensure that your app runs on other machines exactly the same as it does
on yours.

To **find** a package that's on tavern.org,
use the Search box at the top right of this page.

To **use** a package that's on tavern.org:

1. Create a `pubspec.yaml` file
   (if one doesn't already exist)
   and list the package as dependency.
   For example, to use the [jquery](/packages/jquery) package
   in an app, put this in a top-level file named `pubspec.yaml`:

        name: my_app
        dependencies:
          jquery: any

1. Run tavern (typically through the Spark IDE).

1. Import one or more libraries from the package:

        <script src="packages/jquery/jquery.js"></script>

For details and pointers to more documentation, read on.

## Installing and configuring tavern

The Tavern app can be downloaded from the Chrome Apps Webstore. Perhaps more
convenient is simply to install the
[Spark IDE](https://github.com/dart-lang/spark) and run Tavern from there.

## Creating a package

<div class="learn-more">
  <a href="/doc/package-layout.html">
    Learn more about packages &rarr;
  </a>
</div>

A **package** in Tavern is a directory that contains code and any other stuff
that goes along with it like resources, tests, and docs. Frameworks and
reusable libraries are obviously packages, but applications are too. If your
app wants to use Tavern packages, it needs to be a package too.

While everything is a package in Tavern, there are two flavors of packages that
are used slightly differently in practice. A [**library
package**](glossary.html#library-package) is a package that is intended to be
reused by other packages. It will usually have code that other packages import,
and it will likely be hosted somewhere that people can get to. An [**application
package**](glossary.html#application-package) only *consumes* packages but
doesn't itself get reused. In other words, library packages will be used as
dependencies, but application packages won't.

In most cases, there's no difference between the two and we'll just say
"package". In the few places where it does matter, we'll specify "library
package" or "application package".

<div class="learn-more">
  <a href="/doc/pubspec.html">
    Learn more about pubspecs &rarr;
  </a>
</div>

To turn your app into an application package so it can use other packages, you
just need to give it a **pubspec**. This file is written using the
[YAML language](http://yaml.org) and is named `pubspec.yaml`. The simplest
possible pubspec just contains the name of the package. Save the pubspec file as
`pubspec.yaml` in the root directory of your app.

Behold, the simplest possible `pubspec.yaml`:

{% highlight yaml %}
name: my_app
{% endhighlight %}

Now `my_app` is a Tavern package!

## Adding a dependency

<div class="learn-more">
  <a href="/doc/dependencies.html">
    Learn more about dependencies &rarr;
  </a>
</div>

One of Tavern's main jobs is managing **dependencies**. A dependency is just
another package that your package relies on. If your app is using some
transformation library called "transmogrify", then your app package will depend
on the `transmogrify` package.

You specify your package's dependencies in the pubspec file immediately after
your package name. For example:

{% highlight yaml %}
name: my_app
dependencies:
  transmogrify:
{% endhighlight %}

Here, we are declaring a dependency on the (fictional) `transmogrify` package.

## Getting dependencies

<div class="learn-more">
  <a href="/doc/pub-get.html">
    Learn more about downloading packages &rarr;
  </a>
</div>

Once you've declared a dependency, you then tell Tavern to get it for you. If
you're Spark, select `pubspec.yaml` and click the "Run" button.

When you do this, Tavern will create a `packages` directory in the same
directory as `pubspec.yaml`. In there, it will place each package that your
package depends on (these are called your **immediate dependencies**). It will
also look at all of those packages and get everything *they* depend on,
recursively (these are your **transitive dependencies**).

When this is done, you will have a `packages` directory that contains every
single package your program needs in order to run.

## Importing code from a dependency

Now that you have a dependency wired up, you want to be able to use code from
it. Typically this is done by referring to the file at location
`packages\package_name\specific_file_name`.

In Dart though you can import it using the `package:` scheme:

{% highlight dart %}
import 'package:transmogrify/transmogrify.dart';
{% endhighlight %}

This looks inside the `transmogrify` package for a top-level file named
`transmogrify.dart`. Most packages just define a single entrypoint whose name
is the same as the name of the package. Check the documentation for the package
to see if it exposes anything different for you to import.

<aside class="alert alert-info">
This works by looking inside the generated <tt>packages</tt> directory. If you
get an error, the directory may be out of date. Fix it by running
Tavern whenever you change your pubspec.
</aside>

You can also use this style to import libraries from within your own package.
For example, let's say your package is laid out like:

    transmogrify/
      lib/
        transmogrify.dart
        parser.dart
      test/
        parser/
          parser_test.dart

The `parser_test` file *could* import `parser.dart` like this:

{% highlight dart %}
import '../../lib/parser.dart';
{% endhighlight %}

But that's a pretty nasty relative path. If `parser_test.dart` is ever moved
up or down a directory, that path will break and you'll have to fix the code.
Instead, you can do:

{% highlight dart %}
import 'package:transmogrify/parser.dart';
{% endhighlight %}

This way, the import can always get to `parser.dart` regardless of where the
importing file is.

## Upgrading a dependency

The first time you get a new dependency for your package, Tavern will download
the latest version of it that's compatible with your other dependencies. It then
locks your package to *always* use that version by creating a **lockfile**.
This is a file named `pubspec.lock` that Tavern creates and stores next to your
pubspec. It lists the specific versions of each dependency (immediate and
transitive) that your package uses.

If this is an application package, you will check this file into source control.
That way, everyone hacking on your app ensures they are using the same versions
of all of the packages. This also makes sure you use the same versions of stuff
when you deploy your app to production.

When you are ready to upgrade your dependencies to the latest versions, delete
the `pubspec.lock` file and re-run Tavern.

## Publishing a package

<div class="learn-more">
  <a href="/doc/pub-lish.html">
  Learn more about publishing packages &rarr;
  </a>
</div>

Tavern isn't just for using other people's packages. It also allows you to share
your packages with the world. Once you've written some useful code and you want
everyone else to be able to use it, then look at the
[publish instructions](/doc/pub-lish.html) for how to share your package.

Tavern will check to make sure that your package follows the [pubspec
format](pubspec.html) and [package layout conventions](package-layout.html), and
then upload your package to [tavern.org](http://tavern.org). Then
any Tavern user will be able to download it or depend on it in their pubspecs.
For example, if you just published version 1.0.0 of a package named
`transmogrify`, then they can write:

{% highlight yaml %}
dependencies:
  transmogrify: ">= 1.0.0 < 2.0.0"
{% endhighlight %}

Keep in mind that publishing is forever. As soon as you publish your awesome
package, users will be able to depend on it. Once they start doing that,
removing the package would break theirs. To avoid that, Tavern strongly
discourages deleting packages. You can always upload new versions of your
package, but old ones will continue to be available for users that aren't ready
to upgrade yet.
