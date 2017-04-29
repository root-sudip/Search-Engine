from flask import Flask, render_template, request,\
 g, jsonify, send_from_directory, url_for


app = Flask(__name__)

@app.route('/')
def index():
  return render_template('index.html')

@app.route('/search')
def search():
  return render_template('search_result.html', results=['honu', 'hola','apple'])

@app.route('/result/<name>')
def show_result(name):
  return "You clicked on {}".format(name)

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=8080, debug=True)
