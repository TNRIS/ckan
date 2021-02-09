# -*- coding: utf-8 -*-
#
# CKAN documentation build configuration file, created by
# sphinx-quickstart on Sun Oct 25 16:47:17 2009.
#
# This file is execfile()d with the current directory set to its containing dir.
#
# The contents of this file are pickled, so don't put values in the namespace
# that aren't pickleable (module imports are okay, they're removed automatically).
#
# Note that not all possible configuration values are present in this
# autogenerated file.
#
# All configuration values have a default; values that are commented out
# serve to show the default.

import re
import os
import subprocess


import ckan

# If your extensions (or modules documented by autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#sys.path.append(os.path.abspath('.'))

# General configuration
# ---------------------

rst_epilog = '''

.. |virtualenv_parent_dir| replace:: /usr/lib/ckan
.. |virtualenv| replace:: |virtualenv_parent_dir|/default
.. |activate| replace:: . |virtualenv|/bin/activate
.. |config_parent_dir| replace:: /etc/ckan
.. |config_dir| replace:: |config_parent_dir|/default
.. |production.ini| replace:: |config_dir|/production.ini
.. |development.ini| replace:: |config_dir|/development.ini
.. |git_url| replace:: \https://github.com/ckan/ckan.git
.. |postgres| replace:: PostgreSQL
.. |database| replace:: ckan_default
.. |database_user| replace:: ckan_default
.. |datastore| replace:: datastore_default
.. |datastore_user| replace:: datastore_default
.. |test_database| replace:: ckan_test
.. |test_datastore| replace:: datastore_test
.. |apache_config_file| replace:: /etc/apache2/sites-available/ckan_default.conf
.. |apache.wsgi| replace:: |config_dir|/apache.wsgi
.. |data_dir| replace:: |config_dir|/data
.. |sstore| replace:: |config_dir|/sstore
.. |storage_parent_dir| replace:: /var/lib/ckan
.. |storage_dir| replace:: |storage_parent_dir|/default
.. |storage_path| replace:: |storage_parent_dir|/default
.. |reload_apache| replace:: sudo service apache2 reload
.. |restart_apache| replace:: sudo service apache2 restart
.. |restart_solr| replace:: sudo service jetty8 restart
.. |solr| replace:: Solr
.. |restructuredtext| replace:: reStructuredText
.. |nginx| replace:: Nginx
.. |sqlite| replace:: SQLite
.. |python| replace:: Python
.. |sqlalchemy| replace:: SQLAlchemy
.. |javascript| replace:: JavaScript
.. |apache| replace:: Apache
.. |nginx_config_file| replace:: /etc/nginx/sites-available/ckan
.. |reload_nginx| replace:: sudo service nginx reload
.. |jquery| replace:: jQuery
.. |nodejs| replace:: Node.js

.. _Jinja2: http://jinja.pocoo.org/
.. _CKAN front page: http://127.0.0.1:5000
.. _bootstrap: http://getbootstrap.com/2.3.2/
.. _CKAN issue tracker: https://github.com/ckan/ckan/issues

'''

# Add any Sphinx extension module names here, as strings. They can be extensions
# coming with Sphinx (named 'sphinx.ext.*') or your custom ones.
extensions = ['sphinx.ext.autodoc', 'sphinx.ext.todo',
    'sphinx.ext.autosummary', 'ckan.plugins.toolkit_sphinx_extension']
autodoc_member_order = 'bysource'
todo_include_todos = True

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# The suffix of source filenames.
source_suffix = '.rst'

# The encoding of source files.
#source_encoding = 'utf-8'

# The master toctree document.
master_doc = 'contents'

# General information about the project.
project = u'CKAN'
project_short_name = u'CKAN'
copyright = u'''&copy; 2009-2018 <a href="https://okfn.org/">Open Knowledge International</a> and <a href="https://github.com/ckan/ckan/graphs/contributors">contributors</a>.
    Licensed under <a
    href="https://creativecommons.org/licenses/by-sa/3.0/">Creative Commons
    Attribution ShareAlike (Unported) v3.0 License</a>.<br />
    <img src="https://licensebuttons.net/l/by-sa/3.0/80x15.png" alt="CC License Logo" />
    <a href="https://opendefinition.org/"><img src="https://assets.okfn.org/images/ok_buttons/oc_80x15_blue.png" border="0"
      alt="{{ _('Open Content') }}" /></a>
  '''
html_show_sphinx = False

# The version info for the project you're documenting, acts as replacement for
# |version| and |release|, also used in various other places throughout the
# built documents.
#
# The short X.Y version.
version = ckan.__version__.rstrip('abcdefgh')
# The full version, including alpha/beta/rc tags.
release = ckan.__version__
version_re = None
point_releases_ = None

SUPPORTED_CKAN_VERSIONS = 3


def get_release_tags():
    git_tags = subprocess.check_output(
        ['git', 'tag', '-l'], stderr=subprocess.STDOUT).split()

    release_tags_ = [tag for tag in git_tags if tag.startswith('ckan-')]

    # git tag -l prints out the tags in the right order anyway, but don't rely
    # on that, sort them again here for good measure.
    release_tags_.sort()

    return release_tags_


def parse_version(version_):
    '''Parses version string
        ckan-2.1.3 -> ('2', '1', '3')
        ckan-2.1   -> ('2', '1', None)  (the occasion when we didn't do semver)
    '''
    global version_re
    if version_re is None:
        version_re = re.compile('(?:ckan-)?(\d+)\.(\d+)(?:\.(\d+))?[a-z]?')
    return version_re.match(version_).groups()


def get_equivalent_point_release(version_):
    '''Returns the equivalent point release of any given version.

    e.g.
        ckan-2.1.3 -> ckan-2.1
        ckan-2.1   -> ckan-2.1  (the occasion when we didn't do semver)
    '''
    return 'ckan-%s.%s' % parse_version(version_)[:2]


def get_point_releases():
    '''
    returns ['ckan-1.3', 'ckan-1.4', ... 'ckan-2.0', 'ckan-2.1', ...]
    '''
    global point_releases_
    if point_releases_ is None:
        releases = get_release_tags()
        point_releases_ = []
        for release in releases:
            point_release = get_equivalent_point_release(release)
            if point_release not in point_releases_:
                point_releases_.append(point_release)
    return point_releases_


def get_status_of_this_version():
    '''Returns whether this release is supported or another category.
    '''
    equiv_point_release = get_equivalent_point_release(version)
    point_releases_ = get_point_releases()
    supported_point_releases = point_releases_[-int(SUPPORTED_CKAN_VERSIONS):]
    if equiv_point_release in supported_point_releases:
        return 'supported'
    else:
        return 'unsupported'


def get_current_release_tag():
    ''' Return the name of the tag for the current release

    e.g.: "ckan-2.7.4"

    '''
    release_tags_ = get_release_tags()

    current_tag = "ckan-{}".format(version)

    if release_tags_.__contains__(current_tag):
        return current_tag
    else:
        return 'COULD_NOT_DETECT_TAG_VERSION'


def get_latest_release_tag():
    '''Return the name of the git tag for the latest stable release.

    e.g.: "ckan-2.7.4"

    This requires git to be installed.

    '''
    release_tags_ = get_release_tags()

    if release_tags_:
        return release_tags_[-1]
    else:
        return 'COULD_NOT_DETECT_VERSION_NUMBER'


def get_latest_release_version():
    '''Return the version number of the latest stable release.

    e.g. "2.1.1"

    '''
    version = get_latest_release_tag()[len('ckan-'):]

    # TODO: We could assert here that latest_version matches X.Y.Z.

    return version


def get_current_release_version():
    '''Return the version number of the current release.

    e.g. "2.1.1"

    '''
    version = get_current_release_tag()[len('ckan-'):]

    # TODO: We could assert here that latest_version matches X.Y.Z.

    return version


def get_latest_package_name(distro='trusty'):
    '''Return the filename of the Ubuntu package for the latest stable release.

    e.g. "python-ckan_2.1-trusty_amd64.deb"

    '''
    # We don't create a new package file name for a patch release like 2.1.1,
    # instead we just update the existing 2.1 package. So package names only
    # have the X.Y part of the version number in them, not X.Y.Z.
    latest_minor_version = get_latest_release_version()[:3]

    return 'python-ckan_{version}-{distro}_amd64.deb'.format(
        version=latest_minor_version, distro=distro)


def get_min_setuptools_version():
    '''
    Get the minimum setuptools version as defined in requirement-setuptools.txt
    '''
    filename = os.path.join(os.path.dirname(__file__), '..',
                            'requirement-setuptools.txt')
    with open(filename) as f:
        return f.read().split('==')[1].strip()


def write_substitutions_file(**kwargs):
    '''
    Write a file in the doc/ dir containing reStructuredText substitutions.

    Any keyword argument is stored as a substitution.
    '''
    filename = '_substitutions.rst'
    header = ''':orphan:

.. Some common reStructuredText substitutions.

   **This file is autogenerated!** So don't edit it by hand.

   You can include this file at the top of your ``*.rst`` file with a line
   like::

     .. include:: {filename}

   Then use the substitutions in this file, e.g.::

     |latest_release_version|

'''
    with open(filename, 'w') as f:
        f.write(header.format(filename=filename))
        for name, substitution in kwargs.items():
            f.write('.. |{name}| replace:: {substitution}\n'.format(
                    name=name, substitution=substitution))

current_release_tag_value = get_current_release_tag()
current_release_version = get_current_release_version()
latest_release_tag_value = get_latest_release_tag()
latest_release_version = get_latest_release_version()
latest_minor_version = latest_release_version[:3]
is_master = release.endswith('a')
is_supported = get_status_of_this_version() == 'supported'
is_latest_version = version == latest_release_version

write_substitutions_file(
    current_release_tag=current_release_tag_value,
    current_release_version=current_release_version,
    latest_release_tag=latest_release_tag_value,
    latest_release_version=latest_release_version,
    latest_package_name_precise=get_latest_package_name('precise'),
    latest_package_name_trusty=get_latest_package_name('trusty'),
    latest_package_name_xenial=get_latest_package_name('xenial'),
    min_setuptools_version=get_min_setuptools_version(),
)


# The language for content autogenerated by Sphinx. Refer to documentation
# for a list of supported languages.
#language = None

# There are two options for replacing |today|: either, you set today to some
# non-false value, then it is used:
#today = ''
# Else, today_fmt is used as the format for a strftime call.
#today_fmt = '%B %d, %Y'

# List of documents that shouldn't be included in the build.
#unused_docs = []

# List of directories, relative to source directory, that shouldn't be searched
# for source files.
exclude_trees = ['.build']

# The reST default role (used for this markup: `text`) to use for all documents.
#default_role = None

# If true, '()' will be appended to :func: etc. cross-reference text.
#add_function_parentheses = True

# If true, the current module name will be prepended to all description
# unit titles (such as .. function::).
#add_module_names = True

# If true, sectionauthor and moduleauthor directives will be shown in the
# output. They are ignored by default.
#show_authors = False

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = 'sphinx'


# Options for HTML output
# -----------------------

extra_css_files = ['_static/css/custom.css']

on_rtd = os.environ.get('READTHEDOCS', None) == 'True'
if not on_rtd:
    import sphinx_rtd_theme
    html_theme = 'sphinx_rtd_theme'
    html_theme_path = [sphinx_rtd_theme.get_html_theme_path()]

html_sidebars = {
    '**':  ['globaltoc.html'],
}

html_context = {
    'latest_release_tag_value': latest_release_tag_value,
    'is_master': is_master,
    'is_supported': is_supported,
    'is_latest_version': is_latest_version,
    'extra_css_files': extra_css_files,
    'latest_minor_version': latest_minor_version,
}

# The style sheet to use for HTML and HTML Help pages. A file of that name
# must exist either in Sphinx' static/ path, or in one of the custom paths
# given in html_static_path.
#html_style = 'default.css'

# The name for this set of Sphinx documents.  If None, it defaults to
# "<project> v<release> documentation".
# html_title = "%s v%s Guide" % (project, release)

# A shorter title for the navigation bar.  Default is the same as html_title.
# html_short_title = "%s Admin Guide" % (project_short_name)

# The name of an image file (relative to this directory) to place at the top
# of the sidebar.
# html_logo = None

# The name of an image file (within the static path) to use as favicon of the
# docs.  This file should be a Windows icon file (.ico) being 16x16 or 32x32
# pixels large.
#html_favicon = 'images/favicon.ico'

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

# If not '', a 'Last updated on:' timestamp is inserted at every page bottom,
# using the given strftime format.
#html_last_updated_fmt = '%b %d, %Y'

# If true, SmartyPants will be used to convert quotes and dashes to
# typographically correct entities.
#html_use_smartypants = True

# Additional templates that should be rendered to pages, maps page names to
# template names.
#html_additional_pages = {}

# If false, no module index is generated.
#html_use_modindex = True

# If false, no index is generated.
#html_use_index = True

# If true, the index is split into individual pages for each letter.
#html_split_index = False

# If true, the reST sources are included in the HTML build as _sources/<name>.
#html_copy_source = True

# If true, an OpenSearch description file will be output, and all pages will
# contain a <link> tag referring to it.  The value of this option must be the
# base URL from which the finished HTML is served.
#html_use_opensearch = ''

# If nonempty, this is the file name suffix for HTML files (e.g. ".xhtml").
#html_file_suffix = ''

# Output file base name for HTML help builder.
htmlhelp_basename = 'CKANdoc'


# Options for LaTeX output
# ------------------------

# The paper size ('letter' or 'a4').
#latex_paper_size = 'letter'

# The font size ('10pt', '11pt' or '12pt').
#latex_font_size = '10pt'

# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title, author, document class [howto/manual]).
latex_documents = [
  ('contents', 'CKAN.tex', ur'CKAN documentation',
   ur'CKAN contributors', 'manual'),
]

# The name of an image file (relative to this directory) to place at the top of
# the title page.
#latex_logo = None

# For "manual" documents, if this is true, then toplevel headings are parts,
# not chapters.
#latex_use_parts = False

# Additional stuff for the LaTeX preamble.
#latex_preamble = ''

# Documents to append as an appendix to all manuals.
#latex_appendices = []

# If false, no module index is generated.
#latex_use_modindex = True
