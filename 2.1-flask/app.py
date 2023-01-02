from flask import Flask

from views import AdvtViews


app = Flask('server')

app.add_url_rule('/advt/', methods=['POST'], view_func=AdvtViews.as_view('create_advt'))
app.add_url_rule('/advt/<int:advt_id>', methods=['GET', 'PATCH', 'DELETE'], view_func=AdvtViews.as_view('get_advt'))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
