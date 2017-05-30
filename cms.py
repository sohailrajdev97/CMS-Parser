from cmsLogin import *
import getpass

def lxmlParse(url , session):
    return lxml.html.fromstring(session.openForParse(url))

def main():
    print("\n\nCMS Notifier")
    try:
        #login
        username = input("Enter Username : ")
        session = Login(username , getpass.getpass("Enter Password  : "))
    except:
        print("\nUsing Terminal ! Password may be echoed on screen.");

    #parse page containing list of all courses
    doc = lxmlParse("http://id.bits-hyderabad.ac.in/moodle/my/index.php?mynumber=-2" , session)
        
    #get collection of course names
    courses = doc.find_class("course_title")

    for div in courses:
        
        #find the course link
        link = (div.cssselect("a"))[0].get("href")

        #find the course ID
        courseID = (link.split("="))[1]

        #open the data file corresponding to each course
        courseFile = open("./data/course_" + courseID + "_" + username + ".dat", "a+")

        #seek to begining
        courseFile.seek(0)
        notified = []

        #load the already sent notifications in a list for that particular course
        for line in courseFile:
            notified.append(line.rstrip("\n"))

       
        #print course name
        print(div.text_content() + "\n")
         
        #open the course and parse full page
        courseParse = lxmlParse(link , session)

        #collection of contents of a particular course
        contents = courseParse.find_class("activityinstance")

        for content in contents:
            #get ID for each content
        	contentID = ((content.cssselect("a"))[0].get("href").split("="))[1]

            #check if already notified
        	if(contentID not in notified):
        		print("\t**** " + content.find_class("instancename")[0].text_content() + "\n")
        		courseFile.write(contentID + "\n") #add to the notified list (directly to file)

        #get announcements for the given course. announcement is the written text without any file
        announcement = courseParse.find_class("contentwithoutlink")

        #print announcements if there
        if(announcement != []):
        	for div in announcement:
        		print("\t***" + div.text_content()[0:150] + ".......\n")

        print()

                  
if __name__ == "__main__" : main()
