def _getversion():
    try:
        from mercurial import ui, hg
        repo = hg.repository(ui.ui(), '.')
        return str(repo.changelog.rev(repo.heads()[0]))
    except:
        return '0'

version = _getversion()
