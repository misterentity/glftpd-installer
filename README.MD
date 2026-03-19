# glFTPd Installer

An automated installer for [glFTPd](https://glftpd.io) on Linux servers, bundled with a comprehensive set of scripts, modules, and a custom pzs-ng theme. Includes a Windows GUI for remote installation over SSH.

## Features

- Automated installation of glFTPd (32/64-bit auto-detected) with eggdrop sitebot
- Modular architecture -- scripts and modules are loaded dynamically
- Unattended installation mode via `install.cache`
- Windows GUI for remote installation over SSH (with profile save/load, SSH key auth, and real-time log)
- Dynamic section configuration (1-22 sections with custom names)
- Automatic setup of MariaDB for section-traffic and tur-trial3

## Supported Systems

Debian / Ubuntu (must be run as root)

## Requirements

The installer checks for and installs the following packages if not found:

```
cron gcc cmake systemd autoconf bc curl diffutils ftp git iputils-ping
libflac-dev libssl-dev lm-sensors lynx make mariadb-server ncftp passwd
rsync smartmontools tcl tcl-dev tcllib tcl-tls tcpd wget zip bsdmainutils
rsyslog gawk
```

## Quick Start

### Shell Installer (on the Linux server)

```bash
git clone https://github.com/misterentity/glftpd-installer
cd glftpd-installer
chmod +x install.sh
./install.sh
```

### Windows GUI (remote installation)

Requires Python 3.6+ and pip.

```bash
git clone https://github.com/misterentity/glftpd-installer
cd glftpd-installer
pip install -r requirements.txt
python glftpd_installer_gui.py
```

Or just double-click `start_gui.bat` -- it handles dependency installation automatically.

**GUI features:**
- SSH connection with password or key file authentication
- Save/load configuration profiles (JSON)
- Import existing `install.cache` files
- Dynamic section configuration with tooltips
- Real-time installation log with export
- Keyboard shortcuts (Ctrl+S save, Ctrl+O load)

## Included Software

| Component | Version |
|-----------|---------|
| glFTPd | Latest stable (32/64-bit) |
| eggdrop | Latest from GitHub |
| pzs-ng | Latest from GitHub |
| foo-tools | Latest from GitHub (foo-pre) |

## Scripts & Modules

### Modules

- **botnuke** -- Public nukes/unnukes with nuke storage
- **eur0-pre-system** -- Add/del/list affils with foo-pre
- **ircnick** -- Check IRC nicknames of users
- **precheck** -- Pre-upload validation
- **psxc-imdb** -- IMDB lookups and auto-nuking by language
- **section-traffic** -- Section transfer statistics via MariaDB
- **slv-PreBW** -- Bandwidth display during PRE
- **top** -- User/group statistics
- **tur-addip** -- Add IP via IRC
- **tur-archiver** -- Archive sections
- **tur-autonuke** -- Auto-nuke incompletes
- **tur-ircadmin** -- IRC-based site administration
- **tur-request** -- Release request system
- **tur-trial3** -- Trial period management via MariaDB
- **tur-vacation** -- Vacation mode for users
- **whereami** -- Show user location

### Scripts

- **imdbrating** -- Filter movies by genre, score, year from IMDB tags
- **mediainfo** -- Display media information for releases
- **section-manager** -- Add/remove sections without manual config editing
- **tag-empty-inc** -- Tag new directories as empty during creation
- **tmdb** -- TMDB lookups, rescans, symlinks, and nuking (requires free API key from [themoviedb.org](https://themoviedb.org))
- **tur-free** -- Disk space display
- **tur-ftpwho** -- Show connected users
- **tur-precheck** -- Pre-upload file validation
- **tur-predircheck** -- Directory name validation with IRC management
- **tur-rules** -- Auto-generated section rules
- **tur-space** -- Disk space management and cleanup
- **tvmaze** -- TVMaze lookups, rescans, symlinks, and auto-nuking
- **incomplete-list-nuker** -- Nuke incompletes with nuke storage

### Extra Tools

- **backup.sh** -- Backup/restore glFTPd (< 10 seconds restore)
- **syscheck.sh** -- System health checks
- **lastlogin.sh** -- Track user inactivity
- **glftpd-version-check.sh** -- Check for new glFTPd versions
- **update_gl.sh** -- Update glFTPd
- **pzs-ng-update.sh** -- Update pzs-ng

## Unattended Installation

After a regular installation, an `install.cache` file is created in the install directory. This file is used automatically on subsequent runs for fully unattended installation. You can also create one manually:

```bash
sitename="Test"                         # No spaces allowed
port="2010"                             # FTP port
device="/dev/sda1"                      # Device for /site
channelnr="2"                           # Number of IRC channels
channame1="#main n nopass"              # Channel 1 (name, password flag, password)
channame2="#flood y testing"            # Channel 2
announcechannels="#main #flood"        # Announce channels
channelops="#main"                      # Ops channel
ircnickname="l337"                      # Bot owner IRC nickname
sections="3"                            # Number of sections (max 22)

# Recommended section names:
# 0DAY ANIME APPS DOX EBOOKS FLAC GAMES MBLURAY MP3 NSW PS4 PS5 TV-1080
# TV-2160 TV-720 TV-HD TV-NL X264 X264-1080 X264-720 X265-2160 XVID XXX
# XXX-PAYSITE

section1="0DAY"
section1dated="y"
section1zipfiles="y"
section1movie="n"
section2="MP3"
section2dated="y"
section2zipfiles="n"
section2movie="n"
section3="DVDR"
section3dated="n"
section3zipfiles="n"
section3movie="Y"
router="y"                              # Behind a router?
pasv_addr="123.123.123.123"            # Passive address (IP or DNS)
pasv_ports="6000-7000"                  # Passive port range

# IRC server (+ prefix = SSL port, remove :password if none)
ircserver="irc.example.org +7000 ircpassword"

addip="y"                               # Tur-Addip
archiver="y"                             # Tur-Archiver
autonuke="y"                             # Tur-Autonuke
botnuke="y"                              # Botnuke
eur0presystem="y"                        # Eur0-pre-system with foo-pre
ircadmin="y"                             # Tur-Ircadmin
ircnick="y"                              # Ircnick
precheck="y"                             # Precheck
psxcimdbchan="#main"                     # PSXC-IMDB trigger channel
psxcimdb="y"                             # PSXC-IMDB
request="y"                              # Tur-Request
section_traffic="y"                      # Section-Traffic
slvprebw="y"                             # Slv-PreBW
top="y"                                  # Top
trial="y"                                # Tur-Trial
vacation="y"                             # Tur-Vacation
whereami="y"                             # Whereami
username="admin"                         # Admin username
password="password"                      # Admin password
ip="*@192.168.1.*"                       # Admin IP mask
```

## Screenshots

### Normal Installation

![Screenshot_1](https://github.com/misterentity/glftpd-installer/assets/36924638/af283a70-7445-47f0-92fb-91b87aea06c1)
![Screenshot_2](https://github.com/misterentity/glftpd-installer/assets/36924638/ffcf7274-1de5-4e82-8c69-ba9f55450a3d)
![Screenshot_3](https://github.com/misterentity/glftpd-installer/assets/36924638/a13f4665-5ade-4c75-8f9d-41861e91b898)
![Screenshot_4](https://github.com/misterentity/glftpd-installer/assets/36924638/014d40b3-9353-40bf-974d-6af3ade9265f)

### Unattended Installation

![Screenshot_5](https://github.com/misterentity/glftpd-installer/assets/36924638/784c4698-ac20-4210-8581-0f89dac0cbd4)
![Screenshot_6](https://github.com/misterentity/glftpd-installer/assets/36924638/0db1bb75-cdbd-43ea-9586-afceb517e2b3)

## FAQ

**Q: What do I need to know before installing?**

Run the script as root. glFTPd installs to `/glftpd` and the eggdrop to `/glftpd/sitebot`. Make sure the packages listed under Requirements are installed. Only tested on Debian/Ubuntu.

**Q: Is it hard to use?**

No. Run `install.sh` and answer the questions as they come up. There are brief explanations for most options.

**Q: What do I do after installation?**

Create the initial sitebot userfile:

```bash
su - sitebot -c "/glftpd/sitebot/sitebot -m"
```

Then message the bot on IRC (replace `sitename` with your chosen site name):

```
/msg sitename hello
```

Follow the bot's instructions to complete setup. The bot auto-starts via crontab every 10 minutes. To manually start it:

```bash
su - sitebot -c "/glftpd/sitebot/sitebot"
```

**Q: Where can I find more glFTPd scripts?**

Check out https://algorhythm.cc/

## License

This project is licensed under the MIT License.

## Support

For issues and feature requests, please [open an issue](https://github.com/misterentity/glftpd-installer/issues).
