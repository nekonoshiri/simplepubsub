# [プロジェクト情報]
project = "simplepubsub"
copyright = ""
author = ""

# [全般設定]
extensions = ["sphinx.ext.autodoc", "sphinx.ext.viewcode"]
templates_path = []
language = "ja"
exclude_patterns = []
default_role = "any"

# [HTML 出力オプション]
html_theme = "sphinx_rtd_theme"
html_static_path = []

# [autodoc 設定]

# Note:
#    現在 (sphinx 3.2.0) のところ
#    Generic[...] を継承したクラスのコンストラクタの引数が
#    なぜか (*args, **kwds) と表示されてしまうため、
#    autoclass_content を "both" ではなく "class" にして、
#    別途 __init__ に対してドキュメントを生成するように
#    special-members を設定しています。
autoclass_content = "class"
autodoc_member_order = "bysource"
autodoc_default_options = {
    "special-members": "__init__",
    "undoc-members": True,
}
