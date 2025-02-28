## OOTDAI
## Introduction Video
https://youtu.be/AWQO_SSA2yg

## Inspiration
In the realm of Generative AI, we anticipate valuable outcomes when faced with fragmented information. Throughout the day, the initial encounter with fragmented elements typically arises during the process of selecting attire before heading out. Recent research indicates that women dedicate over 10 minutes each morning to this task. Utilizing a fashion advisor to streamline this decision-making process has the potential to afford individuals more time to enjoy life's journey. Consequently, Gemini, renowned for its strong picture identification capabilities and organizational proficiency, emerges as an ideal candidate to serve as our trusted advisor in recommending the day's outfit. Finally, OOTDAI (Outfit Of The Day with AI), pronounced similarly to "stage" in Chinese, will provide a service that allows users to confidently showcase their personal style on the streets, the stage of our lives.

## What it does
OOTDAI unveils a service designed to streamline individuals' daily routines by providing personalized outfit recommendations from their existing wardrobe. Furthermore, OOTDAI explores new clothing collections on the platform to showcase various brands. Additionally, it facilitates attire exchange among users, allowing for the reuse of clothes and contributing to the advancement of environmental conservation goals.

**Providing Personalized Outfit**
Users can upload their clothing items, shoes, bags, and more to our platform. In urgent scenarios where users require quick outfit suggestions tailored to specific styles, occasions, or even a particular garment, Gemini can promptly provide suitable matches from their closet based on their preferences.

**Exploring Clothing Collections**
To generate a diverse array of outfits, we anticipate that OOTDAI can collaborate with fashion brands and Key Opinion Leaders (KOLs). This collaboration would enable users to discover suitable garments and explore various style possibilities. Brands could showcase their products to our users, potentially redirecting our users to their platforms for purchase. Additionally, the favorite set list feature not only allows users to exchange outfit ideas but also provides an opportunity for KOLs to promote brands through the platform's functions, resulting in a mutually beneficial arrangement for all parties involved.

**Facilitating Attire Exchange Among Users**
According to the European Commission, there is an alarming 92 million tons of textile waste generated globally each year. In response to this environmental challenge, OOTDAI will introduce a service that allows users to sell or donate their clothes to others. This initiative not only expands users' closets but also alleviates the burden on our environment by promoting the reuse and recycling of clothing items.


## How we built it
As a prototype, OOTDAI utilizes a web-based presentation to demonstrate its concept. The architecture is built using FastAPI in Python, allowing for swift communication with the Gemini Model (gemini-1.5-pro-latest), which generates formatted clothing descriptions and provides various outfits recommendations based on these descriptions. The frontend presentation is crafted with HTML, CSS, and JavaScript. Data storage is managed using MongoDB. Both MongoDB and the OOTDAI service, encapsulated into an image, are deployed and run using Docker on the Google Cloud Platform (GCP).

Throughout the development process, [Figma](https://www.figma.com/file/1vWcVjXARX8SJgNaD6wlXV/Google-Hackathon?type=design&node-id=0-1&mode=design&t=rtuWCOP6VwKNHlVZ-0) aids us in outlining the frontend display, allowing for seamless visualization and collaboration. Concurrently, we utilize [Trello](https://trello.com/b/N4v8ExxS/google-hackathon-wz0whzwwh) to brainstorm ideas, address issues, and effectively manage our schedule. [GitHub](https://github.com/zhong0/2024_Google_Hackathon) is utilized to control code versions and facilitate collaboration among teammates.


## Challenges we ran into
**Challenges**
Uploading numerous images to Gemini may strain the API's processing capabilities and could potentially exceed file and size limits. Additionally, we anticipate OOTDAI to supply clothing images, thereby enhancing users' ability to visualize outfit suggestions for a more immersive experience.

**Solution**
When users upload images, we utilize the Gemini model to describe clothing or accessories in a structured format. Subsequently, each clothing description and file path are saved to the database. Gemini then utilizes these descriptions to recommend outfits based on textual features. Additionally, Gemini provides us with the file path, enabling us to access the images. This approach effectively addresses the issue and helps us achieve our desired results.


## Accomplishments that we're proud of
Combining the fashion industry with technology, we take pride in our service, which promptly provides users with visualized outfit recommendations. Gemini not only offers personalized outfits for various styles and occasions but also exceeds our expectations with recommendations that ignite valuable insights through collisions in fashion design.

By accepting clothing from both brands and users, our app creates the possibility to enrich the industry with a diverse atmosphere. We not only promote brand exposure but also contribute to environmental conservation—a business model we are proud of.

## What we learned
In this endeavor, we aimed to integrate generative AI into our daily lives, impacting individuals, industries, and the environment on various levels. While fashion may seem boundless and infinite, we recognize that our Earth is singular and precious. It is with this mindset that we are proud to have partnered with Gemini to bring our vision to fruition.

In terms of techniques, we embarked on a journey of learning how to interact effectively with Gemini. Initially uncertain of how Gemini could fulfill our desired tasks, we dedicated time to experimenting with different approaches, including file uploads, recording chat history, outfit recommendations based solely on text, and more. To maintain consistent response quality, we also experimented with various prompt contents, designing response formats accordingly. Ultimately, Gemini emerged as an invaluable ally, greatly assisting us in realizing our application.

## What's next for OOTDAI
We anticipate that OOTDAI can enhance outfit recommendations by incorporating additional information. Therefore, integrating geolocation factors such as local climate, cultural norms, and seasonal trends is our short-term goal. Furthermore, we aim to introduce entertainment functions to appeal to our users and encourage them to try our service. For example, users will be able to upload their outfit and their desired outfit, and Gemini will help them understand the gap between the two, resembling a real advisor.

It's unfortunate that our current display method only showcases outfits piece by piece. To enhance user experience, we're combining it with a 3D outfit visualization model. This feature allows virtual try-ons, reducing time in fitting rooms and minimizing exchanges and returns in e-commerce. OOTDAI aims to empower users to make confident fashion choices and create a more user and environment-friendly shopping process, influencing future fashion trends.

## Try it out in local
* docker build -t {image_name}:{image_version} .
* docker run -d -p 8000:8000 -v ./app:/app {image_name}:{image_version} uvicorn main:app --host 0.0.0.0 --port 8000 --reload

