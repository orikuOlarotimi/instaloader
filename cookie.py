import instaloader
from time import sleep
import json
from flask import Flask, request

app = Flask(__name__)


@app.route("/comments")
def get_post_details():
    ig = instaloader.Instaloader()

    usrname = request.form.get("username")
    password = request.form.get("password")
    url = request.form.get("url")

    ig.context.log("Logging in.")
    ig.context.log("NOTICE: Be careful with password input at script execution")
    ig.login(usrname, password)
    sleep(5)

    try:
        ig.context.log(f"logging from :{ig.context.username}\n\n")
    except:
        ig.context.log("You are not logged in.")
        ig.context.log(f"Logging in as {usrname}")
        ig.context.log(f"NOTICE: Be careful with password input at script execution")
        ig.context.log(f"{usrname}")
        ig.login(usrname, password)
        sleep(3)

    post = instaloader.Post.from_shortcode(ig.context, url.split("/")[-2])

    print(f"Post Caption: {post.caption}")
    print(f"Post Author: {post.owner_profile.username}")

    comments_list = []
    for comment in post.get_comments():
        comment_author = comment.owner.username
        comment_text = comment.text

        comments_list.append(f"{comment_author}: {comment_text}")

    print("Comments:")
    for comment_text in comments_list:
        print(comment_text)
    print("\n")

    result_dict = {"data": comments_list}
    json_string = json.dumps(result_dict)
    print(json_string)
    return json_string


if __name__ == "__main__":
    app.run()
