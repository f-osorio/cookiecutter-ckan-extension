import os
import json
import jinja2
import cookiecutter.find as find
import cookiecutter.generate as gen
from cookiecutter.config import DEFAULT_CONFIG as config
from cookiecutter.environment import StrictEnvironment
from cookiecutter.exceptions import NonTemplatedInputDirException


def recut():
    """
        Recreate setup.py so that we can edit keywords
    """
    # template location
    try:
        # cutting cookie from directory with template
        temp_dir = find.find_template('..')
    except NonTemplatedInputDirException as e:
        # template coming from Github
        {% raw %}
        temp_dir = os.path.abspath(config['cookiecuters_dir'],
                                'cookiecutter-ckan-extension',
                                '{{cookiecutter.project}}')
        {% endraw %}

    # Location for resulting file
    destination = os.getcwd()
    # name of template
    setup_template = 'setup.py'

    # get context
    context = {{ cookiecutter | jsonify }}

    # Process keywords
    keywords = context['keywords'].strip().split()
    keywords = [keyword for keyword in keywords
                if keyword not in ('ckan', 'CKAN', 'A','space',
                                   'seperated','list','of','keywords')]
    keywords.insert(0, 'CKAN')
    keywords = u' '.join(keywords)
    context['keywords'] = keywords

    # Double check 'project_shortname' and 'plugin_class_name'
    if context['project_shortname'] != context['project'][8:]:
        context['project_shortname'] = context['project'][8:]

    plugin_class_name = '{}Plugin'.format(context['project_shortname'])
    if context['plugin_class_name'] != plugin_class_name:
        context['plugin_class_name'] = plugin_class_name

    # Recut cookie
    env = StrictEnvironment()
    env.loader = jinja2.FileSystemLoader(temp_dir)
    gen.generate_file(project_dir=destination,
                      infile=setup_template,
                      context={'cookiecutter': context},
                      env=env)


if __name__ == '__main__':
    recut()
