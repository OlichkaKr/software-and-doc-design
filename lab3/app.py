from config import session, conn_str
from flask import Flask, jsonify
from routes import base_bp

from models import User, Follow, PurchaseSettings, PurchasePlan, SiteSettings

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = conn_str
app.register_blueprint(base_bp)


@app.route("/users", methods=["GET"])
def get_users():
    users = session.query(User).all()
    users_with_all_data = []
    for u in users:
        followers = ''
        for uf in u.followers:
            id_followers = session.query(User).filter_by(id=uf.id_following).all()
            for ids in id_followers:
                followers += ids.public_display_name
                followers += '\n'

        followings = ''
        for ufu in u.following_users:
            id_followings = session.query(User).filter_by(id=ufu.id_follower).all()
            for ids in id_followings:
                followings += ids.public_display_name
                followings += '\n'

        purchase_plan = u.purchase[0].plan
        sites = ''
        for us in u.sites:
            sites += us.title
            sites += '\n'

        user = {
            'id': u.id,
            'first_name': u.first_name,
            'last_name': u.last_name,
            'public_display_name': u.public_display_name,
            'about_me': u.about_me,
            'profile_link': u.profile_link,
            'email': u.email,
            'password': u.password,
            'followers': followers,
            'following_users': followings,
            'purchase': purchase_plan.title,
            'sites': sites
        }
        users_with_all_data.append(user)
    return jsonify({'data': users_with_all_data})


if __name__ == "__main__":
    app.run(debug=True)