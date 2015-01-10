import mechanize
import re
from time import sleep
import threading

#cut something in many parts
def chunkIt(seq, num):
  avg = len(seq) / float(num)
  out = []
  last = 0.0
  while last < len(seq):
    out.append(seq[int(last):int(last + avg)])
    last += avg
  return out

#generates a browser
def genbrowser():
    br = mechanize.Browser()
    br.set_handle_robots(False)
    br.set_handle_redirect(True)
    br.addheaders = [('User-agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.1.5) Gecko/20091102 Firefox/3.6.5')]
    return br


class AMB(threading.Thread):
    # define environment variable
    def __init__(self, rangex, user, passw):
        self.br1 = genbrowser()
        self.alogin(self.br1, user, passw)
        self.range = rangex
        threading.Thread.__init__(self)
        self.timeout_value = 30

    # log the user in
    def alogin(self, br, user, passw):
        br.open('http://addmefast.com', \
                      'email={0}&password={1}&login_button=Login'.format(user.replace('@','%40'), passw))
        if 'Welcome' in br.response().read():
            print "Login successful on add me fast"

    #main function
    def run(self):
        sleep(1)
        for i in self.range:
            try:


                #goes to a page with many links to like
                #self.br1.open(
                #act=getLinksList&params={"network":"1", "page":"1", "isFBpage":"1"}
                self.br1.open(
                'http://addmefast.com/includes/ajax.php', 'act=getLinksList&params={"network":"1", "page":"%s", "isFBpage":"1"}' % (i),timeout=self.timeout_value)



                #gets this : title="http://www.facebook.com/Ocacadordetrolls" id="L_b89734d43ed3a3dce20eeaab183365
                page_and_Lid = re.findall('div class="freepts_row" title="(.*)" id="(.*)["]{1}>', self.br1.response().read())



                #confirmSubscribe(162255, "http://www.facebook.com/TOKZ.cs", "02c08e63ec34b4c0b562ed71162255", "1", 0, "UV9W49sV%2FYIQeuGBKkE7PauwNpaJf345m0G%2FDOM3SA6GKryoh8Vrk212");
                number_and_token = re.findall("""getFBLikesBef\((.*)[,]{1} ".*["]{1}, ".*["]{1}, "1", 0, "(.*)["]{1}\);""", self.br1.response().read())

                i = 0

                while i < len(page_and_Lid):

                    page = page_and_Lid[i][0]
                    Lid = page_and_Lid[i][1]
                    number = number_and_token[i][0]
                    token = number_and_token[i][1]

                    #http://addmefast.com/includes/ajax.php, act=checkFollowed&params={"id":"L_b89734d43ed3a3dce20eeaab183365", "url":"http://www.facebook.com/Ocacadordetrolls", "network":"1"}
                    self.br1.open('http://addmefast.com/includes/ajax.php','act=checkFollowed&params={"id":"%s", "url":"%s", "network":"1"}' % (number, page),timeout=self.timeout_value)


                    #http://addmefast.com/includes/ajax.php, act=updateAction&params={"link_id":"L_b89734d43ed3a3dce20eeaab183365", "url":"http://www.facebook.com/Ocacadordetrolls", "network":"1", "IXY5pZpE":"UV9W49sV%2FYIQeuGBKkE7PauwNpaJf345m0G%2FDOM3SA6GKryoh8Vrk212"}
                    self.br1.open('http://addmefast.com/includes/ajax.php','act=updateAction&params={"link_id":"%s", "url":"%s", "network":"1", "IXY5pZpE":"%s"}' % (Lid, page, token),timeout=self.timeout_value)
                    print "New shit made"
                    i+=1
            except Exception, e:
                print e

if __name__=='__main__':
    nbthreads = input('Number of threads: ')
    z = chunkIt(range(1,int(open("number.txt").read())+1), nbthreads)
    user, passw = open('account.txt').read().split(':', 1)
    while 1:
        for i in z:
            try:
                AMB(i, user, passw).start()
            except:
                pass
        while threading.activeCount() > 1:
            sleep(1)

