# Kyrios

Kyrios is a package manager manager. Today software deployment has
fractured to the point where it is difficult to know ahead of time
which package manager one should use to install something on a given
platform.

For example, if I asked you to install a package called `git-open`,
your first job would be to figure out where that is. A little digging
would show you that it is at https://github.com/paulirish/git-open.
Then you would learn that you need to have `npm` installed in order to
install `git-open`, because `git-open` is apparently written using
javascript, which of course has its own de facto package manager,
npm. But how do you get `npm` installed? Well, you'll have to hunt
that down, too.

But wait, once you've got all of that installed, I might ask you
to install `nephele`. And guess what? That's available here: 
https://github.com/earlye/nephele. It's pretty easy to install.
That is, if you have `pip` available, because `nephele` is written
in python, and *its* package manager is `pip`.

Other package managers one might find on OSX include `homebrew`,
`gem`, `docker`, `vagrant`, `bower`, old-fashioned
`download;configure;make;make-install`, and on and on and on. Other
platforms (linux, Windows) have the same problem, to varying degree.

A lot of these package managers and the packages they manage are
small, but necessary parts of the software development process
itself. So setting up a workstation on which to develop has
become an annoying hassle. There's got to be a way to
simplify things. Kyrios is an attempt to do that.

I'm not building Kyrios to _replace_ those package managers. Instead, 
I just want a single manager to control all the other ones. It would be
nice if it could make "set up my development box" be as simple as
`kyrios {my-profile}.yaml`, perhaps repeatedly if there are packages
that require a reboot.

That's the vision. It's nowhere near that... yet.

# The Name

`Kyrios` means "master" in Greek.

Well, actually it's `kýrios`.

No, that's not quite true either. It's `κύριος`.

Well, that's what Google translate tells me anyway. Greek is hard, so 
I Americanized it. Google tells me that if I take my Americanized
version, `kyrios` and translate it from Greek to English, it means
`mainly`. Meh. Close enough.

# The Roadmap

The following features are what I think are necessary to get from
the null-set to a version 1.0:

* A fairly robust set of package information including dependencies.
Note that dependencies here does not necessarily mean "all the things
a package depends on," because the front-line package managers typically
manage that sort of thing and therefore replicating that info here
would be overkill. Dependencies here really means something more like,
"You need to install this using package manager 'X'."

* A fairly robust collection of package manager definitions for
OSX, Linux, and Windows. Windows in particular will be a challenge
because Cygwin doesn't really have a package manager. This means
lots of rebooting, probably.

* A fairly robust mechanism for removing packages.

Beyond that:

* It would be nice to see a community form around this, where others
are providing package definitions and the like.

# Non-goals

* *Complexity-of-use* - I really don't want this to be difficult to
install or use. I've intentionally kept the dependencies minimal
(python, pip and python.stdplus.org - installed by pip), so that
setting up a new box is basically "get python & pip installed, then
run kyrios.sh."

* *Replacing package manager 'X'* - If you prefer some other package
manager, that's fine. I'm not trying to replace it. I'm trying to make
my own life easier. Yes, I'm aware of things like ansible, puppet, and
chef. No, I'm not going to use them for this problem.

