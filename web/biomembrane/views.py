""" Contains all views for the webservice version of ICS.

Copryight (c) 2013 Nick Klose, Richard Leung, Cameron Mann, Glen Nelson, Omar
Qadri, and James Wang under the 401 IP License.

This Agreement, effective the 1st day of April 2013, is entered into by and
between Dr. Nils Petersen (hereinafter "client") and the students of the
Biomembrane team (hereinafter "the development team"), in order to establish
terms and conditions concerning the completion of the Image Correlation
Spectroscopy application (hereinafter "The Application") which is limited to the
application domain of application-domain (hereinafter "the domain of use for the
application").  It is agreed by the client and the development team that all
domain specific knowledge and compiled research is the intellectual property of
the client, regarded as a copyrighted collection. The framework and code base
created by the development team is their own intellectual property, and may only
be used for the purposes outlined in the documentation of the application, which
has been provided to the client. The development team agrees not to use their
framework for, or take part in the development of, anything that falls within
the domain of use for the application, for a period of 6 (six) months after the
signing of this agreement.
"""
from django.shortcuts import render

def program(request):

    """ Renders a test view.
         Template: /web/web/templates/layout.html

         Request parameters (ie, parameters in the request object):
         - None

         Context parameters (ie, keys in the dictionary passed to the template):
        - sec_ title: The title of the section.
        - copyrightdate: The Year of copyright
    """
    temp = {"sec_title": "Program View Page", "copyrightdate": 2013}
    return render(request, 'icslayout.html', temp)

def home(request):
    """ Renders a home  view.
         Template: /web/web/templates/homepage.html

         Request parameters (ie, parameters in the request object):
         - None

         Context parameters (ie, keys in the dictionary passed to the template):
        - sec_ title: The title of the section
        - copyrightdate: The year of copyright.
    """
    temp = {"sec_title": "Welcome to the Homepage", "copyrightdate": 2013}
    return render(request, 'homepage.html', temp)
