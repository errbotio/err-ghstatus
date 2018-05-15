[![CI Status](https://img.shields.io/travis/argoai/err-ghstatus/master.svg)](https://travis-ci.org/argoai/err-ghstatus/)
[![License: MIT](https://img.shields.io/badge/License-Apachev2-yellow.svg)](https://opensource.org/licenses/MIT)

This is a Github plugin for errbot. It allows to keep track of the relation between your chat users and your github
users and query various statuses of their PRs on Github.

## Base setup

1. Deploy an instance of Errbot if you don't have one already. See [here](http://errbot.io/en/latest/user_guide/setup.html).

2. Talking to Errbot privately as a bot administrator, install the plugin repo for mergequeue.
```
!repos install https://github.com/argoai/err-ghstatus
```

3. Create a github API key for example create a user for the bot and generate a [personal token](https://github.com/settings/tokens).

4. Still talking to Errbot privately as a bot administrator, set the github key with:

```
!plugin config GHStatus {'github-token': 'cafecafecafecafecafecafecafecafecafecafe'}
```

5. Issuing `!help` should give you a new set of commands related to ghstatus.

## Linking a chat user to a github user

Note: the chat user needs to be in the format expected by the chat system here it is an example for Slack with an @:

```
!gh users add @gbinet gbin
```

## Some useful commands

To list your own opened PRs:
```
!gh prs
```

To list someone else PRs:

```
!gh prs @someone
```

To list PRs you need to review:
```
!gh reviews
```

To list PRs someone else needs to review:
```
!gh reviews @someone
```

## More info in `!help`


