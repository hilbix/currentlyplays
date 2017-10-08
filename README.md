> Not ready yet.

# OBS compatible "currently playing" webservice

This is a daemon to poll Spotify for "currently playing".

It is fully automatic in the respect, that it:

- starts when the information is requested,
- stops when the information is no more requested,
- tries to only pull data when it is really needed.

What is needed:

- Permanently run a python based background service.
- Export a single PHP based URL to the Web.
- The webpage can be served using Apache or NginX/php-fpm.
- You can use BasicAuth or similar to protect against others.
- The webpage can be served with or without HTTPS.


## Usage

    git clone https://github.com/hilbix/currentlyplays.git
    cd currentlyplays
    ./spotify.py /tmp/

- Keep the latter running all the time (24/7).

- Make `php/index.php` available to the web somehow.
  It must be run by PHP, as the name suggests.

- For example it is available as https://example.org/web/index.php

- Then open https://example.org/web/index.php in your browser

- Follow instructions.

- As soon as the banner shows, you can add this as IFRAME or to OBS webpage rendering.


## License

This Works is placed under the terms of the Copyright Less License,
see file COPYRIGHT.CLL.  USE AT OWN RISK, ABSOLUTELY NO WARRANTY.

Read: This is free as in free beer, free speech and free baby.
Have you ever seen a baby with a Copyright on it?

