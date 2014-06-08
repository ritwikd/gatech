import cgi

my_param = cgi.getfirst('a')

print "Content-Type: text/html\n"
print my_param