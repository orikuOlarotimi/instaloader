import instaloader
from flask import Flask, jsonify, request, render_template
from time import sleep
from details import username, passwd, link

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("likes.html")


@app.route("/likes", methods=["POST"])
def like():
    post_link = request.form.get("link")
    if not post_link:
        return jsonify({"error": "No link provided"}), 400

    ig = instaloader.Instaloader()

    ig.context.log("Logging in.")
    ig.context.log("NOTICE: Be careful with password input at script execution")

    try:
        ig.login(username, passwd)
        ig.context.log(f"logging from :{ig.context.username}\n\n")
        sleep(5)
        post = instaloader.Post.from_shortcode(ig.context, post_link.split("/")[-2])

        likes = post.get_likes()
        print(likes)
        likers = [profile.username for profile in likes]
        print(f"Post Caption: {post.caption}")
        print(f"Post Author: {post.owner_profile.username}")
        print(f"Likers: {likers}")

        return jsonify({"likers": likers})

    except Exception as e:
        ig.context.log("error during login")
        return jsonify({"error": "error during login may be as a result of incorrect details", "details": str(e)}), 400


if __name__ == "__main__":
    app.run(debug=True)
