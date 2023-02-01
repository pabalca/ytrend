from datetime import datetime
from flask import abort, flash, redirect, render_template, session, url_for, request
from sqlalchemy import func

from ytrend import app
from ytrend.models import Stat, Total, db


@app.route("/", methods=["GET"])
def index():
    q = db.select(
        [
            Total.views,
            Total.subs,
            Total.videos,
            Total.created_at,
            db.func.max(Total.created_at),
        ]
    ).group_by(func.strftime("%Y-%m-%d", Total.created_at))
    stats = db.engine.execute(q).fetchall()

    views = []
    subs = []
    videos = []
    dates = []

    for stat in stats:
        views.append(stat.views)
        subs.append(stat.subs)
        videos.append(stat.videos)
        dates.append(stat.created_at.strftime('%d %b, %H:%M'))

    return render_template(
        "chart.html", views=views, subs=subs, videos=videos, labels=dates
    )


@app.route("/table", methods=["GET"])
def table():
    q = (
        db.select(
            [
                Stat.channel,
                Stat.views,
                Stat.subs,
                Stat.videos,
                Stat.created_at,
                db.func.max(Stat.created_at),
            ]
        )
        .group_by(Stat.channel)
        # .group_by(db.func.strftime("%Y-%m-%d", Stat.created_at))
        .order_by(Stat.views.desc())
    )
    stats = db.engine.execute(q).fetchall()
    return render_template("table.html", stats=stats, page_title="Youtube stats per channel")


@app.route("/raw", methods=["GET"])
def raw():
    stats = Stat.query.order_by(Stat.created_at.desc()).all()
    return render_template("table.html", stats=stats, page_title="all date scraped")
