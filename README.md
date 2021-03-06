# keylogger

"Malware" that logs all user input to an external server, with some extra bells and whistles. See the features section for a more complete picture of what this keylogger can do.

## Setup

```
chmod +x keylogger.py
sudo ./keylogger
```

## Features

- Takes a picture of the user and "tags" them according to a Keras SqueezeNet classifier
- Records copied text from the clipboard and classifies them as a phrase
- Intelligent phrase detection that detects when a user has typed a "complete" phrase
- Gathers unique user information and catalogues the information in a NoSQL database
- Features an API that allows the person on the other side of the keylogger to inspect and view users information and potentially gleam useful information regarding user's passwords.

## API Documentation

```
GET /websites/<website_name>

- Returns all users who have typed a website name as a phrase, and returns the next 2 phrases that the user has typed
- This corresponds to returning the username and password that a user may have typed.
```

```
GET /tags/<n>

- Returns the top n tags based on the SqueezeNet model
```

```
GET /users/ip/<ip>

- Returns the user and their phrases by their IP
```

```
GET /users/os/<os>

- Returns all users and their phrases by their operating system
- Valid inputs are: Mac, Linux, and Windows (any case)
```

```
GET /copypasta/<n>

- Returns the top n phrases that have been copied by a user
```

## Production Environment

- The entire application is designed with a production Mongo database in mind, so we have credentials to access a read only version of our Mongo DB

The credentials to access a read-only version of the Mongo database are:
- Username: everyone
- Password: bambenek

The entire Mongo DB url is:

```
mongodb://everyone:bambenek@ds259079.mlab.com:59079/cs460_keylogger
```

## Problems Encountered (and potential solutions)

**Problem**: Client has access to production-level data

**Solution**: The client should receive the client, models, and utils modules and exclude the server and config module module. The server can receive all of the modules, or exclude the client folder. Since the server module contains the secrets function needed, and the config contains base64 encoded strings of the mongo credentials, the client never needs to communicate to the backend.

**Problem**: Keylogger cross compatibility

**Solution**: The keylogger was designed to be cross-compatible with both Python 2 and Python 3, and support as many platforms as possible. However, there are some issues that had to be dealt with. `pynput`, the package used for logging key presses, only works with Python 2 for Mac (at least in High Sierra). Mac also requires keylogger to run as a root user application.

## Future Work

- Determine which application is currently running, or which application the phrase was entered. This would help with more intelligent detection

## References

- I would like to cite SqueezeNet as we had to learn a little about how it works for us to use it in our project.

```
@article{SqueezeNet,
    Author = {Forrest N. Iandola and Song Han and Matthew W. Moskewicz and Khalid Ashraf and William J. Dally and Kurt Keutzer},
    Title = {SqueezeNet: AlexNet-level accuracy with 50x fewer parameters and $<$0.5MB model size},
    Journal = {arXiv:1602.07360},
    Year = {2016}
}
```

## Disclaimer

Note that this is being advertised as "malware". I am not responsible for any ill will as a result of using this program. Please see the MIT license for more information.
