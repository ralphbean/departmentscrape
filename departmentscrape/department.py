from twill.browser import TwillBrowser
from BeautifulSoup import BeautifulSoup
import ClientForm

import sys

class Department(object):
    """ Represents a new trac department """
    _param_defaults = {
        'uri' : 'www.example.com'
    }
    _field_defaults = {
        'department_from' : '',
        'department_to' : '',
        'department_name' : '',
    }

    def __init__(self, **kw):
        """ Set up a department and connection 

        Possible arguments (with defaults) are:

            uri         'www.example.com'
        """
        self.params = self._param_defaults
        for k, v in kw.iteritems():
            if not k in self._param_defaults.keys():
                raise ValueError, "Unexpected keyword '%s=%s'"%(str(k),str(v))
            if k in self.params:
                self.params[k] = v
            else:
                raise ValueError, "WTF... '%s=%s'" % (str(k), str(v))

        # Setup our connection
        self.br = TwillBrowser()
        self.br._browser.addheaders.append(('User-agent', 'Mozilla/5.0 (X11; U; Linux x86_64; en-US) AppleWebKit/533.2 (KHTML, like Gecko) Chrome/5.0.342.7 Safari/533.2'))

        # Test our connection
        url = 'http://%s' % self.params['uri']
        self.br.go(url)
        code = self.br.get_code()
        if code != 200:
            raise Exception, "(Code: %i)  Failed to access %s." % (code, url)

    def update(self, **kw):
        """ Fill in department values.

        Possible arguments (with defaults) are:

            department_from
            department_to
            department_name
        """
        self.fields = self._field_defaults
        for k, v in kw.iteritems():
            if not k in self._field_defaults.keys():
                raise ValueError, "Unexpected keyword '%s=%s'"%(str(k),str(v))

            if k in self.fields:
                if self.fields[k] == v:
                    pass
                else:
                    self.fields[k] = v
            else:
                raise ValueError, "WTF... '%s=%s'" % (str(k), str(v))

    def submit(self):
        """ Submit a new department.  Returns the HTTP status code. """

        url = 'https://%s' % self.params['uri']
        self.br.go(url)
        code = self.br.get_code()
        if code != 200:
            raise Exception, "(Code: %i)  Failed to access %s." % (code, url)

        form = self.br.get_form('thisForm')
        for k, v in self.fields.iteritems():
            control = form.find_control(k)
            if control.is_of_kind('text'):
                form[k] = str(v)
            elif control.is_of_kind('singlelist'):
                def get_text(item):
                    if len(item.get_labels()) == 0:
                        return ''
                    return item.get_labels()[0].text

                possible = [ get_text(item) for item in control.get_items() ]

                if v not in possible:
                    raise ValueError, '"%s" not a valid option for %s (%s)' % (
                        v, k, str(possible))

                form[k] = [v]
            else:
                raise ValueError, "Unimplemented '%s'." % k
        self.br.clicked(form, form.find_control('submit'))
        self.br.submit()

        code = self.br.get_code()
        if code != 200:
            raise ValueException, "failure with code %i" % code

        soup = BeautifulSoup(self.br.get_html())
        table = soup.findAll(name='table')[0]
        cols = table.findAll(name='td')
        code, name = cols[:2]
        return str(name.text)
