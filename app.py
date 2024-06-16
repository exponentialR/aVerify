from flask import Flask, render_template, request, redirect, url_for, jsonify
import os
import json
from datetime import datetime

app = Flask(__name__)
app.config['PROJECTS_FOLDER'] = 'projects'
app.config['LOG_FOLDER'] = 'logs'
app.config['LOG_FILE'] = os.path.join(app.config['LOG_FOLDER'], 'labels.log')

os.makedirs(app.config['PROJECTS_FOLDER'], exist_ok=True)
os.makedirs(app.config['LOG_FOLDER'], exist_ok=True)


@app.route('/')
def create_or_select_project():
    projects = [{'name': d, 'created_at': datetime.now().strftime('%d %b \'%y, %H:%M')} for d in
                os.listdir(app.config['PROJECTS_FOLDER']) if
                os.path.isdir(os.path.join(app.config['PROJECTS_FOLDER'], d))]
    return render_template('create_project.html', projects=projects)


@app.route('/create_project', methods=['POST'])
def create_project():
    project_name = request.form['project_name']
    project_path = os.path.join(app.config['PROJECTS_FOLDER'], project_name)
    os.makedirs(os.path.join(project_path, 'videos'), exist_ok=True)
    os.makedirs(os.path.join(project_path, 'annotations'), exist_ok=True)
    return redirect(url_for('project_dashboard', project_name=project_name))


@app.route('/project_dashboard/<project_name>')
def project_dashboard(project_name):
    return render_template('project_dashboard.html', project_name=project_name)


@app.route('/upload/<project_name>', methods=['POST'])
def upload(project_name):
    project_path = os.path.join(app.config['PROJECTS_FOLDER'], project_name)
    video_folder = os.path.join(project_path, 'videos')
    annotation_folder = os.path.join(project_path, 'annotations')

    if 'videos' not in request.files or 'annotation' not in request.files:
        return redirect(url_for('project_dashboard', project_name=project_name))

    annotation = request.files['annotation']
    annotation_path = os.path.join(annotation_folder, annotation.filename)
    annotation.save(annotation_path)

    for video in request.files.getlist('videos'):
        video_path = os.path.join(video_folder, video.filename)
        video.save(video_path)

    return redirect(url_for('review', project_name=project_name, annotation_filename=annotation.filename))


def normalize_filename(filename):
    return os.path.basename(filename).split('-')[-1]


@app.route('/review/<project_name>')
def review(project_name):
    project_path = os.path.join(app.config['PROJECTS_FOLDER'], project_name)
    annotation_folder = os.path.join(project_path, 'annotations')
    video_folder = os.path.join(project_path, 'videos')

    annotation_filename = request.args.get('annotation_filename')
    if annotation_filename == 'latest':
        annotations = [f for f in os.listdir(annotation_folder) if os.path.isfile(os.path.join(annotation_folder, f))]
        if not annotations:
            return "No annotation files found.", 404
        annotation_filename = max(annotations, key=lambda f: os.path.getctime(os.path.join(annotation_folder, f)))

    annotation_path = os.path.join(annotation_folder, annotation_filename)
    if not os.path.exists(annotation_path):
        return "Annotation file not found.", 404

    with open(annotation_path) as f:
        annotations = json.load(f)

    videos = [f for f in os.listdir(video_folder) if os.path.isfile(os.path.join(video_folder, f))]
    normalized_videos = {normalize_filename(video): video for video in videos}
    matched_annotations = []

    for annotation in annotations:
        video_url = annotation['video_url']
        video_filename = normalize_filename(video_url)
        if video_filename in normalized_videos:
            annotation['video_filename'] = normalized_videos[video_filename]
            matched_annotations.append(annotation)

    return render_template('review.html', annotations=matched_annotations)


@app.route('/log_label', methods=['POST'])
def log_label():
    data = request.json
    with open(app.config['LOG_FILE'], 'a') as f:
        f.write(json.dumps(data) + '\n')
    return jsonify(success=True)


if __name__ == '__main__':
    app.run(debug=True)
