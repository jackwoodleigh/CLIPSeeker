from flask import Blueprint, render_template, session, current_app
from flask_login import current_user
from .auth import login_required

views = Blueprint('views', __name__)

#root
@views.route('/') # home page aka website {domain}/ 
@login_required
def home(): # whatevers in here will run first for ^
    return render_template("home.html", session=session)

@views.route('/library') # home page aka website {domain}/ 
@login_required
def library(): # whatevers in here will run first for ^
    images = current_app.config['DBM'].retrievePhotos()
    print(images)
    return render_template("library.html", session=session, images=images)

@views.route('/profile') # home page aka website {domain}/ 
@login_required
def profile(): # whatevers in here will run first for ^
    return render_template("profile.html", session=session)

@views.route('/test') # home page aka website {domain}/ 
@login_required
def test():
    return render_template("index.html", session=session)


'''
</a>
        <a href="https://collegesailing.org/news_events/images/uploads/icsa_news/all-aca17-18.jpg" data-toggle="lightbox" data-gallery="gall">
            <img src="https://collegesailing.org/news_events/images/uploads/icsa_news/all-aca17-18.jpg" class="img-fluid">
        </a>
        <a href="https://static01.nyt.com/images/2017/10/20/sports/20FORDHAMSAILING-2/merlin-to-scoop-128256989-124048-superJumbo.jpg" data-toggle="lightbox" data-gallery="gall">
            <img src="https://static01.nyt.com/images/2017/10/20/sports/20FORDHAMSAILING-2/merlin-to-scoop-128256989-124048-superJumbo.jpg" class="img-fluid">
        </a>
        <a href="https://mywentworth-my.sharepoint.com/personal/woodleighj_wit_edu/Documents/Attachments/IMG_0939.jpeg?web=1" data-toggle="lightbox" data-gallery="gall">
            <img src="https://mywentworth-my.sharepoint.com/personal/woodleighj_wit_edu/Documents/Attachments/IMG_0939.jpeg?web=1" class="img-fluid">
        </a>
        <a href="https://navysports.com/images/2021/6/3/Navy_1st.JPG" data-toggle="lightbox" data-gallery="gall">
            <img src="https://navysports.com/images/2021/6/3/Navy_1st.JPG" class="img-fluid">
        </a>
       
        
        <a href="https://avatars.githubusercontent.com/u/366151?s=280&v=4" data-toggle="lightbox" data-gallery="gall">
            <img src="https://avatars.githubusercontent.com/u/366151?s=280&v=4"class="img-fluid" data-gallery="gall">
        </a>
        
        <a href="https://upload.wikimedia.org/wikipedia/en/4/40/TumblrHomepage.jpg" data-toggle="lightbox" data-gallery="gall">
            <img src="https://upload.wikimedia.org/wikipedia/en/4/40/TumblrHomepage.jpg" class="img-fluid">
        </a>

     
        <a href="https://eshsstormalert.com/wp-content/uploads/2023/12/tumblr-era.jpg" data-toggle="lightbox" data-gallery="gall">
            <img src="https://eshsstormalert.com/wp-content/uploads/2023/12/tumblr-era.jpg" class="img-fluid">
        </a>

        <a href="https://www.lifewire.com/thmb/_IKJCjgyJUbwdp4K40clVHBUe3s=/1500x0/filters:no_upscale():max_bytes(150000):strip_icc()/tumblr-1192bb21d751401b9e6e10b6c0eeb459.jpg" data-toggle="lightbox" data-gallery="gall">
            <img src="https://www.lifewire.com/thmb/_IKJCjgyJUbwdp4K40clVHBUe3s=/1500x0/filters:no_upscale():max_bytes(150000):strip_icc()/tumblr-1192bb21d751401b9e6e10b6c0eeb459.jpg" class="img-fluid">
        </a>

        <a href="https://cdn.vox-cdn.com/thumbor/yhCS8Ib6RUQQmYAQrKubv_WjN_w=/0x0:2040x1360/1400x1050/filters:focal(1020x680:1021x681)/cdn.vox-cdn.com/uploads/chorus_asset/file/24087489/STK137_Tumblr_K_Radtke_02.jpg" data-toggle="lightbox" data-gallery="gall">
            <img src="https://cdn.vox-cdn.com/thumbor/yhCS8Ib6RUQQmYAQrKubv_WjN_w=/0x0:2040x1360/1400x1050/filters:focal(1020x680:1021x681)/cdn.vox-cdn.com/uploads/chorus_asset/file/24087489/STK137_Tumblr_K_Radtke_02.jpg" class="img-fluid">
        </a>
'''