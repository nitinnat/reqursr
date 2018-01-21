# reqursr - the recursive concept generator

<br>
To run:
<ul>
<li>Install beautifulsoup and flask </li>
<li> Navigate to the correct directory and run "python app.py" </li>
<li> Go to localhost:5000 to interact with the application!</li>
</ul>

</br>

<br>
Inspiration: Getting into any new subject is a daunting task, especially in ever expanding and rapidly changing fields like machine learning. We have all faced an initial overwhelming option paralysis when starting out, not knowing where to begin or how the different concepts relate to each other. So we wanted to create an application that took any topic as a query and created a concept map of all the important topics and ideas that it was connected to. This not only gives the user a good picture of what the subject entails, but also a roadmap to learning it.
</br>

<br>
What it does: The moment you launch the application, it gives you a plain, google like interface, where there is only a textbox and a button. The user enters any topic of their choice in this search box and presses the 'Go' button. The application then comes up with a visually appealing and intuitive graph of related concepts, abstracting the underlying complexities and providing the user with only the information that is important to them.
</br>

<br>
How we built it: This application relies on natural language processing (Google's Natural Language API) and web scraping (Wikipedia's API) in order to seek out pages related to the topic and find out all the important entities in these documents. These entities are then put together in a graph structure which is displayed.
</br>

<br>
Challenges we ran into: The initial challenge was to consistently extract relevant entities from the web pages related to the topic and select the most relevant ones to be added to the concept graph. The Natural Language API alone was not enough for this task. While it did a great job of identifying the various important entities of any given text, the entities that it picked up were not always relevant to our needs. We had to further prune these entities in order to only select those that had a high chance of being relevant to the topic. Another big challenge was to make all these different technologies work cohesively.
</br>

<br>
Accomplishments that we are most proud of: First of all, we are proud of the fact that we were able to conceive of an idea that we were all passionate about, and deliver a working prototype implementing this idea in a very short period of time. Secondly we are proud of the cross-section of technologies that we ended up using which used the industry best practices, and did not unnecessarily reinvent the wheel, and were able to build on top of what already existed.
</br>

<br>
What's next for ReqursR: There are several fronts on which this application can be further improved. Firstly, in terms of pruning the large list of entities, we propose retraining word2vec to recognize multiple-word entities and provide a similarity score that can be used to remove irrelevant topics. Further, a database backend can be used to reuse previously build graphs which will reduce computation cost and increasingly improve speed the more the application is used. Finally, we can look into improving the user experience by dynamically displaying the graph as it builds to give the user a sense of progress.
</br>

<br>
Built with: Flask, Python, Natural Language API, D3.js
</br>
