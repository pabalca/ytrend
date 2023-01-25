import click
from os import environ
import time
from datetime import datetime
import googleapiclient.discovery

from ytrend import app
from ytrend.models import Stat, Total, db


@app.shell_context_processor
def make_shell_context():
    return dict(db=db, Stat=Stat, Total=Total)


@app.cli.command()
@click.option("--drop", is_flag=True, help="Create after drop.")
def initdb(drop):
    if drop:
        db.drop_all()
    db.create_all()
    click.echo("Initialized database.")


@app.cli.command()
def scrape():

    channels = [
        {"name": "lacampanitaconfernfinance", "id": "UCf932WZebrzMZnn1DR9YQLg"},
        {"name": "intothecryptoverse", "id": "UCRvqjQPSeaWn-uEx-w0XOIg"},
        {"name": "MMCryptoTube", "id": "UCBkGMys0mYl3Myxh3CTsASA"},
        {"name": "bobloukas3493", "id": "UC0zGwzu0zzCImC1BwPuWyXQ"},
        {"name": "InvestAnswers", "id": "UClgJyzwGs-GyaNxUHcLZrkg"},
        {"name": "WhatBitcoinDid", "id": "UCzrWKkFIRS0kjZf7x24GdGg"},
        {"name": "CryptoCrewUniversity", "id": "UC7ndkZ4vViKiM7kVEgdrlZQ"},
        {"name": "CoinBureau", "id": "UCqK_GSMbpiV8spgD3ZGloSw"},
        {"name": "CryptoWorldJosh", "id": "UCgY66N1YS_G9lYMvCQko6yw"},
        {"name": "CryptoBanterGroup", "id": "UCN9Nj4tjXbVTLYWN0EKly_Q"},
        {"name": "JoeParysCrypto", "id": "UCRukJuuBAdoHMTBIsFJAgvw"},
        {"name": "TheCryptoLark", "id": "UCl2oCaw8hdR_kbqyqd2klIA"},
        {"name": "ThomasKralow", "id": "UCBhORXMwPfJtNtsZcUJHO6w"},
        {"name": "CryptoTips", "id": "UCavTvSwEoRABvnPtLg0e6LQ"},
        {"name": "CryptosRUs", "id": "UCI7M65p3A-D3P4v5qW8POxQ"},
        {"name": "CryptoMason", "id": "UCPR9ga3sv5oakMB544M61Bw"},
        {"name": "BitBoyCryptoChannel", "id": "UCjemQfjaXAzA-95RKoy9n_g"},
        {"name": "TheMoon", "id": "UCc4Rz_T9Sb1w5rqqo9pL1Og"},
        {"name": "CryptoCapitalVenture", "id": "UCnMku7J_UtwlcSfZlIuQ3Kw"},
        {"name": "davincij15", "id": "UCP0g6ygQkYjmog801YnNqtQ"},
        {"name": "investruiz", "id": "UCv8N7q4bNT_O1Z6tmid7y7Q"},
        {"name": "WeeklyOpen", "id": "UCldhTluPIGdCxZIlgToAW7Q"},
        {"name": "pompclips", "id": "UCGAhWqzVgKytS0NcKz9bxDA"},
        {"name": "AnthonyPompliano", "id": "UCevXpeL8cNyAnww-NqJ4m2w"},
        {"name": "UpOnly", "id": "UC_Jt1VYHZO4Kc4cJQP5utdw"},
        {"name": "TylerSCrypto", "id": "UCgBQ6YsN4oUTjbAvIwCFLog"},
        {"name": "UnchainedPodcast", "id": "UCWiiMnsnw5Isc2PP1to9nNw"},
        {"name": "JamieTree", "id": "UCWZg7FTpyFB9lSpk-_cVr3Q"},
    ]

    # Youtube API
    api_service_name = "youtube"
    api_version = "v3"
    DEVELOPER_KEY = environ.get('YT_API_KEY')

    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, developerKey=DEVELOPER_KEY
    )

    # Save global stats for the day in a table, easier to index
    total_views = 0
    total_subs = 0
    total_videos = 0

    for channel in channels:
        r = youtube.channels().list(part="statistics", id=channel["id"]).execute()
        stats = r["items"][0]["statistics"]
        viewCount = stats["viewCount"]
        subscriberCount = stats["subscriberCount"]
        videoCount = stats["videoCount"]

        # add all channel stats in total
        total_views += int(viewCount)
        total_subs += int(subscriberCount)
        total_videos += int(videoCount)

        s = Stat(
            channel=channel["name"],
            views=viewCount,
            videos=videoCount,
            subs=subscriberCount,
        )

        db.session.add(s)
        click.echo(f"Adding new stat: {s}")
        time.sleep(0.1)

    total = Total(views=total_views, videos=total_videos, subs=total_subs)
    db.session.add(total)
    db.session.commit()
