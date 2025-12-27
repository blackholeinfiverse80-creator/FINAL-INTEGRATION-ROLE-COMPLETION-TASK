from src.core.module_loader import load_modules


def test_loader_finds_sample_text():
    modules, errors = load_modules()
    assert 'sample_text' in modules
    assert isinstance(modules['sample_text'], object)
    # bad_module should produce an error entry
    assert any('bad_module' in e or 'bad_module' in str(e) for e in errors)


def test_loader_raise_on_invalid():
    try:
        # this should raise because bad_module has invalid config
        load_modules(raise_on_invalid=True)
        assert False, "Expected ValueError on invalid module config"
    except ValueError:
        pass
