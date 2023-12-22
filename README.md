# Retrieve Recently Played Tracks from Spotify with a Google Cloud Function and save them to a mongoDB database

### Usage

The code on this repo uses the authorization code flow from spotify to refresh an already generated token. To understand how the authorization flow works follow the guide : 
https://developer.spotify.com/documentation/web-api/tutorials/code-flow

You can use the following CURL calls to: 

Generate a token [1]:

```
curl -X POST "https://accounts.spotify.com/api/token" \
     -H "Content-Type: application/x-www-form-urlencoded" \
     -d "grant_type=client_credentials&client_id={client_id}&client_secret{client_secret}"
```


Validate User with web browser [2]:
Open your browser to this address 
```
"https://accounts.spotify.com/authorize?response_type=code&client_id={your client_id}&scope=user-read-recently-played&redirect_uri={stored redirect uri from your api dashboard}"
```
this will navigate to spotify to validate your user and then redirect to the website you added to the lists of redirec uris with a code attached to the url example:
http://localhost:8080/code=AQAEDnSU3u03iBdO..nOyyZcS
use the code for the last step


Authenticate a token [3]:

```
curl -X POST "https://accounts.spotify.com/api/token" \
     -H "Content-Type: application/x-www-form-urlencoded" \
     -d "grant_type=authorization_code&redirect_uri={url to redirect saved from your api dashboard}&code={code from last step}"\
     -H "Authorization: {your client_id + ':' + client_secret encoded to base64}"
```

Store Initial credentials to MONGO DB collection [4]:

On your MongoDB create a collection Named Spotify and add a new document with the fields: 


```
settings : "auth"
access_token : "{generated access token from step 1}"
refresh_token : "{generated access token from step 3}"
```



#### Create enviroment variables for the project

Create a file at the root of the project with the name .env.yaml with the following variables:

```
_DB_STRING: 
_DB_NAME: 
_SPOTIFY_CLIENT_ID: 
_SPOTIFY_SECRET: 
```

_DB_STRING Is your connection string to a mongo database
_DB_NAME Is the name of your database
_SPOTIFY_CLIENT_ID Is the client id for your spotify api you can obtain it on the settings option of the api dashboard follow the link : https://developer.spotify.com/dashboard
_SPOTIFY_SECRET Is your client_id + ':' + client_secret encoded to base64 

#### Install Python Packages for local develop with:


```
make install
```

This will install the project requiered packages into your computer.


#### Develop by launching with:


```
make dev
```

This will watch the project directory and restart as necessary. 
Navigate to localhost:8080/ to launch the GCP function locally.


#### Deploy to GCP 
Is required to have a GCP account and the Google Cloud CLI
https://cloud.google.com/sdk/docs/install-sdk

*Note add the name of your GCP project to the makefile line 1 

```
make deploy
```

This will deploy your function to GCP once finished follow the links on console or visit https://console.cloud.google.com/functions/list


[!["Buy Me A Coffee"](https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png)](https://bmc.link/tquickbrownfox)


