from flask_login import login_required, current_user
from flask import Blueprint, render_template
import time
from . import db

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/profile')
@login_required
def profile():
    username = current_user.username

    num_beers = db.engine.execute("SELECT COUNT(*) FROM BeerReviews WHERE username= (?)", (username))
    beers_reviewed = num_beers.first()[0]
    num_beers.close()

    review = db.engine.execute("SELECT Avg(rating) FROM BeerReviews Where username = (?)", (username))
    avg_review = review.first()[0]
    review.close()
    return render_template('profile.html', Name=username, Beer_Purchases = beers_reviewed, Avg_rating=avg_review)

@main.route('/profileBar')
@login_required
def profileBar():
    barUsername = current_user.username
    barName = current_user.name
    barId = current_user.id
    queryTime_dict={}

    query1Start = time.perf_counter()
    reviewNumbers = db.engine.execute("SELECT Count(*) FROM BeerReviews INNER JOIN drink_list on drinkId=beer_id WHERE barId=(?)",(barId))
    query1End = time.perf_counter()
    query1Time = query1End-query1Start
    queryTime_dict["Query1Duration"] = query1Time
    reviews = reviewNumbers.first()[0]
    reviewNumbers.close()

    query2Start = time.perf_counter()
    avgReviews_engine = db.engine.execute("SELECT avg(rating) FROM BeerReviews INNER JOIN drink_list on barId=(?) and beer_id=drinkId",(barId))
    query2End = time.perf_counter()
    query2Time = query2End-query2Start
    queryTime_dict["Query2Duration"] = query2Time
    avgReviews=avgReviews_engine.first()[0]
    avgReviews_engine.close()

    query3Start = time.perf_counter()
    totalDrinks_engine = db.engine.execute("SELECT count(*) FROM drink_list where barId=(?)",(barId))
    query3End = time.perf_counter()
    query3Time=query3End-query3Start
    queryTime_dict["Query3Duration"] = query3Time
    totalDrinks = totalDrinks_engine.first()[0]
    totalDrinks_engine.close()

    query4Start = time.perf_counter()
    listOfTopBeers_engine = db.engine.execute("SELECT name, avg(rating) FROM BeerReviews INNER JOIN drink_list on drinkId=beer_id WHERE barId=(?) GROUP BY name ORDER BY avg(rating) DESC ",(barId))
    query4End = time.perf_counter()
    query4Time = query4End-query4Start
    queryTime_dict["Query4Duration"] = query4Time
    topRated = listOfTopBeers_engine
    topRated_list=[]
    for row in topRated:
        topRated_list.append(row)
    listOfTopBeers_engine.close()

    beerName1=topRated_list[0][0]
    beerRating1= topRated_list[0][1]

    beerName2 = topRated_list[1][0]
    beerRating2 = topRated_list[2][1]

    beerName3 = topRated_list[2][0]
    beerRating3 = topRated_list[2][1]

    beerName4 = topRated_list[3][0]
    beerRating4 = topRated_list[3][1]

    beerName5 = topRated_list[4][0]
    beerRating5 = topRated_list[4][1]

    query5Start = time.perf_counter()
    listOfTopReviewers_engine = db.engine.execute("SELECT username,Count(*) FROM BeerReviews INNER JOIN drink_list on barId=(?) and drinkId=beer_id GROUP BY username ORDER BY count(review_id) DESC LIMIT 5",(barId))
    query5End = time.perf_counter()
    query5Time = query5End - query5Start
    queryTime_dict["Query5Duration"] = query5Time
    topReviewer_list=[]
    for row in listOfTopReviewers_engine:
        topReviewer_list.append(row)
    listOfTopReviewers_engine.close()

    reviewerName1 =topReviewer_list[0][0]
    reviewerNum1 = topReviewer_list[0][1]

    reviewerName2 = topReviewer_list[1][0]
    reviewerNum2 = topReviewer_list[1][1]

    reviewerName3 = topReviewer_list[2][0]
    reviewerNum3 = topReviewer_list[2][1]

    reviewerName4 = topReviewer_list[3][0]
    reviewerNum4 = topReviewer_list[3][1]

    reviewerName5 = topReviewer_list[4][0]
    reviewerNum5 = topReviewer_list[4][1]


    print(queryTime_dict,flush=True)

    return render_template('profile.html', username=barName,num_review=reviews, avg_rating=avgReviews, num_beers=totalDrinks,
                           top_rated1 = beerName1,top_rated1Num=beerRating1, top_rated2 = beerName2, top_rated2Num=beerRating2,
                           top_rated3 = beerName3, top_rated3Num=beerRating3, top_rated4=beerName4, top_rated4Num=beerRating4,
                           top_rated5 = beerName5, top_rated5Num=beerRating5, top_customer1=reviewerName1, top_customer1Num=reviewerNum1,
                           top_customer2 =reviewerName2, top_customer2Num=reviewerNum2,top_customer3=reviewerName3, top_customer3Num=reviewerNum3,top_customer4=reviewerName4, top_customer4Num=reviewerNum4,
                           top_customer5=reviewerName5, top_customer5Num=reviewerNum5)