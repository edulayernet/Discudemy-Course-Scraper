Scraping Tool For Udemy Free Courses!


Usage of Class:

Udemy = UdemyParser() # Create an object from the class base
Udemy.method(*params) # How can I access to the class methods?
\n
Udemy.parse_four_page(page_id) # If you want to get all last added courses, use that method.\nPage ID must be one to five, five is maximum. Why not greater? Because free courses often not available after page five.
\n
Udemy.data_export(courses, path=path, file=file) # Export all courses with using data_export(courses, path=path, file=file).\nPlease do configure path directory as that -> 'your_directory/target/' and if you want you could to add specific file name.
\nTry looping to fetch all courses, so you'll get it like this:\n
```
datas = []
for x in range(1, 3):
    for i in udemy.parse_four_page(x):
        datas.append(i)\n```
