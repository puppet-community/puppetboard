from datetime import datetime, timedelta

from flask import request, Response, stream_with_context
from pypuppetdb.QueryBuilder import AndOperator, EqualsOperator, OrOperator, NullOperator, LessEqualOperator

from puppetboard.app import app, check_env, puppetdb
from puppetboard.core import environments
from puppetboard.utils import yield_or_stop


@app.route('/nodes', defaults={'env': app.config['DEFAULT_ENVIRONMENT']})
@app.route('/<env>/nodes')
def nodes(env):
    """Fetch all (active) nodes from PuppetDB and stream a table displaying
    those nodes.

    Downside of the streaming aproach is that since we've already sent our
    headers we can't abort the request if we detect an error. Because of this
    we'll end up with an empty table instead because of how yield_or_stop
    works. Once pagination is in place we can change this but we'll need to
    provide a search feature instead.

    :param env: Search for nodes in this (Catalog and Fact) environment
    :type env: :obj:`string`
    """
    envs = environments()
    status_arg = request.args.get('status', '')
    check_env(env, envs)

    query = AndOperator()

    if env != '*':
        query.add(EqualsOperator("catalog_environment", env))

    if status_arg in ['failed', 'changed', 'unchanged']:
        query.add(EqualsOperator('latest_report_status', status_arg))
    elif status_arg == 'unreported':
        unreported = datetime.utcnow()
        unreported = (unreported -
                      timedelta(hours=app.config['UNRESPONSIVE_HOURS']))
        unreported = unreported.replace(microsecond=0).isoformat()

        unrep_query = OrOperator()
        unrep_query.add(NullOperator('report_timestamp', True))
        unrep_query.add(LessEqualOperator('report_timestamp', unreported))

        query.add(unrep_query)

    if len(query.operations) == 0:
        query = None

    nodelist = puppetdb.nodes(
        query=query,
        unreported=app.config['UNRESPONSIVE_HOURS'],
        with_status=True,
        with_event_numbers=app.config['WITH_EVENT_NUMBERS'])
    nodes = []
    for node in yield_or_stop(nodelist):
        if status_arg:
            if node.status == status_arg:
                nodes.append(node)
        else:
            nodes.append(node)
    return Response(stream_with_context(
        stream_template('nodes.html',
                        nodes=nodes,
                        envs=envs,
                        current_env=env)))


def stream_template(template_name, **context):
    app.update_template_context(context)
    t = app.jinja_env.get_template(template_name)
    rv = t.stream(context)
    rv.enable_buffering(5)
    return rv