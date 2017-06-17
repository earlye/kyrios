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

