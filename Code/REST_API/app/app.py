from src.classes.DBReader import DBReader
from os import path
from datetime import datetime
from flask import (
    Flask,
    jsonify,
    render_template,
    Response,
    stream_with_context,
)

app = Flask(__name__)
specific_events = ["WatchEvent", "PullRequestEvent", "IssuesEvent"]
db_dir = path.realpath(path.join(path.dirname(__file__), path.pardir,path.pardir,"Database"))
db_file = path.join(db_dir, "github.db")
dbreader = DBReader(db_file)


@app.route("/", methods=["GET"])
def home():
    return render_template(
        "index.html", utc_dt=datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    )


@app.route("/pull_requests/avg/<int:repo_id>", methods=["GET"])
def get_pull_requests_average_time(repo_id):
    results = []
    dbreader = DBReader(db_file)
    try:
        return {'Repo_id':repo_id,'Average_time':dbreader.get_average_time(repo_id)}
    except BaseException as e:
        return {"Error":"We did not find your id in our database!"},404



@app.route("/group_events/", methods=["GET"])
def get_group_events_url():
    return "Please specify an offset in <i>MINUTES</i> at the end of url, home_url/group_events/10 "


@app.route("/group_events/<string:time_scale>/<int:offset>", methods=["GET"])
def get_group_events(offset, time_scale="minutes"):
    if type(offset) != int:
        return "Please use an integer in the URL!"
    if time_scale not in ["days", "hours", "minutes", "seconds"]:
        return "Time Scale should be 'days','hours','minutes' or 'seconds'"
    results = []
    dbreader = DBReader(db_file)
    results = dbreader.get_events_grouped_by_event_type(offset, time_scale)
    return jsonify(results)


@app.route("/pullrequests-live-line-chart/")
def get_live_chart():
    return render_template("line_chart.html")


@app.route("/line-chart-data")
def chart_data() -> Response:
    dbreader = DBReader(db_file)
    response = Response(
        stream_with_context(dbreader.get_chart_data()), mimetype="text/event-stream"
    )
    response.headers["Cache-Control"] = "no-cache"
    response.headers["X-Accel-Buffering"] = "no"
    return response


@app.route("/top-watched-repos/<int:limit>")
def get_top_watched_chart(limit):
    dbreader = DBReader(db_file)
    print(dbreader.get_top_watchevent_repos())
    return render_template(
        "Doughnut_chart.html", pie_chart_data=dbreader.get_top_watchevent_repos(min(10,max(5,limit)))
    )

@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('404.html'), 404
    
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, threaded=True)
