from base_app.core.plugin_manager import PluginManager
def test_plugin_metadata_loaded():
    pm = PluginManager('plugins')
    pm.discover()
    assert 'sample_hello' in pm.meta and 'actions' in pm.meta['sample_hello']
