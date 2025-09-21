
def test_macro_pins_available():
    from base_app.services.macro_manager import MacroManager
    from base_app.services.action_registry import ActionRegistry
    mm = MacroManager()
    mm.pin("demo.action")
    called = {"v": False}
    def handler(_ctx, _args): called["v"] = True
    ar = ActionRegistry()
    ar.register({"id":"demo.action","text":"Demo","handler":handler})
    mm.run(ar, "demo.action")
    assert called["v"] is True
    assert "demo.action" in mm.pinned()
