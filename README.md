# gmail2notmuch
Scan notmuch db for mails with tags X-Keywords in header and add those as notmuch tags

## Description

This script is meant to be used in conjunction with offlineimap and notmuch.
When syncing from GMail with offlineimap and `synclabels` enabled, every mail
gets a `X-Keywords` header addition. Using this script will add those as 
`notmuch`-tags to each respective mail.

## Installation

This script requires `notmuch`'s python bindings to be installed. On Ubuntu or Debian, try:

    sudo apt-get install python-notmuch

## Usage

    ./gmail2notmuch /path/to/notmuch/config/file # Will use specified config file
    NOTMUCH_CONFIG=/path/to/notmuch/config/file ./gmail2notmuch # dito
    ./gmail2notmuch # will use ~/.notmuch-config

Adding `--add-gmail` will add gmail's internal tags like `Sent`, `Important`, etc, too.

## Contributors

* Florian Heinle <florian@florianheinle.de>

## License

GNU General Public License v3.0
