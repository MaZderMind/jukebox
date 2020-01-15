Jukebox Software
================

Spotify-Playback
----------------
Install https://github.com/dtcooper/raspotify
Configure device-name, username and password as described in https://github.com/dtcooper/raspotify#configuration
Configuring username and password is required for standalone operation.

Authorize with Spotify
----------------------
Login to https://developer.spotify.com/ and register an App. Add `http://localhost/` to the allowed Redirect-URLs. Rename the `configuration-exampe.toml` to `configuration.toml` and enter your App-ID, App-Secret and the Spotify-Username under which the Control-App should run.

Start `./jukebox.py`. On first startup it will to an OAuth2 request with ypu and redirect you to a url starting with `http://localhost/…` that is probably not reachable. Copy the URL to the Terminal to complete the OAuth2 flow. The quired Token is saved in a File in `~/.config/jukebox/` and from now on used for the authorization.

Configure Playback Actions
--------------------------
