# Write the design doc for the new kyrios

## Context

kyrios is being restarted as a new tool. The original Python version
(2017–2020, "a package manager manager") is abandoned and will be
removed. This issue holds the design context that has been gathered so
far, so that whoever writes the design doc can pick it up cold.

### Goal

Declarative machine configuration for macOS, Linux and Windows, kept
in one repo and applied by a tool, instead of clicking through
settings on each OS by hand. The short version is "terraform without
the suck."

### Scope roadmap

The tool should grow through three stages. The file format must not
need to change between stages.

1. **Personal machines.** The tool runs locally on each machine. The
   config lives in a git repo that each machine pulls.
2. **Small fleets.** One machine pushes config to others over SSH or
   WinRM. This needs an inventory, meaning a list of hosts.
3. **Company fleets.** This adds MDM integration, reports on whether
   each machine matches its config, and access control.

### Core principle: the live OS is the state

There is no state file. The configuration of the OS is the state.
Every resource has two operations:

- **read** the current value from the OS
- **write** the desired value to the OS

A plan is the difference between what the tool reads and what the
config file says. Because nothing is stored, nothing can drift, need
locking, or need repair. This works because one machine is cheap to
inspect, while a cloud account is not.

### Three kinds of resources

Some settings cannot be changed by code on purpose. On macOS, privacy
permissions (TCC), such as Full Disk Access, can only be granted by a
person in System Settings or by an MDM profile. Changing them from a
script would mean turning off System Integrity Protection. Windows
has similar limits around Defender and some UAC settings. The tool
can still check these settings, even though it cannot apply them.

1. **Applied:** the tool reads the value and writes the desired one.
   Examples: `defaults write`, registry keys, files, packages,
   services.
2. **Checked but manual:** the tool detects that the setting is wrong,
   opens the right settings pane, tells the user exactly what to
   click, and checks again afterward. Example: granting iTerm Full
   Disk Access, which opens
   `x-apple.systempreferences:com.apple.preference.security?Privacy_AllFiles`.
3. **Profile-backed:** on macOS, the tool generates a `.mobileconfig`
   profile for settings that profiles can control, and the user
   installs it with one click. TCC permissions still need MDM.

### Deletion (OPEN)

A state file normally records what the tool has managed. Without one,
removing a setting from the config file leaves the tool unable to
tell whether it should revert that setting or leave it alone. The
options are:

1. **Removing a setting means "stop managing it."** The value stays
   as it is. This is simple and safe, but over time the machine fills
   with settings that no file describes.
2. **Deletion has to be written down.** The user declares `absent` or
   "restore the default" explicitly, and removes that line later once
   it has run everywhere.
3. **Ownership markers in the OS.** The tool writes a marker next to
   what it manages, such as a `# managed by kyrios` comment block in
   config files, a registry value beside the key, or an extra key in
   a plist. The tool finds everything it owns by scanning for its
   markers, so the OS stays the only state.

The current leaning is option 3 where the OS has room for a marker,
and option 2 where it does not (TCC permissions, for example).

brewmaster (see "Earlier attempts" below) used an append-only log of
`add`/`rm` files. That is a form of option 2, kept as a history of
changes. It is not yet decided whether that log is worth keeping or
was only a workaround.

### Rules learned from Ansible ("never do this")

Problems with Ansible that the new tool must avoid:

- It is a programming language pretending to be YAML.
- Each module handles idempotency differently.
- There is no real plan that shows the changes before they run.
- It is slow.
- **Every setup is organized differently, so knowledge does not
  transfer.** Roles, includes, imports, group_vars, host_vars,
  inventory plugins and Jinja templates can be put together in many
  valid ways. Each company builds its own private framework on top of
  Ansible, and that private framework is what a newcomer actually has
  to learn, mostly by reading examples. Variable precedence (around 22
  levels) makes this worse.

**Design goal:** someone who has used kyrios at one company can open
another company's kyrios repo and understand it in five minutes,
without reading examples first.

Neither extreme reaches that goal:

- **A real programming language** (Pulumi-style, in TypeScript or
  Python) gives familiar syntax, but every company still writes a
  different program. The freedom causes the divergence, and a real
  language gives even more freedom.
- **Plain data with no abstraction** looks the same everywhere, but
  it forces repetition across machines and OSes until someone adds
  templating, which leads back to Ansible.

The middle ground:

1. **The tool decides the file layout, not the user.** For example: a
   `base` file, then one file per OS, then one file per host, merged
   in that order. Every repo has the same shape.
2. **One merge rule that fits in a sentence**, such as "more specific
   files override less specific ones, key by key." There is no
   precedence table.
3. **A small, fixed set of ways to combine pieces, and no templating
   language.** If something cannot be expressed, the tool gains a
   feature. Users do not build their own layer on top.
4. **The tool owns the formatting**, the way `gofmt` does for Go, so
   files look the same everywhere.

### Host identity (OPEN; proposed, not confirmed)

Because company fleets are in scope, the way hosts are identified
affects the file layout from the start.

1. **Hosts matched by name:** a `hosts/<hostname>` file applies to
   that machine. This is simple for three laptops and unmanageable for
   three hundred. brewmaster mapped hostnames to profiles, with
   inheritance between profiles.
2. **Hosts have tags, and config targets tags:** a host declares tags
   such as `work`, `dev` or `gpu`, or they are detected from facts
   such as the OS and CPU type. Config files apply to tags. A host
   file only lists its tags. This scales to fleets, but tag files can
   overlap, which brings back the precedence problem.

Proposal: use tags, and forbid conflicts instead of ranking them. If
two tag files set the same value differently for one host, `plan`
fails and names both files. The only overrides allowed are in the
fixed chain `base` → OS → host. No precedence rule is needed, because
the tool refuses the cases that would need one.

### Prior art, and why each falls short

- **nix-darwin + home-manager:** the strongest declarative option for
  macOS and Linux, but it has no real Windows support and Nix is hard
  to learn.
- **Ansible:** see the rules above.
- **pyinfra:** runs on all three OSes without a state file, but it is
  scripts with a declarative layer on top and has no clear plan step.
- **chezmoi:** handles dotfiles well on all three OSes, but does not
  manage system settings.
- **PowerShell DSC:** designed for Windows. The cross-platform version
  never got much use.

### Earlier attempts by the same author

- **brewmaster** (private, github.com/earlye/brewmaster): the closest
  earlier design, limited to Homebrew. Its `vision.md` covers:
  - no state file; the live system (`brew list` and so on) is queried
    fresh every time and never cached
  - an append-only event log of uuidv7-named `add`/`rm`/`list`
    markdown files
  - a profile hierarchy with inheritance in `brewmaster.yml`, with
    machines mapped to profiles by hostname
  - a pipeline of projector, then a planner that understands
    dependencies, then an approval gate, then apply, then commit and
    push
  - a separate private config repo, symlinked to
    `~/.config/brewmaster`
  - `bm init <repo-url>` to set up a new machine
  - written in Rust, released through the homebrew-tap pipeline
  - plans to extend beyond Homebrew to dotfiles, cloned repos and SSH
    config

  It has six tracked issues in `issues/` and no code.
- **kyrios, Python version** (2017–2020): installs across several
  package managers (Homebrew, npm, pip, bash) from YAML profiles. Two
  of its open GitHub issues still apply to the new design:
  - #24: a script that someone can `curl` on a completely blank Mac
  - #29: try not to depend on Python
- **homebrew-brews** (2016): scripts that reinstall Homebrew and a
  hard-coded list of casks.

## Work for this branch

- [ ] Write the design doc, starting from the context above.
- [ ] Move brewmaster's six `issues/*.md` files into kyrios.
- [ ] Tag the last commit of the Python version as `python-final`.
- [ ] Remove the Python code.
- [ ] Decide what to do with kyrios's six open GitHub issues,
      including one from an outside user: close them, leave them, or
      move them into `issues/`.

## Open questions

- Host identity: tags with conflicts as errors, or something else?
- Deletion: ownership markers, explicit `absent`, an event log, or a
  mix?
- Implementation language. brewmaster chose Rust. kyrios #29 argues
  against depending on an interpreter that may not be installed on a
  blank machine.
- Config file format. It should be plain data that the tool can
  format, with no templating.
- How the tool reaches other hosts in the small-fleet stage (SSH and
  WinRM were mentioned), and how the inventory is described without
  changing the file format.
- How the tool is first installed on a blank machine on each OS
  (see #24).
