# Community

xRally is a popular project with more than 300 contributors from more
than 70 companies. We are always excited about new members in our team!

## Talk to us

If you have any idea or question please join us on Gitter or IRC:

* [Gitter messenger](https://gitter.im/rally-dev/Lobby)
* IRC: #openstack-rally channel on irc.freenode.net

## Report a bug

You can report bug on Launchpad.net:
[https://bugs.launchpad.net/rally/](https://bugs.launchpad.net/rally/)

## Contribute

**We welcome new contributors!**

Becoming xRally contributor is simple:

* Join our IRC/Gitter chat
* Share your idea
* Get suggestion from core team
* Code your idea
* Push to upstream!

!!! tip

    Before doing any significant contribution, we highly recommend one to join 
    our IRC or Gitter and share ideas.

### Get The Code

```git clone git@github.com:openstack/rally.git```


### Run the tests locally

Running locally test is super easy:

1. Install tox, tool that triggers tests and manages venvs ```pip install tox```
2. Run ```tox``` without parameters to trigger all default tests

!!! tip

    We highly recommend to run tests locally before submitting patches.


### Set Up Gerrit & Accounts

Before you can submit anything, you would have to setup your account and gerrit.

1. [Create launchpad account](https://launchpad.net/)
2. [Join OpenStack launchpad team](https://launchpad.net/openstack)
3. [Join OpenStack as individual member](https://www.openstack.org/join/register/?membership-type=foundation)
4. [Setup you Gerrit](https://review.openstack.org/#/settings/)
5. Setup your repo name ```git config user.name "should match gerrit name"```
6. Setup your repo email ```git config  user.email "should match gerrit email"```
7. Install git-review to push the code ```pip install git-review```
8. Check that it works properly ```git review -s```


### Standard Workflow

Work on new patch:

1. Create a branch for code change: ```git checkout -b <br-name>```
2. Do the code
3. Run tests ```tox```
4. Commit changes ```git commit -a```
5. Send to review ```git review -R```

Addressing code reviews:

1. Fix the code
2. Amend changes ```git commit -a --amend```
3. Send to review ```git review -R```
