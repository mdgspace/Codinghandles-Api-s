# Contributing 
Contributions of all kind are welcomed

## Run Locally

### Prerequisites : 
 - [Python](https://www.python.org/downloads/)
 - [Pip](https://python.land/virtual-environments/installing-packages-with-pip)
 - [Redis](https://redis.io/docs/latest/operate/oss_and_stack/install/install-redis/)
 - [Google-oAuth-App](https://developers.google.com/identity/protocols/oauth2/javascript-implicit-flow)

### Clone the Repo
```
git clone https://github.com/mdgspace/Codinghandles-Api-s.git
```
### Change current folder to project folder
### Start redis servers
### Create .env file from .env.example
### Initialize virtual enviroment
```
python -m venv venv
source venv/bin/activate
```
### Install packages
```
pip install --no-cache-dir -r requirements.txt
```

### Run application
```
python app.py
```

## Commit messages
Please start your commits with these prefixes for better understanding among collaborators, based on the type of commit:

```
feat: (addition of a new feature)
rfac: (refactoring the code: optimization/ different logic of existing code - output doesn't change, just the way of execution changes)
docs: (documenting the code, be it readme, or extra comments)
bfix: (bug fixing)
chor: (chore - beautifying code, indents, spaces, camelcasing, changing variable names to have an appropriate meaning)
ptch: (patches - small changes in code, mainly UI, for example color of a button, increasing size of tet, etc etc)
conf: (configurational settings - changing directory structure, updating gitignore, add libraries, changing manifest etc)
About
```