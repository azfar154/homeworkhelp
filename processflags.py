from main import db
from main import Flags
from main import Blogpost
total_flags = Flags.query.all()
for flag in total_flags:
    print("Author :"+ flag.author)
    print("Title :" + flag.title)
    delete_question = input("Would you like us to delete this post?")
    if delete_question == "Yes" or delete_question == "yes" or delete_question == "YES":
        blog = Blogpost.query.filter_by(author=flag.author,title=flag.title).first()
        if blog == None:
            print("No post found with the description")
        else:
            db.session.delete(blog)