# 設定帳號資訊
    $ cp dot.opensourcefeeds.cfg $HOME/.opensourcefeeds.cfg
    $ vi $HOME/.opensourcefeeds.cfg

# 安裝 Python 函式庫
    $ virtualenv --no-site-package env --python=python2.7
    $ env/bin/activate
    $ make setup
