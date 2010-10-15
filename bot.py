from jabberbot import JabberBot, botcmd
import datetime
import urllib2
import urllib
import sys
import simplejson
import getpass

# Config Variables
# ------------------------------------------------------------
AGILEURL = 'https://agiletask.me/tasks'
# ------------------------------------------------------------

class SystemInfoJabberBot(JabberBot):

    def __init__(self, username, password, res = None):
        super( SystemInfoJabberBot, self).__init__( username, password, res)
        self.users = {}

    def post_data(self, url, query):
        """Sends data to specified url and returns response"""

        req = urllib2.Request(url)
        # urlencode the query dictionary
        req.data = urllib.urlencode(query)
        try:
            r = urllib2.urlopen(req)
            result = r.read()
        except:
            result = 'The url: %s is not responding.' % (url)
        return result

    def get_data(self, url):
        """Sends data to specified url and returns response"""

        req = urllib2.Request(url)
        # urlencode the query dictionary
        try:
            r = urllib2.urlopen(req)
            result = r.read()
        except:
            result = 'The url: %s is not responding.' % (url)
        return result

    @botcmd
    def key( self, mess, args):
        """Associate your IM client with your AgileTask account, `key KEYGOESHERE`"""
        user = mess.getFrom()
        if user in self.users:
            return 'You are already subscribed.'
        else:
            self.users[user] = args
            self.log( '%s subscribed to the broadcast.' % user)
            return 'You are now subscribed.'

    @botcmd(hidden=True)
    def whoami( self, mess, args):
        """Tells you your username"""
        return mess.getFrom()

    @botcmd
    def add(self, mess, args):
        """Adds a task in AgileTask - Remember you can use !t to send to today"""
        user = mess.getFrom()
        if user in self.users:
            query = {'task[name]':args}
            url = "%s.json?api_key=%s" % (AGILEURL, self.users[user])
            result = self.post_data(url, query)
            print result
            return 'Successfully added, "' + args + '"'
        else:
            return 'You have not associated this IM client with your AgileTask Account.  Please use the `key KEYGOESHERE` command.'

    @botcmd
    def today(self, mess, args):
        """Returns today tasks"""
        user = mess.getFrom()
        if user in self.users:
            # Send urlencoded params to agile tasks
            url = "%s/today.json?api_key=%s" % (AGILEURL, self.users[user])
            result = simplejson.loads(self.get_data(url))
            todayTasks = ''
            for t in result:
                todayTasks = todayTasks + t['task']['name'] + "\n"
            return todayTasks
        else:
            return 'You have not associated this IM client with your AgileTask Account.  Please use the `key KEYGOESHERE` command.'

def main():
    try:
        username = sys.argv[1]
    except:
        print 'Usage: bot.py jabberusernameoremail'
    else:
        password = getpass.getpass("Enter password for " + username + ": ")
        bot = SystemInfoJabberBot(username,password)
        bot.serve_forever()

if __name__ == "__main__":
    main()
