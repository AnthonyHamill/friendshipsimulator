from flask import Flask, request, render_template, url_for
from werkzeug.utils import secure_filename
import os
import feedparser

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'

@app.route('/', methods=['GET', 'POST'])
def home():
    default_feed_url = 'https://fourble.co.uk/dickspicks4-240831-0.rss'
    user_feed_url = request.form.get('user_feed_url', default_feed_url)  # Fetch user-specified feed URL from form input
    default_feed = feedparser.parse(default_feed_url)
    user_feed = feedparser.parse(user_feed_url)

    music_path = ""
    uploaded_file_msg = None

    if request.method == 'POST' and 'audioFile' in request.files:
        file = request.files['audioFile']
        if file and file.filename:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            music_path = url_for('static', filename='uploads/' + filename)
            uploaded_file_msg = f"Uploaded file: {filename}"

    return render_template('index2.html', default_entries=default_feed.entries,
                           user_entries=user_feed.entries, music_path=music_path,
                           uploaded_file_msg=uploaded_file_msg)

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)
