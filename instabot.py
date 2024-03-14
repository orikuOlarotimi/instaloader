import instaloader
from flask import Flask, jsonify
from time import sleep
from details import username, passwd, person
import json

app = Flask(__name__)


@app.route('/')
def main():
    ig = instaloader.Instaloader()

    usrname = username
    password = passwd
    ig.context.log("Logging in.")
    ig.context.log("NOTICE: Be careful with password input at script execution")
    ig.login(usrname, password)
    sleep(5)

    try:
        ig.context.log(f"Logged in as: {ig.context.username}\n")
    except:
        ig.context.log("You are not logged in.")
        ig.context.log(f"Logging in as {usrname}")
        ig.context.log("NOTICE: Be careful with password input at script execution")
        ig.context.log(f"{usrname}")
        ig.login(usrname, password)
        sleep(3)

    try:
        # Perform a top search
        top_search = instaloader.TopSearchResults(ig.context, 'dan_pumping')
        result = []
        search_result = list(top_search.get_profiles())
        for name in search_result:
            username_part = name.__repr__().split()[1]
            user = username_part.strip('()')
            result.append(user)
        result_dict = {"data": result}
        json_string = json.dumps(result_dict)
        print(json_string)
        return json_string


    except Exception as e:
        ig.context.log(f"Error during search: {e}")
        # Return a JSON response indicating the error, along with a 400 status code
        return jsonify({"error": "Failed to perform search", "details": str(e)}), 400


if __name__ == "__main__":
    app.run()
