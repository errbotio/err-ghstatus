from errbot import BotPlugin, botcmd, arg_botcmd
from github import Github

USERS = 'users'

class GHStatus(BotPlugin):
    """
    This plugin allows you to query github for state on developers.
    """
    def get_configuration_template(self):
        """
        Get configuration template for this plugin.
        It works by mapping users on chat to github users.
        """
        return {'github-token': '73fb2928cf017d0ff1e493a7d6ccd4cde1e591f7', 'repo': 'argoai/av'}

    def check_id(self, usr: str):
        try:
            self.build_identifier(usr)
        except Exception as _:
            return False
        return True

    def activate(self):
        if not self.config:
            return  # do not activate if the plugin is not configured
        super().activate()

        self.gh = Github(self.config['github-token'], api_preview=True)
        self.repo = self.gh.get_repo(self.config['repo'])
        self.USERS = USERS  # easier to use for external dependencies.

        if USERS not in self:
            self[USERS]={}

    @botcmd
    def gh_users(self, msg, _):
        """List currently configured users."""
        response = '__Configured users__\n'
        if not self[USERS]:
            return ' -> no user configured yet, use !gh users add'
        for chat_usr, gh_usr in self[USERS].items():
            response += f'- {chat_usr} ▶ {gh_usr}\n'

        return response

    @arg_botcmd('gh_usr')
    @arg_botcmd('chat_usr')
    def gh_users_add(self, _, chat_usr, gh_usr):
        """Add a user mapping from chat user to github user."""
        if not self.check_id(chat_usr):
            return f'{chat_usr} is not a valid {self.mode} user.'  # self.mode is for example 'Slack'

        with self.mutable(USERS) as users:
            users[chat_usr] = gh_usr
        return f'{chat_usr} ▶ {gh_usr} configured.'

    @arg_botcmd('chat_usr')
    def gh_users_rm(self, _, chat_usr):
        """Removes a user mapping."""
        with self.mutable(USERS) as users:
            del users[chat_usr]
        return f'{chat_usr} removed.'

    @botcmd
    def gh_prs(self, msg, chat_usr):
        """Lists PRs opened by your user or the one specified as an argument."""
        if not chat_usr:
            chat_usr = str(msg.frm.aclattr)

        if not self.check_id(chat_usr):
            return f'{chat_usr} is not a valid slack user.'

        users = self[USERS]
        if chat_usr not in users:
            return f'{chat_usr} user is unknown. Use !gh users add.'
        gh_user = users[chat_usr]
        prs = [i for i in self.repo.get_issues(creator=gh_user) if i.pull_request]
        if not prs:
            return 'No PRs found.'
        response = f'__PRs currently opened by {chat_usr}__\n\n'
        for pr in prs:
            response += f'- [{pr.number}]({pr.html_url}) {pr.title}\n'
        return response

    @botcmd
    def gh_reviews(self, msg, chat_usr):
        """Lists the PRs you are specifically named as reviewer on or specify a chat user."""
        if not chat_usr:
            chat_usr = str(msg.frm.aclattr)

        if not self.check_id(chat_usr):
            return f'{chat_usr} is not a valid slack user.'

        users = self[USERS]
        if chat_usr not in users:
            return f'{chat_usr} user is unknown. Use !gh users add.'
        gh_user = users[chat_usr]

        # adding review-requested AND involves is a trick to only get PRs you are explicitely asked to review.
        # otherwise you will get any group you belong to.
        prs = self.gh.search_issues(f'state:open type:pr review-requested:{gh_user} ' 
                                    f'involves:{gh_user} repo:{self.repo.full_name}')

        if not prs:
            return 'No PRs found.'
        response = f'__PRs open for review for {chat_usr}__\n\n'
        for pr in prs:
            response += f'- [{pr.number}]({pr.html_url}) {pr.title}\n'
        return response

