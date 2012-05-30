# Copyright (c) 2012, the Dart project authors.  Please see the AUTHORS file
# for details. All rights reserved. Use of this source code is governed by a
# BSD-style license that can be found in the LICENSE file.

"""This module provides utility functions for handlers."""

import os

import cherrypy
from google.appengine.api import users

import pystache

_renderer = pystache.Renderer(search_dirs = [
        os.path.join(os.path.dirname(__file__), '../views')])

def render(name, *context, **kwargs):
    """Renders a Moustache template with the standard layout.

    The interface of this function is the same as pystache.Renderer.render,
    except that it takes the name of a template instead of the template string
    itself. These templates are located in views/.

    This also surrounds the rendered template in the layout template (located in
    views/layout.mustache)."""

    content = _renderer.render(
        _renderer.load_template(name), *context, **kwargs)

    # We're about to display the flash message, so we should get rid of the
    # cookie containing it.
    cherrypy.response.cookie['flash'] = ''
    cherrypy.response.cookie['flash']['expires'] = 0
    cherrypy.response.cookie['flash']['path'] = '/'
    flash = cherrypy.request.cookie.get('flash')

    return _renderer.render(
        _renderer.load_template("layout"),
        content = content,
        logged_in = users.get_current_user() is not None,
        login_url = users.create_login_url(cherrypy.url()),
        logout_url = users.create_logout_url(cherrypy.url()),
        message = flash and flash.value)

def flash(message):
    """Records a message for the user.

    This message will be displayed and cleared next time a page is rendered for
    the user. Redirects and error pages will not clear the message."""
    cherrypy.response.cookie['flash'] = message
    cherrypy.response.cookie['flash']['path'] = '/'
