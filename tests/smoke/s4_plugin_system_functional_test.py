from base_app.core.plugin_manager import PluginManager
def test_discovery_and_action_call():
    pm = PluginManager('plugins')
    found = pm.discover()
    assert 'sample_hello' in found
    actions = pm.get_actions()
    assert 'hello.sample' in actions
    assert actions['hello.sample']('greg') == 'hello greg'
